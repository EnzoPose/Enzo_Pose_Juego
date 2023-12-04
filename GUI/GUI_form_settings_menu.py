import pygame as pg
from pygame.locals import *
from GUI.GUI_form import Form
from GUI.UI.GUI_slider import Slider
from GUI.UI.GUI_label import Label
from GUI.UI.GUI_button import Button
from GUI.UI.GUI_button_image import Button_Image


class Form_settings_menu(Form):
    def __init__(self, screen, x, y, w, h,path_image,path_bgd):
        super().__init__(screen, x, y, w, h)
        img = pg.image.load(path_image)
        img = pg.transform.scale(img,(w,h))
        self.img =img
    
        bgd_img =  pg.image.load(path_bgd)
        bgd_img = pg.transform.scale(bgd_img,(self._master.get_width(),self._master.get_height()))

        self.bgd_img = bgd_img
        self.slave = img
        

        # if pg.mixer.music.get_busy():
        #     self.is_recording = True
        #     self.btn_play = Button()
        # else:
        #     self.is_recording = False
        #     self.btn_play =  Button()
        # self.volume = pg.mixer.music.get_volume()

        self.volume_slider = Slider(self.slave, x, y, 100, 200, 300, 10, self.volume, "Black", "White")
        self.btn_home = Button_Image(self.slave,x,y,50,100,80,80,onclick= self.button_home,onclick_param="lalala",path_image="GUI\Recursos\home.png")
        # self.volume_label = Label()
        # self.btn_return = Button_Image()

        self.widget_list.append(self.volume_slider)
        self.widget_list.append(self.btn_home)

    def button_home(self,txt):
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
        # self.volume_label.set_text(f"{round(self.volume * 100)}%")
        pg.mixer.music.set_volume(self.volume)

    def update(self,event_list):
        self._master.blit(self.bgd_img,(0,0))
        if self.verify_dialog_result():
            self.render()
            for widget in self.widget_list:
                widget.update(event_list)
            self.draw()
            self.update_volume()
        else:
            self.hijo.update(event_list)