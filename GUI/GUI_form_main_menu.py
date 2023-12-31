import pygame as pg
from pygame.locals import *
from GUI.UI.GUI_button_image import Button_Image
from GUI.UI.GUI_label import Label
from GUI.UI.GUI_textbox import TextBox
from GUI.GUI_form import Form
from GUI.GUI_form_play_menu import Form_play
from GUI.GUI_form_score_menu import *
from GUI.GUI_form_settings_menu import Form_settings_menu
from GUI.GUI_form_controls import Form_controls
from GUI.GUI_form_score_menu import Form_Score
from db_functions import insert_row_into_db,exist_name_in_db,obtain_score_with_id,get_player_id

from models.constantes import ANCHO_VENTANA,ALTO_VENTANA
from models.values import Values


class Main_form(Form):
    def __init__(self, screen, x, y, w, h, path_image, bgd_image,values:Values):
        super().__init__(screen, x, y, w, h)
        img = pg.image.load(path_image)
        img = pg.transform.scale(img,(w,h))
        bgd = pg.image.load(bgd_image)
        self.values = values
        pg.mixer.music.load(self.values.menu_music)
        pg.mixer.music.set_volume(values.music_volume)
        pg.mixer.music.play()

        self.menu_bgd = pg.transform.scale(bgd,(ANCHO_VENTANA,ALTO_VENTANA))
        self.slave = img
        
        self.flag_play = True
        self.player_data = {}



        self.title = Label(self.slave,40,12,720,60,"Main menu","consolas",50,"White","GUI\Recursos\Table.png")
        self.name_label = Label(self.slave,40,130,200,60,"Name","consolas",50,"White","GUI\Recursos\Table.png")

        self.bttn_play = Button_Image(self.slave, x, y, 40, 220, 720, 80, "GUI\Recursos\Play.png",self.button_play,"lalala")
        self.bttn_settings = Button_Image(self.slave, x, y, 40, 320, 720, 80, "GUI\Recursos\settings_bar.png", self.button_settings,"lalala")
        self.bttn_controls = Button_Image(self.slave, x, y, 40, 420, 720, 80, "GUI\Recursos\controls_button.png", self.button_controls,"lalala")
        self.bttn_ranking = Button_Image(self.slave, x, y, 600,120,80,80,r"GUI\Recursos\ranking_button.png",self.button_ranking,"lalala")
        self.txt_box = TextBox(self.slave,x,y,270,145,200,30,"Gray", "White", "Black", "Blue",2,"Consolas",15,"Black")

        
        self.widget_list.append(self.title)
        self.widget_list.append(self.bttn_play)
        self.widget_list.append(self.bttn_settings)
        self.widget_list.append(self.bttn_controls)
        self.widget_list.append(self.txt_box)
        self.widget_list.append(self.name_label)
        self.widget_list.append(self.bttn_ranking)

    
    def button_play(self,txt):
        play_form = Form_play(self._master,250,100,800,600,"GUI\Recursos\Window.png","GUI\Recursos\AdobeStock_81556974.webp",self.values)
        self.values.player_name = self.txt_box._text
        
        if exist_name_in_db(self.values.player_name) > 0:
            print(self.values.player_score)
            self.values.create_player_score_dict(obtain_score_with_id(get_player_id(self.values.player_name)))
        else:
            self.values.create_player_score_dict()
            insert_row_into_db(self.values.player_name,self.values.obtain_total_score())
        self.show_dialog(play_form)


    def button_settings(self,txt):
        settings_form = Form_settings_menu(self._master,250,100,800,600,"GUI\Recursos\Window.png","GUI\Recursos\AdobeStock_81556974.webp",self.values)
        self.show_dialog(settings_form)

    def button_controls(self,txt):
        controls_form = Form_controls(self._master,250,100,800,600,"GUI\Recursos\controls_menu.png","GUI\Recursos\AdobeStock_81556974.webp")
        self.show_dialog(controls_form)
    
    def button_ranking(self,txt):
        ranking_form = Form_Score(self._master,250,100,800,600,"GUI\Recursos\Window.png","GUI\Recursos\AdobeStock_81556974.webp")
        self.show_dialog(ranking_form)

    def update(self, event_list):
        self._master.blit(self.menu_bgd,(0,0))
        if self.verify_dialog_result():
            if self.active:
                self.draw()
                self.render()
                for widget in self.widget_list:
                    widget.update(event_list)
        else:
            self.hijo.update(event_list)
