import os
import logging
from flask import Flask, request, jsonify, send_from_directory, make_response
from main_logic import run_logic
from model.user_model.driver import Driver
from model.user_model.truck import Truck
from model.user_model.request import Request
import sys

app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/run', methods=['POST'])
def run_application():
    try:
        data = request.get_json()

        app.logger.info(f"RECEIVED JSON DATA: \n {data}")

        # Extract data from JSON
        limit_work_minutes = data['dailyLimitWorkInMinutes']
        maximum_inattention_days = data['maximumInattentionDays']
        maximum_trucks = data['maximumTrucksDefined']
        maximum_truck_capacity = data['maximumTruckCapacity(m3)']
        number_of_drivers = data['numberOfAvailableDrivers']

        trucks_data = data['truckInformation']
        requests_data = data['requestsInformation']

        trucks = [Truck(i + 1, truck['volume(m3)'], tuple(map(float, truck['coordinates'].strip('()').split(','))))
                  for i, truck in enumerate(trucks_data)]

        requests = [Request(i + 1, tuple(map(float, req['coordinates'].strip('()').split(','))), req['volume(m3)'])
                    for i, req in enumerate(requests_data)]

        drivers = [Driver(i + 1, 0) for i in range(number_of_drivers)]

        graphhopper_api_key = os.environ.get('GRAPHHOPPER_API_KEY')
        if not graphhopper_api_key:
            raise ValueError("GRAPHHOPPER_API_KEY environment variable is not set. Please provide your API key.")

        result = run_logic(limit_work_minutes, maximum_inattention_days, maximum_trucks, maximum_truck_capacity,
                           drivers, trucks,
                           requests, request, app, graphhopper_api_key)
        app.logger.info(f"RESULTS GENERATED: \n {result}")

        return jsonify({"message": "Success!", "result": result})

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/results/<filename>')
def results_file(filename):
    response = make_response(send_from_directory(os.path.join(app.root_path, 'results'), filename))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response


if __name__ == '__main__':
    sys.path.append('/app')
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.logger.setLevel(logging.DEBUG)
    app.run(debug=True, host='0.0.0.0', port=5000)
