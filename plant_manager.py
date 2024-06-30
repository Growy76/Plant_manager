import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import pickle
import os
import json

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

class PlantGUI:
    def __init__(self, manager):
        self.manager = manager
        self.root = tk.Tk()
        self.root.title("Plant Manager")

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.entry_name = tk.Entry(self.root)
        self.entry_name.pack()
        self.entry_sowing_date = tk.Entry(self.root)
        self.entry_sowing_date.pack()
        self.entry_growing_days = tk.Entry(self.root)
        self.entry_growing_days.pack()

        self.button_add = tk.Button(self.root, text="Add Plant", command=self.add_plant)
        self.button_add.pack()
        self.button_remove = tk.Button(self.root, text="Remove Plant", command=self.remove_plant)
        self.button_remove.pack()
        self.button_save = tk.Button(self.root, text="Save Plants", command=self.save_plants)
        self.button_save.pack()
        self.button_load = tk.Button(self.root, text="Load Plants", command=self.load_plants)
        self.button_load.pack()
        self.canvas.mpl_connect('button_press_event', self.on_click)
        if os.path.exists("window_size.json"):
            with open("window_size.json", "r") as f:
                width, height = json.load(f)
                self.root.geometry(f"{width}x{height}")

        if os.path.exists("plants.pkl"):
            self.manager.load_plants("plants.pkl")
            self.update_plot()

    def on_click(self, event):
        for i, plant in enumerate(self.manager.plants):
            if event.ydata > i - 0.5 and event.ydata < i + 0.5:
                plant.harvested = True
                self.update_plot()
                break


    def add_plant(self):
        name = self.entry_name.get()
        sowing_date = datetime.datetime.strptime(self.entry_sowing_date.get(), "%Y-%m-%d")
        growing_days = int(self.entry_growing_days.get())
        plant = Plant(name, sowing_date, growing_days)
        self.manager.add_plant(plant)
        self.update_plot()

    def remove_plant(self):
        name = self.entry_name.get()
        self.manager.remove_plant(name)
        self.update_plot()

    def save_plants(self):
        self.manager.save_plants("plants.pkl")

    def load_plants(self):
        self.manager.load_plants("plants.pkl")
        self.update_plot()

    def update_plot(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        for i, plant in enumerate(self.manager.plants):
            elapsed_days = (datetime.datetime.now() - plant.sowing_date).days
            remaining_days = max(0, plant.growing_days - elapsed_days)
            color = 'green' if remaining_days > 0 else 'red'
            if plant.harvested:
                color = 'gray'
            ax.barh(i, elapsed_days, color=color)
            ax.text(elapsed_days/2, i, f"{elapsed_days} jours depuis le semis, {remaining_days} jours restants", ha='center', va='center', color='white')
        self.canvas.draw()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        width, height = self.root.winfo_width(), self.root.winfo_height()
        with open("window_size.json", "w") as f:
            json.dump([width, height], f)
    
    def on_closing(self):
        if self.root.winfo_exists():
            width, height = self.root.winfo_width(), self.root.winfo_height()
            with open("window_size.json", "w") as f:
                json.dump([width, height], f)
        self.root.destroy()


if __name__ == "__main__":
    manager = PlantManager()
    gui = PlantGUI(manager)
    gui.run()

