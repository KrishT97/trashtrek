# from scipy.spatial import distance
import osmnx as ox
import geopandas as gpd
import networkx as nx
import numpy as np
import requests


# google map to calculate real distance from coordinates
class PathCalculator:

    def __init__(self,graphhopper_api_key):
        self.initial_trucks_coordinates = None
        self.api_key = graphhopper_api_key
        self.api_url = "https://graphhopper.com/api/1/route"
        self.road_distances = None
        self.time_estimated = None
        self.vehicle_type = "car"

    def store_initial_data(self, initial_trucks_coordinates):
        self.initial_trucks_coordinates = initial_trucks_coordinates

    def calculate_graphhopper(self, trucks_coordinates, requests_coordinates):
        num_trucks = len(trucks_coordinates)
        num_requests = len(requests_coordinates)

        road_distances = np.zeros((num_trucks, num_requests))
        time_estimated = np.zeros((num_trucks, num_requests))

        for i, truck_coord in enumerate(trucks_coordinates):
            for j, request_coord in enumerate(requests_coordinates):

                start_coord = f"{truck_coord[0]},{truck_coord[1]}"
                end_coord = f"{request_coord[0]},{request_coord[1]}"
                api_request_url = f"{self.api_url}?point={start_coord}&point={end_coord}&vehicle={self.vehicle_type}&key={self.api_key}"

                response = requests.get(api_request_url)

                if response.status_code == 200:
                    result = response.json()

                    distance = result['paths'][0]['distance']
                    time = result['paths'][0]['time']

                    road_distances[i, j] = distance / 1000  # km
                    time_estimated[i, j] = time / 60000  # minutes

                    # Calculating distance and time for returning to initial truck coordinates
                    return_start_coord = end_coord
                    return_end_coord = f"{self.initial_trucks_coordinates[i][0]},{self.initial_trucks_coordinates[i][1]}"
                    return_api_request_url = f"{self.api_url}?point={return_start_coord}&point={return_end_coord}&vehicle={self.vehicle_type}&key={self.api_key}"

                    return_response = requests.get(return_api_request_url)

                    if return_response.status_code == 200:
                        return_result = return_response.json()
                        return_distance = return_result['paths'][0]['distance']
                        return_time = return_result['paths'][0]['time']

                        # Adding the return distance and time to the existing values
                        road_distances[i, j] += return_distance / 1000  # km
                        time_estimated[i, j] += return_time / 60000  # minutes
                    else:
                        print(
                            f"API request failed with status code {return_response.status_code} because {return_response.text}")
                else:
                    print(f"API request failed with status code {response.status_code} because {response.text}")

        self.road_distances = road_distances
        self.time_estimated = time_estimated
