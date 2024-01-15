## How truck time calculation works

The idea is to calculate the total minutes each vehicle works in the given iteration, this data is retrieved through the assignments of the trucks to requests and the time in minutes estimations for each of those assignments. 
However, this is a complicated task, as the assignment matrix remains stagnant but the time estimated array gets modified as the estimates are only captured for unassigned requests in the current iteration, so the right indices must be associated for assignments to time estimates.

- Here is the theory behind how the designated algorithm for this function works, the example is defined with 3 trucks and 10 requests to be solved.

As mentioned, the time estimated array is only considered for those requests that are not assigned, so we can't directly assign the indices also, because it is modified and we have to associate the right indices. 

### Iteration 1

Now say we start out with this matrix as our assignment of truck & request matrix (the column being each truck and row each request):

```math
$$  \begin{bmatrix}
    [0 && 0 && 0] \\
    [0 && 0 && 0] \\
    [0 && 0 && 0] \\
    [0 && 0 && 0] \\
    [0 && 0 && 0] \\
    [0 && 0 && 0] \\
    [0 && 0 && 0] \\
    [0 && 0 && 0] \\
    [0 && 0 && 0] \\
    [0 && 0 && 0]
    \end{bmatrix} $$
```
 
and we will have time estimated array as the following (size 3, for each truck, each one with 10 values for the different requests):

```math
$$  \begin{bmatrix}
    [x_1 && x_2 && x_3 && x_4 && x_5 && x_6 && x_7 && x_8 && x_9 && x_{10}] \\
    [y_1 && y_2 && y_3 && y_4 && y_5 && y_6 && y_7 && y_8 && y_9 && y_{10}] \\
    [z_1 && z_2 && z_3 && z_4 && z_5 && z_6 && z_7 && z_8 && z_9 && z_{10}]
    \end{bmatrix} $$
```

Now the _x_ variable indicates all values for truck 1, the _y_ variable for truck 2, and the _z_ variable for truck 3, this will be calculated a priori and will be given to the function, as well as the assignment matrix. 

As there are no assigned requests in the beginning, the time estimated array is considered for all requests. Meaning, we need the time estimated for each unassigned truck-request combination.
We are also going to have a list of indices to keep the order like so:

```math
indices = [1,2,3,4,5,6,7,8,9,10]
```

### Iteration 2

Now, in the next iteration **(second iteration)**, we get some requests assigned to the trucks (3 requests in each iteration as there are 3 trucks) and so the assignment truck request matrix looks like this now:

```math
$$  \begin{bmatrix}
    [0 && 0 && 0] \\
    [0 && 0 && 1] \\
    [0 && 0 && 0] \\
    [0 && 0 && 0] \\
    [0 && 0 && 0] \\
    [0 && 0 && 0] \\
    [0 && 0 && 0] \\
    [1 && 0 && 0] \\
    [0 && 0 && 0] \\
    [0 && 1 && 0]
    \end{bmatrix} $$
```
Now from the indices list, we select the row indices from the matrix that have a _1_, so in this case it will be **2,8 and 10**. 

Then we select the time estimated for these specific indices in the associated truck, as we know each column in the assignment matrix  is a truck. So we select **z2, x8 and y10 values**, z referring to truck 3, x to truck 1 and y to truck 2 (the places in the matrix where there is a 1). As a result now we have the truck_minutes_total variable like this:
```math
truckMinutesTotal=[x8,y10,z2]
```
the time estimated values for each truck, it will be of length 3.

Now we update the indices to be:
```math
indices = [1,3,4,5,6,7,9]
```
removing the indices assigned.

### Iteration 3

Now, in the next iteration **(third iteration)**, the time estimated array is updated leaving us with other values and size 7, due to in the previous assignment, 7 requests were not assigned, so we now have:

```math
$$  \begin{bmatrix}
    [x_1 && x_3 && x_4 && x_5 && x_6 && x_7 && x_9] \\
    [y_1 && y_3 && y_4 && y_5 && y_6 && y_7 && y_9] \\
    [z_1 && z_3 && z_4 && z_5 && z_6 && z_7 && z_9]
    \end{bmatrix} $$
```

The values are different and have nothing to do with the previous time estimated array, i am putting x1,x3..etc not to say that the values in the previous time estimated array are carried in this one, rather that there are now 7 elements for each 3 trucks and to put it as an example to explain the case, being completely different values. 

Also we associate the values to the indices from the list, the order is not 1,2,3,4..etc but as it is in the indices list: 1,3,4,5,6,7,9

We will also have the following assignment matrix in this iteration:

```math
$$  \begin{bmatrix}
    [1 && 0 && 0] \\
    [0 && 0 && 1] \\
    [0 && 0 && 0] \\
    [0 && 1 && 0] \\
    [1 && 0 && 0] \\
    [0 && 0 && 0] \\
    [0 && 0 && 0] \\
    [1 && 0 && 0] \\
    [0 && 0 && 0] \\
    [0 && 1 && 0]
    \end{bmatrix} $$
```

There are 3 more requests assigned, we take a look in the indices list:

```math
indices = [1,3,4,5,6,7,9]
```
we select the indices that have an assignment (row index == 1), from this list 1, 4 and 5 index  have a 1 in them in the index row list of the assignment matrix. We associate the 1,4 and 5 to the time estimated array and the trucks it corresponds to, which leaves us with **x1, y4 and z5**. 

Now:

```math
truckMinutesTotal = [x8+x1,y10+y4,z2+z5]
```

The indices list is now updated again:

```math
indices = [3,6,7,9]
```
### Iteration 4

Now in the next iteration, **(iteration four)**. we have estimated time array:

```math
$$  \begin{bmatrix}
    [x_3 && x_6 && x_7 && x_9] \\
    [y_3 && y_6 && y_7 && y_9] \\
    [z_3 && z_6 && z_7 && z_9]
    \end{bmatrix} $$
```

and our assignment matrix has now 3 more requests assignments:

```math
$$  \begin{bmatrix}
    [1 && 0 && 0] \\
    [0 && 0 && 1] \\
    [0 && 1 && 0] \\
    [0 && 1 && 0] \\
    [1 && 0 && 0] \\
    [1 && 0 && 0] \\
    [1 && 0 && 0] \\
    [1 && 0 && 0] \\
    [0 && 0 && 0] \\
    [0 && 1 && 0]
    \end{bmatrix} $$
```
 
Having the indices list being: [3,6,7,9], we find out which have assignments, and it is 3,6,7. Associating them with the trucks and time estimated array we find **y3,x6 and x7**.  

So now:

```math
truckMinutesTotal=[x8+x1+x6+x7,y10+y4+y3,z2+z5]
```

the indices list is now updated again:

```math
indices = [9]
```
### Iteration 5

In the next iteration **(iteration five)**, the time estimated array will be:

```math
$$  \begin{bmatrix}
    [x_9] \\
    [y_9] \\
    [z_9]
    \end{bmatrix} $$
```

the assignment matrix:

```math
$$  \begin{bmatrix}
    [1 && 0 && 0] \\
    [0 && 0 && 1] \\
    [0 && 1 && 0] \\
    [0 && 1 && 0] \\
    [1 && 0 && 0] \\
    [1 && 0 && 0] \\
    [1 && 0 && 0] \\
    [1 && 0 && 0] \\
    [0 && 1 && 0] \\
    [0 && 1 && 0]
    \end{bmatrix} $$
```

Having the indices list only having 9, we associate it to the right truck, which is truck 2, meaning **y9**. Then the total minutes for truck will look like: 

```math
truckMinutesTotal=[x8+x1+x6+x7,y10+y4+y3+y9,z2+z5]
```

During each iteration, apart from storing the estimated time worked for each truck, the restriction of the time being less than the daily limit is also applied. 

If as an example, the maximum working time of a truck is to be 480 minutes (8 hours), if any truck exceeds that range, it will be eliminated from the assignment operation and not be considered. Returning back to base.
