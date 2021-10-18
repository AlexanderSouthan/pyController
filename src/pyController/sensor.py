# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 23:07:22 2021

@author: aso
"""

from scipy.integrate import solve_ivp

class sensor:
    def __init__(self, start_value, start_time=0, response_function='prop',
                  start_real=None, **kwargs):
        """
        Initialize a sensor instance.

        Parameters
        ----------
        start_value : float
            The sensor reading at the start_time.
        start_time : float, optional
            The time at which the sensor readings start. The default is 0.
        response_function : string, optional
            The type of response the sensor has to a signal. Currently, only
            'prop' is a valid argument which means that the response is
            proportional to the current error in the reading (i.e. the
            difference between reading and real value). It is assumed that the
            time-dependent real value can be approximated by a linear function
            between two time points. The default is 'prop'.
        start_real : float or None, optional
            Gives the real value at the start of data acquisition. If a float
            is given that is different than start_value, the sensor starts with
            an error into data acquisition. If None, the sensor is assumed to
            give the correct value at the start. The default is None.
        **kwargs for response_function == 'prop'
                k : float
                    The proportionality constant used for the calculations.

        Raises
        ------
        ValueError
            If an ivalid response_function is given.

        Returns
        -------
        None.

        """
        self.sensor_values = [start_value]
        self.times = [start_time]
        if start_real is None:
            self.real_values = [start_value]
        else:
            self.real_values = [start_real]
        self.response_function = response_function

        if self.response_function == 'prop':
            self.k = kwargs.get('k', 1)
        else:
            raise ValueError('No valid response function given.')

    def next_sensor_value(self, real_value, time):
        """
        Calculate the next sensor value based on a new real value.

        Parameters
        ----------
        real_value : float
            The next real value which results from the process under
            investigation.
        time : float
            The time at which the real_value is valid in the system.

        Returns
        -------
        curr_reading : float
            The current sensor reading, i.e. the time-delayed value the sensor
            will diplay at time.

        """
        self.real_values.append(real_value)
        self.times.append(time)
        curr_reading = solve_ivp(self.transfer_function,
                                 [self.times[-2], self.times[-1]],
                                 [self.sensor_values[-1]],
                                 t_eval=[self.times[-1]])
        self.sensor_values.append(curr_reading.y[0, 0])
        return curr_reading

    def transfer_function(self, t, y):
        """
        The sensor transfer function.
        
        This function gives the first derivative of the sensor reading with
        time. This is used for a numerical solution of the differential
        equation governing the time-dependent sensor response using solve_ivp
        from the SciPy integration package.

        Parameters
        ----------
        t : float
            The time of the reading.
        y : float
            The sensor reading to be calculated.

        Returns
        -------
        float
            The current derivative of the sensor response.

        """
        if self.response_function == 'prop':
            curr_y = ((self.real_values[-1] - self.real_values[-2])/
                      (self.times[-1] - self.times[-2]) *
                      (t-self.times[-1])+self.real_values[-1])
            return -self.k*y + self.k*curr_y