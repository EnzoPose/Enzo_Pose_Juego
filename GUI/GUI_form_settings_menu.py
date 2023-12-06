import pygame as pg
from pygame.locals import *
from GUI.GUI_form import Form
from GUI.UI.GUI_slider import Slider
from GUI.UI.GUI_label import Label
from GUI.UI.GUI_button import Button
from GUI.UI.GUI_button_image import Button_Image
from models.stage.stage import Stage
from models.values import Values

class Form_settings_menu(Form):
    def __init__(self, screen, x, y, w, h,path_image,path_bgd,values:Values):
        super().__init__(screen, x, y, w, h)
        img = pg.image.load(path_image)
        img = pg.transform.scale(img,(w,h))
        self.img = img
        self.values = values
        
        bgd_img =  pg.image.load(path_bgd)
        bgd_img = pg.transform.scale(bgd_img,(self._master.get_width(),self._master.get_height()))
        self.bgd_img = bgd_img
        self.slave = img
        self.pause_in_game = None

        if self.values.in_level:
            self.values.is_paused = True
            self.pause_in_game = True

        if pg.mixer.music.get_busy():
            self.is_recording = True
            self.btn_play_or_pause_music = Button(self.slave, x, y, 550, 200, 200, 50,"Green","black",self.btn_music_play_or_pause_click,"lalala","On","consolas",25,"Black")
        else:
            self.is_recording = False
            self.btn_play_or_pause_music =  Button(self.slave, x, y, 550, 200, 200, 50,"Red","black",self.btn_music_play_or_pause_click,"lalala","Off","consolas",25,"Black")


        self.music_volume_slider = Slider(self.slave, x, y, 100, 250, 300, 10, self.values.music_volume, "Black", "White")
        self.music_volume_label = Label(self.slave,430,200,100,100,"0%","consolas",25,"Black","GUI\Recursos\Table.png")
        self.music_volume_label_text = Label(self.slave,200,100,100,100,"Music","consolas",25,"Black","GUI\Recursos\Table.png")

        self.sounds_volume_slider = Slider(self.slave,x, y,100,450,300,10,self.values.sound_volume,"Black","White")
        self.sounds_volume_label = Label(self.slave,430,400,100,100,"0%","consolas",25,"Black","GUI\Recursos\Table.png")
        self.sound_volume_label_text = Label(self.slave,200,300,100,100,"Sounds","consolas",25,"Black","GUI\Recursos\Table.png")

        self.btn_home = Button_Image(self.slave,x,y,50,100,80,80,onclick= self.button_home,onclick_param="lalala",path_image="GUI\Recursos\home.png")
        # self.volume_label = Label()
        # self.btn_return = Button_Image()

        self.widget_list.append(self.music_volume_slider)
        self.widget_list.append(self.btn_home)
        self.widget_list.append(self.sounds_volume_slider)
        self.widget_list.append(self.music_volume_label)
        self.widget_list.append(self.music_volume_label_text)
        self.widget_list.append(self.sounds_volume_label)
        self.widget_list.append(self.sound_volume_label_text)
        self.widget_list.append(self.btn_play_or_pause_music)


    def btn_music_play_or_pause_click(self,txt):
        if self.is_recording:
            pg.mixer.music.pause()
            self.btn_play_or_pause_music._color_background = "Red"
            self.btn_play_or_pause_music.set_text("Off")
        else:
            pg.mixer.music.unpause()
            self.btn_play_or_pause_music._color_background = "Green"
            self.btn_play_or_pause_music.set_text("On")

        self.is_recording = not self.is_recording

    def button_home(self,txt):
        if self.pause_in_game:
            self.values.is_paused = False
        else: pass
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
    

    def update_volume(self):
        self.values.music_volume = self.music_volume_slider.value
        self.values.sound_volume= self.sounds_volume_slider.value
        self.music_volume_label.set_text(f"{round(self.values.music_volume * 100)}%")
        self.sounds_volume_label.set_text(f"{round(self.values.sound_volume * 100)}%")
        # self.volume_label.set_text(f"{round(self.volume * 100)}%")
        pg.mixer.music.set_volume(self.values.music_volume)
        
    
    def get_volume(self):
        return self.volume_sounds
    
    def render(self):
        self.slave.blit(self.img,(0,0))
        
    def update(self,event_list):
        if self.verify_dialog_result():
            self.render()
            for widget in self.widget_list:
                widget.update(event_list)
            self.draw()
            self.update_volume()
        else:
            self.hijo.update(event_list)