## Solving the Assignment Problem

When each combination of truck and request results in a global cost, for which, if the problem were to be represented in
3 Trucks and 10 Requests as an example, there would be 30 different global costs, and that leads to an assignment problem. 
We will enumerate the problems with real examples:

1) **What if during the selection of the minimimum in the global costs, there are two minimum values for the local minimum for two or more trucks?**

For example this global costs matrix:

```math
$$  \begin{bmatrix}
    [0.55415517 & 0.4620469 & 0.31047253 & 0.03280298 & 0.05774575 & -0.27522498 & -0.06035956 & -0.4 & 0.02281897 & -0.27421732] \\
    [0.51415517 & 0.4620469 & 0.3604723 & 0.05270298 & 0.05474575 & -0.25522498 & -0.06135956 & -0.4 & 0.02181897 & -0.27421732] \\
    [-0.00247533 & -0.06634494 & 0.20986608 & 0.54505636 & 0.58169866 & 0.31074229 & 0.48571429 & 0.15676352 & 0.5271015 & 0.07265692] 
    \end{bmatrix} $$
```

Here, there are two minima, Request 8 for Truck 1 and 2 (-0.4), in the first iteration that are exactly the same. 
Anyways, one of them could be selected as the global minimum to attend, for example Truck 1 attending Request 8 in
the iteration, however in the next iteration the minimum value for Petition 8 and Truck 2 remains as **0.4**, for which
Truck 2 would have to attend Request 8, which is not supposed to happen as there should be only one assignment of truck
for each petition.

Given that this restriction is violated, the *ModelValidator* class checks the problem with the *check_unique_assignment function*,
and it modifies the assignment matrix so that only one truck attends Petition 8. 

So where is the problem?

If only Truck 1 attends Petition 8, in the next iteration, no matter what, the global minimum is again going to be in 
favor for Truck 2 attending Petition 8. 

As probably guessed, the problem keeps repeating in a cycle, a convergence error.

2) **When a request is attended by a truck, the coordinates of the truck is updated to being of the request, because attending the request means you are
traveling to that particular location which is going to be the request coordinates. What happens upon arriving to the request location and the request remains active for the next iteration?**

In another case example:

```math
$$  \begin{bmatrix}
    [0.51415517 & 0.4320469 & 0.36047253 & 0.05280298 & 0.05774575 & -0.22522498 & -0.06035956 & -0.2 & 0.02181897 & -0.27421732] \\
    [0.50415517 & 0.4620469 & 0.3604723 & 0.05280298 & 0.05774575 & -0.25522498 & -0.06035956 & -0.4 & 0.02281897 & -0.27421732] \\
    [-0.00247533 & -0.06634494 & 0.20986608 & 0.54505636 & 0.58169866 & 0.31074229 & 0.48571429 & 0.15676352 & 0.5271015 & 0.07265692] 
    \end{bmatrix} $$
```

If, for example, Truck 2 attends Request 8, and the coordinates are updated. In the next iteration, this occurs:
_that the value of the Request 8 in Truck 2 will always be the minimum compared to others because the distance cost
is 0 and time cost is also 0 (being in the same location)_, so the same request will be chosen to be attended again.


A possible solution is to remove the request from the assignment matrix and the
respective data of the attended request (Request 8) but it cannot be done so in a simple way, because internally, some of the operations
requires that the data be the same size as the beginning (also resolved later, however the minimum selection approach is discarded due to other drawbacks of the method). This could also bee semi-resolved because
what is done, is to choose the "second minimum" for second iterations forward. But this is also not a precise solution as to with this is that priority is always given in all iterations 
to the minimum value and the second minimum, and those two convergence values ​​are chosen, not taking into account other values.

Other problems may occur, for example if there are _identical minimum values for global costs in two or more trucks_. 
**Which truck is then prioritized?** The idea is that all trucks work collectively, where one truck attends certain requests and another, others in line, in the manner of which one compensates the other.

### Hungarian Algorithm to the rescue

The Hungarian Algorithm is an efficient algorithm for finding the optimal allocation in a given problem (in this case, trucks to requests) with associated costs. 
This algorithm guarantees an optimal solution and addresses convergence issues that may arise in iterative approaches.

Straightforward application:

```
# Representation of global costs 
cost_matrix = np.array([
    [0.55415517, 0.4620469, 0.36047253, 0.05280298, 0.05774575, -0.22522498, -0.06035956, -0.4, 0.02281897, -0.27421732],
    # ... Otras filas ...
])

# Using the Hungarian Algorithm
row_ind, col_ind = linear_sum_assignment(cost_matrix)

# Updating the assignment matrix
assignment_matrix = np.zeros_like(cost_matrix)
assignment_matrix[row_ind, col_ind] = 1
```

The Hungarian Algorithm is especially useful for solving assignment problems where the optimal assignment is sought between a set of source elements and another set of 
destination elements, minimizing or maximizing an associated cost function.

In this case, by applying the Hungarian Algorithm to the global cost matrix that represents the costs associated with assigning trucks to requests, 
it is able to find the optimal assignment that minimizes the total cost. This algorithm ensures that each request is assigned to a single truck and vice versa, 
thus avoiding the duplication and convergence problems.

In summary, the Hungarian Algorithm can be an effective solution to the problem, providing an optimal allocation that solves the duplication and convergence problems observed. 
Incorporating it into the current approach can improve the quality and efficiency of the solution without needing to change the fundamental logic of your code.

Clear description and examples of this method could be found here:

https://en.wikipedia.org/wiki/Hungarian_algorithm


