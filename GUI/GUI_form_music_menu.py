import pygame as pg
from pygame.locals import *
from GUI.GUI_form import Form
from GUI.UI.GUI_slider import Slider
from GUI.UI.GUI_label import Label
from GUI.UI.GUI_button import Button
from GUI.UI.GUI_button_image import Button_Image

class Form_music_menu(Form):
    def __init__(self, screen, x, y, w, h,path_image):
        super().__init__(screen, x, y, w, h)
        img = pg.image.load(path_image)
        img = pg.transform.scale(img,(w,h))
        self.img = img
        self.slave = img.copy()

        if pg.mixer.music.get_busy():
            self.is_recording = True
            self.btn_play = Button()
        else:
            self.is_recording = False
            self.btn_play =  Button()
        self.volume = pg.mixer.music.get_volume()

        self.volume_slider = Slider()
        self.volume_label = Label()
        self.btn_return = Button_Image()
        self.end_dialog()
        self.widget_list = [self.btn_play,self.volume_label,self.volume_slider,self.btn_return]

    def button_home(self):
        self.end_dialog()
    
    def button_play(self):
        if self.is_recording:
            pg.mixer.music.pause()
            self.btn_play._color_background = "Red"
            self._estado = "Stop"
            self.btn_play.set_text(self._estado)
        else:
            pg.mixer.music.unpause()
            self.btn_play._color_background = "Green"
            self._estado = "Reproduciendo"
            self.btn_play.set_text(self._estado)
        
        self.is_recording = not self.is_recording
    
    def render(self):
        self.slave.blit(self.img,(0,0))

    def update_volume(self):
        self.volume = self.volume_slider.value
        self.volume_label.set_text(f"{round(self.volume * 100)}%")
        pg.mixer.music.set_volume(self.volume)

    def update(self,event_list):
        if self.verify_dialog_result():
            self.render()
            for widget in self.widget_list:
                widget.update(event_list)
            self.draw()
            self.update_volume()
        else:
            self.hijo.update(event_list)