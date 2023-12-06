from GUI.GUI_form import Form
from GUI.UI.GUI_button_image import Button_Image
import pygame as pg
class Form_controls(Form):
    def __init__(self, screen, x, y, w,h,path_image,path_bgd):
        super().__init__(screen, x, y, w, h)
        img = pg.image.load(path_image)
        img = pg.transform.scale(img,(w,h))
        self.img = img
        bgd_img =  pg.image.load(path_bgd)
        bgd_img = pg.transform.scale(bgd_img,(self._master.get_width(),self._master.get_height()))
        self.bgd_img = bgd_img

        self.slave = img

        self.btn_home = Button_Image(self.slave,x,y,600,120,80,80,onclick= self.button_home,onclick_param="lalala",path_image="GUI\Recursos\home.png")

        self.widget_list.append(self.btn_home)

    def button_home(self,txt):
        self.end_dialog()


    def render(self):
        self.slave.blit(self.img,(0,0))
        
    def update(self,event_list):
        self._master.blit(self.bgd_img,(0,0))
        if self.verify_dialog_result():
            self.render()
            for widget in self.widget_list:
                widget.update(event_list)
            self.draw()
        else:
            self.hijo.update(event_list)