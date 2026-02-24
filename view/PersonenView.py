import tkinter as tk
from tkinter import ttk, messagebox


class PersonenView(tk.Frame):
    def __init__(self, parent, controller, app_parent=None):
        super().__init__(parent)
        self.controller = controller
        self.app_parent = app_parent
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
            text="Werk persoon bij",
            command=self.werk_persoon_bij
        ).grid(row=3, column=0, columnspan=2, pady=(8, 12))

        tk.Button(
            self,
            text="Verwijder persoon",
            command=self.verwijder_persoon
        ).grid(row=4, column=0, columnspan=2, pady=(8, 12))

        self.tree = ttk.Treeview(
            self,
            columns=("id", "naam", "telefoonnummer"),
            show="headings"
        )

        for col in ("id", "naam", "telefoonnummer"):
            self.tree.heading(col, text=col)

        self.tree.grid(row=5, column=0, columnspan=2, sticky="nsew")

        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)

        self.refresh_tabel()

    def voeg_persoon_toe(self):
        # Zorg dat we de juiste controller gebruiken
        self.controller.activate_controller("personen")
        naam = self.entry_naam.get().strip()
        tel = self.entry_telefoonnummer.get().strip()

        # Validatie: naam is ingevuld
        is_valid, error_msg = self.controller.get_active_controller().validate_persoon_name(naam)
        if not is_valid:
            messagebox.showwarning("Validatiefout", error_msg)
            return

        # Validatie: telefoonnummer is ingevuld en uniek
        is_valid, error_msg = self.controller.get_active_controller().validate_persoon_phone(tel)
        if not is_valid:
            messagebox.showwarning("Validatiefout", error_msg)
            return

        self.controller.get_active_controller().voeg_persoon_toe(naam, tel)
        self.refresh_tabel()
        # Ledig de invoervelden na succesvol toevoegen
        self.entry_naam.delete(0, tk.END)
        self.entry_telefoonnummer.delete(0, tk.END)
        messagebox.showinfo("Succes", f"Persoon '{naam}' succesvol toegevoegd!")
        if self.app_parent: 
            self.app_parent.refresh_dropdown_views() #refresh dropdowns in other views

    def verwijder_persoon(self, id=None):
        # Zorg dat we de juiste controller gebruiken
        self.controller.activate_controller("personen")
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning(
                "Fout",
                "Gelieve een persoon te selecteren om te verwijderen."
            )
            return

        item = self.tree.item(selected_item)
        persoon_id = item["values"][0]
        persoon_naam = item["values"][1]

        # Validatie: kan persoon verwijderd worden?
        can_delete, error_msg = self.controller.get_active_controller().validate_persoon_deletion(persoon_id)
        if not can_delete:
            messagebox.showwarning("Kan niet verwijderen", error_msg)
            return

        # Bevestiging
        if messagebox.askyesno("Bevestiging", f"Wilt u de persoon '{persoon_naam}' echt verwijderen?"):
            self.controller.get_active_controller().verwijder_persoon(persoon_id)
            self.refresh_tabel()
            # Ledig de invoervelden na succesvol verwijderen
            self.entry_naam.delete(0, tk.END)
            self.entry_telefoonnummer.delete(0, tk.END)
            messagebox.showinfo("Succes", "Persoon succesvol verwijderd!")
            if self.app_parent:
                self.app_parent.refresh_dropdown_views()

    def refresh_tabel(self):
        rows = self.controller.get_data()
        self.tree.delete(*self.tree.get_children())

        for row in rows:
            self.tree.insert("", "end", values=row)


    def werk_persoon_bij(self):
        # Zorg dat we de juiste controller gebruiken
        self.controller.activate_controller("personen")
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning(
                "Fout",
                "Gelieve een persoon te selecteren om bij te werken."
            )
            return

        item = self.tree.item(selected_item)
        persoon_id = item["values"][0]

        naam = self.entry_naam.get().strip()
        tel = self.entry_telefoonnummer.get().strip()

        # Validatie: naam is ingevuld
        is_valid, error_msg = self.controller.get_active_controller().validate_persoon_name(naam, exclude_id=persoon_id)
        if not is_valid:
            messagebox.showwarning("Validatiefout", error_msg)
            return

        # Validatie: telefoonnummer is ingevuld en uniek
        is_valid, error_msg = self.controller.get_active_controller().validate_persoon_phone(tel, exclude_id=persoon_id)
        if not is_valid:
            messagebox.showwarning("Validatiefout", error_msg)
            return

        self.controller.get_active_controller().werk_persoon_bij(persoon_id, naam, tel)
        self.refresh_tabel()
        # Ledig de invoervelden na succesvol bijwerken
        self.entry_naam.delete(0, tk.END)
        self.entry_telefoonnummer.delete(0, tk.END)
        messagebox.showinfo("Succes", f"Persoon '{naam}' succesvol bijgewerkt!")
        if self.app_parent:
            self.app_parent.refresh_dropdown_views()


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

