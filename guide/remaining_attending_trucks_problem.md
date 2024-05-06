## What if there is only one truck available to attend the requests?

The _ModelValidator_ class is responsible for the verification of all the requirements being fulfilled in terms of the restrictions that the trucks have (truck capacity, limit of time worked, unique assignment..etc), which in turn, can alter the matrices of the assignments of trucks to requests. 

Suppose the following example:

```math
$$  \begin{bmatrix}
    [0 && 0 && 1] \\
    [0 && 0 && 1] \\
    [0 && 0 && 0] \\ 
    [0 && 1 && 0] \\
    [0 && 1 && 0] \\
    [0 && 1 && 0] \\
    [0 && 0 && 0] 
    \end{bmatrix} $$
```

 As it might be interpretable, there are 3 Trucks and 7 Requests. 
 
 As an example, the algorithm detects that Truck 2 and 3 
 have gotten close to occupying it's maximum capacity. I say close because it wouldn't be accurate to have a restriction for which the definition is made: 
 _the capacity of the objects in the trucks that are being occupied **shouldn't be equal to or more than the truck's maximum capacity**_, we expect that by 
 **getting close to the maximum capacity**, the truck should be not available. For example if the maximum loading capacity of the truck
 is 10 m3, then reaching 9 m3 (a difference of 1 m3, to draw the line somewhere) should be sufficient enough to say that the truck should return to base and can't attend any more requests.

 Back to the example, if both Trucks 2 and 3 have not complied with the maximum capacity restriction, then they will be removed from the variable: assignment_matrix, thus leading to this situation:
 
```math
$$  \begin{bmatrix}
    [0] \\
    [0] \\
    [0] \\
    [0] \\
    [0] \\
    [0] \\
    [0] 
    \end{bmatrix} $$
```

 As the two trucks have been eliminated from the available assignments to be carried out by trucks, returning back to base and there is only one truck left with two requests to attend (Request 3 and 7). 
 
 There might be, initially considering, 
 no reason why one must continue exploring the minimal route, and it wouldn't make sense to calculate parameter and global costs and select
 the best route for the intercepting trucks with the **hungarium algorithm** either if there is just one truck remaining (considering that the last truck will have to understand it's own situation to make the decision of returning to base). 
 So at this instance and as with empirical evidence of errors occurring, the application is detained, and the results up to the moment are provided.
 It is to be assumed that the only vehicle left to attend must travel to Request 3 and 7 in whichever way, from 3 to 7 or
 from 7 to 3, always complying with the limitations it posesses, and that it must of course, return back to base.
