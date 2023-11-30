import pygame
from models.constantes import ANCHO_VENTANA
from models.Items.class_item import Item
from models.platform.class_patform import Platform
# from models.Enemy.class_enemy import Enemy
# from models.player.class_player import Player

class Projectile(Item):
    def __init__(self, surface: pygame.Surface, initial_position: tuple, actions: dict, rect_diference: int, size: tuple,damage):
        super().__init__(surface, initial_position, actions, 0, size)
        self.speed = 0
        self.damage = damage

    def check_collide(self,platform_list,projectile_list,enemy_list):
        object_list = []
        for platform in platform_list:
            object_list.append(platform)

        for enemy in enemy_list:
            object_list.append(enemy)

        for object in object_list:
            if self.colliders["main"].colliderect(object.colliders["main"]):
                self.kill(projectile_list)
                if type(object) != Platform:
                    object.life -= self.damage

    def update(self, screen,platform_list,projectile_list,enemy_list):
        self.rect.x += self.speed
        self.check_collide(platform_list,projectile_list,enemy_list)

        if self.rect.x > ANCHO_VENTANA or self.rect.x < 0:
            self.set_colition(True)
        super().update(screen)

    # def check_collide(self,platform_list,projectile_list,enemy_list):
    #     rect_list = []
    #     for platform in platform_list:
    #         rect_list.append(platform.colliders["main"])

    #     for enemy in enemy_list:
    #         rect_list.append(enemy.colliders["main"])