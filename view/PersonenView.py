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

        tk.Button(
            self,
            text="Voeg persoon toe",
            command=self.voeg_persoon_toe
        ).grid(row=2, column=0, columnspan=2, pady=(8, 12))

        tk.Button(
            self,
            text="Verwijder persoon",
            command=self.verwijder_persoon
        ).grid(row=2, column=3, columnspan=2, pady=(8, 12))

        self.tree = ttk.Treeview(
            self,
            columns=("id", "naam", "telefoonnummer"),
            show="headings"
        )

        for col in ("id", "naam", "telefoonnummer"):
            self.tree.heading(col, text=col)

        self.tree.grid(row=3, column=0, columnspan=2, sticky="nsew")

        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)

        self.refresh_tabel()

    def voeg_persoon_toe(self):
        naam = self.entry_naam.get().strip()
        tel = self.entry_telefoonnummer.get().strip()

        if not naam or not tel:
            messagebox.showwarning(
                "Fout",
                "Gelieve naam en telefoonnummer in te vullen."
            )
            return

        self.controller.get_active_controller().voeg_persoon_toe(naam, tel)
        self.refresh_tabel()

    def verwijder_persoon(self, id=None):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning(
                "Fout",
                "Gelieve een persoon te selecteren om te verwijderen."
            )
            return

        item = self.tree.item(selected_item)
        persoon_id = item["values"][0]

        if not self.controller.get_active_controller().verwijder_persoon(persoon_id):
            messagebox.showwarning(
                "Fout",
                "Deze persoon kan niet verwijderd worden omdat hij/zij aan een scenario is gekoppeld."
            )
            return

        self.controller.get_active_controller().verwijder_persoon(persoon_id)
        self.refresh_tabel()

    def refresh_tabel(self):
        rows = self.controller.get_data()
        self.tree.delete(*self.tree.get_children())

        for row in rows:
            self.tree.insert("", "end", values=row)

    def on_tree_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return

        item = self.tree.item(item_id)
        _, naam, telefoonnummer = item["values"]

        self.entry_naam.delete(0, tk.END)
        self.entry_telefoonnummer.delete(0, tk.END)

        self.entry_naam.insert(0, naam)
        self.entry_telefoonnummer.insert(0, telefoonnummer)

