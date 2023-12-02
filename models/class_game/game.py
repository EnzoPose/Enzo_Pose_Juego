import json
import pygame
from GUI.GUI_form_main_menu import Main_form
from auxiliar.modo import *
from models.stage.stage import Stage
from models.constantes import ANCHO_VENTANA,ALTO_VENTANA,FPS

class Game:
    def __init__(self) -> None:
        self.executing = True
        pygame.init()
        self.screen_surface = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
        self.actual_stage_number = 1
        self.clock = pygame.time.Clock()
        self.actual_stage: Stage = None
        self.amount_player_score = 0
    
    def run_game(self):
        
        main_form = Main_form(self.screen_surface,250,100,800,600,"GUI\Recursos\Window.png","GUI\Recursos\AdobeStock_81556974.webp")
        while self.executing:
    

            self.clock.tick(FPS)
            # if not self.actual_stage or self.actual_stage.stage_passed():
            #     if self.actual_stage_number < 3:
            #         self.actual_stage = Stage(self.screen_surface,ANCHO_VENTANA,ALTO_VENTANA,f"Stage_{self.actual_stage_number}")
            #         self.actual_stage_number +=1


            event_list = pygame.event.get()
            for event in event_list:
                match event.type:
                    case pygame.KEYDOWN:
                        if event.key == pygame.K_TAB:
                            change_mode()
                    case pygame.QUIT:
                        self.executing = False
                        break
            

            main_form.update(event_list)
            # self.screen_surface.blit(self.actual_stage.background_img,self.actual_stage.background_img.get_rect())
            # self.actual_stage.run(get_mode())
            # self.amount_player_score += self.actual_stage.player.score
            pygame.display.update()