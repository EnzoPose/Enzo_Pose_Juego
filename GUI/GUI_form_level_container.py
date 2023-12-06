from GUI.GUI_form import Form
from GUI.UI.GUI_button_image import Button_Image
from GUI.GUI_form_settings_menu import Form_settings_menu
import pygame as pg
from models.stage.stage import Stage
from models.values import Values
class Form_level_container(Form):
    def __init__(self, screen:pg.Surface,level:Stage,values:Values):
        super().__init__(screen,0,0,screen.get_width(), screen.get_height())
        self.font = pg.font.SysFont("consolas",30)
        self.txt_pause = self.font.render("Paused",False,"White")
        values.in_level = True
        values.is_paused = False
        self.values = values
        level.screen = self.slave
        self.level = level
        self.btn_back = Button_Image(self.slave, 0, 0, 1200, 300, 50, 50, r"GUI\Recursos\home.png", self.button_back,"lalala")
        self.btn_settings = Button_Image(self.slave, 0, 0, 1200, 400, 50, 50, r"GUI\Recursos\settings.png", self.button_settings,"lalala")
        self.widget_list.append(self.btn_back)
        self.widget_list.append(self.btn_settings)
        

    def button_back(self,txt):
        self.end_dialog()
    


    def button_settings(self,level):
        settings_form = Form_settings_menu(self._master,250,100,800,600,"GUI\Recursos\Window.png","GUI\Recursos\AdobeStock_81556974.webp",self.values)
        self.show_dialog(settings_form)

    def update(self,event_list):
        if not self.values.is_paused: 
            self.level.run()
        else:
            self.slave.blit(self.txt_pause,(600,400))

        if self.values.win:
            pass
        if self.values.lost:
            pass

        if self.verify_dialog_result():
            for widget in self.widget_list:
                widget.update(event_list)
            self.draw()
        else:
            self.hijo.update(event_list)