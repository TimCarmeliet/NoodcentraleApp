from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, ListProperty, NumericProperty
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.animation import Animation
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel, MDIcon
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from random import uniform, choice
from math import sin, cos, pi
from kivy.core.window import Window
from kivymd.uix.textfield import MDTextField

# Define KV for DynamicBackground
Builder.load_string('''
<DynamicBackground>:
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            texture: self.texture
''')

class DynamicBackground(MDFloatLayout):
    hue = NumericProperty(0)
    texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hue = 0.0
        Clock.schedule_interval(self.animate_background, 1 / 60)
        self.bind(size=self.draw_bg)
        self.bind(pos=self.draw_bg)
    
    def on_hue(self, instance, value):
        self.draw_bg()

    def draw_bg(self, *args):
        h = self.hue
        # Create vibrant shifting colors (purple, pink, cyan, teal)
        r1 = 0.4 + 0.3 * sin(h * 2 * pi)
        g1 = 0.1 + 0.15 * cos(h * 2 * pi + 1)
        b1 = 0.6 + 0.4 * sin(h * 2 * pi + 0.5)
        
        r2 = 0.15 + 0.1 * cos(h * 2 * pi + 2)
        g2 = 0.2 + 0.2 * sin(h * 2 * pi + 1.5)
        b2 = 0.5 + 0.3 * cos(h * 2 * pi)
        
        # Third color for more depth
        r3 = 0.1 + 0.1 * sin(h * 2 * pi + 3)
        g3 = 0.05 + 0.05 * cos(h * 2 * pi)
        b3 = 0.2 + 0.15 * sin(h * 2 * pi + 2)
        
        # Helper to clamp values to valid byte range
        def clamp(v):
            return max(0, min(255, int(v * 255)))
        
        c1 = [r1, g1, b1, 1]
        c2 = [r2, g2, b2, 1]
        c3 = [r3, g3, b3, 1]

        # Use 3-color gradient with clamped values
        texture = Texture.create(size=(1, 3), colorfmt='rgba')
        buf = bytes([
            clamp(c1[0]), clamp(c1[1]), clamp(c1[2]), 255,
            clamp(c2[0]), clamp(c2[1]), clamp(c2[2]), 255,
            clamp(c3[0]), clamp(c3[1]), clamp(c3[2]), 255
        ])
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        self.texture = texture

    def animate_background(self, dt):
        self.hue += 0.0008
        if self.hue > 1:
            self.hue = 0


class ParticleSystem(MDFloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.particles = []
        # Color palette: pink, cyan, gold, white, purple
        self.colors = [
            (1, 0.4, 0.7),    # Pink
            (0.4, 0.9, 1),    # Cyan
            (1, 0.85, 0.3),   # Gold
            (1, 1, 1),        # White
            (0.7, 0.5, 1),    # Purple
            (0.3, 1, 0.8),    # Mint
        ]
        Clock.schedule_interval(self.update_particles, 1.0 / 60.0)
        
    def update_particles(self, dt):
        # More particles, spawn more frequently
        if len(self.particles) < 120:
            if uniform(0, 1) > 0.6:
                self.add_particle()
                
        with self.canvas:
            self.canvas.clear()
            for p in self.particles[:]:
                p['y'] += p['vy']
                p['x'] += p['vx']
                p['life'] -= dt
                p['alpha'] = max(0, p['life'] / p['max_life'])
                
                # Slight horizontal drift
                p['vx'] += uniform(-0.02, 0.02)
                
                if p['life'] <= 0 or p['y'] > self.height or p['x'] < -20 or p['x'] > self.width + 20:
                    self.particles.remove(p)
                    continue
                    
                # Colorful glowing particles
                color = p['color']
                Color(color[0], color[1], color[2], p['alpha'] * 0.7)
                Ellipse(pos=(p['x'], p['y']), size=(p['size'], p['size']))
                
                # Add glow effect (larger, more transparent circle behind)
                Color(color[0], color[1], color[2], p['alpha'] * 0.2)
                glow_size = p['size'] * 2.5
                Ellipse(pos=(p['x'] - p['size']*0.75, p['y'] - p['size']*0.75), size=(glow_size, glow_size))

    def add_particle(self):
        self.particles.append({
            'x': uniform(0, self.width),
            'y': uniform(-20, 0),
            'vx': uniform(-0.8, 0.8),
            'vy': uniform(0.8, 2.5),
            'size': uniform(4, 12),
            'life': uniform(4, 8),
            'max_life': 8,
            'alpha': 1,
            'color': choice(self.colors)
        })

class GradientCard(MDCard):
    gradient_colors = ListProperty([[1, 0, 1, 1], [0, 1, 1, 1]])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gradient_rect = None
        self.bind(gradient_colors=self.update_gradient)
        self.bind(size=self.update_gradient)
        self.bind(pos=self.update_gradient)
        Clock.schedule_once(self.update_gradient)

    def update_gradient(self, *args):
        if not self.gradient_rect:
            with self.canvas.before:
                self.gradient_rect = Rectangle(pos=self.pos, size=self.size)

        texture = Texture.create(size=(2, 1), colorfmt='rgba')
        c1 = [int(c * 255) for c in self.gradient_colors[0]]
        c2 = [int(c * 255) for c in self.gradient_colors[1]]
        buf = bytes(c1 + c2)
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        
        self.gradient_rect.pos = self.pos
        self.gradient_rect.size = self.size
        self.gradient_rect.texture = texture

class ImmersiveCard(GradientCard, RectangularRippleBehavior, ButtonBehavior):
    text = StringProperty()
    icon_source = StringProperty()
    
    def __init__(self, **kwargs):
        if "gradient_colors" not in kwargs:
             # Semi-transparent gradients to let DynamicBackground show through
             kwargs["gradient_colors"] = [[0.15, 0.1, 0.25, 0.7], [0.08, 0.05, 0.15, 0.75]]
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.radius = [dp(20)]
        self.elevation = 4
        self.padding = dp(15)
        self.spacing = dp(10)
        
        self.icon_box = MDFloatLayout(size_hint=(1, 0.55))
        self.add_widget(self.icon_box)
        
        self.text_box = MDBoxLayout(orientation="vertical", size_hint=(1, 0.45), padding=[dp(15), dp(10)])
        self.add_widget(self.text_box)
        
        self.bind(text=self.update_ui)
        self.bind(icon_source=self.update_ui)
        
        # Ensure update_ui is called after initialization
        Clock.schedule_once(lambda dt: self.update_ui(), 0)

    def update_ui(self, *args):
        self.icon_box.clear_widgets()
        self.text_box.clear_widgets()
        
        if self.icon_source:
            from kivy.uix.image import Image
            img = Image(
                source=self.icon_source, 
                pos_hint={"center_x": .5, "center_y": .5},
                size_hint=(0.7, 0.7),
                fit_mode="contain"
            )
            self.icon_box.add_widget(img)
            
        lbl_title = MDLabel(
            text=self.text,
            halign="center",
            valign="center",
            font_style="H3", # Larger font
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            bold=True
        )
        self.text_box.add_widget(lbl_title)
        
        # Spacer
        self.text_box.add_widget(MDLabel(size_hint_y=None, height=dp(10)))
        
        lbl_sub = MDLabel(
            text="Tik om te starten",
            halign="center",
            valign="top",
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=[0.8, 0.8, 0.8, 1]
        )
        self.text_box.add_widget(lbl_sub)

class ModernEditOverlay(MDFloatLayout):
    content_widget = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = [0, 0, 0, 0]
        self.opacity = 0
        # Add a dark background rectangle to ensure it covers everything cleanly
        with self.canvas.before:
            Color(0, 0, 0, 0.7)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
    def open(self):
        anim = Animation(md_bg_color=[0, 0, 0, 0.8], opacity=1, duration=0.3)
        anim.start(self)
        if self.content_widget:
            self.content_widget.opacity = 0
            self.content_widget.pos_hint = {'center_x': 0.5, 'center_y': 0.4}
            anim_content = Animation(opacity=1, pos_hint={'center_x': 0.5, 'center_y': 0.5}, duration=0.3, t='out_back')
            anim_content.start(self.content_widget)

    def dismiss(self, *args):
        anim = Animation(opacity=0, duration=0.2)
        anim.bind(on_complete=lambda x, y: self.parent.remove_widget(self) if self.parent else None)
        anim.start(self)

class EditCard(GradientCard):
    def __init__(self, **kwargs):
        if "gradient_colors" not in kwargs:
             kwargs["gradient_colors"] = [[0.18, 0.15, 0.25, 1], [0.1, 0.08, 0.15, 1]]
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint = (0.85, None)
        self.height = dp(320)
        self.padding = dp(25)
        self.spacing = dp(15)
        self.radius = [dp(20)]
        self.elevation = 8
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

class RealGradientListItem(GradientCard, RectangularRippleBehavior, ButtonBehavior):
    text = StringProperty()
    secondary_text = StringProperty()
    tertiary_text = StringProperty()
    
    def __init__(self, **kwargs):
        if "gradient_colors" not in kwargs:
             kwargs["gradient_colors"] = [[0.2, 0.18, 0.28, 1], [0.12, 0.1, 0.18, 1]]
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(90)
        self.padding = dp(15)
        self.spacing = dp(4)
        self.radius = [dp(15)]
        self.elevation = 3
        self.ripple_behavior = True
        
        self.add_widget(MDLabel(text=self.text, font_style="Subtitle1", theme_text_color="Custom", text_color=[1,1,1,1], bold=True))
        if self.secondary_text:
            self.add_widget(MDLabel(text=self.secondary_text, font_style="Body2", theme_text_color="Custom", text_color=[0.9,0.9,0.9,1]))
        if self.tertiary_text:
            self.add_widget(MDLabel(text=self.tertiary_text, font_style="Caption", theme_text_color="Custom", text_color=[0.7,0.7,0.7,1]))


class ModernListItem(MDBoxLayout, RectangularRippleBehavior, ButtonBehavior):
    """Modern list item with icon and manual background drawing"""
    text = StringProperty("")
    secondary_text = StringProperty("")
    icon = StringProperty("account")
    bg_color = ListProperty([0.15, 0.12, 0.22, 0.95])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(72)
        self.padding = [dp(16), dp(8)]
        self.spacing = dp(16)
        self.ripple_behavior = True
        
        self.bind(size=self._draw_bg)
        self.bind(pos=self._draw_bg)
        Clock.schedule_once(lambda dt: self._draw_bg(), 0.05)
        Clock.schedule_once(lambda dt: self._build_content(), 0.05)
    
    def _draw_bg(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            from kivy.graphics import RoundedRectangle
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
    
    def _build_content(self):
        self.clear_widgets()
        
        # Icon container using MDIcon (not button!) so it doesn't steal clicks
        icon_container = MDFloatLayout(size_hint=(None, 1), width=dp(48))
        icon_widget = MDIcon(
            icon=self.icon,
            halign='center',
            theme_text_color="Custom",
            text_color=[0.7, 0.5, 1, 1],
            font_size=dp(28),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        icon_container.add_widget(icon_widget)
        self.add_widget(icon_container)
        
        # Text container
        text_box = MDBoxLayout(orientation="vertical", spacing=dp(2))
        text_box.add_widget(MDLabel(
            text=self.text,
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            bold=True
        ))
        if self.secondary_text:
            text_box.add_widget(MDLabel(
                text=self.secondary_text,
                font_style="Caption",
                theme_text_color="Custom",
                text_color=[0.7, 0.7, 0.8, 1]
            ))
        self.add_widget(text_box)


class ImmersiveExecutionOverlay(MDFloatLayout):
    step_text = StringProperty("")
    step_type = StringProperty("message") # message, location
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = [0, 0, 0, 0.95] # Darker background
        self.callback = None
        
        with self.canvas.before:
            Color(0.05, 0.05, 0.1, 1) 
            Rectangle(pos=self.pos, size=self.size)
        
        self.build_ui()
        
    def build_ui(self):
        # Close button
        self.btn_close = MDIconButton(
            icon="close",
            pos_hint={"right": 0.95, "top": 0.95},
            theme_text_color="Custom",
            text_color=[1,1,1,1],
            on_release=lambda x: self.dismiss()
        )
        self.add_widget(self.btn_close)

        self.container = MDBoxLayout(orientation="vertical", padding=dp(30), spacing=dp(20), pos_hint={"center_x": .5, "center_y": .5}, size_hint=(0.9, 0.8))
        self.add_widget(self.container)

        self.lbl_step = MDLabel(
            text=self.step_text,
            halign="center",
            font_style="H4",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            size_hint_y=0.4
        )
        self.container.add_widget(self.lbl_step)
        
        self.input_container = MDBoxLayout(orientation="vertical", size_hint_y=None, height=dp(80), spacing=dp(10))
        self.container.add_widget(self.input_container)
        
        # Spacer
        self.container.add_widget(MDLabel(size_hint_y=0.1))
        
        self.btn_action = MDFillRoundFlatButton(
            text="VOLGENDE",
            font_size="24sp",
            size_hint=(1, None),
            height=dp(60),
            pos_hint={"center_x": .5},
            md_bg_color=[1, 0, 0.6, 1]
        )
        self.btn_action.bind(on_release=self.process_action)
        self.container.add_widget(self.btn_action)
        
        self.bind(step_text=lambda x, y: setattr(self.lbl_step, 'text', y))

    def setup_step(self, text, type="message", callback=None):
        self.step_text = text
        self.step_type = type
        self.callback = callback
        
        self.input_container.clear_widgets()
        
        if type == "location":
            self.txt_field = MDTextField(
                hint_text="Voer locatie in...",
                mode="fill",
                fill_color_normal=[0.2, 0.2, 0.3, 1],
                text_color_normal=[1, 1, 1, 1],
                text_color_focus=[1, 1, 1, 1],
                size_hint_x=1
            )
            self.input_container.add_widget(self.txt_field)
            self.btn_action.text = "BEVESTIG"
        else:
            self.btn_action.text = "VOLGENDE"

    def process_action(self, *args):
        result = None
        if self.step_type == "location":
            result = self.txt_field.text
        
        if self.callback:
            self.callback(result)

    def show(self):
        Window.add_widget(self)
        self.opacity = 0
        anim = Animation(opacity=1, duration=0.3)
        anim.start(self)
    
    def dismiss(self):
        anim = Animation(opacity=0, duration=0.3)
        anim.bind(on_complete=lambda x,y: Window.remove_widget(self))
        anim.start(self)



class ScenarioTile(MDCard, RectangularRippleBehavior, ButtonBehavior):
    """
    Simple, robust tile for quick access to scenarios.
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
        self.md_bg_color = self.bg_color
        
        # Icon Area (Centered)
        self.icon_box = MDFloatLayout(size_hint=(1, 0.6))
        
        if self.icon_source:
             from kivy.uix.image import Image
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

# =====================================================
# MODERN DASHBOARD COMPONENTS
# =====================================================

Builder.load_string('''
<DashboardCard>:
    canvas.before:
        # Glow effect (outer)
        Color:
            rgba: self.glow_color[0], self.glow_color[1], self.glow_color[2], self.glow_alpha * 0.3
        RoundedRectangle:
            pos: self.x - dp(8), self.y - dp(8)
            size: self.width + dp(16), self.height + dp(16)
            radius: [dp(28)]
        # Main card background with gradient
        Color:
            rgba: self.bg_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(20)]
        # Glassmorphism overlay (subtle shine)
        Color:
            rgba: 1, 1, 1, self.shine_alpha
        RoundedRectangle:
            pos: self.x + dp(2), self.y + self.height * 0.5
            size: self.width - dp(4), self.height * 0.48
            radius: [dp(18), dp(18), dp(4), dp(4)]
''')

class DashboardCard(MDBoxLayout, RectangularRippleBehavior, ButtonBehavior):
    """Modern glassmorphism card with icon, title and subtitle"""
    
    icon_name = StringProperty("alert")
    icon_source = StringProperty("")  # For custom image icons
    title = StringProperty("Title")
    subtitle = StringProperty("")
    
    bg_color = ListProperty([0.15, 0.12, 0.25, 0.9])
    glow_color = ListProperty([0.6, 0.3, 1.0])  # Purple glow
    glow_alpha = NumericProperty(0)
    shine_alpha = NumericProperty(0.08)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (1, None)
        self.height = dp(160)
        self.padding = dp(10)
        self.spacing = dp(5)
        self.ripple_behavior = True
        
        # Icon container
        self.icon_container = MDFloatLayout(size_hint=(1, 0.6))
        self.add_widget(self.icon_container)
        
        # Text container
        self.text_container = MDBoxLayout(
            orientation='vertical',
            size_hint=(1, 0.4),
            spacing=dp(2)
        )
        self.add_widget(self.text_container)
        
        self.bind(icon_name=self._update_content)
        self.bind(icon_source=self._update_content)
        self.bind(title=self._update_content)
        self.bind(subtitle=self._update_content)
        self.bind(size=self._draw_background)
        self.bind(pos=self._draw_background)
        self.bind(glow_alpha=self._draw_background)
        self.bind(bg_color=self._draw_background)
        
        Clock.schedule_once(lambda dt: self._update_content(), 0.1)
        Clock.schedule_once(lambda dt: self._draw_background(), 0.1)
    
    def _draw_background(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # Glow effect
            Color(self.glow_color[0], self.glow_color[1], self.glow_color[2], self.glow_alpha * 0.3)
            from kivy.graphics import RoundedRectangle
            RoundedRectangle(pos=(self.x - dp(6), self.y - dp(6)), 
                           size=(self.width + dp(12), self.height + dp(12)), 
                           radius=[dp(24)])
            # Main background
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)])
            # Shine overlay
            Color(1, 1, 1, self.shine_alpha)
            RoundedRectangle(pos=(self.x + dp(2), self.y + self.height * 0.5), 
                           size=(self.width - dp(4), self.height * 0.48), 
                           radius=[dp(18), dp(18), dp(4), dp(4)])
    
    def _update_content(self, *args):
        self.icon_container.clear_widgets()
        self.text_container.clear_widgets()
        
        # Icon - prefer image source if available
        if self.icon_source:
            from kivy.uix.image import Image
            icon_widget = Image(
                source=self.icon_source,
                size_hint=(None, None),
                size=(dp(50), dp(50)),
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                fit_mode='contain'
            )
        else:
            # Use MDIcon (not MDIconButton) so it doesn't steal clicks
            icon_widget = MDIcon(
                icon=self.icon_name,
                halign='center',
                theme_text_color="Custom",
                text_color=[1, 1, 1, 1],
                font_size=dp(50),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
        self.icon_container.add_widget(icon_widget)
        
        # Title
        title_label = MDLabel(
            text=self.title,
            halign='center',
            font_style='Subtitle1',
            theme_text_color='Custom',
            text_color=[1, 1, 1, 1],
            bold=True
        )
        self.text_container.add_widget(title_label)
        
        # Subtitle
        if self.subtitle:
            subtitle_label = MDLabel(
                text=self.subtitle,
                halign='center',
                font_style='Caption',
                theme_text_color='Custom',
                text_color=[0.7, 0.7, 0.8, 1]
            )
            self.text_container.add_widget(subtitle_label)
    
    def on_press(self):
        anim = Animation(glow_alpha=0.8, shine_alpha=0.15, duration=0.1)
        anim.start(self)
    
    def on_release(self):
        anim = Animation(glow_alpha=0, shine_alpha=0.08, duration=0.3)
        anim.start(self)


class AnimatedGridLayout(MDGridLayout):
    """Grid layout with staggered entrance animation for children"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.spacing = dp(16)
        self.padding = dp(16)
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        self._animation_pending = []
    
    def add_widget(self, widget, index=0, canvas=None):
        # Start hidden
        widget.opacity = 0
        widget.y_offset = dp(30)
        super().add_widget(widget, index, canvas)
        
        # Schedule staggered animation
        delay = len(self.children) * 0.08
        Clock.schedule_once(lambda dt, w=widget: self._animate_in(w), delay)
    
    def _animate_in(self, widget):
        anim = Animation(opacity=1, duration=0.4, t='out_cubic')
        anim.start(widget)
    
    def animate_all_children(self):
        """Re-animate all children with stagger effect"""
        for i, child in enumerate(reversed(list(self.children))):
            child.opacity = 0
            delay = i * 0.1
            Clock.schedule_once(lambda dt, w=child: self._animate_in(w), delay)


class HeaderWidget(MDBoxLayout):
    """Modern header with title, dropdown and settings"""
    
    title = StringProperty("Noodcentrale")
    subtitle = StringProperty("Home")
    
    def __init__(self, on_settings=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(70)
        self.padding = [dp(20), dp(10)]
        self.on_settings_callback = on_settings
        
        # Left side - title and subtitle
        left_box = MDBoxLayout(orientation='vertical', size_hint_x=0.7)
        
        title_label = MDLabel(
            text=self.title,
            font_style='H5',
            theme_text_color='Custom',
            text_color=[1, 1, 1, 1],
            bold=True
        )
        left_box.add_widget(title_label)
        
        # Subtitle with dropdown icon
        sub_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(24))
        sub_label = MDLabel(
            text=self.subtitle,
            font_style='Caption',
            theme_text_color='Custom',
            text_color=[0.7, 0.7, 0.8, 1]
        )
        sub_box.add_widget(sub_label)
        # Dropdown icon removed as it had no function and confused the user
        sub_box.add_widget(MDLabel())  # Spacer
        left_box.add_widget(sub_box)
        
        self.add_widget(left_box)
        
        # Right side - settings button
        settings_btn = MDIconButton(
            icon='cog',
            theme_text_color='Custom',
            text_color=[1, 1, 1, 1],
            icon_size=dp(28),
            pos_hint={'center_y': 0.5}
        )
        if on_settings:
            settings_btn.bind(on_release=lambda x: on_settings())
        self.add_widget(settings_btn)


# Color palette for scenario cards
SCENARIO_COLORS = {
    'brand': {'bg': [0.3, 0.15, 0.15, 0.9], 'glow': [1.0, 0.4, 0.4]},      # Red
    'amok': {'bg': [0.25, 0.15, 0.35, 0.9], 'glow': [0.52, 0.37, 0.76]},   # Purple
    'dolle': {'bg': [0.35, 0.15, 0.3, 0.9], 'glow': [0.84, 0.37, 0.69]},   # Magenta
    'stil': {'bg': [0.15, 0.2, 0.35, 0.9], 'glow': [0.29, 0.48, 0.92]},    # Blue
    'ongeval': {'bg': [0.35, 0.25, 0.15, 0.9], 'glow': [1.0, 0.59, 0.44]}, # Orange
    'crisisoverleg': {'bg': [0.15, 0.3, 0.25, 0.9], 'glow': [0.0, 0.79, 0.65]}, # Teal
    'interventie': {'bg': [0.25, 0.25, 0.15, 0.9], 'glow': [0.9, 0.8, 0.3]}, # Yellow
    'einde': {'bg': [0.15, 0.25, 0.2, 0.9], 'glow': [0.3, 0.9, 0.5]},      # Green
    'default': {'bg': [0.18, 0.15, 0.25, 0.9], 'glow': [0.6, 0.5, 0.9]}    # Default purple
}

def get_scenario_colors(scenario_name):
    """Get colors based on scenario name keywords"""
    name_lower = scenario_name.lower()
    for key, colors in SCENARIO_COLORS.items():
        if key in name_lower:
            return colors
    return SCENARIO_COLORS['default']

