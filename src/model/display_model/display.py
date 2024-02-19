import networkx as nx
import math
from pyvis.network import Network
import folium
import requests
import os


class Display:

    def __init__(self, graphhopper_api_key):
        self.graph = nx.DiGraph()
        self.interactive_network = Network(notebook=False, height="700px", width="100%")
        self.interactive_map = folium.Map(location=[28.00928603655914, -15.482817464516128], zoom_start=10)
        self.truck_colors = {0: 'blue', 1: 'red', 2: 'green', 3: 'pink', 4: 'black', 5: 'purple', 6: 'beige',
                             7: 'cadetblue', 8:'white', 9:'lightgreen', 10: 'lightgray', 11: 'darkred', 12: 'darkblue',
                             13: 'darkpurple', 14: 'lightred', 15: 'darkgreen'}
        self.request_colors = 'orange'
        self.graphhopper_api_key = graphhopper_api_key
        self.color_type = {'truck': 'lightblue', 'petition': 'lightgreen'}
        self.initial_trucks_coordinates = None
        self.result_directory = "application/results"

    def store_initial_data(self, initial_trucks_coordinates):
        self.initial_trucks_coordinates = initial_trucks_coordinates

    def draw_graph(self, trucks_coordinates, requests_coordinates):
        self.graph.add_nodes_from(trucks_coordinates, type="truck")
        self.graph.add_nodes_from(requests_coordinates, type="request")

        for initial in trucks_coordinates:
            for request in requests_coordinates:
                distancia = ((initial[0] - request[0]) ** 2 + (initial[1] - request[1]) ** 2) ** 0.5

                self.graph.add_edge(initial, request, weight=round(distancia, 2))

        for i in range(len(requests_coordinates) - 1):
            for j in range(i + 1, len(requests_coordinates)):
                distancia = ((requests_coordinates[i][0] - requests_coordinates[j][0]) ** 2 +
                             (requests_coordinates[i][1] - requests_coordinates[j][1]) ** 2) ** 0.5

                self.graph.add_edge(requests_coordinates[i], requests_coordinates[j], weight=round(distancia, 2))

        for node, attrs in self.graph.nodes(data=True):
            color = self.color_type.get(attrs['type'], 'gray')
            self.interactive_network.add_node(str(node), label=f"{node}\n{attrs['type']}", title=str(attrs['type']),
                                              color=color)

        for initial, end, attrs in self.graph.edges(data=True):
            self.interactive_network.add_edge(str(initial), str(end), label=f"{attrs['weight']:.2f}")
            self.interactive_network.add_edge(str(requests_coordinates[i]), str(requests_coordinates[j]),
                                              label=f"{attrs['weight']:.2f}")

        self.interactive_network.show("interactive_graph.html", notebook=False)

        print("Possible combinations for a closed cycle given nodes:",
              math.factorial(len(requests_coordinates) - 1))

    def get_route_from_graphhopper(self, start, end):
        url = f'https://graphhopper.com/api/1/route?point={start[0]},{start[1]}&point={end[0]},{end[1]}&points_encoded=False&vehicle=car&key={self.graphhopper_api_key}'
        response = requests.get(url)
        route_data = response.json()

        snapped_waypoints = route_data['paths'][0]['points']['coordinates']

        coordinates = [(point[1], point[0]) for point in snapped_waypoints]

        return coordinates

    def draw_basic_graph(self, trucks_coordinates, petitions_coordinates, base_url):

        for node in trucks_coordinates:
            lat, lon = node
            folium.Marker([lat, lon], popup=f"Truck: {node}", icon=folium.Icon(color='blue')).add_to(
                self.interactive_map)

        for node in petitions_coordinates:
            lat, lon = node
            folium.Marker([lat, lon], popup=f"Petition: {node}", icon=folium.Icon(color='green')).add_to(
                self.interactive_map)

        for initial in trucks_coordinates:
            for end in trucks_coordinates + petitions_coordinates:
                if initial != end:
                    route = self.get_route_from_graphhopper(initial, end)
                    folium.PolyLine(route, color="gray", weight=3, opacity=0.7).add_to(self.interactive_map)

        result_file_path = f"{self.result_directory}/basic_map_with_routes.html"
        self.interactive_map.save(result_file_path)
        return base_url + "results/" + "basic_map_with_routes.html"

    def draw_graph_order_routes(self, trucks_coordinates, requests_coordinates, assigned_matrix,
                                order_indexes, base_url):

        for i, node in enumerate(trucks_coordinates):
            lat, lon = node
            truck_color = self.truck_colors.get(i, 'gray')
            folium.Marker([lat, lon], popup=f"Truck {i}", icon=folium.Icon(color=truck_color)).add_to(
                self.interactive_map)

        for i, node in enumerate(requests_coordinates):
            lat, lon = node
            request_color = self.request_colors
            request_index = i
            attending_trucks = [truck_index for truck_index, value in enumerate(assigned_matrix[request_index, :]) if
                                value]
            truck_info = ", ".join([f"Truck {truck}" for truck in attending_trucks])
            popup_text = f"Request {i} attended by {truck_info}"
            folium.Marker([lat, lon], popup=folium.Popup(popup_text, parse_html=True),
                          icon=folium.Icon(color=request_color)).add_to(self.interactive_map)

        for i, truck_node in enumerate(trucks_coordinates):
            truck_color = self.truck_colors.get(i, 'gray')

            attended_requests = [index for index, value in enumerate(assigned_matrix[:, i]) if value]

            for request_index in attended_requests:
                route = self.get_route_from_graphhopper(truck_node, requests_coordinates[request_index])
                folium.PolyLine(route, color=truck_color, weight=3, opacity=0.7).add_to(self.interactive_map)

        for i, request_index in enumerate(order_indexes):
            lat, lon = requests_coordinates[request_index]
            order_text = f"Order nº {i + 1}"
            request_color = self.request_colors
            attending_trucks = [truck_index for truck_index, value in enumerate(assigned_matrix[request_index, :]) if
                                value]
            truck_info = ", ".join([f"Truck {truck}" for truck in attending_trucks])
            popup_text = f"{truck_info}:\n{order_text}\n"
            folium.Marker([lat, lon], popup=folium.Popup(popup_text, parse_html=True),
                          icon=folium.Icon(color=request_color)).add_to(self.interactive_map)

        result_file_path = f"{self.result_directory}/map_with_order_routes.html"
        self.interactive_map.save(result_file_path)
        return base_url + "results/" + "map_with_order_routes.html"


