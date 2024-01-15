import numpy as np


class ModelData:

    def __init__(self, requests, drivers, trucks):
        if len(drivers) < len(trucks):
            trucks = trucks[:len(drivers)]
        self.attendance_order = []
        self.trucks_coordinates = ([trucks[i].coordinates for i in range(len(trucks))])
        self.requests_coordinates = ([requests[i].coordinates for i in range(len(requests))])
        self.volumes_requests = [requests[i].volume_object for i in range(len(requests))]
        self.inattention_days, self.requests_priorities = [0] * len(requests), [0] * len(requests)
        self.assignment_truck_request = np.zeros((len(requests), len(trucks)), dtype=int)

    def update(self, assignment_truck_request, inattention_days, requests_priorities, trucks_coordinates,
               requests_coordinates, volumes_requests):
        self.trucks_coordinates, self.requests_coordinates = trucks_coordinates, requests_coordinates
        self.inattention_days, self.requests_priorities = inattention_days, requests_priorities
        self.volumes_requests, self.assignment_truck_request = volumes_requests, assignment_truck_request

    def assign_request(self, row_ind, col_ind):
        self.assignment_truck_request[col_ind, row_ind] = 1

    def change_truck_coordinates(self, row_ind, col_ind, request_coordinates):
        for i in range(len(col_ind)):
            self.trucks_coordinates[row_ind[i]] = request_coordinates[col_ind[i]]

    def fetch_route_attendance_order(self):
        indices = np.argwhere(self.assignment_truck_request == 1)
        indices = indices[:, 0]
        for idx in indices:
            if idx not in self.attendance_order:
                self.attendance_order.append(idx)

