# pyController
Provides currently two classes useful for controlling some parameter in a
process. Examples are controlling a temperature or a pH value.

* **on-off control**/**bang-bang control** in on_off_control.py: Process
control by switching on and off. See
https://en.wikipedia.org/wiki/Bang%E2%80%93bang_control for details.
* **PID control** in pid_control.py: Process control by using terms
proportional to the error, the error integral and the error derivative. See
https://en.wikipedia.org/wiki/PID_controller or docstrings for details.
Currently, a fully functional, basic PID controller is implemented. Feel free
to contribute if additional functionality is desired.