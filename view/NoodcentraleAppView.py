from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.carousel import MDCarousel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton, MDFlatButton, MDFloatingActionButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivy.uix.image import AsyncImage, Image
from kivy.metrics import dp
from kivy.clock import Clock
import os

from kivymd.uix.textfield import MDTextField
from .components import (
    DynamicBackground, ParticleSystem, ImmersiveExecutionOverlay, 
    ModernEditOverlay, EditCard, ImmersiveCard, ScenarioTile,
    HeaderWidget, get_scenario_colors
)
from kivy.core.window import Window


class MainScreen(MDScreen):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.on_enter = self.refresh_scenarios
        self.build_ui()
        self.execution_overlay = None

    def build_ui(self):
        # Background
        self.bg = DynamicBackground()
        # Particles removed as per user request
        
        # Main Layout
        self.layout = MDBoxLayout(orientation="vertical")
        
        # Header (Simple Toolbar-like)
        self.header = HeaderWidget(
            title="Noodcentrale",
            subtitle="Selecteer Scenario",
            on_settings=self.open_config
        )
        self.layout.add_widget(self.header)
        
        # Scrollable Grid of Dashboard Cards
        self.scroll = MDScrollView()
        # Use standard MDGridLayout for reliability
        self.grid = MDGridLayout(cols=2, padding=dp(20), spacing=dp(20), size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        
        self.scroll.add_widget(self.grid)
        self.layout.add_widget(self.scroll)
        
        self.bg.add_widget(self.layout)
        self.add_widget(self.bg)

    def open_config(self):
        self.manager.current = 'config'

    def refresh_scenarios(self):
        self.grid.clear_widgets()
        scenarios = self.controller.get_scenarios()
        
        if not scenarios:
            # Empty state
            card = ScenarioTile(
                text="Geen scenario's\nTik op instellingen",
                icon_name="alert-circle-outline",
                size_hint=(1, None),
                height=dp(150)
            )
            self.grid.add_widget(card)
            return

        for scenario in scenarios:
            s_id, naam, icoon = scenario
            
            # Icon path
            icoon_pad = os.path.join(os.path.dirname(__file__), icoon)
            if not os.path.exists(icoon_pad):
                icoon_pad = os.path.join(os.path.dirname(__file__), "brand_alarm.jpg")
                
            colors = get_scenario_colors(naam)
            
            # Card
            card = ScenarioTile(
                text=naam,
                icon_source=icoon_pad if os.path.exists(icoon_pad) else "",
                icon_name="alert" if not os.path.exists(icoon_pad) else "",
                bg_color=colors["bg"],
                size_hint=(1, None),
                height=dp(160)
            )
            card.bind(on_release=lambda x, sid=s_id, n=naam: self.start_scenario(sid, n))
            
            self.grid.add_widget(card)

    def start_scenario(self, scenario_id, scenario_naam):
        self.controller.activate_controller("stappen")
        stappen = self.controller.get_active_controller().get_stappen_from_scenario(scenario_id)
        
        if not stappen:
            self.show_dialog("Error", "Geen stappen gevonden voor dit scenario")
            return
            
        self.current_stappen = stappen
        self.current_step_index = 0
        self.current_locatie = ""
        
        # Initialize overlay
        self.execution_overlay = ImmersiveExecutionOverlay()
        self.execution_overlay.show()
        
        self.process_next_step()

    def process_next_step(self):
        if self.current_step_index >= len(self.current_stappen):
            self.execution_overlay.dismiss()
            self.show_dialog("Klaar", "Scenario voltooid")
            return
            
        stap = self.current_stappen[self.current_step_index]
        # stap structure: (id, scenario_id, actie, volgorde, bericht)
        actie = stap[2]
        bericht = stap[4]
        
        step_type = "message"
        callback = self.next_step_wrapper
        
        if actie == "locatie":
            step_type = "location"
            callback = self.submit_location
        elif actie == "stuur":
            if "XXX" in bericht and self.current_locatie:
                bericht = bericht.replace("XXX", self.current_locatie)
        
        self.execution_overlay.setup_step(bericht, type=step_type, callback=callback)

    def submit_location(self, text):
        self.current_locatie = text
        self.current_step_index += 1
        self.process_next_step()

    def next_step_wrapper(self, *args):
        self.current_step_index += 1
        self.process_next_step()

    def show_dialog(self, title, text):
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
        )
        self.dialog.open()

