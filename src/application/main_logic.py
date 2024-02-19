from model.engine_model.minimum_calculator import MinimumCalculator
from model.engine_model.model_distance import ModelDistance
from model.engine_model.model_data import ModelData
from model.engine_model.model_validator import ModelValidator
from model.engine_model.cost_estimator import CostEstimator
from model.engine_model.path_calculator import PathCalculator
from model.engine_model.distance_normalizer import DistanceNormalizer
from model.display_model.display import Display


def run_logic(limit_work_minutes,
              maximum_inattention_days,
              maximum_trucks,
              maximum_truck_capacity,
              drivers,
              trucks,
              requests,
              request, app, graphhopper_api_key):

    model_data = ModelData(requests, drivers, trucks)
    model_distance = ModelDistance(requests)
    model_validator = ModelValidator(model_data.trucks_coordinates, model_data.requests_coordinates,
                                     model_data.volumes_requests, model_data.assignment_truck_request,
                                     model_data.requests_priorities, model_data.inattention_days)
    path_calculator = PathCalculator(graphhopper_api_key)
    path_calculator.store_initial_data(model_data.trucks_coordinates)
    display = Display(graphhopper_api_key)
    display.store_initial_data(model_data.trucks_coordinates)
    distance_normalizer = DistanceNormalizer()
    minimum_calculator = MinimumCalculator()
    model_validator.add_limits(maximum_truck_capacity, limit_work_minutes, maximum_inattention_days, maximum_trucks)

    # SHOW INITIAL DATA
    app.logger.info(f"STARTING APPLICATION..... \n")
    app.logger.info(f"INITIAL TRUCK COORDINATES: \n {model_data.trucks_coordinates} \n")
    app.logger.info(f"INITIAL REQUESTS COORDINATES: \n {model_data.requests_coordinates} \n")
    app.logger.info(f"INITIAL VOLUMES OBJECTS: \n {model_data.volumes_requests} \n")
    app.logger.info(f"INITIAL ASSIGNMENT MATRIX: \n {model_data.assignment_truck_request} \n")
    app.logger.info(f"INITIAL INATTENTION DAYS: \n {model_data.inattention_days} \n")

    # VISUALIZATION
    activate_display = True

    # MAIN ALGORITHM LOOP
    for i in range(100):

        app.logger.info("---------------------------------------------------------------------- \n")

        # A TERMINATE CONDITION IN VALIDATOR WHEN ALL REQUESTS HAVE BEEN ASSIGNED
        model_validator.verify_termination()

        # INITIATE TERMINATION WHEN TRUE
        if model_validator.terminate:
            app.logger.info(f"FINISHED IN ITERATION: {i} \n")
            break

        # PRIOR RESTRICTIONS APPLIED TO ORIGINAL MATRIX
        model_validator.check_limit_trucks()
        model_validator.check_truck_capacity()
        model_validator.check_priorities()

        # WE DON'T CALCULATE THE LIMIT OF MINUTES WORKED WHEN IN FIRST ITERATION AS THERE HAVE BEEN NO REQUESTS ASSIGNED
        if not model_distance.is_first_iteration:
            model_validator.calculate_limit_minutes_worked()
            model_validator.check_limit_minutes_worked()
            app.logger.info(f"SUM MINUTES PER TRUCK: \n {model_validator.sum_minutes_per_truck} \n")

        # WITH ONE TRUCK LEFT WORKING, THE APPLICATION COMES TO A HAULT
        if len(model_validator.assignment_truck_request[0]) == 1:
            app.logger.info("________________________________ \n")
            app.logger.info("There is only one truck left in next iteration, the optimization stops,"
                            " as the application currently works with more than one truck. \n")
            app.logger.info("QUITTING..... \n")
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

        cost_estimator.calculate_parameter_costs(model_distance.volumes_requests,
                                                 model_distance.assignment_truck_request,
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

        app.logger.info(
            f"GLOBAL COSTS IN ITERATION {i} FOR UNATTENDED REQUESTS: \n {cost_estimator.global_costs} \n")

        # PICK THE LOWEST VALUE INDICATING MINIMUM COST ROUTE
        minimum_calculator.calculate_minimum(cost_estimator.global_costs)
        app.logger.info(
            f"MINIMUM VALUES OBTAINED FOR UNATTENDED REQUESTS: \n TRUCKS: {minimum_calculator.row_ind}, REQUESTS: {minimum_calculator.col_ind} \n")

        # CHECK SIZES OF ASSIGNMENT INDEXES FOR EXTRACTION
        minimum_calculator.check_size(model_distance.modified_indexes)

        # CONTAIN ASSIGNED REQUEST INDEXES
        model_distance.extend_assigned_requests(minimum_calculator.col_ind)
        app.logger.info(
            f"TOTAL REQUESTS INDEXES ASSIGNED (ALSO ATTENDED): \n {model_distance.assigned_requests_indexes} \n")

        # MODIFY TRUCK COORDINATES TO REQUEST ASSIGNED (UPDATED LOCATION)
        model_data.change_truck_coordinates(minimum_calculator.row_ind, minimum_calculator.col_ind,
                                            model_data.requests_coordinates)

        # UPDATE VALUES IN REQUEST-TRUCK MATRIX
        model_data.assign_request(minimum_calculator.row_ind, minimum_calculator.col_ind)

        # SHOW VALUES IN END OF ITERATION
        app.logger.info(f"TRUCK COORDINATES: \n {model_data.trucks_coordinates} \n")
        app.logger.info(f"REQUESTS COORDINATES: \n {model_data.requests_coordinates} \n")
        app.logger.info(f"ASSIGNMENT MATRIX: \n {model_data.assignment_truck_request} \n")
        app.logger.info(f"VOLUME OBJECTS: \n {model_data.volumes_requests} \n")
        app.logger.info(f"INATTENTION DAYS: \n {model_data.inattention_days} \n")
        app.logger.info(f"REQUESTS PRIORITIES: \n {model_data.requests_priorities} \n")
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
    app.logger.info("---------------------------END RESULTS--------------------------------\n")
    app.logger.info(f"GLOBAL ATTENDANCE ORDER: \n {model_data.attendance_order} \n")
    app.logger.info(
        f"ASSIGNED REQUESTS INDEXES FOR EACH TRUCK IN ORDER: \n {model_distance.assigned_requests_indexes} \n")
    app.logger.info(f"ASSIGNMENT MATRIX: \n {model_data.assignment_truck_request}\n")
    app.logger.info("VISUALIZATION IN REAL MAP SAVED. \n")
    app.logger.info(f"ENDING APPLICATION..... \n")

    basic_route_url = display.draw_basic_graph(path_calculator.initial_trucks_coordinates,
                                               model_data.requests_coordinates,
                                               base_url=request.url_root) \
        if activate_display is True else None

    ordered_route_url = display.draw_graph_order_routes(path_calculator.initial_trucks_coordinates,
                                                        model_data.requests_coordinates,
                                                        model_data.assignment_truck_request,
                                                        model_distance.assigned_requests_indexes,
                                                        base_url=request.url_root) \
        if activate_display is True else None

    return {
        "routeBasicURL": basic_route_url,
        "routeOrderedURL": ordered_route_url,
        "globalAttendanceOrder": str(model_data.attendance_order),
        "assignedRequestsOrderByTruck": str(model_distance.assigned_requests_indexes),
        "assignmentMatrixTruckRequest": str(model_data.assignment_truck_request.tolist())
    }
