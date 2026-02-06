from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from controllers.NoodcentraleAppController import NoodcentraleAppController
from NoodcentraleAppModel import NoodcentraleAppModel
from view.NoodcentraleAppView import MainScreen
from view.ConfigView import ConfigScreen

class NoodcentraleApp(MDApp):
    def build(self):
        self.title = "Noodcentrale App"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Dark"
        
        # Setup MVC
        DB = "noodcentrale.db"
        self.model = NoodcentraleAppModel(DB)
        self.controller = NoodcentraleAppController(self.model)

        # Screen Manager
        self.sm = MDScreenManager()
        
        # Instantiate screens with controller
        self.main_screen = MainScreen(name='menu', controller=self.controller)
        self.config_screen = ConfigScreen(name='config', controller=self.controller)
        
        self.sm.add_widget(self.main_screen)
        self.sm.add_widget(self.config_screen)
        
        return self.sm

if __name__ == "__main__":
    NoodcentraleApp().run()


