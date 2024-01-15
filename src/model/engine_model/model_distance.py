import numpy as np


class ModelDistance:

    def __init__(self, requests):
        self.indexes_requests = [request.id for request in requests]
        self.modified_indexes, self.is_first_iteration = None, True
        self.assigned_requests_indexes = []
        self.requests_coordinates, self.volumes_requests, self.assignment_truck_request = None, None, None
        self.distance_costs_trucks, self.occupation_costs_trucks, self.time_costs_trucks = None, None, None

    def update(self, requests_coordinates, volumes_requests, assignment_truck_request):
        if not self.is_first_iteration:
            self.requests_coordinates = [value for index, value in
                                         enumerate(requests_coordinates) if
                                         index not in self.assigned_requests_indexes]
            self.volumes_requests = np.delete(np.array(volumes_requests),
                                              self.assigned_requests_indexes).tolist()
            self.assignment_truck_request = assignment_truck_request[
                ~np.any(assignment_truck_request >= 1, axis=1)]
            self.modified_indexes = np.delete(np.array(self.indexes_requests),
                                              self.assigned_requests_indexes).tolist()
        else:
            self.requests_coordinates = requests_coordinates
            self.volumes_requests = volumes_requests
            self.assignment_truck_request = assignment_truck_request

    def extend_assigned_requests(self, col_ind):
        self.assigned_requests_indexes.extend(col_ind.tolist())
