# TrashTrek Web Service🚀
## Optimization of Truck Logistics for the Disposal of Voluminous Waste: A Multicriteria Approach

### Description
The objective of this project is the development of software to optimize the management of the
collection of voluminous waste, specifically addressing the challenges associated with
**Traveling Salesman Problem** (TSP) and the **Vehicle Routing Problem** (VRP). 

These problems, being NP-complete, present a series of complexities that require intelligent and efficient solutions to ensure optimal route management.
The development of efficient software for voluminous waste management must address these
mathematical challenges and advanced algorithms, providing approximate solutions that can
approach the optimal solution in reasonable computational times. The successful implementation of these
strategies will ensure efficient and sustainable route management.

General challenges faced, part of which are comprised within TSP and VRP type of problems:
- **Exponential Complexity**: The number of possible routes grows factorially with the number of points, which turns the search for the optimal solution into a problem computationally challenging.
- **Consideration of Restrictions**: The inclusion of vehicle capacity restrictions and temporal restrictions add an additional layer of complexity to the problem.
- **Vehicle Assignment**: Determining the optimal number of vehicles and allocating efficiently a collection of requests to each one, considering capacity and temporary restrictions.
- **Multi-Route Optimization**: Coordinating multiple vehicles to minimize total distance traveled and other variables, which adds additional complexity.

The project delves into the specific location of **Gran Canaria** in Canary Islands, but can be replicated towards other cases.

Features presented in the project:

- Distance by road and estimated time calculated with **GraphHopper Routing API**
- Real map generated with **Folium**
- **Multicriteria with multi-variable restrictions** model engine personalized for pickup of voluminous objects
- **Hungarian algorithm** robust method for mínimum search
- Most **optimal route search** optimization amongst numerous combinations

The global costs is considered for three parameters, each one having to be normalized and have an associated weight constant; **distance costs**, **vehicle occupation costs** and **awaited time costs**. As mentioned before, the hungarium algorithm is then utilized to pick the least cost amongst other intercepting costs.

The goal is to _**minimize** distance and awaited time costs_ and _**maximize** occupation of the vehicle_ for the selection of the most optimal route given a series of requests to be attended by the trucks in service.

There are various restrictions that are verified within each iteration, here are the following:
- Number of trucks in service cannot exceed the limit of trucks specified initially.
- Each truck will have an estimated time worked, it should not exceed to the limit defined as per the maximum working time.
- For each request, there should only be one truck assigned to it.
- There is a dissatention time gathered for each request that is not attended on that day, is left for the next day. There is a maximum of days the request remains unattended and should receive maximum priority upon getting close to that limit of maximum defined.
- Each truck has a maximum capacity, it should not attend more requests if capacity of the vehicle has reached its limit, it returns back to base.

More information on problem-solving implementations in the _guide_ folder of the repository.

An example:

<br/><br/>
<img width="600" alt="image832" src="https://github.com/KrishT97/truck_route_planner/assets/92883393/1bc4cd0b-431e-45c3-9589-adcc88e133f3">
<br/><br/>
<img width="600" alt="image1060" src="https://github.com/KrishT97/truck_route_planner/assets/92883393/1c438469-193c-4aae-b2b1-b8d5e8a73c60">
<br/><br/>

Within the visualization results for different examples, the order signifies the sequence for the trucks attendance, the starting point is the initial coordinates for each truck, each mark is then the request to be attended by truck _x_ and order _y_, in the end all trucks return back to base. 

The interactive maps are saved as __html__ files, they should be opened explicitely externally.

## Software Architecture



<h2>Getting started <img align="center" height="50" src="https://github.com/KrishT97/trashtrek/assets/92883393/6fa6e9cc-5371-4637-9117-c1831ba17454"></h2>

These instructions will cover usage information to run the a docker container within the local system.

### Prerequisites
In order to run the container you'll need docker installed.

* [Windows](https://docs.docker.com/windows/started)
* [OS X](https://docs.docker.com/mac/started/)
* [Linux](https://docs.docker.com/linux/started/)


### Building the Docker Image

There are two options:

**a) Pull the image**

The docker image can be found in Docker Hub, with a simple pull request using the following command the app can be run in your local machine:

```shell
docker pull your-dockerhub-username/trashtrek:latest
```
**b) Build the image with the github repository**

1. Clone the Repository
```shell
git clone https://github.com/KrishT97/trashtrek.git
```
2. Navigate to the Project Directory
```shell
cd trashtrek
```
3. Build the Docker Image
```shell
docker build -t trashtrek:latest .
```

### Container Parameters

*`-p YOUR_CHOSEN_PORT:5000` - Choose the port you want the application to be accessible on your local machine.

The Flask app inside the Docker container always listens on port 5000, and users can choose any available port on their host machine to map to port 5000 in the container.

### Environment Variables

* `GRAPHHOPPER_API_KEY` - It is a mandatory requirement you provide a GraphHopper API key

### Running the Docker Container

```
docker run -p YOUR_CHOSEN_PORT:5000 -e GRAPHHOPPER_API_KEY='YOUR_API_KEY' trashtrek:latest
```

### Access the Application

Navigate to http://localhost:YOUR_CHOSEN_PORT to access the webservice

#### Example with POSTMAN

To demonstrate the usage of the application, here's an example using POSTMAN:

1. Open POSTMAN and create a POST request to
   `http://localhost:YOUR_CHOSEN_PORT/run`
2. In the request body, provide a JSON payload with relevant data. An example case for Gran Canaria:

```json
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
      "coordinates": "(27.755366, -15.604631)",
      "volume(m3)": 0.2
    },
    {
      "coordinates": "(27.749766, -15.574826)",
      "volume(m3)": 0.5
    },
    {
      "coordinates": "(27.838164, -15.442441)",
      "volume(m3)": 0.3
    },
    {
      "coordinates": "(28.085078, -15.434928)",
      "volume(m3)": 0.15
    },
    {
      "coordinates": "(28.102367, -15.437888)",
      "volume(m3)": 0.1
    },
    {
      "coordinates": "(28.100206, -15.454219)",
      "volume(m3)": 1
    }
  ]
}

```

3. Send the POST request, and you'll receive a JSON response with the optimized route.

#### Example Results

Upon successful execution of the TrashTrek Web Service, you will receive a JSON response with the optimized route. The result may look like the following:

```json
{
  "optimized_route": [
    {"location": [40.7128, -74.0060], "quantity": 20, "assigned_to": "Driver1"},
    {"location": [41.8781, -87.6298], "quantity": 25, "assigned_to": "Driver2"},
    {"location": [34.0522, -118.2437], "quantity": 30, "assigned_to": "Driver1"}
  ],
  "total_distance": 150.5,
  "total_cost": 35.75
}
```

## Authors

* **Krish Sadhwani**- aspiring Data Scientist & Engineer from the University of Las Palmas of Gran Canaria

## Acknowledgements  

* Special thanks to the _GraphHopper Team_ & _Co-Founder Peter_ for providing an extended trial with upgraded API usage for the functionality of the project.

* Under tutoring & monitoring by Dr. José Juan Hernández Cabrera, from the department of _Information & Systems_ in the field of _Computational Sciences & Artificial Intelligence_ in the ULPGC

* This could only have been done because of the collaboration with **Monentia**, technological consultancy & information systems development company in Gran Canaria, Spain. As well as members & staff of institution ULPGC (**Universidad Las Palmas de Gran Canaria**) for the overall guidance & approval of the final degree project. 


