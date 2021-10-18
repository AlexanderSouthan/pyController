# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 10:08:03 2021

@author: Alexander Southan
"""

class on_off_control():
    def __init__(self, set_point, set_point_type='upper_limit', amplitude=1):
        self.set_point = set_point
        self.set_point_type = set_point_type
        self.amplitude = amplitude

        self.signal = []
        self.time = []
        self.error = []
        self.response = []

    def calc_response(self, new_signal, new_time=None):
        self.signal.append(new_signal)
        self.time.append(new_time)
        self.error.append(self.set_point - self.signal[-1])
        if self.set_point_type == 'upper_limit':
            self.response.append(self.amplitude if self.error[-1] < 0 else 0)
        elif self.set_point_type == 'lower_limit':
            self.response.append(self.amplitude if self.error[-1] > 0 else 0)
        return self.response[-1]