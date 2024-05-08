from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle

class TireBox(BoxLayout):
    def __init__(self, tire_name, pressure, temperature, mileage, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.tire_name = tire_name
        self.pressure = pressure
        self.size_hint = (None, None)
        self.width = 200  # Adjust to fit your content
        self.height = 300  # Adjust to fit your content

        with self.canvas.before:
            self.bg_color = Color(1, 0, 0, 
                                  1) if pressure < 30 else Color(0, 1, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.tire_image_source = 'images/flat_tire.jpg' if pressure < 30 else 'images/tire.jpg'
        self.tire_image = Image(source=self.tire_image_source, size_hint=(1, 0.6), allow_stretch=True)
        self.add_widget(self.tire_image)

        self.tire_label = Label(
            text=f'{tire_name} Tire\nPressure: {pressure} PSI\nTemperature: {temperature}°F\nMileage: {mileage} miles',
            size_hint=(1, 0.4))
        self.add_widget(self.tire_label)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class CarStatsApp(App):
    def build(self):
        # Define grid layout for the tire information
        tire_grid = GridLayout(cols=2, padding=10, spacing=10, size_hint=(.7, 1))
        # Define a vertical layout for the additional information
        info_box = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(.3, 1))

        tires = [
            ('Front Left', 28, 75, 1200),
            ('Front Right', 32, 75, 1200),
            ('Rear Left', 29, 75, 1200),
            ('Rear Right', 34, 75, 1200)
        ]
        
        # Initialize a variable to check if any tire is in a bad state
        any_tire_bad = False

        for tire_name, pressure, temperature, mileage in tires:
            tire_box = TireBox(tire_name, pressure, temperature, mileage)
            tire_box.bind(size=tire_box.update_rect, pos=tire_box.update_rect)
            tire_grid.add_widget(tire_box)
            if pressure < 30:
                any_tire_bad = True

        # Define a vertical layout for the additional information
        info_box = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(.3, 1))

        # Define the labels with centered text
        humidity_label = Label(text='Trailer Humidity: 45%', size_hint=(1, 0.1), halign='center', valign='middle')
        humidity_label.bind(size=lambda *x: setattr(humidity_label, 'text_size', humidity_label.size))
        
        road_temp_label = Label(text='Road Temperature: 89°F', size_hint=(1, 0.1), halign='center', valign='middle')
        road_temp_label.bind(size=lambda *x: setattr(road_temp_label, 'text_size', road_temp_label.size))

        if any_tire_bad:
            warning_label = Label(text='WARNING! Check tire pressure.', size_hint=(1, 0.2), color=(1, 0, 0, 1), halign='center', valign='middle')
            warning_label.bind(size=lambda *x: setattr(warning_label, 'text_size', warning_label.size))
        else:
            warning_label = Label()  # Empty label if there is no warning

        info_box.add_widget(humidity_label)
        info_box.add_widget(road_temp_label)
        info_box.add_widget(warning_label)

        # Define the root layout
        root_layout = BoxLayout(orientation='horizontal', padding=10)
        root_layout.add_widget(tire_grid)
        root_layout.add_widget(info_box)

        return root_layout

if __name__ == '__main__':
    CarStatsApp().run()
