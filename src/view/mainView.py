from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListView
from kivy.uix.listview import ListItemButton
from kivy.adapters.models import SelectableDataItem
from kivy.cache import Cache
from kivy.core.image import Image
from kivy.graphics.texture import Texture
from kivy.core.image import Image as CoreImage

import io
import os.path
import AstroProcess
import ImageRaw
import imageio
import re

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

class DataItem(SelectableDataItem):
    def __init__(self, name, **kwargs):
        self.name = name
        super(DataItem, self).__init__(**kwargs)

class ViewSelectionList(BoxLayout):
    def __init__(self, **kwargs):
        super(ViewSelectionList, self).__init__(**kwargs)

        data_items = []
        list_item_args_converter = lambda row_index, obj: {'text': obj.name,'size_hint_y': None,'height': 25}
        self.list_adapter = \
            ListAdapter(data=data_items,
                    args_converter=list_item_args_converter,
                    selection_mode='single',
                    propagate_selection_to_data=False,
                    allow_empty_selection=False,
                    cls=ListItemButton)
        #self.list_adapter = \
        #    ListAdapter(data=data_items,
        #            args_converter=list_item_args_converter,
        #            selection_mode='single',
        #            propagate_selection_to_data=False,
        #            allow_empty_selection=False,
        #            cls=ListItemButton)
        #self.list_adapter.bind(on_selection_change=app.preview(self.list_adapter.selection))
        #self.list_adapter.bind(on_selection_change=root.preview(self.list_adapter.selection))
        #self.list_view = ListView(adapter=self.list_adapter)

        #self.add_widget(self.list_view)

    def update_list_data(self, path, filename):
            items = self.list_adapter.data
            item = DataItem(name=filename[0])
            items.append(item)

    def clear(self):
        print "Clear"
        self.list_adapter.data = []

    def remove(self, *args):
        if self.list_adapter.selection:
            for i in self.list_adapter.selection:
                for j in self.list_adapter.data:
                    if j.name is i.text:
                        self.list_adapter.data.remove(j)

class ViewWindow(FloatLayout):
    pass

class ViewPreProcess(BoxLayout):
    pass

class RootWindow(TabbedPanel):
    manager = ObjectProperty(None)
    def switch_to(self, header):
        # set the Screen manager to load  the appropriate screen
        # linked to the tab head instead of loading content
        self.manager.current = header.screen
        # we have to replace the functionality of the original switch_to
        self.current_tab.state = "normal"
        header.state = 'down'
        self._current_tab = header

class mainApp(App):
    source = StringProperty(None)
    def build(self):
        self.source = "./backgroundDefault.jpg"
        self.image = []
        self.texture = Texture.create()
        root = RootWindow()
        return root

    def update_list_data(self, path, filename):
        if filename:
            self.root.ids["ViewPreProcess"].ids["SelectionList"].update_list_data(path,filename)
            #Cache.remove("kv.image", self.root.ids["ViewPreProcess"].ids["Image"].source + "|False|0")
            #Cache.remove("kv.texture", self.root.ids["ViewPreProcess"].ids["Image"].source + "|False|0")
            defPath = os.path.join(path, filename[0])
            if re.search('.CR2',defPath):
                self.image = ImageRaw.ImageRaw(defPath).getndarray()
                h,l,r = self.image.shape
                self.texture = Texture.create(size=(l,h))
                self.texture.blit_buffer(pbuffer = self.image.tostring(),bufferfmt="ushort",colorfmt='rgb')
            else:
                self.texture = Image(defPath).texture


            #self.texture = Image(os.path.join(path, filename[0])).texture
            #print self.texture
            #self.root.ids["ViewPreProcess"].ids["Image"].ids["currentImage"] = Image(wTexture)
            #self.root.ids["ViewPreProcess"].ids["Image"].ids["currentImage"].source = os.path.join(path, filename[0])
            self.root.ids["ViewPreProcess"].ids["Image"].ids["currentImage"].texture = self.texture
            self.root.ids["ViewPreProcess"].ids["Image"].ids["currentImage"].size = self.texture.size
            self.root.ids["ViewPreProcess"].ids["Image"].ids["currentImage"].reload()
            print "size:"+str(self.root.ids["ViewPreProcess"].ids["Image"].ids["currentImage"].size)
            #print "Reload : "+str(self.root.ids["ViewPreProcess"].ids["Image"].ids["currentImage"].source)

    def clear(self):
        self.root.ids["ViewPreProcess"].ids["Image"].ids["currentImage"].texture = Texture.create()
        self.root.ids["ViewPreProcess"].ids["Image"].ids["currentImage"].reload()

    def preview(self, selection):
        if selection:
            self.root.ids["ViewPreProcess"].ids["Image"].source = selection[0].text
            self.root.ids["ViewPreProcess"].ids["Image"].ids["currentImage"].reload()
            #print "Reload : "+str(self.root.ids["ViewPreProcess"].source)

    def masterDark(self):
        items = self.root.ids["ViewPreProcess"].ids["SelectionList"].list_adapter.data
        self.darkList = []
        for i in items:
            print i.name
            dark = ImageRaw.ImageRaw(i.name).getndarray()
            print dark
            self.darkList.append(dark)
        self.result_dark = AstroProcess.processMasterDark(self.darkList)
        imageio.imsave('../../Pictures_test/MasterDark.tiff', self.result_dark)
        del self.darkList

if __name__ == '__main__':
    mainApp().run()
