import json
import os


class CarsStore(object):
    """
    This class represents a car and provides methods for creating, reading, updating, and deleting cars.
    """

    def __init__(self):
        """
        Constructor for the cars class.
        """
        self.cars_dict = {}

    def create_car(self, id, make, module, year):
        """
        This method creates a new car and adds it to the cars dictionary.
        """
        new_car = {
            'id': id,
            'make': make,
            'module': module,
            'year': year
        }

        self.cars_dict[id] = new_car
        return json.dumps(new_car)

    def get_car(self, id):
        """
        This method retrieves a car from the cars dictionary.
        """
        return json.dumps(self.cars_dict[id])

    def update_car(self, id, make, module, year):
        """
        This method updates an existing car in the cars dictionary.
        """
        self.cars_dict[id]['make'] = make
        self.cars_dict[id]['module'] = module
        self.cars_dict[id]['year'] = year
        return json.dumps(self.cars_dict[id])

    def delete_car(self, id):
        """
        This method deletes a car from the cars dictionary.
        """
        del self.cars_dict[id]
        return json.dumps({'response': 'Success'})

    def is_car_exist(self, id):
        """
        This method checks if a car exists in the cars dictionary.
        """
        if id in self.cars_dict:
            return True
        else:
            return False

    def save_cars_state(self):
        """
        This method saves the cars dictionary to a file.
        """
        with open('cars.json', 'w') as f:
            json.dump(self.cars_dict, f)

    def load_cars_state(self):
        """
        This method loads the cars dictionary from a file.
        """
        if os.path.exists('cars.json'):
            with open('cars.json', 'r') as f:
                self.cars_dict = json.load(f)

    def get_cars_state(self):
        """
        This method returns the cars dictionary.
        """
        return json.dumps(self.cars_dict)

    def delete_cars_state(self):
        """
        This method deletes the cars dictionary.
        """
        self.cars_dict.clear()
        self.save_cars_state()
