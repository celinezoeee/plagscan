from kivy.app import App
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.lang import Builder

Builder.load_file('kivyy.kv')

#bild links oben 
Config.set('kivy', 'window_icon', 'image/bild.png')
 
# create the layout class
class Filechooser(BoxLayout):
    def select(self, *args):
        try: self.label.text = args[1][0]
        except: pass
 

class MyProgressBar(Widget):
    pass

class WelcomeView(GridLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.cols = 1
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.add_widget(Image(source='image/bild.png', size=(50, 50)))  # hier das bild dann einfügen
        self.greeting = Label(text='Welcome!', font_size=18, color='#9010ad')
        self.add_widget(self.greeting)

        self.button = Button(text='Click to continue!')
        self.button.bind(on_release=self.switch_to_filechooser)
        self.add_widget(self.button)

    def switch_to_filechooser(self, instance):
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = 'filechooser'
        return True

class Plagscan(App):
    def build(self):
        # return Filechooser()
    
        screen_manager = ScreenManager()

        # Create and add the welcome screen
        welcome_screen = Screen(name='welcomeView')
        welcome_view = WelcomeView(screen_manager)
        welcome_screen.add_widget(welcome_view)
        screen_manager.add_widget(welcome_screen)

        # Create and add the filechooser screen
        filechooser_screen = Screen(name='filechooser')
        filechooser = Filechooser()
        filechooser_screen.add_widget(filechooser)
        screen_manager.add_widget(filechooser_screen)

        return screen_manager

if __name__ == '__main__':
    app = Plagscan()
    app.run()
 