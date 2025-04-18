class DummyResource():
    """
    Class
    """

    def __init__(self, address):
        self.address = address

    @property
    def resource_name(self):
        return self.address

    def read(self):
        return ''

    def read_stb(self):
        return 0

    def write(self, data, extra=None):
        pass

    def query(self, data):
        if data == "*IDN?" or data == 'QIDN?':
            return str('test,test,test,test')
        return '1'

    def read_raw(self, bit=None):
        pass

    def query_id(self):
        return 'test'

    def control_ren(self, val):
        pass

    write_termination = ''
    read_termination = ''
    baud_rate = 0
