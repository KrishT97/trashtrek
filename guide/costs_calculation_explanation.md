## Calculating parameter and global costs to retrieve minimum cost route

As the problem statement states a multicriteria approach, there are 3 criterias considered to calculate the global cost, each one being the parameters:

- Road distance costs between Truck_i and Request_x
- Occupation costs for Truck_i
- Time awaited by user with Request_x

Considering that the global cost will be obtained my minimizing road distances and time awaited by user, whilst maximizing occupation of the vehicle.
This means that the ideal case to be solved first would be an object of maximum size to be disposed, that is located under minimum distance and uses minimum time awaited.

The weights are defined for each parameter, and the lists of arrays are normalized in scale of 0,1 to compare the parameters amongs themselves:

globalCost= 𝑤_𝑑𝑖𝑠𝑡 · 𝑋 (𝑛𝑜𝑟𝑚𝑎𝑙𝑖𝑧ed_𝑑𝑖𝑠𝑡) − 𝑤_𝑜𝑐𝑢𝑝 · 𝑋 (𝑛𝑜𝑟𝑚𝑎𝑙𝑖𝑧ed_𝑜𝑐𝑢𝑝) + 𝑤_𝑡𝑖me · 𝑋 (𝑛𝑜𝑟𝑚𝑎𝑙𝑖𝑧ed_𝑡𝑖me)

This will return an array with size of the numbers of trucks, having as many values in each list as number of requests.
With 3 trucks and 10 requests defined as an example, there will be 30 values.

From these values, the hungarian algorithm will be used to associate each truck to the request that minimizes the route, ending up with requests picked by the algorithm for each truck.

Achieved with the following:
```
self.row_ind, self.col_ind = linear_sum_assignment(global_costs)
```
This returns the indices of requests and trucks from which the minimum route is made.

