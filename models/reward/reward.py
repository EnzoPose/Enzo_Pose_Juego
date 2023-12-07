import pygame as pg
from models.Items.class_item import Item

class Reward(Item):
    def __init__(self, surface: pg.Surface, initial_position: tuple, actions: dict, rect_diference: int, size: tuple,score=0,health=0):
        super().__init__(surface, initial_position, actions, rect_diference, size)

        self.score = score
        self.health = health

    def update(self,screen):
        '''
        Brief:
        Este método de clase actualiza la instancia de la clase (en este contexto, una Reward del juego) en la pantalla si no ha ocurrido una colisión.
        Parametros:
        - screen: Objeto que representa la pantalla en la que se realiza la actualización.
        Retorno: 
        No retorna ningún valor.

        '''
        if not self.colition:
                super().update(screen)