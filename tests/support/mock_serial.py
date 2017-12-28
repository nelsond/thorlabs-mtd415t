class MockSerial:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate

        self.is_open = False

        self.out_buffer = []
        self.in_buffer = []

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def write(self, value):
        if not self.is_open:
            raise RuntimeError('Serial device is closed')

        self.out_buffer.append(value)

    def readline(self):
        value = self.in_buffer.pop()
        return bytes(value.encode('ascii'))
