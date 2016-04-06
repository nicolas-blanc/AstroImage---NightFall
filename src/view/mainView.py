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
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListView
from kivy.uix.listview import ListItemButton
from kivy.adapters.models import SelectableDataItem
from kivy.cache import Cache
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.filechooser import FileSystemLocal
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from skimage import data, io

import threading
import skimage
import io as iolib
import os.path
import sys
import re
import imageio

Builder.load_file('ViewWindow.kv')

class ViewExplorer(BoxLayout):
    pass

class ViewImage(BoxLayout):
    pass

class CustomDropDown(DropDown):
    pass

class ViewMenu(BoxLayout):
    #editButton = ObjectProperty(None)
    #stack = ObjectProperty(None)
    #def __init__(self, *args, **kwargs):
    #    super(BoxLayout, self).__init__(*args, **kwargs)
    #    #Clock.schedule_interval(self.update, 1./60)
    #    self.editButton = Button(text="Edit",size_hint=(0.3,0.1),id="editButton")
    #    self.editButton.bind(on_release=self.showProcess)
    #    print self.Stack
    #    self.ids.Stack.add_widget(self.editButton)
    #    self.refs = [self.editButton.__self__]
    pass

    #def showProcess(self):
    #    self.ids["DropDown"].open(self.editButton)


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
        self.selection = []
        data_items = []
        list_item_args_converter = lambda row_index, obj: {'text': obj.name,'size_hint_y': None,'height': 25}
        self.list_adapter = ListAdapter(data=data_items,
                    args_converter=list_item_args_converter,
                    selection_mode='single',
                    propagate_selection_to_data=True,
                    allow_empty_selection=True,
                    cls=ListItemButton)

        self.list_adapter.bind(on_selection_change=self.reload)

    def update_list_data(self, path, filename):
            items = self.list_adapter.data
            item = DataItem(name=filename[0])
            items.append(item)

    def clear(self):
        print "Clear"
        self.list_adapter.data = []

    def remove(self, path):
        for j in self.list_adapter.data:
            if j.name is path:
                self.list_adapter.data.remove(j)

    def reload(self, *args):
        self.selection = []
        for i in self.list_adapter.selection:
            self.selection.append(i)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.push()
            touch.apply_transform_2d(self.to_local)
            ret = super(ViewSelectionList, self).on_touch_down(touch)
            touch.pop()
            print self.parent
            return ret


class ViewFileChooser(BoxLayout):
    pass

class ViewWindow(FloatLayout):
    pass

class ViewPreProcess(BoxLayout):
    pass

class RootWindow(BoxLayout):
    manager = ObjectProperty(None)
    def switch_to(self, header):
        self.manager.current = "MainView"


class DataImage():
    def __init__(self, path, image, **kwargs):
        self.path = path
        self.image = image

class mainApp(App):
    source = StringProperty(None)
    processName = StringProperty(None)
    result = ObjectProperty(None)
    threadProcess = ObjectProperty(None)
    popup = ObjectProperty(None)
    def build(self):
        self.source = "./backgroundDefault.jpg"
        self.pictureList = []
        self.texture = Texture.create()
        self.texture.wrap="clamp_to_edge"
        self.customDropDown = CustomDropDown()
        root = RootWindow()
        return root

    def update_list_data(self, path, filename):
        exist = False
        if filename:
            print "Path : " + str(path) + " | Filename " + str(filename[0])
            for i in self.root.ids["ViewPreProcess"].ids["SelectionList"].list_adapter.data:
                if filename is i.name:
                    print "Filename "+str(Filename)+" already exist\n"
                    exist = True
            if not exist:
                self.root.ids["ViewPreProcess"].ids["SelectionList"].update_list_data(path,filename)
                defPath = os.path.join(path, filename[0])
                if re.search('.CR2',defPath):
                    image = ImageRaw.ImageRaw(defPath).getndarray()
                    #print "Append \n"
                    self.pictureList.append(DataImage(path=filename[0],image=image))
                    h,l,r = image.shape
                    self.texture = Texture.create(size=(l,h))
                    self.texture.blit_buffer(pbuffer = image.tostring(),bufferfmt="ushort",colorfmt='rgb')
                elif re.search('[.jpg|.png|.gif|.tiff]',defPath):
                    image = io.imread(defPath)
                    self.pictureList.append(DataImage(path=filename[0],image=image))
                    h,l,r = image.shape
                    self.texture = Texture.create(size=(l,h))
                    self.texture.blit_buffer(pbuffer = image.tostring(),bufferfmt="ubyte",colorfmt='rgb')
                    self.texture.flip_vertical()


                self.root.ids["ViewPreProcess"].ids["Image"].ids["currentImage"].texture = self.texture
                self.root.ids["ViewPreProcess"].ids["Image"].ids["currentImage"].size = self.texture.size
                self.root.ids["ViewPreProcess"].ids["Image"].ids["currentImage"].reload()


    def clear(self):
        self.root.ids["ViewPreProcess"].ids["Image"].ids["currentImage"].texture = Texture.create()
        self.root.ids["ViewPreProcess"].ids["Image"].ids["currentImage"].reload()
        self.pictureList = []
        self.root.ids["ViewWindow"].ids["Image"].ids["currentImage"].texture = Texture.create()
        self.root.ids["ViewWindow"].ids["Image"].ids["currentImage"].reload()

    def preview(self):
        #self.root.ids["ViewPreProcess"].ids["SelectionList"].list_adapter.on_selection_change()
        select = self.root.ids["ViewPreProcess"].ids["SelectionList"].list_adapter.selection
        if select:
            print "Selection change to "+str(select[0].text)
            if re.search('.CR2',select[0].text):
                for i in self.pictureList:
                    if i.path is select[0].text:
                        print "Find Image\n"
                        h,l,r = i.image.shape
                        self.texture = Texture.create(size=(l,h))
                        self.texture.blit_buffer(pbuffer = i.image.tostring(),bufferfmt="ushort",colorfmt='rgb')
            else:
                if self.root.ids["ViewPreProcess"].ids["Explorer"].ids["icon_view_tab"].show_hidden:
                    path = self.root.ids["ViewPreProcess"].ids["Explorer"].ids["list_view_tab"].path
                else:
                    path = self.root.ids["ViewPreProcess"].ids["Explorer"].ids["icon_view_tab"].path
                self.texture = Image(source=os.path.join(path, select[0].text)).texture

            self.root.ids["ViewPreProcess"].ids["Image"].ids["currentImage"].texture = self.texture
            self.root.ids["ViewPreProcess"].ids["Image"].ids["currentImage"].reload()
        else:
            self.root.ids["ViewPreProcess"].ids["Image"].ids["currentImage"].texture = Texture.create()
            self.root.ids["ViewPreProcess"].ids["Image"].ids["currentImage"].reload()

    def remove(self):
        select = self.root.ids["ViewPreProcess"].ids["SelectionList"].list_adapter.selection
        if select:
            if re.search('.CR2',select[0].text):
                for i in self.pictureList:
                    if i.path is select[0].text:
                        print "Remove "+str(i.path)
                        self.pictureList.remove(i)
            self.root.ids["ViewPreProcess"].ids["SelectionList"].remove(select[0].text)

    def startProcess(self):
        self.threadProcess = threading.Thread(target=self.process, args=())
        self.threadProcess.start()
        self.popup = Popup(title='Render State', content=Label(text='Render in progress. It may take more than a minute'),
              auto_dismiss=False)
        self.popup.open()
        self.count = 0
        Clock.schedule_interval(self.updatePopup, 0.5)

    def updatePopup(self,dt):
        if self.threadProcess.isAlive():
            if self.count == 0:
                self.popup.content = Label(text='Render in progress. It may take more than a minute.')
            if self.count == 1:
                self.popup.content = Label(text='Render in progress. It may take more than a minute..')
            if self.count == 2:
                self.popup.content = Label(text='Render in progress. It may take more than a minute...')
            self.count = self.count+1
            if self.count == 3 :
                self.count = 0
        else:
            self.popup.dismiss()
            Clock.unschedule(self.updatePopup)


    def process(self):
        if len(self.pictureList) > 1:
            dataList = []
            for i in self.pictureList:
                dataList.append(i.image)
            print "SizeData : " + str(len(dataList))
            if self.processName is "MasterDark":
                print "processMasterDark"
                self.result = AstroProcess.processMasterDark(dataList)
                imageio.imsave('../../Pictures_test/MasterDark.tiff', self.result)
            elif self.processName is "MasterFlat":
                print "processMasterFlat"
                self.result = AstroProcess.processMasterFlat(dataList)
                imageio.imsave('../../Pictures_test/MasterFlat.tiff', self.result,'../../Pictures_test/MasterDark.tiff')
            elif self.processName is "MasterBias":
                print "processMasterBias"
                self.result = AstroProcess.processMasterBias(dataList)
                imageio.imsave('../../Pictures_test/MasterFlat.tiff', self.result)
            elif self.processName is "Registration":
                print "Registration"



            self.root.manager.current = 'MainView'
            h,l,r = self.result.shape
            self.texture = Texture.create(size=(l,h))
            self.texture.blit_buffer(pbuffer = self.result.tostring(),bufferfmt="ushort",colorfmt='rgb')
            self.root.ids["ViewWindow"].ids["Image"].ids["currentImage"].texture = self.texture
            self.root.ids["ViewWindow"].ids["Image"].ids["currentImage"].reload()
            del self.pictureList
            self.clear()
        elif len(self.pictureList) == 1:
            if self.processName is "medianFilter":
                print "medianFilter"
                self.result = TreatmentProcess.medianFilter(self.pictureList[0].image)
                print self.result
            elif self.processName is "logCorrect":
                print "logCorrect"
                self.result = TreatmentProcess.logCorrect(self.pictureList[0].image)
            elif self.processName is "gammaCorrect":
                print "gammaCorrect"
                self.result = TreatmentProcess.gammaCorrect(self.pictureList[0].image)
            elif self.processName is "luminosityCorrect":
                print "luminosityCorrect"
                self.result = TreatmentProcess.luminosityCorrect(self.pictureList[0].image)
            elif self.processName is "saturationCorrect":
                print "saturationCorrect"
                self.result = TreatmentProcess.saturationCorrect(self.pictureList[0].image)
            elif self.processName is "deletionGreenDominant":
                print "deletionGreenDominant"
                self.result = TreatmentProcess.deletionGreenDominant(self.pictureList[0].image)

            self.root.manager.current = 'MainView'

            h,l,r = self.result.shape
            self.texture = Texture.create(size=(l,h))
            self.texture.blit_buffer(pbuffer = self.result.tostring(),bufferfmt="ubyte",colorfmt='rgb')
            self.root.ids["ViewWindow"].ids["Image"].ids["currentImage"].texture = self.texture
            self.root.ids["ViewWindow"].ids["Image"].ids["currentImage"].reload()

        else:
            print "No enought pictures\n"

    def loadFile(self):
        if self.root.ids["ViewFileChooser"].ids["Explorer"].ids["icon_view_tab"].show_hidden:
            path = self.root.ids["ViewFileChooser"].ids["Explorer"].ids["list_view_tab"].path
            selection = self.root.ids["ViewFileChooser"].ids["Explorer"].ids["list_view_tab"].selection
        else:
            path = self.root.ids["ViewFileChooser"].ids["Explorer"].ids["icon_view_tab"].path
            selection = self.root.ids["ViewFileChooser"].ids["Explorer"].ids["icon_view_tab"].selection
        if selection:
            self.root.manager.current = 'MainView'
            di = self.pictureList[len(self.pictureList)-1]
            self.pictureList = []
            self.pictureList.append(di)

            self.root.ids["ViewWindow"].ids["Image"].ids["currentImage"].texture = self.texture
            self.root.ids["ViewWindow"].ids["Image"].ids["currentImage"].reload()
        else:
            print "No picture selected\n"

    def findFile(self):
        if self.root.ids["ViewPreProcess"].ids["Explorer"].ids["icon_view_tab"].show_hidden:
            path = self.root.ids["ViewPreProcess"].ids["Explorer"].ids["list_view_tab"].path
        else:
            path = self.root.ids["ViewPreProcess"].ids["Explorer"].ids["icon_view_tab"].path
        file_system = FileSystemLocal()
        print "Path : " + str(path)
        for i in file_system.listdir(path):
            if re.search(".CR2",i):
                print "I : " + str(i)
                filename = []
                filename.append(i)
                self.update_list_data(path,filename)

    def showProcess(self):
        self.customDropDown.open(self.root.ids["ViewWindow"].ids["Menu"].ids["editbutton"])

    def saveFile(self):
        if not self.result == None:
            imageio.imsave('../../Pictures_test/'+'render.tiff', self.result)
            print "Save !"

if __name__ == '__main__':

    path1 = '../image/'
    sys.path.append(path1)
    import ImageRaw
    import ImageFitsColor

    path1 = '../process/'
    sys.path.append(path1)
    import AstroProcess
    import TreatmentProcess


    mainApp().run()
