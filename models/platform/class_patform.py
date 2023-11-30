import pygame
from models.object_game.Class_object import Object

class Platform(Object):
    def __init__(self, surface: pygame.Surface, initial_position: tuple, actions: dict, rect_diference: int, size: tuple):
        self.surface = pygame.image.load(surface)
        super().__init__(self.surface, initial_position, actions, rect_diference, size)

        self.rect_for_collide_enemy_r = pygame.rect.Rect(self.colliders["main"].right,self.colliders["main"].top - 20,10,20)
        self.rect_for_collide_enemy_l = pygame.rect.Rect(self.colliders["main"].left - 10, self.colliders["main"].top -20,10,20)

    def update(self,screen):
        super().update(screen)