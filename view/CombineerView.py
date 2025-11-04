import tkinter as tk
from tkinter import ttk, messagebox

class CombineerView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.activate_controller("combineer")
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Personen koppelen aan scenario's", font=("Arial", 12)).pack(pady=5)
