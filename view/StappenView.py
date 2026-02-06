from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFillRoundFlatButton, MDRaisedButton, MDFlatButton, MDFloatingActionButton
from kivymd.uix.list import MDList
from .components import ModernEditOverlay, EditCard
from kivymd.uix.list import ThreeLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.scrollview import MDScrollView
from kivymd.toast import toast
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.core.window import Window

class StappenView(MDFloatLayout, MDTabsBase):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        # Scroll view for list
        scroll = MDScrollView()
        self.list_container = MDList(padding=dp(10), spacing=dp(10))
        scroll.add_widget(self.list_container)
        self.add_widget(scroll)
        
        # FAB for adding new step
        self.fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"right": 0.95, "y": 0.05},
            md_bg_color=[0.4, 0.7, 1, 1]
        )
        self.fab.bind(on_release=lambda x: self.open_edit_dialog(None))
        self.add_widget(self.fab)
        
        self.refresh_stappen_tabel()

    def open_edit_dialog(self, stap_data=None):
        """
        stap_data: (id, scenario_id, actie, volgorde, bericht) or None for new
        """
        self.controller.activate_controller("stappen")
        scenarios = self.controller.get_active_controller().get_scenarios()
        
        self.overlay = ModernEditOverlay()
        card = EditCard(size_hint=(0.9, None), height=dp(450))
        
        # Title
        title_text = "Stap Bewerken" if stap_data else "Nieuwe Stap"
        title = MDLabel(
            text=title_text,
            halign="center",
            font_style="H6",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            size_hint_y=None,
            height=dp(40)
        )
        card.add_widget(title)
        
        # Scenario selector
        self.selected_scenario_id = stap_data[1] if stap_data else None
        scenario_text = "Selecteer Scenario"
        if self.selected_scenario_id:
            for s in scenarios:
                if s[0] == self.selected_scenario_id:
                    scenario_text = s[1]
                    break
        
        self.scenario_btn = MDRaisedButton(
            text=scenario_text, 
            pos_hint={"center_x": .5}, 
            size_hint=(1, None),
            height=dp(45),
            md_bg_color=[0.4, 0.5, 0.7, 1]
        )
        
        s_items = [
            {"text": f"{s[1]}", "on_release": lambda x=s: self.set_scenario_edit(x)}
            for s in scenarios
        ]
        self.s_menu = MDDropdownMenu(caller=self.scenario_btn, items=s_items, width_mult=4)
        self.scenario_btn.bind(on_release=lambda x: self.s_menu.open())
        card.add_widget(self.scenario_btn)
        
        # Fields
        self.action_field = MDTextField(hint_text="Actie (locatie/stuur/leeg)", mode="rectangle")
        self.order_field = MDTextField(hint_text="Volgorde (nummer)", mode="rectangle", input_type="number")
        self.msg_field = MDTextField(hint_text="Bericht", mode="rectangle", multiline=True)
        
        if stap_data:
            self.action_field.text = stap_data[2] or ""
            self.order_field.text = str(stap_data[3])
            self.msg_field.text = stap_data[4] or ""
        
        card.add_widget(self.action_field)
        card.add_widget(self.order_field)
        card.add_widget(self.msg_field)
        
        # Buttons
        btn_box = MDBoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(50))
        btn_cancel = MDFlatButton(text="ANNULEER", on_release=self.overlay.dismiss)
        
        btn_save = MDFillRoundFlatButton(
            text="OPSLAAN" if stap_data else "TOEVOEGEN",
            md_bg_color=[0.3, 0.8, 0.5, 1]
        )
        btn_save.bind(on_release=lambda x: self.save_stap(stap_data[0] if stap_data else None))
        
        btn_box.add_widget(btn_cancel)
        btn_box.add_widget(btn_save)
        
        if stap_data:
            btn_delete = MDFlatButton(text="VERWIJDER", theme_text_color="Error")
            btn_delete.bind(on_release=lambda x: self.delete_stap(stap_data[0]))
            btn_box.add_widget(btn_delete)
        
        card.add_widget(btn_box)
        
        self.overlay.content_widget = card
        self.overlay.add_widget(card)
        Window.add_widget(self.overlay)
        self.overlay.open()

    def set_scenario_edit(self, scenario_row):
        self.selected_scenario_id = scenario_row[0]
        self.scenario_btn.text = scenario_row[1]
        self.s_menu.dismiss()

    def save_stap(self, stap_id):
        if not self.selected_scenario_id:
            toast("Selecteer een scenario.")
            return
        
        volgorde = self.order_field.text.strip()
        bericht = self.msg_field.text.strip()
        actie = self.action_field.text.strip()
        
        if not volgorde or not bericht:
            toast("Vul minstens volgorde en bericht in.")
            return
        
        self.controller.activate_controller("stappen")
        
        if stap_id:
            # Update: delete old, add new (simple approach since model may not have update)
            self.controller.get_active_controller().delete_stap(stap_id)
        
        self.controller.get_active_controller().voeg_stap_toe(
            self.selected_scenario_id, actie, volgorde, bericht
        )
        
        toast("Opgeslagen!" if stap_id else "Toegevoegd!")
        self.overlay.dismiss()
        self.refresh_stappen_tabel()

    def delete_stap(self, stap_id):
        self.controller.activate_controller("stappen")
        self.controller.get_active_controller().delete_stap(stap_id)
        toast("Verwijderd!")
        self.overlay.dismiss()
        self.refresh_stappen_tabel()

    def refresh_stappen_tabel(self):
        self.controller.activate_controller("stappen")
        rows = self.controller.get_active_controller().data_inladen()
        self.list_container.clear_widgets()
        
        for row in rows:
            scenario_id = int(row[1])
            scenario_naam_list = self.controller.get_active_controller().get_scenario_naam(scenario_id)
            s_naam = scenario_naam_list[0][0] if scenario_naam_list else "?"
            
            text = f"{s_naam} - Stap {row[3]}"
            secondary = f"{row[2] or 'actie'}: {row[4][:40]}..." if len(row[4]) > 40 else f"{row[2] or 'actie'}: {row[4]}"
            
            item = ThreeLineAvatarIconListItem(
                text=text, 
                secondary_text=f"Actie: {row[2] or 'geen'}",
                tertiary_text=f"Bericht: {row[4]}",
            )
            icon = IconLeftWidget(icon="format-list-numbered")
            item.add_widget(icon)
            item.bind(on_release=lambda x, r=row: self.open_edit_dialog(r))
            self.list_container.add_widget(item)