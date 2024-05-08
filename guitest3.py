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

# Import vehicle classes
from vehicle_management2 import Car, Truck, Trailer, FourWheelTruck, SixWheelTruck

class VehicleApp(App):
    def build(self):
        # Setup serial connection (adjust COM port as necessary)
        self.ser = serial.Serial('COM3', 9600, timeout=1)
        time.sleep(2)  # wait for the connection to establish
        
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.is_muted = False  # Track mute state

        # Dropdown for vehicle type selection including specific truck types
        self.spinner = Spinner(
            text='Select Vehicle Type',
            values=('Car', 'Trailer', 'Four-Wheel Truck', 'Six-Wheel Truck'),
            size_hint=(None, None),
            size=(300, 44),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.spinner.bind(text=self.show_selected_value)

        # Label to display information
        self.info_label = Label(text='Select a vehicle type to display data.')
        self.layout.add_widget(self.spinner)
        self.layout.add_widget(self.info_label)

        # Button to mute/unmute alerts
        anchor_layout = AnchorLayout(anchor_x='right', anchor_y='bottom', size_hint=(1, None), height=70)
        self.mute_button = Button(
            background_normal='images/unmute_icon.png',  # Initial image for unmuted state
            size_hint=(0.1, None),
            height=60,
            text=''  # No text
        )
        anchor_layout.add_widget(self.mute_button)
        self.layout.add_widget(anchor_layout)
        self.mute_button.bind(on_press=self.toggle_mute)

        # Schedule updates for vehicle data
        Clock.schedule_interval(self.update_vehicle_data, 1)  # update every 1 second

        return self.layout

    def show_selected_value(self, spinner, text):
        initial_road_temp = 15.0  # Default road temperature
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

    def toggle_mute(self, instance):
        self.is_muted = not self.is_muted
        new_icon = 'images/mute_icon.png' if self.is_muted else 'images/unmute_icon.png'
        self.mute_button.background_normal = new_icon

    def read_hall_sensor(self):
        with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
            line = ser.readline().decode('utf-8').strip()
            speeds = [float(speed) for speed in line.split(',')]
            return speeds

    def update_vehicle_data(self, dt):
        try:
            wheel_speeds = self.read_hall_sensor()
            self.vehicle.update_wheel_speed(wheel_speeds)
            self.update_display()
        except Exception as e:
            print(f"Failed to read from the sensor: {e}")
    
    def on_stop(self):
        Clock.unschedule(self.update_vehicle_data)

if __name__ == '__main__':
    VehicleApp().run()
