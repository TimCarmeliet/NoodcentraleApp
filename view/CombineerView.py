import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class CombineerView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.activate_controller("combineer")
        self.build_ui()


    def refresh_dropdowns(self):
        #Laad personen en scenario's in dropdowns
        personen = self.controller.get_active_controller().get_personen()
        scenarios = self.controller.get_active_controller().get_scenarios()

        self.personen_dict = {p[1]: p[0] for p in personen}  # naam -> id
        self.scenario_dict = {s[1]: s[0] for s in scenarios}  # naam -> id

        self.combo_persoon['values'] = list(self.personen_dict.keys())
        self.combo_scenario['values'] = list(self.scenario_dict.keys())

    def voeg_koppeling_toe(self):
        #voeg een koppeling tussen persoon en scenario toe
        persoon_naam = self.combo_persoon.get()
        scenario_naam = self.combo_scenario.get()

        if not persoon_naam or not scenario_naam:
            messagebox.showwarning("Fout" , "Gelieve een persoon en scenario te selecteren.")

        persoon_id = self.personen_dict[persoon_naam]
        scenario_id = self.scenario_dict[scenario_naam]

        self.controller.get_active_controller().voeg_koppeling_toe(scenario_id, persoon_id)
        self.refresh_koppeling_tabel()
        messagebox.showinfo("Succes", f"{persoon_naam} is gekoppeld aan scenario {scenario_id}.")

    def verwijder_koppeling(self):
        id = int(simpledialog.askstring("Verwijder registratie","Welke persoon wil je verwijderen van welk scenario?"))
        self.controller.get_active_controller().delete_scenario_user(id)
        messagebox.showinfo("Succes", "Registratie succesvol verwijderd!")
        self.refresh_koppeling_tabel()


    def refresh_koppeling_tabel(self):
        #Toont alle koppelingen in de tabel
        rows = self.controller.get_active_controller().data_inladen()
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            naam = int(row[0])
            scenario_naam = self.controller.get_active_controller().get_scenario_naam(row[1])
            user_naam = self.controller.get_active_controller().get_persoon_naam(row[2])
            self.tree.insert("", "end", values=(naam, scenario_naam[0][0], user_naam[0][0]))
        
    def build_ui(self):
        #Dropdowns en knop voor koppeling
        tk.Label(self, text="Persoon: ").grid(row=0, column=0, sticky="e", pady=5)
        self.combo_persoon = ttk.Combobox(self, width=47, state="readonly")
        self.combo_persoon.grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(self, text="Scenario:").grid(row=1, column=0, sticky="e", pady=5)
        self.combo_scenario = ttk.Combobox(self, width=47, state="readonly")
        self.combo_scenario.grid(row=1, column=1, sticky="w", pady=5)

        tk.Button(self, text="Koppel persoon aan scenario", 
                  command=self.voeg_koppeling_toe).grid(row=2, column=0, columnspan=2, pady=(8, 12))
        
        tk.Button(self, text="Verwijder persoon van scenario", 
                  command=self.verwijder_koppeling).grid(row=3, column=0, columnspan=2, pady=(8, 12))
        
        # de naam van de personen en scenario's in de tabel weergeven en niet ID's
        #Tabel met bestaande koppelingen
        self.tree = ttk.Treeview(self, columns=("id", "scenario", "user"), show="headings")
        for col in ("id", "scenario", "user"):
            self.tree.heading(col, text=col)
            self.tree.grid(row=4, column=0, columnspan=2, sticky="nsew")

        self.refresh_dropdowns()
        self.refresh_koppeling_tabel()