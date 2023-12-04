from GUI.GUI_form import Form
from GUI.GUI_form_level_container import Form_level_container
from GUI.UI.GUI_button_image import Button_Image
from GUI.UI.GUI_label import Label
from models.stage.stage import Stage
from models.constantes import ANCHO_VENTANA,ALTO_VENTANA

import pygame as pg


class Form_play(Form):
    def __init__(self, screen, x, y, w, h,path_image,path_bgd):
        super().__init__(screen, x, y, w, h)
        self.level_manager = ["Stage_1", "Stage_2", "Stage_3"]
        img = pg.image.load(path_image)
        img = pg.transform.scale(img,(w,h))
        
        bgd_img =  pg.image.load(path_bgd)
        bgd_img = pg.transform.scale(bgd_img,(self._master.get_width(),self._master.get_height()))
        self.bgd_img = bgd_img
        self.slave = img
        self.score = 0
        self.player_data = {}

        self.btn_stage_1 = Button_Image(self.slave,x,y,150,100,500,100,onclick= self.run_stage,onclick_param=self.level_manager[0],path_image="GUI\Recursos\level_1.png")
        self.btn_stage_2 = Button_Image(self.slave,x,y,150,250,500,100,onclick= self.run_stage,onclick_param=self.level_manager[1],path_image="GUI\Recursos\level_2.png")
        self.btn_stage_3 = Button_Image(self.slave,x,y,150,400,500,100,onclick= self.run_stage,onclick_param=self.level_manager[2],path_image="GUI\Recursos\level_3.png")
        self.btn_home = Button_Image(self.slave,x,y,50,100,80,80,onclick= self.button_home,onclick_param="lalala",path_image="GUI\Recursos\home.png")
        self.title = Label(self.slave,40,12,720,60,"Level selector","consolas",50,"White","GUI\Recursos\Table.png")

        self.widget_list.append(self.btn_stage_1)
        self.widget_list.append(self.btn_stage_2)
        self.widget_list.append(self.btn_stage_3)
        self.widget_list.append(self.btn_home)
        self.widget_list.append(self.title)

    def button_home(self,txt):
        self.end_dialog()

    def run_stage(self,lvl_index):
        stage = Stage(self._master,ANCHO_VENTANA,ALTO_VENTANA,lvl_index)
        form_level_container = Form_level_container(self._master,stage)
        self.show_dialog(form_level_container)
    
    def update(self,event_list):
        self._master.blit(self.bgd_img,(0,0))
        if self.verify_dialog_result():
            for widget in self.widget_list:
                widget.update(event_list)
            self.draw()
        else:
            self.hijo.update(event_list)