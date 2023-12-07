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
        '''
        Brief:
        Este método de clase verifica si la instancia de la clase "Projectile" ha colisionado con elementos de la lista proporcionada de plataformas, proyectiles y enemigos. Realiza acciones específicas dependiendo del tipo de colisión.

        Parametros:
        - platform_list: Lista de instancias de la clase "Platform".
        - projectile_list: Lista de instancias de la clase "Projectile".
        - enemy_list: Lista de instancias de la clase "Enemy".

        Retorno: 
        No retorna ningún valor.
        '''
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
        '''
        Brief:
        Este método de clase actualiza la instancia de la clase "Projectile" en la pantalla, moviéndola según su velocidad y verificando colisiones con elementos de las listas proporcionadas de plataformas, proyectiles y enemigos. Además, se verifica si la instancia ha salido de los límites de la pantalla.

        Parametros:
        - screen: Objeto que representa la pantalla en la que se realiza la actualización.
        - platform_list: Lista de instancias de la clase "Platform".
        - projectile_list: Lista de instancias de la clase "Projectile".
        - enemy_list: Lista de instancias de la clase "Enemy".

        Retorno: 
        No retorna ningún valor.
        '''
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