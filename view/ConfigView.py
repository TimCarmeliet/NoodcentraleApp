from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.tab import MDTabs
from kivymd.uix.boxlayout import MDBoxLayout
from .PersonenView import PersonenView
from .ScenarioView import ScenarioView
from .CombineerView import CombineerView
from .StappenView import StappenView
from kivymd.app import MDApp
from .components import DynamicBackground

class ConfigScreen(MDScreen):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        self.bg = DynamicBackground()
        layout = MDBoxLayout(orientation="vertical")
        
        # Toolbar with back button
        toolbar = MDTopAppBar(title="Instellingen", elevation=0)
        toolbar.md_bg_color = [0,0,0,0]
        toolbar.left_action_items = [["arrow-left", lambda x: self.go_back()]]
        layout.add_widget(toolbar)

        # Tabs
        self.tabs = MDTabs(background_color=[0,0,0,0], indicator_color=[0, 1, 1, 1], text_color_active=[1,1,1,1], text_color_normal=[0.7,0.7,0.7,1])
        
        # Initialize sub-views as Tabs
        # Note: These views need to inherit from MDTabsBase and a Layout
        self.tabs.add_widget(PersonenView(self.controller, title="Personen"))
        self.tabs.add_widget(ScenarioView(self.controller, title="Scenario's"))
        self.tabs.add_widget(CombineerView(self.controller, title="Koppelen"))
        self.tabs.add_widget(StappenView(self.controller, title="Stappen"))
        
        layout.add_widget(self.tabs)
        self.bg.add_widget(layout)
        self.add_widget(self.bg)
        
    def go_back(self):
        app = MDApp.get_running_app()
        app.sm.current = 'menu'
        # Optional: Refresh menu if needed when coming back
