## Reviewing an example case

We will define the initial data as the following:

### Vehicles
Three vehicles defined:
- Vehicle 0- Punto Limpio Maspalomas (27.770183, -15.597304)
- Vehicle 1- Punto Limpio Arucas (28.128852, -15.504827)
- Vehicle 2- Punto Limpio El Batán (28.093512, -15.425922)

### Requests
Ten requests defined:
- Request 0- To dispose center table in Las Torres, Las Palmas (28.118482, -15.445237)
- Request 1- To dispose individual bed in Tamaraceite, Las Palmas (28.100746, -15.474429)
- Request 2- To dispose small cabinet in Arucas, Las Palmas (28.130995, -15.515053)
- Request 3- To dispose double bed in Teror, Las Palmas (28.065085, -15.545675)
- Request 4- To dispose desk near Playa Canteras, Las Palmas (28.138761, -15.435350)
- Request 5- To dispose television in Arucas, Las Palmas (28.118830, -15.526022)
- Request 6- To dispose dining table in Teror, Las Palmas (28.059831, -15.547753)
- Request 7- To dispose office chair in Puerto Mogán, Lomo Quiebre (27.818894, -15.765593)
- Request 8- To dispose large bookshelf in Vecindario (27.838164, -15.442441)
- Request 9- To dispose big mirror in Puerto Rico de Gran Canaria (27.789653, -15.717291)

### Other information
- The maximum time of work for vehicles is of 8 hours.
- Maximum days of requests unattended are 10.
- Maximum number of vehicles to be used are 10.
- Maximum capacity of vehicles is of 10 m3.
- Maximum number of drivers available are 10.

The body of the POST data as follows:
```
{
  "dailyLimitWorkInMinutes": 480,
  "maximumInattentionDays": 10,
  "maximumTrucksDefined": 10,
  "maximumTruckCapacity(m3)": 10,
  "numberOfAvailableDrivers": 10,
  "truckInformation": [
    {
      "coordinates": "(28.093512, -15.425922)",
      "volume(m3)": 10
    },
    {
      "coordinates": "(28.128852, -15.504827)",
      "volume(m3)": 10
    },
    {
      "coordinates": "(27.770183, -15.597304)",
      "volume(m3)": 10
    }
  ],
  "requestsInformation":[
    {
      "coordinates": "(28.118482, -15.445237)",
      "volume(m3)": 0.5
    },
    {
      "coordinates": "(28.100746, -15.474429)",
      "volume(m3)": 1.5
    },
    {
      "coordinates": "(28.130995, -15.515053)",
      "volume(m3)": 0.05
    },
    {
      "coordinates": "(28.065085, -15.545675)",
      "volume(m3)": 2.5
    },
    {
      "coordinates": "(28.138761, -15.435350)",
      "volume(m3)": 2.0
    },
    {
      "coordinates": "(28.118830, -15.526022)",
      "volume(m3)": 0.32
    },
    {
      "coordinates": "(28.059831, -15.547753)",
      "volume(m3)": 1.11
    },
    {
      "coordinates": "(27.818894, -15.765593)",
      "volume(m3)": 0.33
    },
    {
      "coordinates": "(27.838164, -15.442441)",
      "volume(m3)": 0.55
    },
    {
      "coordinates": "(27.789653, -15.717291)",
      "volume(m3)": 0.23
    }
  ]
}
```
Two trucks are located in the north, whilst one in the south. The volume (m3) figures are generic and approximates.

For this case, let us visualize the basic map (_the object drawings are not part of the visualization but serve as illustration for this example_):

<img src="https://github.com/KrishT97/trashtrek/blob/main/extras/visualization_results1.png" width="600"/>

<img src="https://github.com/KrishT97/trashtrek/blob/main/extras/visualization_results2.png" width="600"/>

As we can see, the **green icons reflect the requests** whilst the **blue, the trucks**.

Running the algorithm, the following interpretations are obtained, the assignment matrix looks like the following:

```math
$$  \begin{bmatrix}
    [1 && 0 && 0] \\
    [1 && 0 && 0] \\
    [0 && 1 && 0] \\
    [0 && 1 && 0] \\
    [1 && 0 && 0] \\
    [0 && 1 && 0] \\
    [0 && 1 && 0] \\
    [0 && 0 && 1] \\
    [0 && 0 && 1] \\
    [0 && 0 && 1]
    \end{bmatrix} $$
```
_** Read eg. truck_work_time_explanation.md in order to understand the structure interpretation of the assignment matrix_.

As we might figure: 
- Truck 0 _(blue)_(_starting the associations from 0_) ---> Request 0, 1 and 4.
- Truck 1 _(red)_---> Request 2, 3, 5 and 6.
- Truck 2 _(green)_---> Request 7, 8 and 9.

The order to follow (_obtained from the globalAttendanceOrder parameter_):
```
[3, 4, 8, 1, 6, 7, 0, 5, 9, 2]
```

The route mapping (_attendance in order_):
1. Truck 1 ---> Request 3.
2. Truck 0 ---> Request 4.
3. Truck 2 ---> Request 8.
4. Truck 0 ---> Request 1.
5. Truck 1 ---> Request 6.
6. Truck 2 ---> Request 7.
7. Truck 0 ---> Request 0.
8. Truck 1 ---> Request 5.
9. Truck 2 ---> Request 9.
10. Truck 1 ---> Request 2.

** _Within the visualization, the order is displayed **by the trucks** and not the actual global attendance, therefore mapped to be sequential by truck index. This data is shown within the assignedRequestsOrderByTruck variable in the results section. The reason is supposing that all vehicles will travel at the same time or schedule, seeing the assignment ordered by each truck index will better visualize the route each truck follows independently._

Now, visualizing the results obtained from the routing:

<img src="https://github.com/KrishT97/trashtrek/blob/main/extras/visualization_results3.png" width="600"/>

<img src="https://github.com/KrishT97/trashtrek/blob/main/extras/visualization_results4.png" width="600"/>

### Analysis

The request with the largest object to dispose (double bed in Teror) is attended first by the closest contact, being Truck 1. Next, for Truck 0, the route it follows leads it to going first to Las Canteras (large desk) and then to Tamaraceite (single bed), this is because it is prioritizing heavy loads firstly to be resolved (_given that larger objects produce higher urgency from the client's perspective_), and then finally it heads to Las Torres (center table, the smaller object in m3 out of the two attended previously).

**Truck 1** follows a clear route, it heads to the request in Teror (double bed) and then to the other nearest request, also in Teror (dining table), then, it goes to Arucas (television) and the other request also in the same zone (small cabinet), this last request being the closest to base, ending the transit.  

**Truck 2** remains in the south and deals with the requests over in that region, as expected. Heading first to Vecindario to retrieve a large bookshelf, then heading to the furthest request from it in Puerto Mogán. Reason being to return back to base effectively after the next request in Puerto Rico, as it is on the way whilst wanting to return to base later, and because the office chair occupies more than a mirror in terms of overall volume (m3).

Large objects are complicated to deal with and resolve upon attending requests, not only because of the size of occupancy for the vehicle but also other factors, like trying to carry it and fit it in the truck, apart from other factors as mentioned previously of customers wanting to dispose it as fast as possible producing inconvenience (for example, it will not be a similar experience for an individual to have a broken chair sitting at their doorstep than having a large sofa occupying the hallway). 

This is why dealing first with voluminous objects is crucial, smaller objects can then easily be handled even if their isn't much space left in the vehicle . 

### To keep in mind

One strange aspect might be considered for the results obtained and the visualization. Why would in certain examples a truck travel all the way from
the south to the north (after all, it has to also return back) whilst there being other trucks near the locations in the north (from _Las Palmas_)?

The answer is due to the multicriteria approach, the distance is not the only metric to be handled, and we need to ensure
that all trucks work cooperatively. Also, each truck **must** work, in order for the hungarian algorithm to also make assignments, it will consider **all** trucks specified. That is how the application is designed, so a question arises; **is there a possibility that less trucks
than the specified could attend all requests more efficiently**? 

Yes, however this implementation is not made and may require multiple events running in parallel to find the best search, and providing more optimal solutions upon findings. Or simply using another, more complex, selection method to not consider all trucks, but even a subset amongst those present to find the most efficient route. Furthermore it may seem, that the approach is also more computing-intensive, an optimization problem scaled in complexity, but could be a part of a _further investigation proposal_.  

However, and to contradict the above theory from one perspective, we want to consider that the trucks **should all be operational**, for which the specification of it in the initial data makes it be considered no matter where located in the map.

Due to this, the trucks, even if located in the south region have to attend requests in the north region if the other trucks in that region are occupied. 

One advantage of this system (considering all trucks) amongst other, is the load balance. 

Distributing the weight and overall consumption throughout all trucks ensure an optimal balancing, 
it also gives place to a more well organized and regulated structure, whilst also guaranteeing that the 
trucks capacity doesn't alter their speed & thus time, so much (as not one or some, a subset, are doing all the work and 
taking all the weight of the objects to be disposed from the requests demands, instead, all are).

