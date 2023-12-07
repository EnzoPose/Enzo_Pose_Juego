import pygame as pg
from models.charapter.charapter import Charapter
from models.platform.class_patform import Platform
from models.Projectile.class_projectile import Projectile
from models.constantes import ANCHO_VENTANA,ALTO_VENTANA

class Boss(Charapter):
    def __init__(self, surface: pg.Surface, initial_position: list, animations: dict, rect_diference: int, size: list, life: int, damage: int, cadence: int, damage_colition):
        super().__init__(surface, initial_position, animations, rect_diference, size, life, damage)

        self.damage_colition = damage_colition
        self.cadence = cadence
        self.last_attack = 0
        self.last_shot = 0
        self.is_doing = "walk"
        self.clock = pg.time.Clock()
        self.elapsed_time = 0
        self.interval = 2500
        self.is_jumping = True
        self.is_alive = True
        self.is_looking_player = False
        self.attack_sound = pg.mixer.Sound("assets\img\Sounds\enemy_attack.mp3")

        self.pov_rect = pg.rect.Rect(self.colliders["main"].left - 200, self.colliders["main"].top + 50, 900,self.height) if not self.is_loking_right else \
        pg.rect.Rect(self.colliders["main"].right + 200, self.colliders["main"].top + 50 , 900,self.height)

    def kill(self):
        '''
        Brief:
        Este método de clase establece el estado del jefe como no vivo.

        Parametros:
        No tiene parámetros.

        Retorno: 
        No retorna ningún valor.
        '''
        self.is_alive = False

    def check_collition_platform(self,platform_list:list[Platform]):
        '''
        Brief:
        Este método de clase verifica las colisiones del jefe con las plataformas, ajusta su comportamiento y posición en consecuencia.

        Parametros:
        platform_list: Lista de objetos de tipo Platform, que representa las plataformas en el juego.

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
        Este método de clase verifica si el jefe está mirando al jugador.

        Parametros:
        player: Objeto de tipo Player, que representa al jugador en el juego.

        Retorno: 
        No retorna ningún valor.
        '''
        if self.pov_rect.colliderect(player.colliders["main"]):
            self.is_looking_player = True
        else:
            self.is_looking_player = False

    def event_update(self):
        '''
        Brief:
        Este método de clase actualiza los eventos del jefe, determinando si debe atacar al jugador.

        Retorno: 
        No retorna ningún valor.
        '''
        if self.elapsed_time >= self.interval:
            if self.is_looking_player:
                self.is_doing = "attack"
            else:
                self.attack_sound.play()
                self.is_doing = "attack_up"
            self.elapsed_time = 0
        else:
            if self.elapsed_time <= self.interval:
                if (self.is_doing == "attack" or self.is_doing == "attack_up" ) and self.step_counter >= 6:
                    if self.is_loking_right:
                        self.is_doing = "walk"
                    else:
                        self.is_doing = "walk_l"
            

    def do_attack(self):
        '''
        Brief:
        Este método de clase realiza el ataque del jefe, creando proyectiles y reproduciendo el sonido de ataque.

        Retorno: 
        No retorna ningún valor.
        '''
        now = pg.time.get_ticks()
        if now - self.last_shot > self.cadence:
            self.create_projectile(r"assets\img\Enemy\Attack\bullet.png",(60,40),"Enemy")
            self.attack_sound.play()

            self.last_shot = now

    def event_management(self):
        '''
        Brief:
        Este método de clase administra los eventos del jefe, determinando su comportamiento según el estado actual.

        Retorno: 
        No retorna ningún valor.
        '''
        match self.is_doing:
            case "walk":
                self.speed_x = 6
                self.move_x()
                self.pov_rect.left =  self.colliders["main"].right
                self.pov_rect.top = self.colliders["main"].top
                self.animate(self.animations["walk"],1)
            case "walk_l":
                self.speed_x = -6
                self.move_x()
                self.pov_rect.right = self.colliders["main"].left
                self.pov_rect.top = self.colliders["main"].top
                self.animate(self.animations["walk_l"],1)
            case "attack":
                self.speed_x = 0
                self.do_attack()
                if self.is_loking_right:
                    self.animate(self.animations["attack"],0.3)
                else: 
                    self.animate(self.animations["attack_l"],0.3)
                # self.elapsed_time = 0
            case "attack_up":
                self.speed_x = 0
                self.projectile_rain(r"assets\img\Enemy\Attack\bullet.png",(10,10),"Enemy")
                if self.is_loking_right:
                    self.animate(self.animations["attack_up"],0.3)
                else:
                    self.animate(self.animations["attack_up_l"],0.3)
                # self.elapsed_time = 0



    def update(self,screen,platform_list,player,sound_volume):
        '''
        Brief:
        Este método de clase actualiza el estado del jefe durante el juego, gestionando su comportamiento en función de los eventos.

        Parámetros:
        - screen: Superficie de la pantalla donde se dibujará el jefe.
        - platform_list: Lista de plataformas presentes en el juego.
        - player: Lista que contiene al jugador (podría ser un solo jugador, pero la implementación original tiene player como una lista).
        - sound_volume: Volumen de los sonidos del jefe.

        Retorno: 
        No retorna ningún valor.
        '''
        self.sound_volume = sound_volume
        self.projectile_collide_sound.set_volume(self.sound_volume)
        self.attack_sound.set_volume(self.sound_volume)
        self.elapsed_time += self.clock.tick(30)
        self.gravity_fall()
        self.verify_is_looking_player(player[0])
        self.event_management()
        self.event_update()
        self.check_collition_platform(platform_list)
        super().update(screen,platform_list,player)