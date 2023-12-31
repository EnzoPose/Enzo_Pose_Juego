import pygame as pg
from models.charapter.charapter import Charapter
from models.platform.class_patform import Platform
from models.constantes import ANCHO_VENTANA

class Enemy(Charapter):
    def __init__(self, surface: pg.surface, initial_position: list, animations: dict, rect_diference: int, size: list,life:int,damage:int,cadence:int,damage_colition):
        super().__init__(surface, initial_position, animations, rect_diference, size,life,damage)
        self.attack_sound = pg.mixer.Sound("assets\img\Sounds\enemy_attack.mp3")

        self.damage_colition = damage_colition
        self.cadence = cadence
        self.last_shot = 0
        self.is_doing = "walk"
        self.is_jumping = True
        self.is_alive = True
        self.is_looking_player = False
        self.pov_rect = pg.rect.Rect(self.colliders["main"].left - 200, self.colliders["main"].top + 50 , 500,self.height) if not self.is_loking_right else \
        pg.rect.Rect(self.colliders["main"].right + 200, self.colliders["main"].top + 50 , 500,self.height)
        
        self.sound_volume = 0.1

    def kill(self):
        '''
        Brief:
        Este método de clase establece el estado de vida del enemigo como falso.

        Parametros:
        No tiene parámetros.

        Retorno: 
        No retorna ningún valor.

        '''
        self.is_alive = False

    def check_collition_platform(self,platform_list:list[Platform]):
        '''
        Brief:
        Este método de clase verifica la colisión del enemigo con plataformas y ajusta su comportamiento en consecuencia.

        Parametros:
        - platform_list: Lista de plataformas con las que verificar la colisión.

        Retorno: 
        No retorna ningún valor.
        '''
        for platform in platform_list:
            if self.colliders["right"].colliderect(platform.colliders["left"]) or self.colliders["main"].right >= ANCHO_VENTANA \
                or self.colliders["right"].colliderect(platform.rect_for_collide_enemy_r):
                self.is_loking_right = False
                self.is_doing = "walk_l"

            elif self.colliders["left"].colliderect(platform.colliders["right"]) or self.colliders["main"].left <= 0 \
                or self.colliders["left"].colliderect(platform.rect_for_collide_enemy_l):
                self.is_loking_right = True
                self.is_doing = "walk"
            
            elif self.colliders["bottom"].colliderect(platform.colliders["top"]):
                self.is_jumping = False
                self.colliders["main"].bottom = platform.colliders["main"].top + 1
                self.colliders["left"].bottom = self.colliders["main"].bottom
                self.colliders["right"].bottom = self.colliders["main"].bottom
                self.colliders["bottom"].bottom = self.colliders["main"].bottom 
                self.colliders["top"].top = self.colliders["main"].top
                self.displacement_y = 0

    def verify_is_looking_player(self,player):
        '''
        Brief:
        Este método de clase verifica si el enemigo está mirando al jugador y ajusta su comportamiento en consecuencia.

        Parametros:
        - player: Objeto del jugador con el que verificar la orientación.

        Retorno: 
        No retorna ningún valor.

        '''
        if self.pov_rect.colliderect(player.colliders["main"]):
            self.is_looking_player = True
            self.is_doing = "attack"
        else:
            self.is_looking_player = False
            if self.is_loking_right:
                self.is_doing = "walk"
            else: self.is_doing = "walk_l"


    def do_attack(self):
        '''
        Brief:
        Este método de clase ejecuta la animación y la lógica del ataque del enemigo.

        Parametros:
        No tiene parámetros.

        Retorno: 
        No retorna ningún valor.
        '''
        now = pg.time.get_ticks()
        if self.is_loking_right:
            self.animate(self.animations["attack"],0.8)
        else:
            self.animate(self.animations["attack_l"],0.8)
        if now -self.last_shot > self.cadence:
            self.create_projectile(r"assets\img\Enemy\Attack\bullet.png",(60,40),"Enemy")
            self.attack_sound.play()
            self.last_shot = now

    def event_management(self):
        '''
        Brief:
        Este método de clase gestiona los eventos del enemigo según su estado actual.

        Parametros:
        No tiene parámetros.

        Retorno: 
        No retorna ningún valor.
        '''

        match self.is_doing:
            case "walk":
                self.speed_x = 3
                self.move_x()
                self.pov_rect.left =  self.colliders["main"].right
                self.pov_rect.top = self.colliders["main"].top
                self.animate(self.animations["walk"],1)
            case "walk_l":
                self.speed_x = -3
                self.move_x()
                self.pov_rect.right = self.colliders["main"].left
                self.pov_rect.top = self.colliders["main"].top
                self.animate(self.animations["walk_l"],1)
            case "attack":
                if self.is_looking_player:
                    self.speed_x = 0
                    self.do_attack()


    def update(self,screen,platform_list,enemy_list,sound_volume):
        '''
        Brief:
        Este método de clase actualiza el estado del enemigo, gestionando la lógica de movimiento, orientación y eventos.

        Parametros:
        - screen: Superficie de pantalla donde se realiza la actualización.
        - platform_list: Lista de plataformas para verificar colisiones.
        - enemy_list: Player en formato lista para la gestión de eventos.
        - sound_volume: Volumen del sonido para ajustar efectos de sonido.

        Retorno: 
        No retorna ningún valor.
        '''
        self.sound_volume = sound_volume
        self.projectile_collide_sound.set_volume(self.sound_volume)
        self.attack_sound.set_volume(self.sound_volume)
        self.gravity_fall()
        self.verify_is_looking_player(enemy_list[0])
        self.event_management()
        self.check_collition_platform(platform_list)
        super().update(screen,platform_list,enemy_list)