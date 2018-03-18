# -*- coding: utf-8 -*-
"""
This module provides the MTD415TDevice class.

See https://www.thorlabs.de/thorproduct.cfm?partnumber=MTD415T for more details
on the actual temperature controller.

Example:
    from mtd415t_device import MTD415TDevice
    from time import sleep

    temp_controller = MTD415TDevice(auto_save=True)
    temp_controller.temp_setpoint = 15.025
    sleep(10)
    temp_controller.temp # => 15.020

---
Nelson Darkwah Oppong, December 2017
n@darkwahoppong.com
"""

from .helpers import validate_is_float_or_int, validate_is_in_range
from .serial_device import SerialDevice


class MTD415TDevice(SerialDevice):
    """
    This class allows controlling and configuring the digital temperature
    controller MTD415T from Thorlabs. You need to connect the temperature
    controller to a serial port on your computer to get started.

    Args:
        port (string): Serial port, e. g. '/dev/ttyUSB0'
        auto_save (boolean, optional): Enable or disable automatic write to
            non-volatile memory after any change
    """

    # error bits, see MTD415T datasheet, p. 18
    _ERRORS = {
        0:  'not enabled',
        1:  'internal temperature too high',
        2:  'thermal latch-up',
        3:  'cycling time too small',
        4:  'no sensor',
        5:  'no tec',
        6:  'tec polarity reversed',
        13: 'value out of range',
        14: 'invalid command'
    }

    def __init__(self, port, auto_save=False, *args, **kwargs):
        self._auto_save = auto_save
        super(MTD415TDevice, self).__init__(port, baudrate=115200, **kwargs)

    def query(self, setting):
        """
        Retrieve setting

        Args:
            setting (string): Setting name, generally a single character

        Returns:
            string: The setting value
        """

        if type(setting) == str:
            setting = setting.encode('ascii')

        cmd = setting + b'?'
        return super(MTD415TDevice, self).query(cmd)

    def write(self, data, *args, **kwargs):
        """
        Writes data

        Args:
            data (string): Data
        """
        if type(data) == str:
            data = data.encode('ascii')

        return super(MTD415TDevice, self).write(data, *args, **kwargs)

    def set(self, setting, value):
        """
        Set a setting to the given integer value

        Args:
            setting (string): Setting name, generally single character
            value (int): Set value
        """
        value = int(value)
        cmd = '{}{:d}'.format(setting, value).encode('ascii')
        self.write(cmd)

        # ensure returned data is removed from the buffer
        self.read()

        if self._auto_save:
            self.save()

    def save(self):
        """Save settings to non-volatile memory"""
        self.write('M')

        # ensure returned data is removed from the buffer
        self.read()

    def clear_errors(self):
        """Clears error flags"""
        self.write('c')

        # ensure returned data is removed from the buffer
        self.read()

    @property
    def auto_save(self):
        """Auto save (boolean)"""
        return self._auto_save

    @auto_save.setter
    def auto_save(self, value):
        self._auto_save = (True if value is True else False)

    @property
    def idn(self):
        """Product name and version number (string)"""
        return self.query('m').decode('ascii')

    @property
    def uid(self):
        """Unique device identifier (string)"""
        return self.query('u').decode('ascii')

    @property
    def error_flags(self):
        """Error flags from the error register of the device (tuple, LSB
        first)"""
        err = int(self.query('E').decode('ascii'))
        return tuple(c == '1' for c in reversed('{:016b}'.format(err)))

    @property
    def errors(self):
        """Errors from the error register of the device (tuple)"""
        flags = self.error_flags
        errors = []
        for idx, err in self._ERRORS.items():
            if flags[idx] is False:
                continue

            errors.append(err)

        return tuple(errors)

    @property
    def tec_current_limit(self):
        """TEC current limit in A (float, >= 0.200 and <= 2.000)"""
        value = self.query('L')
        return float(value) / 1e3

    @tec_current_limit.setter
    def tec_current_limit(self, value):
        validate_is_float_or_int(value, 'TEC current limit')

        validate_is_in_range(value, 0.2, 2, 'TEC current limit', ' A')
        value = round(value*1e3)

        self.set('L', value)

    @property
    def tec_current(self):
        """TEC current in A (float)"""
        value = self.query('A')
        return float(value) / 1e3

    @property
    def tec_voltage(self):
        """TEC voltage in V (float)"""
        value = self.query('U')
        return float(value) / 1e3

    @property
    def temp(self):
        """Current temperature in ° C (float)"""
        value = self.query('Te')
        return float(value) / 1e3

    @property
    def temp_setpoint(self):
        """Temperature setpoint in ° C (float, >= 5.000 and <= 45.000)"""
        value = self.query('T')
        return float(value) / 1e3

    @temp_setpoint.setter
    def temp_setpoint(self, value):
        validate_is_float_or_int(value, 'Temperature setpoint')

        validate_is_in_range(value, 5, 45, 'Temperature setpoint', '° C')
        value = round(value*1e3)

        self.set('T', value)

    @property
    def status_temp_window(self):
        """Temperature window for the status pin in K (float, >= 1e-3 and <=
        32.768)"""
        value = self.query('W')
        return float(value) / 1e3

    @status_temp_window.setter
    def status_temp_window(self, value):
        validate_is_float_or_int(value, 'Status temperature window')

        validate_is_in_range(value, 1e-3, 32.768,
                             'Status temperature window', '° C')
        value = round(value*1e3)

        self.set('W', value)

    @property
    def status_delay(self):
        """Delay for changing the status pin in s (int, >=1 and <= 32768)"""
        value = self.query(b'd')
        return int(value)

    @status_delay.setter
    def status_delay(self, value):
        validate_is_float_or_int(value, 'Status delay')

        value = int(value)
        validate_is_in_range(value, 1, 32768, 'Status delay', ' s')

        self.set('d', value)

    @property
    def critical_gain(self):
        """Critical gain in A/K (float, >=10e-3 and <= 100)"""
        value = self.query('G')
        return float(value) / 1e3

    @critical_gain.setter
    def critical_gain(self, value):
        validate_is_float_or_int(value, 'Critical gain')

        validate_is_in_range(value, 10e-3, 100, 'Critical gain', ' A/K')
        value = round(value*1e3)

        self.set('G', value)

    @property
    def critical_period(self):
        """Critical period in s (float, >=100e-3 and <= 100.000)"""
        value = self.query('O')
        return float(value) / 1e3

    @critical_period.setter
    def critical_period(self, value):
        validate_is_float_or_int(value, 'Critical period')

        validate_is_in_range(value, 100e-3, 100e3, 'Critical period', ' s')
        value = round(value*1e3)

        self.set('O', value)

    @property
    def cycling_time(self):
        """Cycling time in s (float, >= 1e-3 and <= 1.000)"""
        value = self.query('C')
        return float(value) / 1e3

    @cycling_time.setter
    def cycling_time(self, value):
        validate_is_float_or_int(value, 'Cycling time')

        validate_is_in_range(value, 1e-3, 1, 'Cycling time', ' s')
        value = round(value*1e3)

        self.set('C', value)

    @property
    def p_gain(self):
        """Proportional gain in A/K (float, >=0 and <= 100.000)"""
        value = self.query('P')
        return float(value) / 1e3

    @p_gain.setter
    def p_gain(self, value):
        validate_is_float_or_int(value, 'P gain')

        validate_is_in_range(value, 0, 100, 'P gain', ' A/K')
        value = round(value*1e3)

        self.set('P', value)

    @property
    def i_gain(self,):
        """Integrator gain in A/(K x s) (float, >=0 and <= 100.000)"""
        value = self.query('I')
        return float(value) / 1e3

    @i_gain.setter
    def i_gain(self, value):
        validate_is_float_or_int(value, 'I gain')

        validate_is_in_range(value, 0, 100, 'I gain', ' A/(K x s)')
        value = round(value*1e3)

        self.set('I', value)

    @property
    def d_gain(self):
        """Differential gain in (A x s)/K (float, >=0 and <= 100.000)"""
        value = self.query('D')
        return float(value) / 1e3

    @d_gain.setter
    def d_gain(self, value):
        validate_is_float_or_int(value, 'D gain')

        validate_is_in_range(value, 0, 100, 'D gain', ' (A x s)/K')
        value = round(value*1e3)

        self.set('D', value)
