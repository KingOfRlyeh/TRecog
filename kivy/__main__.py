import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

import matplotlib as mpl
if kivy.metrics.platform == 'win':
    mpl.use('TkAgg', force=True)
    
import math

import os
import trecogalg

gpath = 'C:/Users/jwbol/OneDrive/Documents/TRecog local/TRecog/kivy/C_maj_5_0.wav'
gfilename = 'C_maj_5_0.wav'

WINDOW_MIN_WIDTH = 640
WINDOW_MIN_HEIGHT = 360

class Analyzer(App):
     pass

class Root(RelativeLayout):
    path = StringProperty(gpath)
    filename = StringProperty(gfilename)
    threshold = NumericProperty(5)  
    font_scaling = NumericProperty()
    
    def on_size(self, *args):
        self.font_scaling = min(Window.width/WINDOW_MIN_WIDTH, Window.height/WINDOW_MIN_HEIGHT)

    
    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        global gpath
        global gfilename
        
        self.path = filename[0]
        gpath = filename[0]
        self.filename = os.path.basename(filename[0])
        gfilename = os.path.basename(filename[0])
        self.dismiss_popup()
    
    def value(self, value):
        self.threshold = value
        print(value)
    
    def update_chordname(self):
        self.ids.chordnamelabel.text = trecogalg.get_chordname(self.path, threshold=self.threshold)

    

        
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class MatGraph(FigureCanvasKivyAgg):
    global gpath
    fig = trecogalg.get_chromograph(gpath, 0.5)
    def __init__(self, **kwargs):
        super(MatGraph, self).__init__(plt.gcf())
        
    def generate(self, value):
        fig =  trecogalg.get_chromograph(gpath, value)
        super(MatGraph, self).__init__(fig)
        super(MatGraph, self).draw()
        
        

Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register("MatGraph", cls= MatGraph, is_template= True)

if __name__ == '__main__':
    Analyzer().run()