import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class ScenarioView(tk.Frame):
    def __init__(self, parent, controller, app_parent=None):
        super().__init__(parent)
        self.controller = controller
        self.app_parent = app_parent
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
        tk.Button(
            self,
            text="Werk scenario bij",
            command=self.werk_scenario_bij
        ).grid(row=3, column=0, columnspan=2, pady=(8, 12))

        tk.Button(self, text="Verwijder scenario", command=self.verwijder_scenario).grid(row=4, column=0, columnspan=2, pady=(8, 12))

        #activate personen controller
        self.controller.activate_controller("scenario")

        #SCENARIO tabel toevoegen
        self.s_tree = ttk.Treeview(self, columns=("id", "naam", "naam icoon"), show="headings")
        for col in ("id", "naam", "naam icoon"):
            self.s_tree.heading(col, text=col)

        #scenario tabel refreshen met de recentste date
        self.refresh_scenario_tabel()
        self.s_tree.grid(row=5, column=0, columnspan=2, pady=5, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)

        self.s_tree.bind("<ButtonRelease-1>", self.on_tree_click)


    def voeg_scenario_toe(self):
        # Zorg dat we de juiste controller gebruiken
        self.controller.activate_controller("scenario")
        naam = self.entry_snaam.get().strip()
        icoon = self.entry_sicoon.get().strip()

        # Validatie: naam is ingevuld
        is_valid, error_msg = self.controller.get_active_controller().validate_scenario_name(naam)
        if not is_valid:
            messagebox.showwarning("Validatiefout", error_msg)
            return

        # Validatie: icoon bestand bestaat
        is_valid, error_msg = self.controller.get_active_controller().validate_icon(icoon)
        if not is_valid:
            messagebox.showwarning("Validatiefout", error_msg)
            return

        # Validatie: icoon is uniek
        is_valid, error_msg = self.controller.get_active_controller().validate_icon_uniqueness(icoon)
        if not is_valid:
            messagebox.showwarning("Validatiefout", error_msg)
            return

        self.controller.get_active_controller().voeg_scenario_toe(naam, icoon)
        self.refresh_scenario_tabel()
        # Ledig de invoervelden na succesvol toevoegen
        self.entry_snaam.delete(0, tk.END)
        self.entry_sicoon.delete(0, tk.END)
        messagebox.showinfo("Succes", f"Scenario '{naam}' succesvol toegevoegd!")
        if self.app_parent:
            self.app_parent.refresh_dropdown_views() # Refresh de dropdowns in de andere views

    def werk_scenario_bij(self):
        # Zorg dat we de juiste controller gebruiken
        self.controller.activate_controller("scenario")
        scenario_id = self.s_tree.selection()
        if not scenario_id:
            messagebox.showwarning(
                "Fout",
                "Gelieve een scenario te selecteren om bij te werken."
            )
            return

        item = self.s_tree.item(scenario_id)
        scenario_id = item["values"][0]

        naam = self.entry_snaam.get().strip()
        icoon = self.entry_sicoon.get().strip()

        # Validatie: naam is ingevuld
        is_valid, error_msg = self.controller.get_active_controller().validate_scenario_name(naam, exclude_id=scenario_id)
        if not is_valid:
            messagebox.showwarning("Validatiefout", error_msg)
            return

        # Validatie: icoon bestand bestaat
        is_valid, error_msg = self.controller.get_active_controller().validate_icon(icoon)
        if not is_valid:
            messagebox.showwarning("Validatiefout", error_msg)
            return

        # Validatie: icoon is uniek
        is_valid, error_msg = self.controller.get_active_controller().validate_icon_uniqueness(icoon, exclude_id=scenario_id)
        if not is_valid:
            messagebox.showwarning("Validatiefout", error_msg)
            return

        self.controller.get_active_controller().werk_scenario_bij(scenario_id, naam, icoon)
        self.refresh_scenario_tabel()
        # Ledig de invoervelden na succesvol bijwerken
        self.entry_snaam.delete(0, tk.END)
        self.entry_sicoon.delete(0, tk.END)
        messagebox.showinfo("Succes", f"Scenario '{naam}' succesvol bijgewerkt!")
        if self.app_parent:
            self.app_parent.refresh_dropdown_views() # Refresh dropdowns in andere views
        
    """
    def verwijder_scenario(self):
        scenario_id = int(simpledialog.askstring("Verwijder Scenario","Welk scenario wil je verwijderen?"))
        if self.controller.get_active_controller().verwijder_scenario(scenario_id) is False:
            messagebox.showwarning("Fout", "Gelieve gekoppelde stappen/gebruikers te verwijderen.")
        else:
             messagebox.showinfo("Succes", "Scenario succesvol verwijderd!")
        self.refresh_scenario_tabel()
    """
    def verwijder_scenario(self, id=None):
        # Zorg dat we de juiste controller gebruiken
        self.controller.activate_controller("scenario")
        scenario_id = self.s_tree.selection()
        if not scenario_id:
            messagebox.showwarning(
                "Fout",
                "Gelieve een scenario te selecteren om te verwijderen."
            )
            return

        item = self.s_tree.item(scenario_id)
        scenario_id = item["values"][0]
        scenario_naam = item["values"][1]

        # Validatie: kan scenario verwijderd worden?
        can_delete, error_msg = self.controller.get_active_controller().validate_scenario_deletion(scenario_id)
        if not can_delete:
            messagebox.showwarning("Kan niet verwijderen", error_msg)
            return

        # Bevestiging
        if messagebox.askyesno("Bevestiging", f"Wilt u het scenario '{scenario_naam}' echt verwijderen?"):
            self.controller.get_active_controller().verwijder_scenario(scenario_id)
            self.refresh_scenario_tabel()
            # Ledig de invoervelden na succesvol verwijderen
            self.entry_snaam.delete(0, tk.END)
            self.entry_sicoon.delete(0, tk.END)
            messagebox.showinfo("Succes", "Scenario succesvol verwijderd!")
            if self.app_parent:
                self.app_parent.refresh_dropdown_views()

    def refresh_scenario_tabel(self):
        rows = self.controller.get_data()
        self.s_tree.delete(*self.s_tree.get_children())
        for row in rows:
            self.s_tree.insert("", "end", values=row)  

    def on_tree_click(self, event):
        item_id = self.s_tree.identify_row(event.y)
        if not item_id:
            return

        item = self.s_tree.item(item_id)
        _, naam, icoon = item["values"]

        self.entry_snaam.delete(0, tk.END)
        self.entry_sicoon.delete(0, tk.END)

        self.entry_snaam.insert(0, naam)
        self.entry_sicoon.insert(0, icoon)

