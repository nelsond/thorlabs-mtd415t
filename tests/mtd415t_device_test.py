from thorlabs_mtd415t import MTD415TDevice
from pytest import fixture, raises
from support import MockSerial
import random


@fixture
def mtd415t_device_with_mock_serial():
    mtd415t = MTD415TDevice('loop://')
    mtd415t._serial = MockSerial('loop://', 115200)

    return mtd415t, mtd415t._serial


# .__init__
def test_it_sets_auto_save_to_false_by_default():
    mtd415t = MTD415TDevice('loop://')

    assert mtd415t.auto_save is False


def test_it_sets_auto_save_on_init():
    mtd415t = MTD415TDevice('loop://', auto_save=True)

    assert mtd415t.auto_save is True


# .query
def test_it_queries_setting_and_returns_result(
        mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('0')
    result = mtd415t.query('test')

    assert result == b'0'


def test_it_queries_setting(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('0')
    mtd415t.query('test')

    assert mock_serial.out_buffer.pop() == b'test?\n'


def test_it_retries_query_for_unknown_command(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('hello world')
    mock_serial.in_buffer.append('unknown command\n')
    result = mtd415t.query('test', retry=True)

    assert result == b'hello world'


# .close
def test_it_closes_serial(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mtd415t.close()

    assert mtd415t.is_open is False


# .log
def test_it_returns_log(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mtd415t.write(b'Test')

    assert len(mtd415t.log) == 1


# .read
def test_it_reads_data(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('0\n')

    assert mtd415t.read() == b'0\n'


# .write
def test_it_writes_data(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mtd415t.write('test')

    assert mock_serial.out_buffer.pop() == b'test\n'


# .set
def test_it_sets_setting(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('0')
    mtd415t.set('T', 1000)

    assert mock_serial.out_buffer.pop() == b'T1000\n'


def test_it_reads_after_it_has_set_setting(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('0')
    mtd415t.set('T', 1000)

    assert len(mock_serial.in_buffer) == 0


def test_it_calls_save_after_set_if_auto_save_is_enabled(
        mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mtd415t.auto_save = True
    mock_serial.in_buffer.extend(('0', '0'))
    mtd415t.set('T', 1000)

    assert mock_serial.out_buffer == [b'T1000\n', b'M\n']


# .save
def test_it_saves_settings(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('0')
    mtd415t.save()

    assert mock_serial.out_buffer.pop() == b'M\n'


def test_it_reads_after_it_saves_settings(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('0')
    mtd415t.save()

    assert len(mock_serial.in_buffer) == 0


# .clear_errors
def test_it_clears_errors(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('0')
    mtd415t.clear_errors()

    assert mock_serial.out_buffer.pop() == b'c\n'


def test_it_reads_after_it_clears_errors(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('0')
    mtd415t.clear_errors()

    assert len(mock_serial.in_buffer) == 0


# .auto_save
def test_it_returns_auto_save(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mtd415t._auto_save = 'Test'

    assert mtd415t.auto_save == 'Test'


def test_it_sets_auto_save(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mtd415t.auto_save = True

    assert mtd415t._auto_save is True


def test_it_does_not_set_auto_save_to_invalid_value(
        mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mtd415t.auto_save = 'Test'

    assert mtd415t.auto_save is False


# .idn
def test_it_returns_idn(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('XYZ\n')

    assert mtd415t.idn == 'XYZ'


def test_it_queries_idn_property(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('XYZ\n')
    mtd415t.idn

    assert mock_serial.out_buffer.pop() == b'm?\n'


# .uid
def test_it_returns_uid(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('ABC\n')

    assert mtd415t.uid == 'ABC'


def test_it_queries_uid_property(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('ABC')
    mtd415t.uid

    assert mock_serial.out_buffer.pop() == b'u?\n'


# .error_flags
def test_it_returns_error_flags(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    idx = random.randint(0, 15)
    mock_serial.in_buffer.append(str(1 << idx))
    expected_result = tuple(True if i == idx else False for i in range(16))

    assert mtd415t.error_flags == expected_result


def test_it_queries_error_flags(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append(str(1 << 2))
    mtd415t.error_flags

    assert mock_serial.out_buffer.pop() == b'E?\n'


# .errors
def test_it_returns_not_enabled_error(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append(str(1 << 0))

    assert mtd415t.errors == ('not enabled',)


def test_it_returns_internal_temperature_too_high_error(
        mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append(str(1 << 1))

    assert mtd415t.errors == ('internal temperature too high',)


def test_it_returns_thermal_latch_up_error(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append(str(1 << 2))

    assert mtd415t.errors == ('thermal latch-up',)


def test_it_returns_cycling_time_too_small_error(
        mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append(str(1 << 3))

    assert mtd415t.errors == ('cycling time too small',)


def test_it_returns_no_sensor_error(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append(str(1 << 4))

    assert mtd415t.errors == ('no sensor',)


def test_it_returns_no_tec_error(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append(str(1 << 5))

    assert mtd415t.errors == ('no tec',)


def test_it_returns_tec_polarity_reversed_error(
        mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append(str(1 << 6))

    assert mtd415t.errors == ('tec polarity reversed',)


def test_it_returns_value_out_of_range_error(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append(str(1 << 13))

    assert mtd415t.errors == ('value out of range',)


def test_it_returns__error(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append(str(1 << 14))

    assert mtd415t.errors == ('invalid command',)


# .tec_current_limit
def test_it_returns_tec_current_limit(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('2000')

    assert mtd415t.tec_current_limit == 2.0


def test_it_queries_tec_current_limit(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('2000')
    mtd415t.tec_current_limit

    assert mock_serial.out_buffer.pop() == b'L?\n'


def test_it_sets_tec_current_limit(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('1234')
    mtd415t.tec_current_limit = 1.234

    assert mock_serial.out_buffer.pop() == b'L1234\n'


def test_it_raises_value_error_for_invalid_tec_current_limit(
        mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('1234')

    with raises(ValueError):
        mtd415t.tec_current_limit = random.choice((0.1, 3.0, 'invalid'))


# .tec_current
def test_it_returns_tec_current(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('1234')

    assert mtd415t.tec_current == 1.234


def test_it_queries_tec_current_property(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('1234')
    mtd415t.tec_current

    assert mock_serial.out_buffer.pop() == b'A?\n'


# .tec_voltage
def test_it_returns_tec_voltage(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('621')

    assert mtd415t.tec_voltage == 0.621


def test_it_queries_tec_voltage_property(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('621')
    mtd415t.tec_voltage

    assert mock_serial.out_buffer.pop() == b'U?\n'


# .temp
def test_it_returns_temperature(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('5321')

    assert mtd415t.temp == 5.321


def test_it_queries_temperature_property(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('5321')
    mtd415t.temp

    assert mock_serial.out_buffer.pop() == b'Te?\n'


# .temp_setpoint
def test_it_returns_temp_setpoint(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('5321')

    assert mtd415t.temp_setpoint == 5.321


def test_it_queries_temp_setpoint(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('5321')
    mtd415t.temp_setpoint

    assert mock_serial.out_buffer.pop() == b'T?\n'


def test_it_sets_temp_setpoint(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('5321')
    mtd415t.temp_setpoint = 5.321

    assert mock_serial.out_buffer.pop() == b'T5321\n'


def test_it_raises_value_error_for_invalid_temp_setpoint(
        mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('1234')

    with raises(ValueError):
        mtd415t.temp_setpoint = random.choice((4.213, 45.001, 'invalid'))


# .status_temp_window
def test_it_returns_status_temp_window(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('5321')

    assert mtd415t.status_temp_window == 5.321


def test_it_queries_status_temp_window(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('5321')
    mtd415t.status_temp_window

    assert mock_serial.out_buffer.pop() == b'W?\n'


def test_it_sets_status_temp_window(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('5321')
    mtd415t.status_temp_window = 5.321

    assert mock_serial.out_buffer.pop() == b'W5321\n'


def test_it_raises_value_error_for_invalid_status_temp_window(
        mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('1234')

    with raises(ValueError):
        mtd415t.status_temp_window = random.choice((1e-4, 32.769, 'invalid'))


# .status_delay
def test_it_returns_status_delay(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('5321')

    assert mtd415t.status_delay == 5321


def test_it_queries_status_delay(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('5321')
    mtd415t.status_delay

    assert mock_serial.out_buffer.pop() == b'd?\n'


def test_it_sets_status_delay(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('5321')
    mtd415t.status_delay = 5321

    assert mock_serial.out_buffer.pop() == b'd5321\n'


def test_it_raises_value_error_for_invalid_status_delay(
        mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('1')

    with raises(ValueError):
        mtd415t.status_delay = random.choice((0.1, 32769, 'invalid'))


# .critical_gain
def test_it_returns_critical_gain(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('12200')

    assert mtd415t.critical_gain == 12.2


def test_it_queries_critical_gain(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('12200')
    mtd415t.critical_gain

    assert mock_serial.out_buffer.pop() == b'G?\n'


def test_it_sets_critical_gain(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('12200')
    mtd415t.critical_gain = 12.2

    assert mock_serial.out_buffer.pop() == b'G12200\n'


def test_it_raises_value_error_for_invalid_critical_gain(
        mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('1')

    with raises(ValueError):
        mtd415t.critical_gain = random.choice((1e-3, 101, 'invalid'))


# .critical_period
def test_it_returns_critical_period(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('24567')

    assert mtd415t.critical_period == 24.567


def test_it_queries_critical_period(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('24567')
    mtd415t.critical_period

    assert mock_serial.out_buffer.pop() == b'O?\n'


def test_it_sets_critical_period(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('24567')
    mtd415t.critical_period = 24.567

    assert mock_serial.out_buffer.pop() == b'O24567\n'


def test_it_raises_value_error_for_invalid_critical_period(
        mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('1')

    with raises(ValueError):
        mtd415t.critical_period = random.choice((10e-3, 101e3, 'invalid'))


# .cycling_time
def test_it_returns_cycling_time(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('123')

    assert mtd415t.cycling_time == 0.123


def test_it_queries_cycling_time(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('123')
    mtd415t.cycling_time

    assert mock_serial.out_buffer.pop() == b'C?\n'


def test_it_sets_cycling_time(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('123')
    mtd415t.cycling_time = 0.123

    assert mock_serial.out_buffer.pop() == b'C123\n'


def test_it_raises_value_error_for_invalid_cycling_time(
        mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('1')

    with raises(ValueError):
        mtd415t.cycling_time = random.choice((1e-4, 1.1, 'invalid'))


# .p_gain
def test_it_returns_p_gain(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('1234')

    assert mtd415t.p_gain == 1.234


def test_it_queries_p_gain(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('123')
    mtd415t.p_gain

    assert mock_serial.out_buffer.pop() == b'P?\n'


def test_it_sets_p_gain(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('1234')
    mtd415t.p_gain = 1.234

    assert mock_serial.out_buffer.pop() == b'P1234\n'


def test_it_raises_value_error_for_invalid_p_gain(
        mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('1')

    with raises(ValueError):
        mtd415t.p_gain = random.choice((-1, 101, 'invalid'))


# .i_gain
def test_it_returns_i_gain(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('1234')

    assert mtd415t.i_gain == 1.234


def test_it_queries_i_gain(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('123')
    mtd415t.i_gain

    assert mock_serial.out_buffer.pop() == b'I?\n'


def test_it_sets_i_gain(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('1234')
    mtd415t.i_gain = 1.234

    assert mock_serial.out_buffer.pop() == b'I1234\n'


def test_it_raises_value_error_for_invalid_i_gain(
        mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('1')

    with raises(ValueError):
        mtd415t.i_gain = random.choice((-1, 101, 'invalid'))


# .d_gain
def test_it_returns_d_gain(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('1234')

    assert mtd415t.d_gain == 1.234


def test_it_queries_d_gain(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('123')
    mtd415t.d_gain

    assert mock_serial.out_buffer.pop() == b'D?\n'


def test_it_sets_d_gain(mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('1234')
    mtd415t.d_gain = 1.234

    assert mock_serial.out_buffer.pop() == b'D1234\n'


def test_it_raises_value_error_for_invalid_d_gain(
        mtd415t_device_with_mock_serial):
    mtd415t, mock_serial = mtd415t_device_with_mock_serial

    mock_serial.in_buffer.append('1')

    with raises(ValueError):
        mtd415t.d_gain = random.choice((-1, 101, 'invalid'))
