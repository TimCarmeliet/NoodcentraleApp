import tkinter as tk
from tkinter import ttk, messagebox

class ScenarioView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.activate_controller("scenario")
        self.build_ui()

    def build_ui(self):
        #VELDEN OM EEN NIEUW SCENARIO TOE TE VOEGEN
        tk.Label(self, text="Naam: ").grid(row=0, column=0, sticky="e", pady=5)
        self.entry_snaam = tk.Entry(self, width=50)
        self.entry_snaam.grid(row=0, column=1, sticky="w", pady=5)
        
        tk.Label(self, text="Icoon: ").grid(row=1, column=0, sticky="e", padx=(0, 1), pady=5)
        self.entry_sicoon = tk.Entry(self, width=50)
        self.entry_sicoon.grid(row=1, column=1, sticky="w", pady=5)

        #KNOP OM TOE TE VOEGEN
        tk.Button(self, text="Voeg scenario toe", command=self.voeg_scenario_toe).grid(row=2, column=0, columnspan=2, pady=(8, 12))

        #activate personen controller
        self.controller.activate_controller("scenario")

        #SCENARIO tabel toevoegen
        self.s_tree = ttk.Treeview(self, columns=("id", "naam", "naam icoon"), show="headings")
        for col in ("id", "naam", "naam icoon"):
            self.s_tree.heading(col, text=col)

        #scenario tabel refreshen met de recentste date
        self.refresh_scenario_tabel()
        self.s_tree.grid(row=3, column=0, columnspan=2, pady=5, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)


    def voeg_scenario_toe(self):
        naam = self.entry_snaam.get().strip()
        icoon = self.entry_sicoon.get().strip()

        #CONTROLE volledig ingevoerd?
        if not naam or not icoon:
            messagebox.showwarning("Fout", "Gelieve naam en de bestandsnaam van het icoon in te vullen.")
            return

        self.controller.get_active_controller().voeg_scenario_toe(naam, icoon)
        self.refresh_scenario_tabel()

    def refresh_scenario_tabel(self):
        rows = self.controller.get_data()
        self.s_tree.delete(*self.s_tree.get_children())
        for row in rows:
            self.s_tree.insert("", "end", values=row)  

