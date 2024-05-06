## How real accurate data is retrieved for route optimization

As for the parameter costs, the data had to be retrieved from a source that would be reliable enought to offer precise and accurate measurements. The distance from truck to request and time awaited/taken may seem correlated, as to one might think that, if there is a large distance, so would the time awaited be larger.

However there may be cases for how in certain scenarios, the distance and time taken might not be correlated. Taking as example the conditions given for a specific road, the time it takes to get from Node A to B when it is an uphill road is larger than if the same road was a decline. This argument is especially valid to apply for cases to be solved in the region of Gran Canaria due to it's mountainous terrain.

The distancess between requests and trucks is crucial, but cannot be taken directly as connections from one node to another like shown in the figure:

![image](https://github.com/KrishT97/truck_route_planner/assets/92883393/75477acc-8051-4642-a6dd-2b217e6895f1)

As trucks and requests coordinates are not exactly a straight line distanced from each other in terms of the vehicle travelling, due to working in real locations, the road routes have to be considered so that a vehicle would have to travel that road route to get to the destination. 

So, the **road distances in kilometres**, and with it the **time estimates in minutes**, are achieved between the vehicle and requests routes through the GraphHopper Routing API:


![image](https://github.com/KrishT97/truck_route_planner/assets/92883393/db6e1c58-61f6-4bd4-9e23-ea450d85c273)

This way the costs obtained from the criterias are accurate, as a more precise way of dealing the data is used. Both variables from the API can be captured through the JSON response when making an API call. With options like travel profile for which one could tweak for the vehicles, as well as an easy-to-use interface for data retrieval and access amongst numerous parameteres, it is a flexible and fast software that delivers useful and reliable geographical data through routes captured by input pairing coordinates.
