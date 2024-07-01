from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
import datetime
import pickle

class Plant:
    def __init__(self, name, sowing_date, growing_days):
        self.name = name
        self.sowing_date = sowing_date
        self.growing_days = growing_days
        self.harvested = False

class PlantManager:
    def __init__(self):
        self.plants = []

    def add_plant(self, plant):
        self.plants.append(plant)

    def remove_plant(self, plant_name):
        self.plants = [plant for plant in self.plants if plant.name != plant_name]

    def save_plants(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.plants, f)

    def load_plants(self, filename):
        with open(filename, 'rb') as f:
            self.plants = pickle.load(f)

class PlantApp(App):
    def build(self):
        self.manager = PlantManager()
        self.layout = BoxLayout(orientation='vertical')
        self.plant_list = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.plant_list)
        self.add_plant_button = Button(text='Add Plant')
        self.add_plant_button.bind(on_press=self.add_plant)
        self.layout.add_widget(self.add_plant_button)
        return self.layout

    def add_plant(self, instance):
        name = TextInput(text='Name')
        sowing_date = TextInput(text='Sowing Date (YYYY-MM-DD)')
        growing_days = TextInput(text='Growing Days')
        add_button = Button(text='Add')
        add_button.bind(on_press=lambda x: self.create_plant(name.text, sowing_date.text, growing_days.text))
        self.layout.add_widget(name)
        self.layout.add_widget(sowing_date)
        self.layout.add_widget(growing_days)
        self.layout.add_widget(add_button)

    def create_plant(self, name, sowing_date, growing_days):
        sowing_date = datetime.datetime.strptime(sowing_date, "%Y-%m-%d")
        growing_days = int(growing_days)
        plant = Plant(name, sowing_date, growing_days)
        self.manager.add_plant(plant)
        self.update_plant_list()

    def update_plant_list(self):
        self.plant_list.clear_widgets()
        for plant in self.manager.plants:
            elapsed_days = (datetime.datetime.now() - plant.sowing_date).days
            remaining_days = max(0, plant.growing_days - elapsed_days)
            progress = ProgressBar(max=plant.growing_days, value=elapsed_days)
            self.plant_list.add_widget(Label(text=plant.name))
            self.plant_list.add_widget(progress)

if __name__ == "__main__":
    PlantApp().run()
