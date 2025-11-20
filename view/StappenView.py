import tkinter as tk
from tkinter import ttk, messagebox

class StappenView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.activate_controller("stappen")
        self.build_ui()

    def add_stappen(self):
        scenario = self.combo_scenario.get()
        scenario_id = self.controller.get_active_controller().get_scenario_id(scenario)
        id = scenario_id[0][0]
        actie = self.entry_actie.get()
        volgorde = self.entry_volgorde.get()
        bericht = self.entry_bericht.get()

        self.controller.get_active_controller().voeg_stap_toe(id, actie, volgorde, bericht)
        self.refresh_stappen_tabel()
        
    def refresh_dropdowns(self):
        #scenario's in dropdowns
        scenarios = self.controller.get_active_controller().get_scenarios()

        self.scenario_dict = {s[1]: s[0] for s in scenarios}  # naam -> id

        self.combo_scenario['values'] = list(self.scenario_dict.keys())

    def refresh_stappen_tabel(self):
        rows = self.controller.get_active_controller().data_inladen()
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)

    def build_ui(self):

        tk.Label(self, text="Scenario:").grid(row=0, column=0, sticky="e", pady=5)
        self.combo_scenario = ttk.Combobox(self, width=47, state="readonly")
        self.combo_scenario.grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(self, text="Actie (optioneel):").grid(row=1, column=0, sticky="e", pady=5)
        self.entry_actie = tk.Entry(self, width=50)
        self.entry_actie.grid(row=1, column=1, sticky="w", pady=5)

        tk.Label(self, text="Volgorde:").grid(row=2, column=0, sticky="e", pady=5)
        self.entry_volgorde = tk.Entry(self, width=50)
        self.entry_volgorde.grid(row=2, column=1, sticky="w", pady=5)

        tk.Label(self, text="Bericht:").grid(row=3, column=0, sticky="e", pady=5)
        self.entry_bericht = tk.Entry(self, width=100)
        self.entry_bericht.grid(row=3, column=1, sticky="w", pady=5)

        tk.Button(self, text="Voeg stappen toe", command=self.add_stappen).grid(row=4, column=1, sticky="w", pady=5)
        
        #Tabel met bestaande koppelingen
        self.tree = ttk.Treeview(self, columns=("id", "scenario_id", "actie", "volgorde", "bericht"), show="headings")
        for col in ("id", "scenario_id", "actie", "volgorde", "bericht"):
            self.tree.heading(col, text=col)
            self.tree.grid(row=5, column=0, columnspan=3, sticky="nsew")


        self.refresh_dropdowns()
        self.refresh_stappen_tabel()