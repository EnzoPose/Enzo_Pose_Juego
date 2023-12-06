import pygame as pg
from GUI.GUI_form import Form
from GUI.UI.GUI_button_image import Button_Image
from GUI.UI.GUI_label import Label


class Form_game_over(Form):
    def __init__(self, screen, x, y, w, h,path_img,path_bgd):
        super().__init__(screen, x, y, w, h)
        img = pg.image.load(path_img)
        img = pg.transform.scale(img,(w,h))
        self.img = img
        self.slave = img
        bgd_img =  pg.image.load(path_bgd)
        bgd_img = pg.transform.scale(bgd_img,(self._master.get_width(),self._master.get_height()))
        self.bgd_img = bgd_img
        self.reset_level = False

        self.game_over_text_label = Label(self.slave,20,10,750,70,"GAME OVER","consolas",60,"White","GUI\Recursos\Table.png")
        self.btn_play_again = Button_Image(self.slave,x,y,250,200,300,80,r"GUI\Recursos\Play_again.png",self.play_again,"lalala")
        self.widget_list.append(self.btn_play_again)
        self.widget_list.append(self.game_over_text_label)

    def play_again(self,txt):
        self.reset_level = True
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