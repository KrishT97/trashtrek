## How real accurate data is retrieved for route optimization

As for the parameter costs, the data had to be retrieved from somewhere. The distance from truck to request and time awaited/taken may seem correlated, as to one might think that, if there is a large distance, so would the time awaited be larger.

However there may be cases for how in certain scenarios, the distance and time taken might not be correlated. For example if the location of request is located up on a hill road, for which, the distance recorded might not be much, but because it is an incline, the vehicle takes longer than expected. With a decline road, we get much faster to the destination.

Therefore considering both as separate parameters, and also because the optimization is revolved around a mountainous location like Gran Canaria, it is safe to work with this analogy.

The distances is crucial, but cannot be taken directly as connections from one node to another like so:

![image](https://github.com/KrishT97/truck_route_planner/assets/92883393/75477acc-8051-4642-a6dd-2b217e6895f1)

As trucks and requests coordinates are not exactly a straight line distanced from each other in terms of the vehicle travelling, as they are mapped in real locations, the road routes have to be considered so that a vehicle would have to travel that route to get to the destination. 

So, the **road distances**, and with it the **time estimates**, are achieved through the GraphHopper Routing API:


![image](https://github.com/KrishT97/truck_route_planner/assets/92883393/db6e1c58-61f6-4bd4-9e23-ea450d85c273)

This way the costs obtained from the criterias are more accurate, taking into account, a more precise way of dealing the data. Both variables from the API can be captured through the json response for the api request. With options like travel profile for which one could tweak, it is a flexible and fast software that delivers useful and reliable geographical data.
