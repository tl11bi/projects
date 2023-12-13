import json
from datetime import datetime

# the following class is used to represent a list of cars
class Cars:
    car_list = []

    def __init__(self):
        self.car_list = []
    def create_car(self, id, make, module, year):
        write_message("create_car called")
        new_car = {'id': id, 'make': make, 'module': module, 'year': year}
        if self.get_car(id):
            write_message("POST /api/v1/objects/cars already exist")
            return None
        self.car_list.append(new_car)
        write_message("POST /api/v1/objects/cars" + str(new_car))
        return json.dumps(new_car)
    def get_car(self, id):
        write_message("get_car called")
        for car in self.car_list:
            if car['id'] == id:
                write_message("GET /api/v1/objects/cars" + str(car))
                return car
        write_message("GET /api/v1/objects/cars not found")
        return None

    def update_car(self, id, make, module, year):
        write_message("update_car called")
        for car in self.car_list:
            if car['id'] == id:
                car['make'] = make
                car['module'] = module
                car['year'] = year
                write_message("PUT /api/v1/objects/cars" + str(car))
                return json.dumps(car)
        write_message("PUT /api/v1/objects/cars not found")
        return None

    def delete_car(self, id):
        write_message("delete_car called")
        for car in self.car_list:
            if car['id'] == id:
                self.car_list.remove(car)
                write_message("DELETE /api/v1/objects/cars" + str(car))
                return json.dumps(car)
        write_message("DELETE /api/v1/objects/cars not found")
        return None


def write_message(message):
    to_save = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ': ' + message + '\n'
    with open('message.txt', 'a') as f:
        # write the message with time stamp
        f.write(to_save)
    print(to_save)
