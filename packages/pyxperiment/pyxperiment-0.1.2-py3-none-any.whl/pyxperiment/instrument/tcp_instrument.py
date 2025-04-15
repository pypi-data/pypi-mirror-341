"""
    pyxperiment/controller/tcp_instrument.py: The base class for instruments
    with tcp socket based communication, ignoring VISA

    This file is part of the PyXperiment project.

    Copyright (c) 2022 PyXperiment Developers

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

from abc import ABCMeta
import socket
import select

from .instrument import Instrument

class TcpSocketInstrument(Instrument, metaclass=ABCMeta):
    """
    Uses direct socket connection for controlling TCP instrument
    """

    def __init__(self, resource, local_port=0):
        super().__init__('')
        self.resource = resource
        self.local_port = local_port
        self.buffer_size = 256
        self.recv_timeout = 1
        addr = resource.split('::')
        self.inst = socket.create_connection(
            (addr[1], int(addr[2])),
            self.recv_timeout,
            ('0.0.0.0', self.local_port)
        )
        self.inst.setblocking(False)

    @property
    def location(self):
        with self._lock:
            return self.resource

    def reset(self):
        with self._lock:
            self.inst.close()
            addr = self.resource.split('::')
            self.inst = socket.create_connection(
                (addr[1], int(addr[2])),
                self.recv_timeout,
                ('0.0.0.0', self.local_port)
            )
            self.inst.setblocking(False)

    def read(self):
        """
        Low-level read
        """
        with self._lock:
            ready = select.select([self.inst], [], [], self.recv_timeout)
            if ready[0]:
                return self.inst.recv(self.buffer_size).decode().translate(
                    {ord(c): None for c in ['\r', '\n']}
                    )
        raise TimeoutError('The instrument failed to answer within a specified timeout')

    def query_id(self):
        """
        Read the instrument ID string
        """
        return self.query("*IDN?")

    def write(self, data):
        """
        Low-level write
        """
        with self._lock:
            self.inst.send((data + '\n').encode())

    def query(self, data):
        """
        Write followed by immediate read
        """
        with self._lock:
            self.inst.send((data + '\n').encode())
            ready = select.select([self.inst], [], [], self.recv_timeout)
            if ready[0]:
                return self.inst.recv(self.buffer_size).decode().translate(
                    {ord(c): None for c in ['\r', '\n']})
        raise TimeoutError('The instrument failed to answer within a specified timeout')
