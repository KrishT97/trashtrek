## Implementation of trucks returning back to base

One fundamental aspect to consider upon establishing the routes for the trucks is the starting point (which usually is 
from a waste disposal area, base as to be referred) and that after completing the requests, must return back to base
as a necessary requisite for the disposal of the objects.

The aspect further also affects the calculation of the parameter and global costs obtained, as now, upon calculating the
costs to travel to a request point in map, there should be an additional factor of returning back to base. To which, the
requests that are situated furthest from base, will lead to higher costs and would as a result, be least prioritized.

A way to tackle this implementation is to follow this approach:

Now, for each of the costs calculated we want to add the cost for that specific request location returning 
back to the base location, for this, whilst retrieving the distance and time in GraphHopper Routing API in the main
logic in this line of code:

`path_calculator.calculate_graphhopper(model_data.trucks_coordinates, model_distance.requests_coordinates)`

For this, instead of obtaining the one way distance and time for the requests in here:

`road_distances[i, j] = distance / 1000  # km`

`time_estimated[i, j] = time / 60000  # minutes`

After the section, an additional factor will now be added, making a new request to the API, for the distances and time taken between the requests and the initial truck coordinates (base coordinates) as such:

 `road_distances[i, j] += distance_return / 1000  # km`
 
 `time_estimated[i, j] += time_return / 60000  # minutes`

  This solves the issue, distance and time taken of returning routes that are large will consequently mean that the 
  request is located far away from base, and if the truck travels to that location, it also has to be able to come 
  back leading to additional consumption. Leading to higher parameter and global costs associated to the request. 

A few advantages to this proposal and its implementation:
- Realistic Scenario Modeling:

In real-world scenarios, vehicles, like trucks, often need to return to a central location or base after completing their tasks. Ignoring the return journey might result in suboptimal routes and inaccurate cost estimations.

- Completeness of Cost Estimation:

Including the return journey provides a more comprehensive cost estimation, accounting for both the outbound and inbound legs of the trip. This can lead to better-informed decision-making in route optimization.

- Optimizing Total Travel Time and Distance:

By considering the entire round trip (from the base to requests and back to the base), the optimization algorithm can better prioritize routes that minimize the overall travel time and distance for each vehicle.

- Handling Practical Constraints:

For waste disposal trucks, it's common for them to start and end their routes at a waste disposal area (base). Therefore, modeling the return journey is crucial for addressing practical constraints and accurately reflecting the operational reality.

- Algorithm Robustness:

Including the return journey in the optimization algorithm enhances its robustness by preventing solutions that might seem optimal only because they ignore the return leg. This can lead to more reliable and realistic route plans.

