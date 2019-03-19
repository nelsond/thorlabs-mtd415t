"""
This module provides the SerialDevice class

Example:
    from serial_device import SerialDevice

    device = SerialDevice(port='/dev/ttyUSB0', baudrate=9600)
    device.query('HELLO') # => "Hello"

---
Nelson Darkwah Oppong, December 2017
n@darkwahoppong.com

"""

from time import time


class SerialDevice(object):
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200,
                 max_log_length=100, **kwargs):
        from serial import serial_for_url

        self._serial = serial_for_url(port, baudrate=baudrate, **kwargs)

        self._log = []
        self._max_log_length = max_log_length

    def _logger(self, kind, message):
        log = self._log

        # remove first entry if log is too long
        if len(log) > self._max_log_length:
            log.pop(0)

        entry = {
            'kind': kind,
            'time': time(),
            'content': message
        }

        log.append(entry)

    def open(self):
        """
        Open serial connection to device.
        """
        self._serial.open()

    def close(self):
        """
        Close serial connection to device.
        """
        self._serial.close()

    def query(self, cmd):
        """
        Send command to device and immediately read response

        Args:
            cmd (bytes): Command

        Returns:
            bytes: The response from the device
        """
        self.write(cmd)
        return self.read()

    def write(self, data, line_ending=b'\n'):
        """
        Send data to device.

        Args:
            data (bytes): Data
        """
        if not self.is_open:
            self.open()

        string = data + line_ending
        self._logger('write', string)

        self._serial.write(string)

    def read(self):
        if not self.is_open:
            self.open()

        result = self._serial.readline()
        self._logger('read', result)

        return result

    @property
    def is_open(self):
        """Status of the serial connection (boolean)"""
        return self._serial.is_open

    @property
    def log(self):
        """Log entries (list)"""
        return list(self._log)
