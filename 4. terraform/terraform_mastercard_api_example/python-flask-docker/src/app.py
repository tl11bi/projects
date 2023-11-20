from flask import Flask, render_template, request
from cars import Cars
import socket

app = Flask(__name__)

all_cars = Cars()

@app.route("/")
def index():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        return render_template('index.html', hostname=host_name, ip=host_ip)
    except:
        return render_template('error.html')


@app.route("/api/v1/objects/logs", methods=['GET'])
def get_all_actions():
    with open('message.txt', 'r') as f:
        return f.read()


@app.route("/health")
def health():
    return "OK"


@app.route("/api/v1/objects/cars/", methods=['POST'])
def cars():
    if request.method == 'POST':
        request_data = request.get_json()
        result = all_cars.create_car(id=request_data['id'], make=request_data['make'], module=request_data['module'], year=request_data['year'])
        if result:
            return result, 201
        else:
            return "403 Already Exists", 403

@app.route("/api/v1/objects/cars/<car_id>", methods=['GET', 'PUT', 'DELETE'])
def get_cars(car_id):
    result = None
    if request.method == 'GET':
        print(car_id)
        result = all_cars.get_car(id=car_id)
    elif request.method == 'PUT':
        request_data = request.get_json()
        result = all_cars.update_car(id=car_id, make=request_data['make'], module=request_data['module'], year=request_data['year'])
    elif request.method == 'DELETE':
        result = all_cars.delete_car(id=car_id)
    if result:
        return result, 201
    else:
        return "404 Not Found", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
