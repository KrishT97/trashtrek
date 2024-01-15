import numpy as np


class CostEstimator:

    def __init__(self, weight_distance, weight_occupation, weight_time):
        self.volumes_requests, self.assignment_truck_request, self.global_costs = None, None, None
        self.distance_costs_trucks, self.occupation_costs_trucks, self.time_costs_trucks = [], [], []
        self.weight_distance, self.weight_occupation, self.weight_time = weight_distance, weight_occupation, weight_time

    def calculate_parameter_costs(self, volumes_requests, assignment_truck_request, road_distances, time_estimated):

        for z in range(len(assignment_truck_request[0])):
            self.distance_costs_trucks.append(road_distances[z])
            if len(volumes_requests) == len(assignment_truck_request):
                self.occupation_costs_trucks.append(
                    np.array([volumes_requests[i] for i in range(len(volumes_requests))]))
            else:
                if not volumes_requests:
                    self.occupation_costs_trucks.append(np.array(np.array([0.0])))
                else:
                    self.occupation_costs_trucks.append(np.array([volumes_requests[0]]))
            self.time_costs_trucks.append(time_estimated[z])

    def calculate_global_costs(self, normalized_trucks_distance, normalized_trucks_occupation, normalized_trucks_time):
        self.global_costs = self.weight_distance * normalized_trucks_distance - self.weight_occupation * normalized_trucks_occupation + self.weight_time * normalized_trucks_time
