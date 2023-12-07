import pygame as pg
from models.Items.class_item import Item

class Trap(Item):
    def __init__(self, surface: pg.Surface, initial_position: tuple, actions: dict, rect_diference: int, size: tuple,damage:int):
        super().__init__(surface, initial_position, actions, rect_diference, size)

        self.damage_colition = damage

    def update(self,screen):
        '''
        Brief:
        Este método de clase actualiza el estado de la instancia de la clase, llamando al método "update" de la clase padre.
        Parametros:
        - screen: Objeto que representa la pantalla en la que se realiza la actualización.

        Retorno: 
        No retorna ningún valor.

        '''
        super().update(screen)