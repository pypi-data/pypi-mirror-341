"""
    pyxperiment/controller/data_context.py:
    Performs data collection and instrument manipulation

    This file is part of the PyXperiment project.

    Copyright (c) 2023 PyXperiment Developers

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""

import threading
import time
import datetime
import concurrent.futures
import queue
from typing import Union, cast

from pyxperiment.data_format.text_data_format import TextDataWriter
from pyxperiment.data_storage import DataStorage, DataAccessor
from .control_manager import (
    ScanManager, ReadableManager, RampManager, DoubleScanManager, AsyncReadableManager
)

class DataContext(DataAccessor):
    """
    Performs data collection and instrument manipulation
    """

    def __init__(self):
        self._writables = []# type: list[Union[ScanManager, DoubleScanManager, RampManager]]
        self._readables = []# type: list[Union[ReadableManager, AsyncReadableManager]]
        self.elapsed = 0
        self._max_delay = 0
        self._update_semaphore = threading.BoundedSemaphore(1)
        self.__is_paused = False
        self.__msg_flag = False
        self.__msg_queue = queue.Queue()
        self.status = ''
        self.finished = False
        self.__backsweep = False
        self._curves_num = 1
        self.curve_callback = None
        self.thread = cast(threading.Thread, None)
        self.data_writer = cast(TextDataWriter, None)
        self.all_data = cast(DataStorage, None)

    def rearm(self):
        self.status = ''
        self.finished = False

    def add_observable(self, writable, values, delay):
        """
        Добавить устройство, используемое для чтения параметров, по оси Х
        """
        self._writables.append(RampManager(writable, values[0], values[1], delay))

    def add_writable(self, writable, values, delay):
        """
        Добавить устройство, используемое для задания параметра
        """
        self._writables.append(ScanManager(writable, values, delay))

    def add_double_writable(self, writable1, writable2, values1, values2, delay):
        """
        Добавить устройство, используемое для задания параметра
        """
        self._writables.append(DoubleScanManager(writable1, writable2, values1, values2, delay))

    def add_readables(self, readables):
        """
        Добавить устройство, используемое для чтения величины
        """
        for control in readables:
            if not getattr(control, 'init_get_value', None) or len(readables) == 1:
                self._readables.append(ReadableManager(control))
            else:
                self._readables.append(AsyncReadableManager(control))

    def add_curve_callback(self, callback):
        self.curve_callback = callback

    def set_data_writer(self, data_writer):
        self.data_writer = data_writer

    def set_curves_num(self, num, delay, backsweep):
        self._curves_num = num
        self._curve = 1
        self.curves_delay = delay
        self.__backsweep = backsweep

    @property
    def curves_num(self):
        """Общее число повторов каждой записи"""
        return self._curves_num

    @property
    def currentCurve(self):
        """Текущий номер повтора записи"""
        return self._curve

    @property
    def backsweep(self):
        """Сканировать на обратном ходе"""
        return self.__backsweep

    @property
    def maxDelay(self):
        """Максимальная задержка считывания точки на этой кривой"""
        return self._max_delay

    def get_sweepables(self):
        return self._writables

    def get_measurables(self):
        return self._readables

    def _delay(self, secs):
        """Временная задержка, проверка управляющих команд пауза/стоп"""
        if secs > 0:
            time.sleep(secs)
        if self.__stop_flag:
            raise InterruptedError("Stopped by user")

    def _process_writable(self, wr):
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)
        init_readables = cast(
            list[AsyncReadableManager],
            list(filter(lambda x: isinstance(x, AsyncReadableManager), self._readables))
            )

        self._curve = 1
        while self._curve <= self.curves_num:
            self.status = 'Starting iterations'
            wr.reset()
            sweep_time = []
            # Reset all the measurable devices
            for instr in self._readables:
                instr.reset()
            # Add the new curve to the storage
            self.all_data.add_curve(sweep_time, wr, self._readables)

            self.status = 'Sweeping'# Sweeping forward
            start_time = datetime.datetime.now()
            reference_time = time.perf_counter()
            desired_time = wr.delay / 1000.0

            while True:
                elapsed_time = time.perf_counter() - reference_time
                self.elapsed = desired_time - elapsed_time
                self._max_delay = min(self._max_delay, self.elapsed)
                to_sleep = self.elapsed
                if to_sleep > 0:
                    while to_sleep > 0.02:
                        time.sleep(0.001)
                        elapsed_time = time.perf_counter() - reference_time
                        to_sleep = desired_time - elapsed_time
                # Capture the actual output value
                future = executor.submit(wr.update)
                # Trigger all the devices to start measuring
                if init_readables:
                    concurrent.futures.wait(
                        [executor.submit(rd.init_update) for rd in init_readables]
                        )
                # Finish reading the devices
                futures = [executor.submit(rd.update) for rd in self._readables]
                futures.append(future)
                concurrent.futures.wait(futures)
                sweep_time.append(time.perf_counter() - reference_time)
                if not wr.forward():
                    break
                if self.__stop_flag:
                    self.data_writer.save_internal(self.all_data)
                    raise InterruptedError("Stopped by user")
                if self.__is_paused:
                    pause_time = time.perf_counter()
                    self._update_semaphore.acquire()
                    desired_time = desired_time - pause_time + time.perf_counter()
                if self.__msg_flag:
                    if not self.__msg_queue.empty():
                        msg = self.__msg_queue.get_nowait()
                        self.data_writer.save_internal(self.all_data)
                    self.__msg_flag = False
                desired_time += wr.delay / 1000.0
            sweep_time[-1] = datetime.datetime.now()
            sweep_time[0] = start_time
            # Flush the data to disk, if nesessary
            self.data_writer.after_sweep(0, self.all_data)
            # Call the callback (if set)
            if self.curve_callback:
                self.curve_callback()
            # Разворачиваем назад
            self._curve += 1
            if self._curve <= self.curves_num:
                self._sweep_to_start(0)
                self.status = 'Delay before next iteration'
                self._delay(self.curves_delay)
        self._curve = self.curves_num

    def _sweep_to_start(self, num):
        """
        Called after a writable sweep is finished to decide what to do next
        """
        wr = self._writables[num]
        # Nothing to do to if sweeping time
        if wr.get_instrument().device_name() == 'Time':
            wr.reset()
        # Reverse the direction
        elif num == 0 and self.__backsweep:
            wr.revert()
        # We don't go back if ended at the same value
        elif wr.values[0] == wr.values[-1]:
            wr.reset()
        # Go back the same path without reading at 10 times the speed
        else:
            self.status = 'Sweepeing ' + ('slow' if num > 0 else '') + 'device back to start...'
            while True:
                wr.update()
                if not wr.backward():
                    break
                self._delay(wr.delay / 1000.0 / 10)

    def _process_slow_writable(self, num):
        wr = self._writables[num]
        if num == 0:
            self._process_writable(wr)
            return

        self.status = 'Starting iterations slow'
        # Sweeping forward
        wr.reset()
        while True:
            # If slow writable needs extra time to set point, we wait for it
            wr.update()
            while not wr.is_point_set():
                self.status = 'Waiting for slow X device to set point...'
                self._delay(0.1)
                wr.update()
            # Ожидание перед началом итерации
            self.status = 'Delay slow device before iteration...'
            current_time = time.perf_counter()
            target_time = current_time + wr.delay / 1000.0
            while (target_time - current_time) > 0.5:
                self._delay(0.5)
                wr.update()
                current_time = time.perf_counter()
            if target_time > current_time:
                self._delay(target_time - current_time)
                wr.update()
            # Сканируем быстрым устройством
            self._process_slow_writable(num-1)
            # Передвигаем медленное устройство на следующую точку
            if not wr.forward():
                break
            # Разворачиваем назад более быстрое устройство
            self._sweep_to_start(num-1)
        # Flush the data to disk, if nesessary
        self.data_writer.after_sweep(num, self.all_data)
        # Create a new data storage
        if num == 1:
            self.all_data = DataStorage(self._writables, self._readables, self.curves_num)

    def __update_task(self):
        for mgr in self._readables + self._writables:
            mgr.get_instrument().to_remote()
        try:
            self.all_data = DataStorage(self._writables, self._readables, self.curves_num)
            self._process_slow_writable(len(self._writables)-1)
            self.status = 'Complete'
        except InterruptedError:
            self.status = 'Interrupted'
        for mgr in self._readables + self._writables:
            mgr.get_instrument().to_local()
        self.finished = True

    def save(self):
        """Сохранение данных по внешней команде"""
        self.__msg_queue.put(1)
        self.__msg_flag = True

    def start(self):
        self.__stop_flag = False
        self.thread = threading.Thread(target=self.__update_task)
        self.thread.start()

    def pause(self, state):
        if self.__is_paused != state:
            self.__is_paused = state
            if state:
                self._update_semaphore.acquire()
            elif not state:
                self._update_semaphore.release()

    @property
    def is_paused(self):
        return self.__is_paused

    def stop(self):
        self.__stop_flag = True
        self.pause(False)
        self.thread.join()
        if isinstance(self._writables[0], RampManager):
            self._writables[0].stop_ramp()

    def __to_start_task(self):
        try:
            self._sweep_to_start(0)
            self.status = 'Complete'
        except InterruptedError:
            self.status = 'Interrupted'
        for mgr in self._readables + self._writables:
            mgr.get_instrument().to_local()

    def sweepToStart(self):
        self.__stop_flag = False
        self.thread = threading.Thread(target=self.__to_start_task)
        self.thread.start()

    @property
    def filename(self):
        return self.data_writer.get_filename()

    def get_data(self):
        return self.all_data.get_data()

    def get_curve(self, index=-1):
        return self.all_data.get_curve(index)

    def get_length(self):
        return self.all_data.get_length()
