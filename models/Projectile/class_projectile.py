import pygame

from models.constantes import ANCHO_VENTANA
from models.Items.class_item import Item
from models.platform.class_patform import Platform


class Projectile(Item):
    def __init__(self, surface: pygame.Surface, initial_position: tuple, actions: dict, rect_diference: int, size: tuple,damage,who_created_it):
        super().__init__(surface, initial_position, actions, 0, size)
        self.speed = 0
        self.speed_y = 0
        self.damage = damage
        self.who_created_it = who_created_it

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
                    if self.who_created_it == "Player":
                        object.life -= self.damage
                    elif self.who_created_it == "Enemy" and object.is_invencible == False:
                        object.colition_time_enemy_or_trap = pygame.time.get_ticks()
                        object.is_invencible = True
                        object.life -= self.damage
                        object.hurt_sound.play()



    def update(self, screen,platform_list,projectile_list,enemy_list):
        self.rect.x += self.speed
        self.rect.y += self.speed_y
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