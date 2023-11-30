import json
import pygame

from models.player.class_player import Player
from constantes import ANCHO_VENTANA,ALTO_VENTANA,FPS

class Game:
    def __init__(self) -> None:
        self.executing = True
        self.surface = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
        pygame.init()
        self.actual_stage_number = 1
        self.clock = pygame.time.Clock()
        self.actual_stage = None
        self.initial_player_config = self.__get_configs().get("player")

    def __get_configs(self) -> dict:
        try:
            with open('./configs/config.json', 'r') as configs:
                return json.load(configs)[f'stage_{self.__actual_stage_number}']
        except Exception as e:
            pass
    
    def run_game():
        player_megaman = Player()