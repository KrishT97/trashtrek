## Checking unique assignment for each truck

Each truck and request association has to be unique. It cannot be that truck 1 has request number 8 to attend and truck 2 also has that request.

Every single request should have only one truck assigned to it, if not, there are routing errors and the optimization fails. 
The system is not designed to create those errors in the first place, but to make sure, a condition is added to correct the error if the mistake is somehow made.

The basic idea is to analyze each row in the assignment of trucks and requests matrix and see if the sum of any row is > 1.

An example:

```math
$$  \begin{bmatrix}
    [0 && 0 && 0] \\
    [0 && 0 && 0] \\
    [1 && 1 && 0] \\
    [0 && 0 && 0] \\
    [0 && 1 && 0] \\
    [0 && 1 && 0] \\
    [0 && 0 && 0] \\
    [0 && 1 && 0] \\
    [0 && 0 && 0] \\
    [1 && 0 && 0]
    \end{bmatrix} $$
```
Request 3 is assigned to truck 1 and truck 2, the changes to be made is for the first truck to get the assignment, leaving us with:
```math
$$  \begin{bmatrix}
    [0 && 0 && 0] \\
    [0 && 0 && 0] \\
    [1 && 0 && 0] \\
    [0 && 0 && 0] \\
    [0 && 1 && 0] \\
    [0 && 1 && 0] \\
    [0 && 0 && 0] \\
    [0 && 1 && 0] \\
    [0 && 0 && 0] \\
    [1 && 0 && 0]
    \end{bmatrix} $$
```

The translation of this code in NumPy with Python:
```
np.array([np.array([1] + [0] * (len(row) - 1)) if sum(row) > 1 else row for row in self.assignment_truck_request])
```

A simple way to solve the issue, without taking a look into external conditions (like load of requests for each truck).
