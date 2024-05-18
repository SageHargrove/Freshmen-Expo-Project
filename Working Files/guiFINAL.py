from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
import serial
import time
from test import *

# Import vehicle classes
from vehicle_management3 import Car, Truck, Trailer, FourWheelTruck, SixWheelTruck

class VehicleApp(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark background color
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, None), height=Window.height)
        # Create a header with increased font size
        header = Label(text='Vehicle Monitoring System', size_hint=(1, None), height=50, color=(0.9, 0.9, 0.9, 1), font_size='32sp')
        self.layout.add_widget(header)
        self.vehicle = None

        # Dropdown for vehicle type selection including specific truck types
        self.spinner = Spinner(
            text='Select Vehicle Type',
            values=('Car', 'Trailer', 'Four-Wheel Truck', 'Six-Wheel Truck'),
            size_hint=(None, None),
            size=(300, 44),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_size='24sp'  # Increase font size in spinner
        )
        self.spinner.bind(text=self.show_selected_value)

        # Label to display information
        self.info_label = Label(text='Select a vehicle type to display data.', color=(0.8, 0.8, 0.8, 1), font_size='24sp')
        self.layout.add_widget(self.spinner)
        self.layout.add_widget(self.info_label)


        # Schedule updates for vehicle data
        Clock.schedule_interval(self.update_vehicle_data, 1)  # update every 1 second

        return self.layout

    def show_selected_value(self, spinner, text):
        initial_road_temp = 80.0  # Default road temperature
        vehicle_class = {
            'Car': Car,
            'Trailer': Trailer,
            'Four-Wheel Truck': FourWheelTruck,
            'Six-Wheel Truck': SixWheelTruck
        }.get(text, Car)  # Default to Car if no match
        self.vehicle = vehicle_class(initial_road_temp)
        self.update_display()

    def update_display(self):
        self.info_label.text = self.vehicle.display_status()


    # 10/10 would not recommend working with pyserial
    def read_hall_sensor(self): # Arduino 1 in charge of reading back of tire temps and tire rotations
        ser = serial.Serial('COM3', 4800, timeout=1) # Sets up ser as arduino serial monitor
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip() # This line of code is the bane of my existance
                if line == '':
                    line = '1 83.63' # just incase line is missed will revent to average object temp
                else:
                    spin = line[0]
                    temp = line[2:6]

                time.sleep(1)
                return spin, temp


    def road_temp(self): # Ardunio 2 in charged of reading road temperature
        ser = serial.Serial('COM6', 2400, timeout=1)
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if line == '':
                    line = '81.63'
                else:
                    temp = line[0:4]
                print(temp)
                time.sleep(1)
                return temp


    def update_vehicle_data(self, dt):
        if not hasattr(self, 'vehicle') or self.vehicle is None:
            return
        wheel_spin, wheel_temp = self.read_hall_sensor() # Calls the 2 temp functions to get arduino readings
        road_temp = self.road_temp()
        try:
            wheel_speeds = int(wheel_spin)  # Convert string to float
            temp = float(wheel_temp)
            road = float(road_temp) 
        except ValueError:
            print("Invalid wheel speed data:") # If error is encountered
            return  # Skip updating if the conversion fails

        self.vehicle.update_wheel_speed(wheel_speeds)
        self.vehicle.update_temp(temp)
        self.vehicle.update_road_temp(road)
        self.update_display()

    
    def on_stop(self):
        Clock.unschedule(self.update_vehicle_data)

if __name__ == '__main__':
    VehicleApp().run()