from GUI.GUI_form import Form
from GUI.UI.GUI_label import Label
from GUI.UI.GUI_button_image import Button_Image 
import pygame as pg
from db_functions import get_top_3_players

class Form_Score(Form):
    def __init__(self, screen, x, y, w, h,path_image, bgd_image):
        super().__init__(screen, x, y, w, h)
        img = pg.image.load(path_image)
        img = pg.transform.scale(img,(w,h))
        self.img = img

        bgd_img =  pg.image.load(bgd_image)
        bgd_img = pg.transform.scale(bgd_img,(self._master.get_width(),self._master.get_height()))
        self.bgd_img = bgd_img
        self.slave = img

        self.top_3_players = get_top_3_players()
        self.name_player_1 = Label(self.slave,50,200,350,100,f"{self.top_3_players[0][0]}","consolas",25,"White","GUI\Recursos\Table.png")
        self.score_player_1 = Label(self.slave,400,200,350,100,f"{self.top_3_players[0][1]}","consolas",25,"White","GUI\Recursos\Table.png")
        self.name_player_2 = Label(self.slave,50,320,350,100,f"{self.top_3_players[1][0]}","consolas",25,"White","GUI\Recursos\Table.png")
        self.score_player_2 = Label(self.slave,400,320,350,100,f"{self.top_3_players[1][1]}","consolas",25,"White","GUI\Recursos\Table.png")
        self.name_player_3 = Label(self.slave,50,440,350,100,f"{self.top_3_players[2][0]}","consolas",25,"White","GUI\Recursos\Table.png")
        self.score_player_3 = Label(self.slave,400,440,350,100,f"{self.top_3_players[2][1]}","consolas",25,"White","GUI\Recursos\Table.png")
        self.ranking_label = Label(self.slave,225,90,350,100,"Ranking","consolas",25,"White","GUI\Recursos\Table.png")
        self.btn_home = Button_Image(self.slave,x,y,600,120,80,80,onclick= self.button_home,onclick_param="lalala",path_image="GUI\Recursos\home.png")

        self.widget_list.append(self.name_player_1)
        self.widget_list.append(self.score_player_1)
        self.widget_list.append(self.name_player_2)
        self.widget_list.append(self.score_player_2)
        self.widget_list.append(self.name_player_3)
        self.widget_list.append(self.score_player_3)        
        self.widget_list.append(self.ranking_label)
        self.widget_list.append(self.btn_home)

    def button_home(self,txt):
        self.end_dialog()

    def update(self,event_list):
        self._master.blit(self.bgd_img,(0,0))
        if self.verify_dialog_result():
            for widget in self.widget_list:
                widget.update(event_list)
            self.draw()
        else:
            self.hijo.update(event_list)