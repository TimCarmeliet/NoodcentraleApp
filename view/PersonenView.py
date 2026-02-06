from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton, MDFloatingActionButton
from kivymd.uix.list import MDList
from kivymd.uix.scrollview import MDScrollView
from kivymd.toast import toast
from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.core.window import Window

from .components import ModernEditOverlay, EditCard, RealGradientListItem
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget

class PersonenView(MDFloatLayout, MDTabsBase):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        # Main content: List
        scroll = MDScrollView()
        self.list_container = MDList(padding=dp(12), spacing=dp(8))
        scroll.add_widget(self.list_container)
        
        self.add_widget(scroll)
        
        # Modern Floating Action Button
        self.fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"right": 0.95, "bottom": 0.05},
            md_bg_color=[0.6, 0.3, 0.9, 1]  # Purple
        )
        self.fab.bind(on_release=lambda x: self.open_edit_dialog(None))
        self.add_widget(self.fab)
        
        self.refresh_tabel()


    def open_edit_dialog(self, person_data=None):
        """
        Opens the overlay with a form.
        person_data: tuple (id, naam, tel) if editing, else None
        """
        self.overlay = ModernEditOverlay()
        
        card = EditCard(size_hint=(0.85, None), height=dp(300))
        
        # Form Fields
        name_field = MDTextField(hint_text="Naam", mode="rectangle")
        phone_field = MDTextField(hint_text="Telefoonnummer", mode="rectangle")
        
        if person_data:
            name_field.text = person_data[1]
            phone_field.text = person_data[2]
            
        card.add_widget(name_field)
        card.add_widget(phone_field)
        
        # Buttons
        btn_box = MDBoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(50))
        
        btn_cancel = MDFlatButton(text="ANNULEER")
        btn_cancel.bind(on_release=self.overlay.dismiss)
        
        btn_save = MDFillRoundFlatButton(text="OPSLAAN" if person_data else "TOEVOEGEN")
        btn_save.bind(on_release=lambda x: self.save_person(
            person_data[0] if person_data else None,
            name_field.text,
            phone_field.text
        ))

        btn_box.add_widget(btn_cancel)
        btn_box.add_widget(btn_save)
        
        if person_data:
            btn_delete = MDFlatButton(text="VERWIJDER", theme_text_color="Error")
            btn_delete.bind(on_release=lambda x: self.delete_person(person_data[0]))
            btn_box.add_widget(btn_delete)
        
        card.add_widget(btn_box)
        
        self.overlay.content_widget = card
        self.overlay.add_widget(card)
        
        # Add overlay to the main Window to float above everything
        Window.add_widget(self.overlay)
        self.overlay.open()

    def save_person(self, pid, naam, tel):
        self.controller.activate_controller("personen")
        naam = naam.strip()
        tel = tel.strip()
        
        if not naam or not tel:
            toast("Vul alles in aub.")
            return

        if pid:
            self.controller.get_active_controller().update_persoon(pid, naam, tel)
            toast("Aangepast!")
        else:
            self.controller.get_active_controller().voeg_persoon_toe(naam, tel)
            toast("Toegevoegd!")
            
        self.overlay.dismiss()
        self.refresh_tabel()

    def delete_person(self, pid):
        self.controller.activate_controller("personen")
        self.controller.get_active_controller().delete_persoon(pid)
        toast("Verwijderd!")
        self.overlay.dismiss()
        self.refresh_tabel()

    def refresh_tabel(self):
        self.controller.activate_controller("personen")
        rows = self.controller.get_data()
        self.list_container.clear_widgets()
        
        for row in rows:
            # row: (id, naam, telefoonnummer)
            item = TwoLineAvatarIconListItem(
                text=row[1],
                secondary_text=f"Tel: {row[2]}"
            )
            icon = IconLeftWidget(icon="account")
            item.add_widget(icon)
            item.bind(on_release=lambda x, r=row: self.open_edit_dialog(r))
            self.list_container.add_widget(item)

