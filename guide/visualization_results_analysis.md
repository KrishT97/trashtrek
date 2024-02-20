## Reviewing an example case

The initial truck coordinates start out as such:

```
[(28.093512, -15.425922), (28.128852, -15.504827), (27.770183, -15.597304), (27.843992, -15.438345)]
```
Meaning, the first two trucks are located within the _Las Palmas_ region, the third in _Maspalomas_ and the last in _Vecindario_. 
The locations reflecting the "punto limpios" (garbage disposal areas) in Gran Canaria.

A set of request coordinates as follows scattered around the map:

```
[(28.118482, -15.445237), (28.100746, -15.474429), (28.130995, -15.515053), (28.065085, -15.545675), (28.138761, -15.43535), (28.11883, -15.526022), (28.059831, -15.547753), (28.008196, -15.533061), (27.851273, -15.466471)]
```
As one might guess, practically almost all are within the _Las Palmas_ region, expect one which is in the _Vecindario_ region.

For this case, let us visualize the basic map:

<img src="https://github.com/KrishT97/trashtrek/blob/main/extras/basic_map.png" width="600"/>

As we can see, the **green icons reflect the requests** whilst the **blue, the trucks**.

Running the algorithm, the following interpretations are obtained, the asssignment matrix looks like the following:

```math
$$  \begin{bmatrix}
    [1 && 0 && 0 && 0] \\
    [0 && 0 && 0 && 1] \\
    [0 && 1 && 0 && 0] \\
    [0 && 1 && 0 && 0] \\
    [1 && 0 && 0 && 0] \\
    [0 && 0 && 0 && 1] \\
    [0 && 1 && 0 && 0] \\
    [0 && 0 && 1 && 0] \\
    [0 && 0 && 1 && 0]
    \end{bmatrix} $$
```
_** Read eg. truck_work_time_explanation.md in order to understand the structure interpretation of the assignment matrix_.

As we might figure: 
- Truck 0 _(blue)_(_starting the associations from 0_) ---> Request 0 and 4.
- Truck 1 _(red)_---> Request 2, 3 and 6.
- Truck 2 _(green)_---> Request 7 and 8.
- Truck 3 _(cadet blue)_---> Request 1 and 5.

The order to follow (_obtained from the globalAttendanceOrder parameter_):
```
[1, 3, 4, 8, 0, 5, 6, 7, 2]
```

The route mapping (_attendance in order_):
1. Truck 3 ---> Request 1.
2. Truck 1 ---> Request 3.
3. Truck 0 ---> Request 4.
4. Truck 2 ---> Request 8.
5. Truck 0 ---> Request 0.
6. Truck 3 ---> Request 5.
7. Truck 1 ---> Request 6.
8. Truck 2 ---> Request 7.
9. Truck 1 ---> Request 2.

Now, visualizing the results obtained from the routing:

<img src="https://github.com/KrishT97/trashtrek/blob/main/extras/routes_map.png" width="600"/>

### Analysis

One strange aspect might be considered for the results obtained and the visualization. Why does Truck 2 (green truck) and Truck 3 (cadet blue) travel all the way from
the south to the north (after all, it has to also return back) whilst there being other trucks near the locations in the north (from _Las Palmas_)?

The answer is due to the multicriteria approach, keep in mind, the distance is not the only metric to be handled, and we need to ensure
that all trucks work cooperatively. Also, each truck **must** work, in order for the hungarian algorithm to also make assignments, it will consider **all** trucks specified. That is how the application is designed, so a question arises; **is there a possibility that less trucks
than the specified could attend all requests more efficiently**? 

Yes, however this implementation is not made and may require multiple events running in parallel to find the best search, and providing more optimal solutions upon findings. Or simply using another, more complex, selection method to not consider all trucks, but even a subset amongst those present to find the most efficient route. However it may seem that the approach is also more computing-intensive, an optimization problem scaled in complexity, but could be a part of a _further investigation proposal_.  

However, and to contradict the above theory from one perspective, we want to consider that the trucks **should all be operational**, for which the specification of it in the initial data makes it be considered no matter where located in the map.

Due to this, the trucks, even if located in the south region have to attend requests in the north region. 
One advantage of this system (considering all trucks) amongst other, is the load balance. 

Distributing the weight and overall consumption throughout all trucks ensure an optimal balancing, 
it also gives place to a more well organized and regulated structure, whilst also guaranteeing that the 
trucks capacity doesn't alter their speed & thus time, so much (as not one or some, a subset, are doing all the work and 
taking all the weight of the objects to be disposed from the requests demands, instead, all are).
