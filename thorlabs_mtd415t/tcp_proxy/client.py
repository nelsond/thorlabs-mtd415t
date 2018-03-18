"""
This class provides the Client class.

Example:
    from thorlabs_mtd415t import tcp_proxy

    c = tcp_proxy.Client('localhost', 3333)
    c.connect()
    c.set('temp_setpoint', 12.234)
    c.disconnect()

---
Nelson Darkwah Oppong, March 2018
n@darkwahoppong.com
"""

import socket


class Client(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port

        self.is_connected = False

    def connect(self, timeout=10):
        """
        Connects to server
        """

        if self.is_connected is True:
            self.disconnect()

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(timeout)
        self._socket.connect((self._host, self._port))

        self.is_connected = True

        return True

    def disconnect(self):
        """
        Disconnects from server
        """
        if self.is_connected is False:
            return False

        self._socket.close()

        return True

    def set(self, prop, value):
        if prop != 'temp_setpoint':
            raise Exception('Unknown or unsupported property: {}'.format(prop))

        try:
            value = float(value)
        except:
            msg = 'Invalid value for setting temp_setpoint: {}'.format(value)
            raise ValueError(msg)

        if value > 45 or value < 5:
            raise ValueError('temp_setpoint out of range (>=5, <= 45)')

        return self._send('set_temp_setpoint:{:.3f}'.format(value))

    def _send(self, data):
        if self.is_connected is False:
            raise Exception('Not connected')

        self._socket.send(data.encode('ascii'))
        result = self._socket.recv(1024).strip().decode('ascii')

        return result == 'OK'
