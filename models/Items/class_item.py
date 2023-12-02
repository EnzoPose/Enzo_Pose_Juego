import pygame
from models.object_game.Class_object import Object

class Item(Object):
    def __init__(self, surface: pygame.Surface, initial_position: tuple, actions: dict, rect_diference: int, size: tuple):
        super().__init__(surface, initial_position, actions, rect_diference, size)
        self.colition = False

    def set_colition(self, flag:bool):
        self.colition = flag

    def get_colition(self):
        return self.colition

    def kill(self,items_list):
        self.colition = True

        if self in items_list:
            items_list.remove(self)

    def update(self,screen):
        if not self.colition:
            super().update(screen)