from scipy.spatial import distance
import numpy as np


class ModelValidator:

    def __init__(self, trucks_coordinates, requests_coordinates, volumes_requests, assignment_truck_request,
                 requests_priorities, inattention_days):

        self.maximum_trucks, self.maximum_inattention_days = None, None
        self.limit_work_minutes, self.maximum_truck_capacity = None, None
        self.terminate = False
        self.time_estimated, self.average_attendance_time = None, None
        self.sum_minutes_per_truck = np.zeros(len(trucks_coordinates))
        self.indices_associations = list(range(0, len(requests_coordinates)))

        self.trucks_coordinates, self.requests_coordinates = trucks_coordinates, requests_coordinates
        self.volumes_requests, self.assignment_truck_request = volumes_requests, assignment_truck_request
        self.requests_priorities, self.inattention_days = requests_priorities, inattention_days

    def update(self, assignment_truck_request, inattention_days, requests_priorities, trucks_coordinates,
               requests_coordinates, volumes_requests):
        self.trucks_coordinates, self.requests_coordinates = trucks_coordinates, requests_coordinates
        self.volumes_requests, self.assignment_truck_request = volumes_requests, assignment_truck_request
        self.requests_priorities, self.inattention_days = requests_priorities, inattention_days

    def store_attendance_time(self, average_attendance_time):
        self.average_attendance_time = average_attendance_time

    def add_limits(self, maximum_truck_capacity, limit_work_minutes, maximum_inattention_days, maximum_trucks):
        self.maximum_truck_capacity, self.limit_work_minutes = maximum_truck_capacity, limit_work_minutes
        self.maximum_inattention_days, self.maximum_trucks = maximum_inattention_days, maximum_trucks

    def check_limit_trucks(self):
        self.assignment_truck_request = self.assignment_truck_request[:, :self.maximum_trucks] if len(
            self.assignment_truck_request[0]) > self.maximum_trucks else self.assignment_truck_request
        self.trucks_coordinates = self.trucks_coordinates[:self.maximum_trucks]

    def calculate_limit_minutes_worked(self):
        if len(self.time_estimated[0]) == len(self.requests_coordinates):
            result = np.where(self.assignment_truck_request == 1)
            indices = np.argsort(result[1])
            sorted_result = (result[0][indices], result[1][indices])
            for i in range(len(self.sum_minutes_per_truck)):
                self.sum_minutes_per_truck[i] += self.time_estimated[sorted_result[1], sorted_result[0]][i]
                self.sum_minutes_per_truck[i] += self.average_attendance_time
            self.indices_associations = [ele for ele in self.indices_associations if ele not in sorted_result[0]]
        elif len(self.time_estimated[0]) != len(self.requests_coordinates):
            new_indices = list(range(0, len(self.indices_associations)))
            indices_pairs = dict(zip(new_indices, self.indices_associations))
            result = np.where(self.assignment_truck_request == 1)
            matches = np.intersect1d(self.indices_associations, result[0])
            mapping = dict(zip(result[0], result[1]))
            new_result = [np.array(matches), np.array([mapping[element] for element in matches])]
            indices_new = np.argsort(new_result[1])
            sorted_result = (new_result[0][indices_new], new_result[1][indices_new])
            lst_results = []
            for x in sorted_result[0]:
                key = [k for k, v in indices_pairs.items() if v == x]
                lst_results.extend(key)
            if len(lst_results) == 1:
                self.sum_minutes_per_truck[int(sorted_result[1])] += float(self.time_estimated[sorted_result[1]])
                self.sum_minutes_per_truck[int(sorted_result[1])] += self.average_attendance_time
            else:
                for i in range(len(lst_results)):
                    self.sum_minutes_per_truck[i] += self.time_estimated[sorted_result[1], lst_results][i]
                    self.sum_minutes_per_truck[i] += self.average_attendance_time
            self.indices_associations = [i for i in self.indices_associations if i not in matches]

    def check_limit_minutes_worked(self):
        indices_to_remove = []
        for i in range(len(self.sum_minutes_per_truck)):
            if self.sum_minutes_per_truck[i] > self.limit_work_minutes:
                indices_to_remove.append(i)
        if len(indices_to_remove) != 0:
            self.trucks_coordinates = [i for j, i in enumerate(self.trucks_coordinates) if j not in indices_to_remove]
            self.assignment_truck_request = np.delete(self.assignment_truck_request, indices_to_remove, axis=1)
            self.sum_minutes_per_truck = [i for j, i in enumerate(self.sum_minutes_per_truck) if j not in indices_to_remove]

    def add_timings(self, time_estimated):
        self.time_estimated = time_estimated

    def check_truck_capacity(self):
        list_of_i_values = [i for i in range(len(self.assignment_truck_request[0])) if sum(
            self.volumes_requests[z] for z in range(len(self.assignment_truck_request[:, 0])) if
            self.assignment_truck_request[z, i] == 1) >= self.maximum_truck_capacity - 1]

        self.assignment_truck_request = np.delete(self.assignment_truck_request, list_of_i_values, 1)

        self.trucks_coordinates = [val for idx, val in enumerate(self.trucks_coordinates) if
                                   idx not in list_of_i_values]

    def check_priorities(self):
        self.requests_priorities = [1 if self.inattention_days[p] >= 10 else 0 for p in
                                    range(len(self.inattention_days))]

    def check_unique_assignment(self):
        self.assignment_truck_request = np.array([np.array([1] + [0] * (len(row) - 1)) if sum(row) > 1 else row

                                                  for row in self.assignment_truck_request])

    def verify_termination(self):
        counter = 0
        for row in self.assignment_truck_request:
            counter += sum(row)
        if counter == len(self.assignment_truck_request) or len(self.assignment_truck_request) == 0:
            self.terminate = True
