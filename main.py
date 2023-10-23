import sys
import traceback

from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from app.app import BaseApp
from utility.singleton import SingletonInstane


class KivyRPGApp(BaseApp, SingletonInstane):
    def __init__(self, app_name):
        super(KivyRPGApp, self).__init__(app_name)
        
    def initialize(self):
        self.build() 

    def on_stop(self):
        pass

    
    def build(self):
        self.map_scroll_view = ScrollView(size_hint=(1, 1))
        self.map_layout = BoxLayout(orientation="vertical", size=(2000,2000), size_hint=(None, None))
        btn = Button(size_hint=(1,1))
        self.map_layout.add_widget(btn)
        self.map_scroll_view.add_widget(self.map_layout)
        self.add_widget(self.map_scroll_view)
    
    def update(self, dt):
        pass
    
