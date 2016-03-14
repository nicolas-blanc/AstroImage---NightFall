from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

Builder.load_file('ViewWindow.kv')

class ViewExplorer(BoxLayout):
    pass

class ViewImage(BoxLayout):
    pass

class ViewMenu(BoxLayout):
    pass

class ViewProcess(BoxLayout):
    pass

class ViewRender(BoxLayout):
    pass

class ViewShortcut(GridLayout):
    pass

class ViewWindow(FloatLayout):
    pass

class mainApp(App):
    def build(self):
        return ViewWindow()


if __name__ == '__main__':
    mainApp().run()
