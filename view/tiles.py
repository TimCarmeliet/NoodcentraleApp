from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivy.properties import StringProperty, ListProperty
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle

class ScenarioTile(MDCard, RectangularRippleBehavior, ButtonBehavior):
    """
    Simple, robust tile for quick access to scenarios.
    No complex animations or glassmorphism to ensure speed and reliability.
    """
    text = StringProperty("")
    icon_source = StringProperty("")
    icon_name = StringProperty("alert")
    bg_color = ListProperty([0.2, 0.2, 0.3, 1])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.ripple_behavior = True
        self.padding = dp(16)
        self.spacing = dp(8)
        self.radius = [dp(16)]
        self.elevation = 4
        
        # Determine background color based on text (simple hashing for variety)
        # or use the provided bg_color
        self.md_bg_color = self.bg_color
        
        # Icon Area (Centered)
        self.icon_box = MDFloatLayout(size_hint=(1, 0.6))
        
        if self.icon_source:
             self.icon_widget = Image(
                source=self.icon_source,
                pos_hint={"center_x": .5, "center_y": .5},
                size_hint=(None, None),
                size=(dp(48), dp(48)),
                fit_mode="contain"
            )
        else:
            self.icon_widget = MDIcon(
                icon=self.icon_name,
                halign="center",
                theme_text_color="Custom",
                text_color=[1, 1, 1, 1],
                font_size=dp(48),
                pos_hint={"center_x": .5, "center_y": .5}
            )
            
        self.icon_box.add_widget(self.icon_widget)
        self.add_widget(self.icon_box)
        
        # Text Area
        self.lbl_text = MDLabel(
            text=self.text,
            halign="center",
            valign="top",
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            bold=True,
            size_hint_y=0.4
        )
        self.add_widget(self.lbl_text)

