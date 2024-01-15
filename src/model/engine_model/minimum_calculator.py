from scipy.optimize import linear_sum_assignment
import numpy as np


class MinimumCalculator:

    def __init__(self):
        self.row_ind = None
        self.col_ind = None

    def calculate_minimum(self, global_costs):
        self.row_ind, self.col_ind = linear_sum_assignment(global_costs)

    def check_size(self, modified_indexes):
        if modified_indexes:
            self.col_ind = np.array([modified_indexes[idx] - 1 for idx in self.col_ind])

