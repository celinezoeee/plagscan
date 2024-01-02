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
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup


Builder.load_file('kivyy.kv')

#bild links oben 
Config.set('kivy', 'window_icon', 'image/bild.png')


# ladebalken -> todo: andere farbe?
class MyProgressBar(ProgressBar):
    def __init__(self, welcome_view, **kwargs):
        super().__init__(**kwargs)
        self.welcome_view = welcome_view
        #self.bar_color = (0.5, 0, 0.5) # hier die farbe ändern

    def update_progress(self, dt):
        self.value += 1 #wie schnell soll es laden?

        if self.value >= 100:
            self.switch_to_filechooser()

    def switch_to_filechooser(self):
        self.welcome_view.switch_to_filechooser()


#### -> um später einen kreis als ladebalken zu haben ? 
class CircularProgressBar(ProgressBar):
    def __init__(self, welcome_view, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)  # keine automatische größenanpassung
        self.size = (100, 100)  # größe des kreises
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # derweil in der mitte positionieren 
        self.welcome_view = welcome_view
        self.thickness = 20  # kleiner ring? 
        self.label = CoreLabel(text="0%", font_size=self.thickness)
        self.texture_size = None
        self.refresh_text()
        self.draw()

    def draw(self):
        with self.canvas:
            self.canvas.clear()
            Color(0, 0, 0)  #schwarz
            Ellipse(pos=self.pos, size=self.size)
            Color(0.5, 0, 0.5) #violett
            Ellipse(pos=self.pos, size=self.size, angle_end=(0.001 if self.value_normalized == 0 else self.value_normalized*360))
            Color(0, 0, 0)
            Ellipse(pos=(self.pos[0] + self.thickness / 2, self.pos[1] + self.thickness / 2),
                    size=(self.size[0] - self.thickness, self.size[1] - self.thickness))
            Color(1, 1, 1, 1)
            Rectangle(texture=self.label.texture, size=self.texture_size,
                      pos=(self.size[0] / 2 - self.texture_size[0] / 2 + self.pos[0], self.size[1] / 2 - self.texture_size[1] / 2 + self.pos[1]))

    def refresh_text(self):
        self.label.refresh()
        self.texture_size = list(self.label.texture.size)

    #im kreis die %
    def set_value(self, value):
        self.value = value
        self.label.text = str(int(self.value_normalized*100)) + "%"
        self.refresh_text()
        self.draw()

######


class WelcomeView(GridLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        
        # ausrichtung vom welcome screen -> hier mittig
        self.cols = 1
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        ###

        self.add_widget(Image(source='image/bild.png', size=(50, 50)))  # hier das bild dann einfugen

        self.greeting = Label(text='Welcome!', font_size=18, color='#9010ad')
        self.add_widget(self.greeting)

        # ladebalken einfügen
        self.progress_bar = MyProgressBar(welcome_view=self, max=100)
        #self.progress_bar = CircularProgressBar(welcome_view=self, max=80) #kreisladebalken

        self.add_widget(self.progress_bar)

        # laden
        Clock.schedule_interval(self.progress_bar.update_progress, 1 / 25)
        #Clock.schedule_interval(self.animate_progress, 0.1) #kreisladebalken
     
    def switch_to_filechooser(self):
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = 'filechooser'
        

    def show_popup(self):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Popup Content'))
        popup = Popup(title='Popup Title', content=content, size_hint=(None, None), size=(400, 400))
        popup.open()

    

class Filechooser(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_chooser = FileChooserListView()

        self.select_files_button = Button(text='Select Files', size_hint_y=None, height=50)
        self.select_files_button.bind(on_press=self.show_progress_bar)
        self.add_widget(self.select_files_button)

        self.progress_bar = None

    def show_progress_bar(self, instance):
        
        self.remove_widget(self.select_files_button) #löscht den button und ersetzt ihn mit:
        #einem kreisladebalken->
        self.progress_bar = CircularProgressBar(welcome_view=None, max=100)
        self.add_widget(self.progress_bar)
        Clock.schedule_interval(self.update_progress, 0.1)


    def update_progress(self, dt):
        if self.progress_bar.value < 100:
            self.progress_bar.set_value(self.progress_bar.value + 1)
        else:
            #todo: nach dem "laden" -> ein popup fenser öffnen für die berechnungen
            #self.parent.parent.show_popup()
            pass
            

    def select(self, *args):
        #ich kann es anklicken-> todo:nur das es auch den file öffnet
        print("file ausgewählt")
        # für die auswahl implementieren ...




class Plagscan(App):
    def build(self):
        screen_manager = ScreenManager()

        # wilkommen
        welcome_screen = Screen(name='welcomeView')
        welcome_view = WelcomeView(screen_manager)
        welcome_screen.add_widget(welcome_view)
        screen_manager.add_widget(welcome_screen)

        # filechooser
        filechooser_screen = Screen(name='filechooser')
        filechooser = Filechooser()
        filechooser_screen.add_widget(filechooser)
        screen_manager.add_widget(filechooser_screen)

        return screen_manager


if __name__ == '__main__':
    app = Plagscan()
    app.run()
