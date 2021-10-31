[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![build workflow](https://github.com/AlexanderSouthan/pyController/actions/workflows/main.yml/badge.svg)](https://github.com/AlexanderSouthan/pyController/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/AlexanderSouthan/pyController/branch/main/graph/badge.svg?token=ONUNYT0FH5)](https://codecov.io/gh/AlexanderSouthan/pyController)

# pyController
## Installation
Downloading and running the following code in the repository folder should work:
```
pip install -e .
```
## Provides currently:
* two classes useful for controlling some parameter in a
process. Examples are controlling a temperature or a pH value.
* a sensor class that simulates a time-delayed sensor response. Useful for
example for a pH probe or a temperature sensor.

### Process control:
* **on-off control**/**bang-bang control** in on_off_control.py: Process
control by switching on and off. See
https://en.wikipedia.org/wiki/Bang%E2%80%93bang_control for details.
* **PID control** in pid_control.py: Process control by using terms
proportional to the error, the error integral and the error derivative. See
https://en.wikipedia.org/wiki/PID_controller or docstrings for details.
Currently, a fully functional, basic PID controller is implemented. Feel free
to contribute if additional functionality is desired.

### Sensor response:
* **time-dependent sensor response** in sensor.py: A time-dependent sensor
response is calculated based on numerical solution of an underlying
differential equation. Currently, the sensor approaches the real value based
on kinetics that are proportional to the sensor error.
