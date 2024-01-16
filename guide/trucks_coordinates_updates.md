## Trucks coordinates need to get updated in each iteration

The concept is simple, the trucks keep moving when requests are assigned to it. If the starting position of trucks is so:

```
trucks = [Truck(1, 10, (28.093512, -15.425922)), Truck(2, 10, (28.128852, -15.504827)),
          Truck(3, 10, (27.770183, -15.597304))]
````
If there is a particular request:

```
request = [Request(1, (27.755366, -15.604631), 0.2),....]
```
From which the Hungarian algorithm detected that Truck 3 had to solve the Request 1, the coordinates for that truck gets updated after obtaining the minimum route through the algorithm. Which means:
```
trucks = [Truck(1, 10, (28.093512, -15.425922)), Truck(2, 10, (28.128852, -15.504827)),
          Truck(3, 10, (27.755366, -15.604631))]
```
Now for any other requests down the line, the distance calculations between trucks and requests in next iterations will take the positions for the trucks above updated.
