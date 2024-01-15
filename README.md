# Truck Route Planner
### Optimization of Truck Logistics for the Disposal of Voluminous Waste: A Multicriteria Approach

The objective of this project is the development of software to optimize the management of the
collection of voluminous waste, specifically addressing the challenges associated with
**Traveling Salesman Problem** (TSP) and the **Vehicle Routing Problem** (VRP). 

These problems, being NP-complete, present a series of complexities that require intelligent and efficient solutions to ensure optimal route management.
The development of efficient software for bulky waste management must address these
mathematical challenges and advanced algorithms, providing approximate solutions that can
approach the optimal solution in reasonable computational times. The successful implementation of these
strategies will ensure efficient and sustainable route management.

General challenges faced, part of which are comprised within TSP and VRP type of problems:
- Exponential Complexity: The number of possible routes grows factorially with the number of points, which turns the search for the optimal solution into a problem computationally challenging.
- Consideration of Restrictions: The inclusion of vehicle capacity restrictions and temporal restrictions add an additional layer of complexity to the problem.
- Vehicle Assignment: Determining the optimal number of vehicles and allocating efficiently a collection of requests to each one, considering capacity and temporary restrictions.
- Multi-Route Optimization: Coordinating multiple vehicles to minimize total distance traveled and other variables, which adds additional complexity.

The project delves into the specific location of Gran Canaria in Canary Islands, but can be replicated towards other cases.

Features presented:

- Distance by road and estimated time calculated with **GraphHopper Routing API**
- Real map generated with **Folium**
- **Multicriteria with multi-variable restrictions** model engine personalized for pickup of voluminous objects
- **Hungarian algorithm** robust method for mínimum search
- Most **optimal route search** optimization amongst numerous combinations

The global costs is considered for three parameters, each one having to be normalized and have an associated weight constant; **distance costs**, **vehicle occupation costs** and **awaited time costs**. As mentioned before, the hungarium algorithm is then utilized to pick the least cost amongst other intercepting costs.

The goal is to _**minimize** distance and awaited time costs_ and _**maximize** occupation of the vehicle_ for the selection of the most optimal route given a series of requests to be attended by the trucks in service.

There are various restrictions that are verified within each iteration, here are the following:
- Number of trucks in service cannot exceed the limit of trucks specified initially.
- Each truck will have an estimated time worked, it should not exceed to the limit defined as per the maximum working time.
- For each request, there should only be one truck assignmed to it.
- There is a dissatention time gathered for each request that is not attended on that day is left for the next day. There is a maximum of days the request remains attended and should receive maximum priority upon getting close to that limit of maximum defined.
- Each truck has a maximum capacity, it should not attend more requests if capacity of the vehicle has reached its limit, it returns back to base.


An example:

<br/><br/>
<img width="600" alt="image832" src="https://github.com/KrishT97/truck_route_planner/assets/92883393/1bc4cd0b-431e-45c3-9589-adcc88e133f3">
<br/><br/>
<img width="600" alt="image1060" src="https://github.com/KrishT97/truck_route_planner/assets/92883393/1c438469-193c-4aae-b2b1-b8d5e8a73c60">
<br/><br/>
Special thanks to the GraphHopper Team & Co-Founder Peter for providing upgraded API usage for the functionality of the project. 

This could only have been done because of the collaboration with Monentia, technological consultancy & information systems development company in Gran Canaria, Spain. As well as institution of Universidad Las Palmas de Gran Canaria for the approval of final project. 


