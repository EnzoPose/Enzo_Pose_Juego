from GUI.GUI_form import Form
from GUI.UI.GUI_button_image import Button_Image
from GUI.GUI_form_settings_menu import Form_settings_menu
from GUI.GUI_form_game_over import Form_game_over
import pygame as pg
from models.stage.stage import Stage
from models.values import Values
from models.constantes import ANCHO_VENTANA,ALTO_VENTANA

class Form_level_container(Form):
    def __init__(self, screen:pg.Surface,level:Stage,values:Values):
        super().__init__(screen,0,0,screen.get_width(), screen.get_height())
        self.font = pg.font.SysFont("consolas",30)
        self.txt_pause = self.font.render("Paused",False,"White")
        values.in_level = True
        values.is_paused = False
        values.current_level = level.stage_name
        self.values = values 


        level.screen = self.slave
        self.level = level
        self.btn_back = Button_Image(self.slave, 0, 0, 1200, 300, 50, 50, r"GUI\Recursos\home.png", self.button_back,"lalala")
        self.btn_settings = Button_Image(self.slave, 0, 0, 1200, 400, 50, 50, r"GUI\Recursos\settings.png", self.button_settings,"lalala")
        self.widget_list.append(self.btn_back)
        self.widget_list.append(self.btn_settings)
        
        self.form_game_over = Form_game_over(self._master,250,100,800,600,"GUI\Recursos\Window.png","GUI\Recursos\AdobeStock_81556974.webp")

    def button_back(self,txt):
        self.end_dialog()
    


    def button_settings(self,level):
        settings_form = Form_settings_menu(self._master,250,100,800,600,"GUI\Recursos\Window.png","GUI\Recursos\AdobeStock_81556974.webp",self.values)
        self.show_dialog(settings_form)


        

    def reset_level(self):
        self.form_game_over = Form_game_over(self._master,250,100,800,600,"GUI\Recursos\Window.png","GUI\Recursos\AdobeStock_81556974.webp")
        self.level.__init__(self.slave,ANCHO_VENTANA,ALTO_VENTANA,self.values.current_level,self.values)




    def update(self,event_list):
        if not self.values.is_paused and self.level.win == False and self.level.lost == False:
            self.level.run()

        elif self.values.is_paused:
            self.slave.blit(self.txt_pause,(600,400))
        elif self.level.lost:
            self.show_dialog(self.form_game_over)
            if self.form_game_over.reset_level:
                self.reset_level()
        elif self.level.win:
            self.txt_win = self.font.render(f"You win, your score {self.level.player.score}",False,"White")
            self.slave.blit(self.txt_win,(450,300))



        if self.verify_dialog_result():
            for widget in self.widget_list:
                widget.update(event_list)
            self.draw()
        else:
            self.hijo.update(event_list)