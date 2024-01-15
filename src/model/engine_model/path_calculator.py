import osmnx as ox
import geopandas as gpd
import networkx as nx
import numpy as np
import requests


class PathCalculator:

    def __init__(self):
        self.api_key = "YOUR_API_KEY"
        self.api_url = "https://graphhopper.com/api/1/route"
        self.road_distances = None
        self.time_estimated = None
        self.vehicle_type = "car"

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
                else:
                    print(f"API request failed with status code {response.status_code} because {response.text}")

        self.road_distances = road_distances
        self.time_estimated = time_estimated
