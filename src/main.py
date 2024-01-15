import numpy as np

from model.engine_model.minimum_calculator import MinimumCalculator
from model.engine_model.model_distance import ModelDistance
from model.user_model.truck import Truck
from model.user_model.driver import Driver
from model.user_model.request import Request
from model.engine_model.model_data import ModelData
from model.engine_model.model_validator import ModelValidator
from model.engine_model.cost_estimator import CostEstimator
from model.engine_model.path_calculator import PathCalculator
from model.engine_model.distance_normalizer import DistanceNormalizer
from model.display_model.display import Display

# DATA INITIALIZATION

limit_work_minutes = 480  # 8 hours daily
maximum_inattention_days = 10
maximum_trucks = 10
maximum_truck_capacity = 10

requests = [Request(1, (27.755366, -15.604631), 0.2), Request(2, (27.749766, -15.574826), 0.5),
            Request(3, (27.838164, -15.442441), 0.3), Request(4, (28.085078, -15.434928), 0.15),
            Request(5, (28.102367, -15.437888), 0.1), Request(6, (28.100206, -15.454219), 1),
            Request(7, (28.118482, -15.445237), 0.5), Request(8, (28.100746, -15.474429), 1.5),
            Request(9, (28.130995, -15.515053), 0.05), Request(10, (28.065085, -15.545675), 2.5),
            Request(11, (28.138761, -15.435350), 2.0), Request(12, (28.118830, -15.526022), 0.32),
            Request(13, (28.059831, -15.547753), 1.11), Request(14, (28.008196, -15.533061), 0.33),
            Request(15, (27.851273, -15.466471), 0.11), Request(16, (27.789653, -15.717291), 0.03),
            Request(17, (27.818894, -15.765593), 1.78), Request(18, (27.983236, -15.780623), 0.98),
            Request(19, (28.101658, -15.701096), 0.65), Request(20, (28.147253, -15.649500), 0.22)]


drivers = [Driver(1, 0), Driver(2, 0), Driver(3, 0),Driver(4, 0), Driver(5, 0),Driver(6, 0), Driver(7, 0)]

trucks = [Truck(1, 10, (28.093512, -15.425922)), Truck(2, 10, (28.128852, -15.504827)),
          Truck(3, 10, (27.770183, -15.597304)), Truck(4, 10, (27.843992, -15.438345)),
          Truck(5, 10, (27.926863, -15.424706)), Truck(6,10, (27.993744, -15.388339)),
          Truck(7, 10, (28.153197, -15.413843))]

# CLASSES INITIALIZATION

# problem_definition
model_data = ModelData(requests, drivers, trucks)
model_distance = ModelDistance(requests)
model_validator = ModelValidator(model_data.trucks_coordinates, model_data.requests_coordinates,
                                 model_data.volumes_requests, model_data.assignment_truck_request,
                                 model_data.requests_priorities, model_data.inattention_days)
path_calculator = PathCalculator()
distance_normalizer = DistanceNormalizer()
minimum_calculator = MinimumCalculator()
model_validator.add_limits(maximum_truck_capacity, limit_work_minutes, maximum_inattention_days, maximum_trucks)

# SHOW INITIAL DATA
print("INITIAL TRUCK COORDINATES: \n", model_data.trucks_coordinates)
print("INITIAL REQUESTS COORDINATES: \n", model_data.requests_coordinates)
print("INITIAL VOLUMES OBJECTS: \n", model_data.volumes_requests)
print("INITIAL ASSIGNMENT MATRIX: \n", model_data.assignment_truck_request)
print("INITIAL INATTENTION DAYS: \n", model_data.inattention_days)

# VISUALIZATION
activate_display = True

# MAIN ALGORITHM LOOP
for i in range(20):

    print("----------------------------------------------------------------------")

    # A TERMINATE CONDITION IN VALIDATOR WHEN ALL REQUESTS HAVE BEEN ASSIGNED
    model_validator.verify_termination()

    # INITIATE TERMINATION WHEN TRUE
    if model_validator.terminate:
        print("FINISHED IN ITERATION:", i)
        break

    # PRIOR RESTRICTIONS APPLIED TO ORIGINAL MATRIX
    model_validator.check_limit_trucks()
    model_validator.check_truck_capacity()
    model_validator.check_priorities()

    # WE DON'T CALCULATE THE LIMIT OF MINUTES WORKED WHEN IN FIRST ITERATION AS THERE HAVE BEEN NO REQUESTS ASSIGNED
    if not model_distance.is_first_iteration:
        model_validator.calculate_limit_minutes_worked()
        model_validator.check_limit_minutes_worked()
        print("SUM MINUTES PER TRUCK:")
        print(model_validator.sum_minutes_per_truck)

    # WITH ONE TRUCK LEFT WORKING, THE APPLICATION COMES TO A HAULT
    if len(model_validator.assignment_truck_request[0]) == 1:
        print("________________________________")
        print("There is only one truck left in next iteration, the optimization stops,"
              " as the application currently works with more than one truck.")
        print("QUITTING.....")
        break

    # UPDATE RESTRICTIONS MODIFICATIONS TO MODEL DATA (UPDATED FROM ORIGINAL DATA)
    model_data.update(model_validator.assignment_truck_request, model_validator.inattention_days,
                      model_validator.requests_priorities, model_validator.trucks_coordinates,
                      model_validator.requests_coordinates, model_validator.volumes_requests)

    # UPDATE MODEL DISTANCES DATA (VARIABLE DATA FOR CALCULATION)
    model_distance.update(model_data.requests_coordinates, model_data.volumes_requests,
                          model_data.assignment_truck_request)
    # COSTS CALCULATION

    path_calculator.calculate_graphhopper(model_data.trucks_coordinates, model_distance.requests_coordinates)

    cost_estimator = CostEstimator(0.3, 0.4, 0.3)

    cost_estimator.calculate_parameter_costs(model_distance.volumes_requests, model_distance.assignment_truck_request,
                                             path_calculator.road_distances, path_calculator.time_estimated)

    # ADD TOTAL TIMINGS IN VALIDATOR FOR NEXT ITERATION
    model_validator.add_timings(path_calculator.time_estimated)

    # VERIFY NORMALIZATION REQUISITES
    distance_normalizer.verify(model_distance.requests_coordinates)

    # NORMALIZE DATA
    distance_normalizer.normalize(cost_estimator.distance_costs_trucks, cost_estimator.occupation_costs_trucks,
                                  cost_estimator.time_costs_trucks)
    # CALCULATE GLOBAL COSTS
    cost_estimator.calculate_global_costs(distance_normalizer.normalized_trucks_distance,
                                          distance_normalizer.normalized_trucks_occupation,
                                          distance_normalizer.normalized_trucks_time)

    print(f"GLOBAL COSTS IN ITERATION {i} FOR UNATTENDED REQUESTS: \n", cost_estimator.global_costs)

    # PICK THE LOWEST VALUE INDICATING MINIMUM COST ROUTE
    minimum_calculator.calculate_minimum(cost_estimator.global_costs)
    print("MINIMUM VALUES OBTAINED FOR UNATTENDED REQUESTS: \n", "TRUCKS: ", minimum_calculator.row_ind, "REQUESTS: ",
          minimum_calculator.col_ind)

    # CHECK SIZES OF ASSIGNMENT INDEXES FOR EXTRACTION
    minimum_calculator.check_size(model_distance.modified_indexes)

    # CONTAIN ASSIGNED REQUEST INDEXES
    model_distance.extend_assigned_requests(minimum_calculator.col_ind)
    print("TOTAL REQUESTS INDEXES ASSIGNED (ALSO ATTENDED): \n", model_distance.assigned_requests_indexes)

    # MODIFY TRUCK COORDINATES TO REQUEST ASSIGNED (UPDATED LOCATION)
    model_data.change_truck_coordinates(minimum_calculator.row_ind, minimum_calculator.col_ind,
                                        model_data.requests_coordinates)

    # UPDATE VALUES IN REQUEST-TRUCK MATRIX
    model_data.assign_request(minimum_calculator.row_ind, minimum_calculator.col_ind)

    # SHOW VALUES IN END OF ITERATION
    print("TRUCK COORDINATES: \n", model_data.trucks_coordinates)
    print("REQUESTS COORDINATES: \n", model_data.requests_coordinates)
    print("ASSIGNMENT MATRIX: \n", model_data.assignment_truck_request)
    print("VOLUME OBJECTS: \n", model_data.volumes_requests)
    print("INATTENTION DAYS: \n", model_data.inattention_days)
    print("REQUESTS PRIORITIES: \n", model_data.requests_priorities)
    model_validator.update(model_data.assignment_truck_request, model_data.inattention_days,
                           model_data.requests_priorities, model_data.trucks_coordinates,
                           model_data.requests_coordinates,
                           model_data.volumes_requests)

    # TO KEEP A TRACK ON THE ORDER OF ATTENDED REQUESTS
    model_data.fetch_route_attendance_order()

    # POSTERIOR RESTRICTIONS APPLIED TO ORIGINAL MATRIX MODIFIED
    model_validator.check_unique_assignment()

    # AFTER FIRST ITERATION, UPDATE BOOLEAN
    model_distance.is_first_iteration = False

# AFTER THE ITERATIONS LOOP IS OVER, THE RESULTS ARE SHOWN
print("END RESULTS:")
print("ATTENDANCE ORDER:", model_data.attendance_order)
print("ASSIGNED REQUESTS FOR EACH TRUCK IN ORDER", model_distance.assigned_requests_indexes)
print("ASSIGNMENT MATRIX:")
print(model_data.assignment_truck_request)
print("VISUALIZATION IN REAL MAP SAVED.")
Display().draw_graph_folium_results(model_data.trucks_coordinates,
                                    model_data.requests_coordinates, model_data.assignment_truck_request,
                                    model_distance.assigned_requests_indexes) if activate_display is True else None
