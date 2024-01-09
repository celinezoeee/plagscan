from kivy.config import Config
from kivymd.app import MDApp
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
#from kivy.core.text import Label as CoreLabel #kreisladebalken ? 
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.graphics import Line
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window


from code_1 import plagiarism_checker

Builder.load_file('kivyy.kv')

# ladebalken
class MyProgressBar(MDProgressBar):
    def __init__(self, welcome_view, **kwargs):
        super().__init__(**kwargs)
        self.welcome_view = welcome_view
        self.color = (1, 0, 1, 1) # hier die farbe ändern
        self.size = (50, 50)

    def update_progress(self, dt):
        self.value += 1 #wie schnell soll es laden?

        if self.value >= 100:
            self.switch_to_mainview()

    def switch_to_mainview(self):
        self.welcome_view.switch_to_mainview()

"""
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
"""

class WelcomeView(GridLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        
        # ausrichtung vom welcome screen -> mittig
        self.cols = 1
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        ###

        self.add_widget(Image(source='image/logo_loki.png', size=(50, 50)))  # hier das bild dann einfugen

        self.greeting = Label(text='Welcome!', font_size=18, color=(1, 0, 1, 1))
        self.add_widget(self.greeting)

        # ladebalken einfügen
        self.progress_bar = MyProgressBar(welcome_view=self, max=100)
        self.add_widget(self.progress_bar)
        # laden
        Clock.schedule_interval(self.progress_bar.update_progress, 1 / 25)
     
    def switch_to_mainview(self):
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = 'mainview'

"""
#für das dialog fenster        
KV = '''
MDFloatLayout:

    MDFlatButton:
        text: "ALERT DIALOG"
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_release: app.show_alert_dialog()
        
'''
"""

class MainView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def select_1(self, instance, value):
        if value:
            selected_file = value[0]
            try:
                with open(selected_file, 'r') as file:
                    file_content_1 = file.read()
                    self.ids.label_1.text = f"{file_content_1}"
                    
            except Exception as e:
                print(f"Error reading the file: {e}")
        
        else:
            print("Error!")
        return file_content_1

    def select_2(self, instance, value):
        if value:
            selected_file = value[0]
            try:
                with open(selected_file, 'r') as file:
                    file_content_2 = file.read()
                    self.ids.label_2.text = f"{file_content_2}"
                    
            except Exception as e:
                print(f"Error reading the file: {e}")
        
        else:
            print("Error!")
        return file_content_2
    


    def calcultations(self, file_content_1, file_content_2):
        cosine_sim, lev_sim, sm_wa_sim, jac_sim, result = plagiarism_checker(file_content_1, file_content_2)
        return cosine_sim, lev_sim, sm_wa_sim, jac_sim, result

    def press_compare(self):
        default_text_1 = 'Select a file to start the scan...'
        default_text_2 = 'Select a file to start the scan...'

        file_content_1 = self.ids.label_1.text
        file_content_2 = self.ids.label_2.text

        if file_content_1 != default_text_1 and file_content_2 != default_text_2: #überprüft ob der default text noch darsteht dann führt er die berechnungen so lange nicht aus...
            cosine_sim, lev_sim, sm_wa_sim, jac_sim, result = self.calcultations(file_content_1, file_content_2)

            result = (
                f"[size=25][u]Calculations:[/u][/size]\n"
                f"Cosine Similarity: {cosine_sim:.2f}\n"
                f"Levenshtein Similarity: {lev_sim:.2f}\n"
                f"Smith-Waterman Similarity: {sm_wa_sim:.2f}\n"
                f"Jaccard Similarity: {jac_sim:.2f}\n\n"
                f"Overall Result: {result:.2f}%"
            )

            dialog = MDDialog(
                text=result, #gibt die berechnungen der zwei files aus
                buttons=[
                    MDFlatButton(
                        text="Back",
                        on_release=lambda *args: dialog.dismiss()
                    )
                ]
            )
            dialog.open()
        else:
        # Meldung anzeigen, wenn nicht beide Dateien ausgewählt sind
            error_dialog = MDDialog(
                text="Please select two files!",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda *args: error_dialog.dismiss()
                    )
                ]
            )
            error_dialog.open()



class Plagiloki(MDApp): #hier den namen links oben ändern
    def build(self):
        self.theme_cls.theme_style = 'Dark'  #theme style
        self.icon = "image/logo_loki_free.png" #icon (links oben) hier ändern

        screen_manager = ScreenManager()

        # wilkommen
        welcome_screen = Screen(name='welcomeView')
        welcome_view = WelcomeView(screen_manager)
        welcome_screen.add_widget(welcome_view)
        screen_manager.add_widget(welcome_screen)

        # filechooser
        mainview_screen = Screen(name='mainview')
        mainview = MainView()
        mainview_screen.add_widget(mainview)    
        screen_manager.add_widget(mainview_screen)
        
        return screen_manager


if __name__ == '__main__':
    app = Plagiloki()
    app.run()
