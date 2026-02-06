from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFillRoundFlatButton, MDRaisedButton, MDFloatingActionButton, MDFlatButton
from kivymd.uix.list import MDList
from kivymd.uix.scrollview import MDScrollView
from kivymd.toast import toast
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.core.window import Window
from .components import ModernEditOverlay, EditCard
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget

class CombineerView(MDFloatLayout, MDTabsBase):
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
            md_bg_color=[0.8, 0.4, 0.6, 1]  # Pink
        )
        self.fab.bind(on_release=lambda x: self.open_edit_dialog(None))
        self.add_widget(self.fab)
        
        self.refresh_koppeling_tabel()

    def open_edit_dialog(self, link_data=None):
        """
        link_data: (id, scenario_id, user_id)
        Note: Current model doesn't support easy update for links, mostly add/delete.
        """
        from kivymd.uix.label import MDLabel
        
        self.controller.activate_controller("combineer")
        users = self.controller.get_active_controller().get_personen()
        scenarios = self.controller.get_active_controller().get_scenarios()
        
        self.overlay = ModernEditOverlay()
        card = EditCard(size_hint=(0.9, None), height=dp(400))
        
        # Title
        title = MDLabel(
            text="Koppeling Maken",
            halign="center",
            font_style="H6",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            size_hint_y=None,
            height=dp(40)
        )
        card.add_widget(title)
        
        # State
        self.selected_person_id = link_data[2] if link_data else None
        self.selected_scenario_id = link_data[1] if link_data else None
        
        # UI Elements
        person_text = "Selecteer Persoon"
        if self.selected_person_id:
            for p in users:
                if p[0] == self.selected_person_id:
                    person_text = p[1]
                    break
                    
        scenario_text = "Selecteer Scenario"
        if self.selected_scenario_id:
            for s in scenarios:
                if s[0] == self.selected_scenario_id:
                    scenario_text = s[1]
                    break
        
        self.person_btn = MDRaisedButton(
            text=person_text, 
            pos_hint={"center_x": .5}, 
            size_hint=(1, None),
            height=dp(50),
            md_bg_color=[0.3, 0.5, 0.8, 1]
        )
        self.scenario_btn = MDRaisedButton(
            text=scenario_text, 
            pos_hint={"center_x": .5}, 
            size_hint=(1, None),
            height=dp(50),
            md_bg_color=[0.8, 0.4, 0.5, 1]
        )
        
        # Menus
        p_items = [
            {"text": f"{p[1]}", "on_release": lambda x=p: self.set_person(x, self.person_btn)}
            for p in users
        ]
        self.p_menu = MDDropdownMenu(caller=self.person_btn, items=p_items, width_mult=4)
        self.person_btn.bind(on_release=lambda x: self.p_menu.open())
        
        s_items = [
            {"text": f"{s[1]}", "on_release": lambda x=s: self.set_scenario(x, self.scenario_btn)}
            for s in scenarios
        ]
        self.s_menu = MDDropdownMenu(caller=self.scenario_btn, items=s_items, width_mult=4)
        self.scenario_btn.bind(on_release=lambda x: self.s_menu.open())
        
        card.add_widget(self.person_btn)
        card.add_widget(self.scenario_btn)
        
        # Spacer
        card.add_widget(MDLabel(size_hint_y=None, height=dp(20)))
        
        btn_box = MDBoxLayout(orientation="horizontal", spacing=dp(15), size_hint_y=None, height=dp(50))
        btn_cancel = MDFlatButton(text="ANNULEER", on_release=self.overlay.dismiss)
        
        btn_save = MDFillRoundFlatButton(text="KOPPELEN", md_bg_color=[0.4, 0.8, 0.5, 1])
        btn_save.bind(on_release=lambda x: self.save_link(link_data[0] if link_data else None))
        
        btn_box.add_widget(btn_cancel)
        btn_box.add_widget(btn_save)
        
        if link_data:
            btn_delete = MDFlatButton(text="VERWIJDER", theme_text_color="Error")
            btn_delete.bind(on_release=lambda x: self.delete_link(link_data[0]))
            btn_box.add_widget(btn_delete)
            
        card.add_widget(btn_box)
        
        self.overlay.content_widget = card
        self.overlay.add_widget(card)
        Window.add_widget(self.overlay)
        self.overlay.open()

    def set_person(self, row, btn):
        self.selected_person_id = row[0]
        btn.text = row[1]
        self.p_menu.dismiss()
        
    def set_scenario(self, row, btn):
        self.selected_scenario_id = row[0]
        btn.text = row[1]
        self.s_menu.dismiss()

    def save_link(self, link_id):
        if not self.selected_person_id or not self.selected_scenario_id:
            toast("Selecteer beide.")
            return
            
        self.controller.activate_controller("combineer")
        
        # If editing (link_id exists), we delete old and add new (since it's a link table)
        if link_id:
            self.controller.get_active_controller().delete_scenario_user(link_id)
            
        self.controller.get_active_controller().voeg_koppeling_toe(self.selected_scenario_id, self.selected_person_id)
        toast("Gekoppeld!")
        self.overlay.dismiss()
        self.refresh_koppeling_tabel()

    def delete_link(self, link_id):
        self.controller.activate_controller("combineer")
        self.controller.get_active_controller().delete_scenario_user(link_id)
        toast("Verwijderd!")
        self.overlay.dismiss()
        self.refresh_koppeling_tabel()

    def refresh_koppeling_tabel(self):
        self.controller.activate_controller("combineer")
        rows = self.controller.get_active_controller().data_inladen()
        self.list_container.clear_widgets()
        for row in rows:
            kid = row[0]
            scenario_naam_list = self.controller.get_active_controller().get_scenario_naam(row[1])
            user_naam_list = self.controller.get_active_controller().get_persoon_naam(row[2])
            
            s_naam = scenario_naam_list[0][0] if scenario_naam_list else "?"
            u_naam = user_naam_list[0][0] if user_naam_list else "?"
            
            item = TwoLineAvatarIconListItem(
                text=u_naam,
                secondary_text=f"Scenario: {s_naam}",
            )
            icon = IconLeftWidget(icon="link-variant")
            item.add_widget(icon)
            item.bind(on_release=lambda x, r=row: self.open_edit_dialog(r))
            self.list_container.add_widget(item)