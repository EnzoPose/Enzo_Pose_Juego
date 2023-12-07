import pygame
from models.object_game.Class_object import Object

class Item(Object):
    def __init__(self, surface: pygame.Surface, initial_position: tuple, actions: dict, rect_diference: int, size: tuple):
        super().__init__(surface, initial_position, actions, rect_diference, size)
        self.colition = False

    def set_colition(self, flag:bool):
        '''
        Brief:
        Este método de clase establece el estado de colisión del objeto.

        Parametros:
        - flag: Valor booleano que indica si el objeto está en colisión o no.

        Retorno: 
        No retorna ningún valor.
        '''
        self.colition = flag

    def get_colition(self):
        '''
        Brief:
        Este método de clase obtiene el estado de colisión del objeto.

        Parametros:
        No tiene parámetros.

        Retorno: 
        Valor booleano que indica si el objeto está en colisión o no.

        '''
        return self.colition

    def kill(self,items_list):
        '''
        Brief:
        Este método de clase realiza la eliminación del objeto de una lista y establece su estado de colisión.

        Parametros:
        - items_list: Lista que contiene el objeto a eliminar.

        Retorno: 
        No retorna ningún valor.

        '''
        self.colition = True

        if self in items_list:
            items_list.remove(self)

    def update(self,screen):
        '''
        Brief:
        Este método de clase actualiza la representación gráfica del objeto en la pantalla llamando al método de la clase Object.
        Parametros:
        - screen: Superficie de la pantalla.

        Retorno: 
        No retorna ningún valor.
        '''
        super().update(screen)