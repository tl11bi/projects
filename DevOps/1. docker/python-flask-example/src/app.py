from flask import Flask, render_template, request
from cars_v1 import CarsStore
import socket
from app_logs import AppLogs

app = Flask(__name__)


all_cars = CarsStore()
all_logs = AppLogs()
@app.route("/")
def index():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        return render_template('index.html', hostname=host_name, ip=host_ip)
    except:
        return render_template('error.html')


@app.route("/api/v1/objects/logs", methods=['GET', 'DELETE'])
def get_or_delete_all_logs():
    if request.method == 'GET':
        with open('/var/log/app.log', 'r') as f:
            logs = f.read()
            return logs, 200

    elif request.method == 'DELETE':
        with open('/var/log/app.log', 'w') as f:
            f.write('')
            return "OK", 200

@app.route("/health")
def health():
    return "OK"

@app.route("/api/v1/objects/cars_state", methods=['GET', 'POST', 'DELETE', 'PUT'])
def application_state():
    if request.method=='GET':
        return all_cars.get_cars_state(), 200
    elif request.method=='PUT':
        all_cars.load_cars_state()
    elif request.method=='POST':
        all_cars.save_cars_state()
    elif request.method=='DELETE':
        all_cars.delete_cars_state()
    return "OK", 200

@app.route("/api/v1/objects/cars", methods=['POST'])
def create_new_cars():
    request_data = request.get_json()
    if all_cars.is_car_exist(request_data['id']):
        all_logs.write_logs("POST /api/v1/objects/cars 400")
        return "Car already exists", 400
    else:
        all_logs.write_logs("POST /api/v1/objects/cars 201")
        return all_cars.create_car(request_data['id'], request_data['make'], request_data['module'], request_data['year']), 201

@app.route("/api/v1/objects/cars/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def get_or_update_or_delete_car(id):
    if request.method == 'GET':
        if all_cars.is_car_exist(id):
            all_logs.write_logs("GET /api/v1/objects/cars/{} 200".format(id))
            return all_cars.get_car(id), 200
        else:
            all_logs.write_logs("GET /api/v1/objects/cars/{} 404".format(id))
            return "Car not found", 404
    elif request.method == 'PUT':
        request_data = request.get_json()
        if all_cars.is_car_exist(id):
            all_logs.write_logs("PUT /api/v1/objects/cars/{} 200".format(id))
            return all_cars.update_car(id, request_data['make'], request_data['module'], request_data['year']), 200
        else:
            all_logs.write_logs("PUT /api/v1/objects/cars/{} 404".format(id))
            return "Car not found", 404
    elif request.method == 'DELETE':
        if all_cars.is_car_exist(id):
            all_logs.write_logs("DELETE /api/v1/objects/cars/{} 200".format(id))
            return all_cars.delete_car(id), 200
        else:
            all_logs.write_logs("DELETE /api/v1/objects/cars/{} 404".format(id))
            return "Car not found", 404



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
