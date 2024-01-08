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
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.graphics import Line
from kivymd.uix.progressbar import MDProgressBar

Builder.load_file('kivyy.kv')

#bild links oben 
Config.set('kivy', 'window_icon', 'image/bild.png')


# ladebalken -> todo: andere farbe?
class MyProgressBar(MDProgressBar):
    def __init__(self, welcome_view, **kwargs):
        super().__init__(**kwargs)
        self.welcome_view = welcome_view
        self.color = (0.5, 0, 0.5) # hier die farbe ändern

    def update_progress(self, dt):
        self.value += 1 #wie schnell soll es laden?

        if self.value >= 100:
            self.switch_to_mainview()

    def switch_to_mainview(self):
        self.welcome_view.switch_to_mainview()


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
     
    def switch_to_mainview(self):
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = 'mainview'
        



"""
class FileContentView(BoxLayout):
    def __init__(self, filechooser, file_path, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.filechooser = filechooser

        # Zurück-Button
        back_button = Button(text='Zurück', size_hint_y=None, height=50)
        back_button.bind(on_press=self.go_back)
        self.add_widget(back_button)

        # Dateiinhalt anzeigen
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()

            content_label = Label(text=f"Inhalt der ausgewählten Datei:\n{file_content}")
            self.add_widget(content_label)

        except Exception as e:
            print(f"Fehler beim Lesen der Datei: {e}")

    def go_back(self, instance):
        # Zurück zum Filechooser
        self.filechooser.clear_widgets()
        self.filechooser.add_widget(Filechooser())

    def show_file_content(self, file_path):
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()

            self.content_label.text = f"Inhalt der ausgewählten Datei:\n{file_content}"

        except Exception as e:
            print(f"Fehler beim Lesen der Datei: {e}")
"""


class MainView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def select_1(self, instance, value):
        if value:
            selected_file = value[0]
            try:
                with open(selected_file, 'r') as file:
                    file_content = file.read()
                    self.ids.label_1.text = f"Inhalt der ausgewählten Datei 1:\n{file_content}"
                    
            except Exception as e:
                print(f"Fehler beim Lesen der Datei: {e}")
        
        else:
            print("Keine Datei ausgewählt.")

    def select_2(self, instance, value):
        if value:
            selected_file = value[0]
            try:
                with open(selected_file, 'r') as file:
                    file_content = file.read()
                    self.ids.label_2.text = f"Inhalt der ausgewählten Datei 2:\n{file_content}"
                    
            except Exception as e:
                print(f"Fehler beim Lesen der Datei: {e}")
        
        else:
            print("Keine Datei ausgewählt.")
    def press_compare(self):
        if self.ids.label_1.text and self.ids.label_2.text:
            print("comparing now !!!")



"""
###############
class Filechooser(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filechooser_1 = None
        self.filechooser_2 = None
        self.content_label = Label()  # Assuming content_label is a Kivy Label
        self.add_widget(self.content_label)  # Add content_label to the layout

    def select(self, file_chooser, instance, value):
        if value:
            selected_file = value[0]

            try:
                with open(selected_file, 'r') as file:
                    file_content = file.read()

                self.content_label.text = f'Inhalt der ausgewählten Datei:\n{file_content}'

            except Exception as e:
                print(f"Fehler beim Lesen der Datei {selected_file}: {e}")
        else:
            print("Keine Datei ausgewählt.")


#########################



                if file_chooser == self.filechooser_1:
                    current_label = self.ids.label_1
                elif file_chooser == self.filechooser_2:
                    current_label = self.ids.label_2
                else:
                    return

                current_label.text = f'Inhalt der ausgewählten Datei:\n{file_content}'


#######################
                

        #todo: soll dann nur gehen wenn zwei files ausgwählt worden sind
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
            self.show_popup()  # Popup anzeigen
            Clock.unschedule(self.update_progress)  # Das Aktualisieren des Ladebalkens stoppen
            pass
            

    #öffnen dann ein pupup fenster 
    def show_popup(self):
        content = BoxLayout(orientation='vertical')
         # statt dem bild dann die berechnungen
        image = Image(source='image/bild.png', size=(420, 200))
        content.add_widget(image)

        close_button = Button(text='Schließen', size_hint_y=None, height=50)
        close_button.bind(on_press=self.dismiss_popup) #wenn ich auf den button clicke schließt er das pupup fenster
        content.add_widget(close_button)


        popup = Popup(title='Berechnungen', content=content, size_hint=(None, None), size=(700, 300))
        popup.open()

    def dismiss_popup(self, instance):
        popup = self.children[0]
        popup.dismiss()

"""
##--------------------------------------------------------
    


class Plagiloki(MDApp): #hier den namen links oben ändern
    def build(self):
        self.theme_cls.theme_style = 'Dark'  #theme style 

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
