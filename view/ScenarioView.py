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
from .components import ModernEditOverlay, EditCard, HoverTwoLineListItem
from kivymd.uix.list import IconLeftWidget

class ScenarioView(MDFloatLayout, MDTabsBase):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        scroll = MDScrollView()
        self.list_container = MDList(padding=dp(12), spacing=dp(8))
        scroll.add_widget(self.list_container)
        
        self.add_widget(scroll)
        
        self.fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"right": 0.95, "bottom": 0.05},
            md_bg_color=[0.2, 0.7, 0.6, 1]  # Teal
        )
        self.fab.bind(on_release=lambda x: self.open_edit_dialog(None))
        self.add_widget(self.fab)
        
        self.refresh_scenario_tabel()

    def open_edit_dialog(self, scenario_data=None):
        self.overlay = ModernEditOverlay()
        card = EditCard()
        
        from kivymd.uix.label import MDLabel
        title = MDLabel(
            text="Scenario Bewerken" if scenario_data else "Nieuw Scenario",
            halign="center",
            font_style="H6",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            size_hint_y=None,
            height=dp(40)
        )
        card.add_widget(title)
        
        name_field = MDTextField(hint_text="Naam Scenario", mode="rectangle")
        icon_field = MDTextField(hint_text="Icoon bestandsnaam", mode="rectangle")
        
        if scenario_data:
            name_field.text = scenario_data[1]
            icon_field.text = scenario_data[2]
            
        card.add_widget(name_field)
        card.add_widget(icon_field)
        
        btn_box = MDBoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(50))
        
        btn_cancel = MDFlatButton(text="ANNULEER")
        btn_cancel.bind(on_release=self.overlay.dismiss)
        
        btn_save = MDFillRoundFlatButton(text="OPSLAAN" if scenario_data else "TOEVOEGEN")
        btn_save.bind(on_release=lambda x: self.save_scenario(
            scenario_data[0] if scenario_data else None,
            name_field.text,
            icon_field.text
        ))
        
        btn_box.add_widget(btn_cancel)
        btn_box.add_widget(btn_save)
        
        if scenario_data:
            btn_delete = MDFlatButton(text="VERWIJDER", theme_text_color="Error")
            btn_delete.bind(on_release=lambda x: self.delete_scenario(scenario_data[0]))
            btn_box.add_widget(btn_delete)

        card.add_widget(btn_box)
        
        self.overlay.content_widget = card
        self.overlay.add_widget(card)
        Window.add_widget(self.overlay)
        self.overlay.open()

    def save_scenario(self, sid, naam, icoon):
        self.controller.activate_controller("scenario")
        naam = naam.strip()
        icoon = icoon.strip()
        
        if not naam or not icoon:
            toast("Vul alles in.")
            return

        if sid:
            # Correctly update the scenario without deleting it (which preserves ID and links)
            self.controller.get_active_controller().update_scenario(sid, naam, icoon)
            toast("Aangepast!")
        else:
            self.controller.get_active_controller().voeg_scenario_toe(naam, icoon)
            toast("Toegevoegd!")
            
        self.overlay.dismiss()
        self.refresh_scenario_tabel()

    def delete_scenario(self, sid):
        self.controller.activate_controller("scenario")
        if self.controller.get_active_controller().verwijder_scenario(sid) is False:
            toast("Fout: Verwijder eerst gekoppelde items.")
        else:
            toast("Verwijderd!")
            self.overlay.dismiss()
        self.refresh_scenario_tabel()

    def refresh_scenario_tabel(self):
        self.controller.activate_controller("scenario")
        rows = self.controller.get_data()
        self.list_container.clear_widgets()
        for row in rows:
            item = HoverTwoLineListItem(
                text=row[1],
                secondary_text=f"Icoon: {row[2]}"
            )
            icon = IconLeftWidget(icon="alert-circle-outline")
            item.add_widget(icon)
            item.bind(on_release=lambda x, r=row: self.open_edit_dialog(r))
            self.list_container.add_widget(item)

