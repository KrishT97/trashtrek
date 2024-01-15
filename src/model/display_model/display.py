import networkx as nx
import math
from pyvis.network import Network
import folium
from folium import plugins
import requests


class Display:

    def __init__(self):
        self.graph = nx.DiGraph()
        self.interactive_network = Network(notebook=False, height="700px", width="100%")
        self.interactive_map = folium.Map(location=[28.00928603655914, -15.482817464516128], zoom_start=10)
        self.truck_colors = {0: 'blue', 1: 'red', 2: 'green', 3: 'cadetblue', 4: 'black', 5: 'purple', 6: 'beige'}
        self.request_colors = 'orange'
        self.graphhopper_api_key = "YOUR_API_KEY"

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

    def draw_graph_folium_results(self, trucks_coordinates, requests_coordinates, assigned_matrix,
                                  order_indexes):

        for i, node in enumerate(trucks_coordinates):
            lat, lon = node
            truck_color = self.truck_colors.get(i, 'gray')
            folium.Marker([lat, lon], popup=f"Truck {i}", icon=folium.Icon(color=truck_color)).add_to(
                self.interactive_map)

        for i, node in enumerate(requests_coordinates):
            lat, lon = node
            folium.Marker([lat, lon], popup=f"Petition {i}", icon=folium.Icon(color=self.request_colors)).add_to(
                self.interactive_map)

        for i in range(len(order_indexes) - 1):
            start_request = order_indexes[i]
            end_request = order_indexes[i + 1]

            start_truck = assigned_matrix[start_request].nonzero()[0][0]
            end_truck = assigned_matrix[end_request].nonzero()[0][0]

            route = self.get_route_from_graphhopper(
                requests_coordinates[start_request], requests_coordinates[end_request]
            )

            truck_color = self.truck_colors.get(start_truck, 'gray')
            folium.PolyLine(route, color=truck_color, weight=3, opacity=0.7).add_to(self.interactive_map)

            lat, lon = requests_coordinates[start_request]
            order_text = f"Truck {start_truck}: Order {i + 1}"
            folium.Marker([lat, lon], popup=folium.Popup(order_text, parse_html=True),
                          icon=folium.Icon(color=truck_color)).add_to(self.interactive_map)

        last_request = order_indexes[-1]
        last_truck = assigned_matrix[last_request].nonzero()[0][0]
        lat, lon = requests_coordinates[last_request]
        last_order_text = f"Truck {last_truck}: Order {len(order_indexes)}"
        folium.Marker([lat, lon], popup=folium.Popup(last_order_text, parse_html=True),
                      icon=folium.Icon(color=self.truck_colors.get(last_truck, 'gray'))).add_to(self.interactive_map)

        self.interactive_map.save("interactive_map_with_routes_results.html")
