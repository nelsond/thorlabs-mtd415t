# Python library for Thorlabs MTD415 OEM temperature controller [![Build Status](https://travis-ci.org/nelsond/thorlabs-mtd415t.svg?branch=master)](https://travis-ci.org/nelsond/thorlabs-mtd415t) [![Build status](https://ci.appveyor.com/api/projects/status/lfc793mgjyngyt3y?svg=true)](https://ci.appveyor.com/project/nelsond/thorlabs-mtd415t)

Simple wrapper for the Thorlabs MTD415T OEM temperature controller
module.

## Requirements

This module requires Python >= 3.5. It may also still work with Python 2.7 but 
is not explicitely tested for that environment.

* `pyserial` >= 3.4

## Install

Install with pip

```shell
$ pip install git+https://github.com/nelsond/thorlabs-mtd415t.git
```

## Example usage
```python

from thorlabs_mtd415t import MTD415TDevice
from time import sleep

# create a new temperature controller instance with auto save enabled
temp_controller = MTD415TDevice('/dev/ttyUSB0', auto_save=True)

# set tec current limit
temp_controller.tec_current_limit = 0.5

# set pid gains
temp_controller.p_gain = 1
temp_controller.i_gain = 0.1
temp_controller.d_gain = 0

# clear any errors
temp_controller.clear_errors()

# set temperature setpoint
temp_controller.temp_setpoint = 15.025

# check current temperature after 10s
sleep(10)
temp_controler.temp # => 15.020

# close serial port
temp_controller.close()
temp_controller.is_open # => False
```

## Development

Install requirements for development environment

```shell
$ pip install -r requirements/dev.txt
```

Run tests

```shell
$ py.test tests/
```

Generate coverage report

```shell
$ py.test --cov=thorlabs_mtd415t tests/
```
## License

MIT License, see file `LICENSE`.

## Helpful links

- [Official documentation for Thorlabs MTD415](https://www.thorlabs.com/thorproduct.cfm?partnumber=MTD415T)
- [PySerial documentation](https://pypi.python.org/pypi/pyserial)


---
Thorlabs is registered trademark of Thorlabs, Inc.
