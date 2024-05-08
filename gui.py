from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
import serial
import time


# Import vehicle classes
from vehicle_management import Car, Truck, Trailer, FourWheelTruck, SixWheelTruck

# Setup serial connection (adjust COM port as necessary)
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # wait for the connection to establish


class VehicleApp(App):
    def build(self):
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

        self.start_updating_vehicle_data()
        return self.layout

    def show_selected_value(self, spinner, text):
        if not hasattr(self, 'vehicle') or self.vehicle.vehicle_type != text:
            # Set initial data assuming no sensor data has been read yet
            initial_temperature = [0, 0, 0, 0]  # Default temperatures
            initial_road_temp = 0  # Default road temperature

            # Create a new vehicle instance of the selected type
            vehicle_class = self.vehicle_types[text]
            self.vehicle = vehicle_class(initial_temperature, initial_road_temp)
            self.update_display()



    def update_display(self):
        # Update GUI with vehicle data
        self.vehicle.update_sensors()
        self.info_label.text = self.vehicle.display_status()


    def toggle_mute(self, instance):
        # Toggle mute state and update button image
        self.is_muted = not self.is_muted
        new_icon = 'images/mute_icon.png' if self.is_muted else 'images/unmute_icon.png'
        self.mute_button.background_normal = new_icon

    def start_updating_vehicle_data(self):
        Clock.schedule_interval(self.update_vehicle_data, 1)  # update every 1 second

    def update_vehicle_data(self, dt):
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:  # Make sure the line isn't empty
                data = line.split(',')
                tire_temperature = list(map(float, data[0:4]))
                road_temperature = float(data[4])
    
                # Access current vehicle type from the spinner
                current_vehicle_type = self.spinner.text
                vehicle_class = self.vehicle_types.get(current_vehicle_type, Car)  # Default to Car if no match
    
                # Update the vehicle instance with new data
                self.vehicle = vehicle_class(tire_temperature, road_temperature)
                self.update_display()



    def on_stop(self):
        Clock.unschedule(self.update_vehicle_data)
        ser.close()  # Close serial port when app closes
    
            
if __name__ == '__main__':
    VehicleApp().run()
