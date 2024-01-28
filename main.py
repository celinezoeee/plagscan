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
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.graphics import Line
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window

#include the calculations
from code_1 import plagiarism_checker

Builder.load_file('kivyy.kv') # den .kv file includen

# loading bar for the first window
class MyProgressBar(MDProgressBar):
    def __init__(self, welcome_view, **kwargs):
        super().__init__(**kwargs)
        self.welcome_view = welcome_view
        self.color = (1, 0, 1, 1) # change the color (loading bar)
        self.size = (50, 50)

    def update_progress(self, dt):
        self.value += 1 # how fast should it load?

        if self.value >= 100:
            self.switch_to_mainview() #then switch to the next window

    def switch_to_mainview(self):
        self.welcome_view.switch_to_mainview()



class WelcomeView(GridLayout): # first window
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        
        # alignment of the welcome screen -> in the center
        self.cols = 1
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        ###

        self.add_widget(Image(source='image/logo_loki_klein.png', size=(50, 50)))  # insert a image

        self.greeting = Label(text='Welcome!', font_size=18, color=(1, 0, 1, 1))
        self.add_widget(self.greeting)

        # insert loading bar
        self.progress_bar = MyProgressBar(welcome_view=self, max=100)
        self.add_widget(self.progress_bar)
        # load
        Clock.schedule_interval(self.progress_bar.update_progress, 1 / 25)
     
    #then switch to second window 
    def switch_to_mainview(self):
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = 'mainview'


class MainView(BoxLayout): # second window
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    #select first file 
    def select_1(self, instance, value):
        file_content_1 = None  
        try:
            if value:
                selected_file = value[0]
                try:
                    # display the content of the selected file
                    with open(selected_file, 'r') as file:
                        file_content_1 = file.read()
                        self.ids.label_1.text = f"{file_content_1}"
                    
                except Exception as e:
                    # if an incorrect file has been selected
                    error_dialog = MDDialog(
                        text="Please select a valid file!",
                        buttons=[
                            MDFlatButton(
                                text="Back",
                                on_release=lambda *args: error_dialog.dismiss()
                            )
                        ]
                    )
                    error_dialog.open()
        except Exception as e:
            print("Error!")
        
        return file_content_1

    def select_2(self, instance, value):
        file_content_2 = None 
        try:
            if value:
                selected_file = value[0]
                try:
                    # display the content of the selected file
                    with open(selected_file, 'r') as file:
                        file_content_2 = file.read()
                        self.ids.label_2.text = f"{file_content_2}"
                    
                except Exception as e:
                    # if an incorrect file has been selected
                    error_dialog = MDDialog(
                        text="Please select a valid file!",
                        buttons=[
                            MDFlatButton(
                                text="Back",
                                on_release=lambda *args: error_dialog.dismiss()
                            )
                        ]
                    )
                    error_dialog.open()
        except Exception as e:
            print(f"Error!")

        return file_content_2
    

    # the results of the calculations
    def calcultations(self, file_content_1, file_content_2):
        cosine_sim, lev_sim, sm_wa_sim, jac_sim, result = plagiarism_checker(file_content_1, file_content_2)
        return cosine_sim, lev_sim, sm_wa_sim, jac_sim, result

    # when clicking the button, it checks and then it shows the calculations
    def press_compare(self):
        
        default_text_1 = 'Select a file to start the scan... (.m, .txt)'
        default_text_2 = 'Select a file to start the scan... (.m, .txt)'

        file_content_1 = self.ids.label_1.text
        file_content_2 = self.ids.label_2.text

        if file_content_1 != default_text_1 and file_content_2 != default_text_2: # checks if the default text is still present
            cosine_sim, lev_sim, sm_wa_sim, jac_sim, result = self.calcultations(file_content_1, file_content_2)
            
            #shows the calculations
            result = (
                f"[size=25][u]Calculations:[/u][/size]\n"
                f"Cosine Similarity: {cosine_sim:.2f}%\n"
                f"Levenshtein Similarity: {lev_sim:.2f}%\n"
                f"Smith-Waterman Similarity: {sm_wa_sim:.2f}%\n"
                f"Jaccard Similarity: {jac_sim:.2f}%\n\n"
                f"Overall Result: {result:.2f}%"
            )

            dialog = MDDialog(
                text=result, # displays the calculations from the two selected files
                buttons=[
                    MDFlatButton(
                        text="Back",
                        on_release=lambda *args: dialog.dismiss() # back to main view
                    )
                ]
            )
            dialog.open()
        else:
        # display a message if not both files are selected
            error_dialog = MDDialog(
                text="Please select two files!",
                buttons=[
                    MDFlatButton(
                        text="Back",
                        on_release=lambda *args: error_dialog.dismiss()
                    )
                ]
            )
            error_dialog.open()


class Plagiloki(MDApp): # change the name at the top left 
    def build(self):
        self.theme_cls.theme_style = "Dark"  #theme style
        self.icon = "image/logo_loki_free_klein.png" #icon image 

        screen_manager = ScreenManager()

        # welcome
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
