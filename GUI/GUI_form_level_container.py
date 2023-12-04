from GUI.GUI_form import Form
from GUI.UI.GUI_button_image import Button_Image
import pygame as pg
from models.stage.stage import Stage
class Form_level_container(Form):
    def __init__(self, screen:pg.Surface,level:Stage):
        super().__init__(screen,0,0,screen.get_width(), screen.get_height())
        level.screen = self.slave
        self.level = level

        self.btn_back = Button_Image(self.slave, 0, 0, 1200, 300, 50, 50, r"GUI\Recursos\back.png", self.button_back,"lalala")

        self.widget_list.append(self.btn_back)

    def button_back(self,txt):
        self.end_dialog()

    def update(self,event_list):

        self.level.run()
        if self.verify_dialog_result():
            for widget in self.widget_list:
                widget.update(event_list)
            self.draw()
        else:
            self.hijo.update(event_list)