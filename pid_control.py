# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 10:08:57 2021

@author: Alexander Southan
"""

class pid_control:
    def __init__(self, set_point, p_gain, i_gain, d_gain,
                 set_point_type='lower_limit', response_limits=None):
        """
        Initialize a PID controller instance.

        Parameters
        ----------
        set_point : float
            The set point of the PID controller, i.e. the target value of the
            process parameter to be controlled.
        p_gain : float
            The gain of the term proportional to the error.
        i_gain : float
            The gain of the term proportional to the error intergral.
        d_gain : float
            The gain of the term proportional to the error derivative.
        set_point_type : string, optional
            Defines if the set_point is a lower limit ('lower_limit': feedback
            smaller than the set_point generates a positive response or an
            upper limit ('upper_limit': feedback greater than the set_point
            generates a positive response). The default is 'lower_limit'.
        response_limits : None or list, optional
            If None, the response is calculated purely based on the math and
            can be negative or positive. If a list is given, it must contain
            two elements that can either be None or a float. The first element
            is the lower limmit for the response, the second element the upper
            limit. Giving a limit might make sense if a negative reponse is
            physically meaningless, e.g. if a pump is controlled to add a
            solution to a reactor that cannot be removed afterwards (lower
            limit is 0 in this case). The default is None.

        Returns
        -------
        None.

        """
        self.set_point = set_point
        self.p_gain = p_gain
        self.i_gain = i_gain
        self.d_gain = d_gain
        self.set_point_type = set_point_type
        self.response_limits = response_limits

        self.signal = []
        self.time = []
        self.error = []
        self.p_terms = []
        self.i_terms = []
        self.d_terms = []
        self.d_smoothed = []
        self.response = []

    def calc_response(self, new_signal, new_time, d_window=1):
        """
        Calculate the output of the PID controller.

        All data is stored in the lists self.signal, self.time, self.error,
        self.p_terms, self.i_terms, self.d_terms, self.d_smoothed,
        self.response for later use.

        Parameters
        ----------
        new_signal : float
            The feedback that comes from the process. Typically a sensor signal
            like temperature, pH value, pressure etc.
        new_time : float
            The time at which new_signal was obtained.
        d_window : int, optional
            The number of past error derivative values that is used for
            averaging of the derivative. If greater than 1, this results in a
            smoothing of the error derivative The default is 1 which means that
            no smoothing is performed.

        Returns
        -------
        float
            The current output signal of the PID controller.

        """
        self.signal.append(new_signal)
        self.time.append(new_time)

        if self.set_point_type == 'lower_limit':
            self.error.append(self.set_point - self.signal[-1])
        elif self.set_point_type == 'upper_limit':
            self.error.append(self.signal[-1] - self.set_point)

        self.p_terms.append(self.error[-1])

        if len(self.i_terms) == 0:
            self.i_terms.append(0)

            self.d_terms.append(0)
            self.d_smoothed.append(0)
        else:
            time_diff = self.time[-1] - self.time[-2]
            error_diff = self.error[-1] - self.error[-2]

            self.i_terms.append(self.i_terms[-1] + self.error[-1]*time_diff)

            self.d_terms.append(error_diff/time_diff)
            if len(self.d_terms) < d_window:
                d_window = len(self.d_terms)
            self.d_smoothed.append(sum(self.d_terms[-d_window:])/d_window)

        curr_response = (self.p_gain * self.p_terms[-1] +
                         self.i_gain * self.i_terms[-1] +
                         self.d_gain * self.d_smoothed[-1])


        if self.response_limits is None:
            self.response.append(curr_response)
        else:
            # If response violates limits from self.response_limits, it is
            # corrected to one of the limit values.
            if (self.response_limits[0] is not None) and (
                    curr_response < self.response_limits[0]):
                self.response.append(self.response_limits[0])
            elif (self.response_limits[1] is not None) and (
                    curr_response > self.response_limits[1]):
                self.response.append(self.response_limits[1])
            else:
                self.response.append(curr_response)

        return self.response[-1]