import numpy as np


class DistanceNormalizer:

    def __init__(self):
        self.normalized_trucks_distance, self.normalized_trucks_occupation = None, None
        self.normalized_trucks_time, self.is_verified = None, False
        self.predetermined_scale_factor_distance = 100
        self.predetermined_scale_factor_occupation = 10
        self.predetermined_scale_factor_time = 60

    def normalize(self, distance_costs_trucks, occupation_costs_trucks, time_costs_trucks):
        if self.is_verified:

            self.normalized_trucks_distance = (distance_costs_trucks - np.min(distance_costs_trucks)) / (
                    np.max(distance_costs_trucks) - np.min(distance_costs_trucks))
            self.normalized_trucks_occupation = (occupation_costs_trucks - np.min(occupation_costs_trucks)) / (
                    np.max(occupation_costs_trucks) - np.min(occupation_costs_trucks))
            self.normalized_trucks_time = (time_costs_trucks - np.min(time_costs_trucks)) / (
                    np.max(time_costs_trucks) - np.min(time_costs_trucks))
        else:
            self.normalized_trucks_distance = np.array([[dist[0]] for dist in distance_costs_trucks]) / self.predetermined_scale_factor_distance
            self.normalized_trucks_occupation = np.array([[occupation[0]] for occupation in occupation_costs_trucks]) / self.predetermined_scale_factor_occupation
            self.normalized_trucks_time = np.array([[time[0]] for time in time_costs_trucks]) / self.predetermined_scale_factor_time

    def verify(self, requests_coordinates):
        self.is_verified = False if len(requests_coordinates) == 1 else True
