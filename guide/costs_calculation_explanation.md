## Calculating parameter and global costs to retrieve minimum cost route

As the problem statement abbreviates a **multicriteria** approach, there are 3 criterias considered to calculate the global costs, each one being the parameters:

- Road distance costs between Truck<sub>i</sub> and Request<sub>x</sub>
- Occupation costs for Truck<sub>i</sub>
- Time awaited by user with Request<sub>x</sub>

Considering that the global cost will be obtained my _minimizing_ road distances and time awaited by user, whilst _maximizing_ occupation of the vehicle.

This means that the ideal case to be solved first would be an object/s of maximum size to be disposed, that is located under minimum distance and uses minimum time awaited. Keeping in mind that distance and time both don't have to be correlated (_eg. an incline road in terms of distance could be of low cost but high when it comes to time due to energy consumption of the vehicle and factors englobing the acceleration_).

The weights are defined for each parameter, and the lists of arrays are normalized in scale of 0,1 to compare the parameters amongst themselves:

globalCost= 𝑤<sub>dist</sub> · 𝑋<sub>𝑛𝑜𝑟𝑚𝑎𝑙𝑖𝑧ed_𝑑𝑖𝑠𝑡</sub> − 𝑤<sub>𝑜𝑐𝑢𝑝</sub> · 𝑋<sub>𝑛𝑜𝑟𝑚𝑎𝑙𝑖𝑧ed_𝑜𝑐𝑢𝑝</sub> + 𝑤<sub>𝑡𝑖me</sub> · 𝑋<sub>𝑛𝑜𝑟𝑚𝑎𝑙𝑖𝑧ed_𝑡𝑖me</sub>

Before applying the global costs, it would be necessary to normalize the three parameters to have them be comparable against one another (as the three are in different scales, distance in km, occupation in m3 and time in min). There is a verification procedure to validate the sizes of the lists containing the data, if there is only one data, it is not possible to normalize. Thus a technique is applied, which consists in dividing the value by a fixed maximum for the parameter (determined through empirical analysis).

The global costs will return an array with size of the numbers of trucks, having as many values in each list as number of requests.

With 3 trucks and 10 requests as an example, there will be 30 values. Each row in the array is a list referring to the vehicle, each element in the list to the petition. In this case, the array would be composed of 3 lists with 10 elements in each.

From these values, the _hungarian algorithm_ will be used to associate each truck to the request that minimizes the route, ending up with requests picked by the algorithm for each truck.

Achieved with the following:
```
self.row_ind, self.col_ind = linear_sum_assignment(global_costs)
```
This returns the indices of requests and trucks from which the minimum route is made in the iteration.

