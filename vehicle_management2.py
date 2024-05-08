class Vehicle:
    def __init__(self, vehicle_type, road_temperature, wheel_count=4):
        self.vehicle_type = vehicle_type
        self.road_temperature = road_temperature
        self.wheel_count = wheel_count
        # Initialize all tire temperatures to a default value
        self.tire_temperature = [20.0] * self.wheel_count  # Default temperature for each tire
        self.wheel_speed = [0.0] * self.wheel_count

    def update_wheel_speed(self, speeds):
        self.wheel_speed = speeds

    def display_status(self):
        status = f"Type: {self.vehicle_type}\n"
        status += f"Tire Temperature: {self.tire_temperature}\n"
        status += f"Road Temperature: {self.road_temperature}\n"
        status += f"Wheel Count: {self.wheel_count} \n"
        status += f"Wheel Speeds: {self.wheel_speed}"
        return status

class Car(Vehicle):
    def __init__(self, road_temperature):
        super().__init__("Car", road_temperature)

class Truck(Vehicle):
    def __init__(self, road_temperature, vehicle_type="Truck", wheel_count=4):
        super().__init__(vehicle_type, road_temperature, wheel_count)

class Trailer(Vehicle):
    def __init__(self, road_temperature):
        super().__init__("Trailer", road_temperature, wheel_count=8)

class FourWheelTruck(Truck):
    def __init__(self, road_temperature):
        super().__init__(road_temperature, "Four Wheel Truck")

class SixWheelTruck(Truck):
    def __init__(self, road_temperature):
        super().__init__(road_temperature, "Six Wheel Truck", wheel_count=6)
