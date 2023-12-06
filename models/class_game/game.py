import json
import pygame
from GUI.GUI_form_main_menu import Main_form
from auxiliar.modo import *
from models.stage.stage import Stage
from models.constantes import ANCHO_VENTANA,ALTO_VENTANA,FPS
from models.values import Values

class Game:
    def __init__(self) -> None:
        self.executing = True
        pygame.init()
        self.screen_surface = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
        self.clock = pygame.time.Clock()
    
    def run_game(self):
        
        values = Values()
        pygame.display.set_caption("Megaman Remix")
        main_form = Main_form(self.screen_surface,250,100,800,600,"GUI\Recursos\Window.png","GUI\Recursos\AdobeStock_81556974.webp",values)
        while self.executing:
            self.clock.tick(FPS)
            event_list = pygame.event.get()
            for event in event_list:
                match event.type:
                    case pygame.KEYDOWN:
                        if event.key == pygame.K_TAB:
                            change_mode()
                        elif event.key == pygame.K_p:
                            values.is_paused = not values.is_paused
                    case pygame.QUIT:
                        self.executing = False
                        break
            

            main_form.update(event_list)
            pygame.display.update()