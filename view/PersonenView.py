import tkinter as tk
from tkinter import ttk, messagebox

class PersonenView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.activate_controller("personen")
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Naam:").grid(row=0, column=0, sticky="e", pady=5)
        self.entry_naam = tk.Entry(self, width=50)
        self.entry_naam.grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(self, text="Telefoonnummer:").grid(row=1, column=0, sticky="e", pady=5)
        self.entry_telefoonnummer = tk.Entry(self, width=50)
        self.entry_telefoonnummer.grid(row=1, column=1, sticky="w", pady=5)

        tk.Button(self, text="Voeg persoon toe", command=self.voeg_persoon_toe).grid(row=2, column=0, columnspan=2, pady=(8,12))

        self.tree = ttk.Treeview(self, columns=("id", "naam", "telefoonnummer"), show="headings")
        for col in ("id", "naam", "telefoonnummer"):
            self.tree.heading(col, text=col)
        self.tree.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.refresh_tabel()

    def voeg_persoon_toe(self):
        naam = self.entry_naam.get().strip()
        tel = self.entry_telefoonnummer.get().strip()
        if not naam or not tel:
            messagebox.showwarning("Fout", "Gelieve naam en telefoonnummer in te vullen.")
            return
        self.controller.get_active_controller().voeg_persoon_toe(naam, tel)
        self.refresh_tabel()

    def refresh_tabel(self):
        rows = self.controller.get_data()
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)
