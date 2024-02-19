## What happens to requests that have remained unattended?

Usually the algorithm would ensure that all requests receive an assignment from the trucks in service, however when any of the restrictions are not fulfilled, there could be situations where the application comes to a hault. For example if the time worked for all trucks has exceeded the limit defined, as there are no trucks in service, the application ends.

There could be instances where the requests are remained unresolved, and should be transferred in the next application execution. However this concept is not exactly delivered in this system due to it being made to run in one single event. 

The problems leads to dissatisfied users, if the days are prolonged and the request still remains unattended.


<img width="264" alt="image" src="https://github.com/KrishT97/truck_route_planner/assets/92883393/5566e6b9-55a8-4f1c-92fc-e0b442090c12">


To solve this, the basic outline is made, which is having a list of priorities (zeros) and a list of inattention days (zeros), and if a request is remained unattended that day, the next day it takes part in requests to be solved and its inattention days adds up.

If the number of inattention days for a specific request exceeds a limit, for example 10, meaning the request has undergone >10 days of inattention. It will immediately be prioritized (0 converted to 1 in list, thinking of a bit value), and before attending any requests when running the application again the following day, the **priority request** will be the first one to be attended, not mattering what is its global cost and how high it is.

This ensures satisfation of users, so that the system resolves all requests, meaning that the trucks resolve the requests, even if it takes a while for them to arrive and dispose the object/s.
