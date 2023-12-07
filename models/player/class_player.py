import pygame as pg
import random
from models.charapter.charapter import Charapter
from models.platform.class_patform import Platform
from models.reward.reward import Reward
from models.trap.trap import Trap
from models.constantes import ANCHO_VENTANA,ALTO_VENTANA

class Player(Charapter):
    def __init__(self, surface: pg.surface, initial_position: tuple, animations: dict, rect_diference: int,size:tuple,life:int,damage:int):
        super().__init__(surface, initial_position, animations, rect_diference,size,life,damage)
    
        self.is_invulnerable = False
        self.is_doing = None
        self.last_shot = 0
        self.score = 0
        
        self.is_invencible = False
        self.colition_time_enemy_or_trap = 0
        
        self.attack_sound = pg.mixer.Sound("assets\img\Sounds\player_attack.mp3")
        self.collect_coin_sound = pg.mixer.Sound("assets\img\Sounds\collect_coin.mp3")
        self.jump_sound = pg.mixer.Sound("assets\img\Sounds\jump.mp3")
        self.hurt_sound = pg.mixer.Sound("assets\img\Sounds\hurt.mp3")
        


    def verify_player_events(self):
        '''
        Brief:
        Este método de clase verifica los eventos del jugador (teclas presionadas) y actualiza el estado del jugador en consecuencia.

        Parametros:
        No tiene parámetros.

        Retorno: 
        No retorna ningún valor.
        '''
        event = pg.key.get_pressed()

        if event[pg.K_LEFT] and not event[pg.K_RIGHT]:
            
            self.is_doing = "left"
        elif event[pg.K_RIGHT] and not event[pg.K_LEFT]:
            self.is_loking_right = True
            self.is_doing = "right"
        elif event[pg.K_UP] and not self.is_jumping:
                self.is_doing = "jump"
        elif event[pg.K_SPACE] and not event[pg.K_LEFT] and not event[pg.K_RIGHT]:
            self.is_doing = "attack"
        else:
            self.is_doing = "stay"


    def do_actions(self):
        '''
        Brief:
        Este método de clase ejecuta acciones específicas para el jugador según el estado actual definido por la variable "is_doing".

        Parametros:
        No tiene parámetros.

        Retorno: 
        No retorna ningún valor.

        '''
        match self.is_doing:
            case "right":
                self.is_loking_right = True
                if not self.is_jumping:
                    self.animate(self.animations["walk"],0.5)
                self.speed_x = 15
            case "left":
                self.is_loking_right = False
                if not self.is_jumping:
                    self.animate(self.animations["walk_l"],0.5)
                self.speed_x = -15
            case "stay":
                if self.is_loking_right:
                    if not self.is_jumping:
                        self.animate(self.animations["idle"],0.3)
                    else: self.animate(self.animations["jump"],1)
                elif not self.is_loking_right:
                    if not self.is_jumping:
                        self.animate(self.animations["idle_l"],0.3)
                    else: self.animate(self.animations["jump_l"],1)
                self.speed_x = 0

            case "jump":
                if not self.is_jumping:
                    self.jump_sound.play()
                    self.is_jumping = True
                    self.displacement_y = self.jump_power
                    self.animate(self.animations["jump"],1) if self.is_loking_right else self.animate(self.animations["jump_l"],1)

            case "attack":
                self.speed_x = 0
                now = pg.time.get_ticks()
                if self.is_loking_right:
                    self.animate(self.animations["attack"],1)
                else:
                    self.animate(self.animations["attack_l"],1)
                if now - self.last_shot > self.cadence:
                    self.attack_sound.play()
                    self.create_projectile(r"assets\img\Player\Attack\projectile\0.png",(30,30),"Player")
                    self.last_shot = now

    
    def verify_screen_limit(self, width):
        '''
        Brief:
        Este método de clase verifica si el personaje ha alcanzado los límites de la pantalla y ajusta sus colliders en consecuencia.

        Parametros:
        - width: Ancho de la pantalla.

        Retorno: 
        No retorna ningún valor.

        '''
        if self.colliders["main"].left < 0:
            # El personaje ha superado el límite izquierdo de la pantalla
            self.colliders["main"].left = 0
            self.colliders["left"].left = 0
            self.colliders["right"].right = self.colliders["main"].right
            self.colliders["top"].left = 0
            self.colliders["bottom"].left = 0

        elif self.colliders["main"].right > width:
            # El personaje ha superado el límite derecho de la pantalla
            self.colliders["main"].right = width
            self.colliders["left"].left = self.colliders["main"].left
            self.colliders["right"].right = width
            self.colliders["top"].right = width
            self.colliders["bottom"].right = width
        
        elif self.colliders["main"].y <= 0:
            self.displacement_y = 3


    def verify_colition_coin(self,item_list:list[Reward]):
        '''
        Brief:
        Este método de clase verifica la colisión del jugador con elementos de tipo "Reward" (por ejemplo, monedas) y realiza acciones correspondientes como eliminar el elemento, actualizar el puntaje y la vida del jugador, y reproducir un sonido.

        Parametros:
        - item_list: Lista de instancias de la clase "Reward".

        Retorno: 
        No retorna ningún valor.
        '''
        for item in item_list:
            if self.colliders["main"].colliderect(item.colliders["main"]) and item.get_colition() == False:
                item.set_colition(True)
                item.kill(item_list)
                self.collect_coin_sound.play()
                self.score += item.score * random.randint(1,3)
                self.life += item.health

    def verify_colition_body_damage(self,item_list:list):   
        '''
        Brief:
        Este método de clase verifica la colisión del jugador con elementos que pueden causar daño (por ejemplo, enemigos o trampas) y realiza acciones correspondientes como reducir la vida del jugador y establecer su estado de invencibilidad.

        Parametros:
        - item_list: Lista de instancias que pueden causar daño.

        Retorno: 
        No retorna ningún valor.
        '''
        for item in item_list:
            if self.colliders["main"].colliderect(item.colliders["main"]):
                if not self.is_invencible:
                    self.colition_time_enemy_or_trap = pg.time.get_ticks()
                    self.is_invencible = True
                    self.life -= item.damage_colition
                    self.hurt_sound.play()


    
    def verify_colission_platforms(self, platforms_list:list[Platform]):
        '''
        Brief:
        Este método de clase verifica la colisión del jugador con plataformas y ajusta su posición y estado en consecuencia.

        Parametros:
        - platforms_list: Lista de instancias de la clase "Platform".

        Retorno: 
        No retorna ningún valor.
        '''
        self.gravity_fall()
        self.is_jumping = True
        for platform in platforms_list:
            if self.colliders["bottom"].colliderect(platform.colliders["top"]):
                self.is_jumping = False
                self.colliders["main"].bottom = platform.colliders["main"].top + 1
                self.colliders["left"].bottom = self.colliders["main"].bottom
                self.colliders["right"].bottom = self.colliders["main"].bottom
                self.colliders["bottom"].bottom = self.colliders["main"].bottom 
                self.colliders["top"].top = self.colliders["main"].top
                self.displacement_y = 0



            elif self.colliders["right"].colliderect(platform.colliders["left"]):
                for collider_key in self.colliders:
                    self.colliders[collider_key].right = platform.colliders["left"].left
                self.colliders["left"].right = self.colliders["main"].left + self.colliders["left"].width 
            
            elif self.colliders["left"].colliderect(platform.colliders["right"]):
                for collider_key in self.colliders:
                    self.colliders[collider_key].left = platform.colliders["right"].right
                self.colliders["right"].right = self.colliders["main"].right

            elif self.colliders["top"].colliderect(platform.colliders["bottom"]):
                self.displacement_y = 3

    def set_sound_volume(self,sound_volume):
        '''
        Brief:
        Este método de clase establece el volumen de los sonidos asociados al jugador.
        Parametros:
        - sound_volume: Volumen deseado para los sonidos.

        Retorno: 
        No retorna ningún valor.
        '''
        self.volume = sound_volume
        self.jump_sound.set_volume(self.volume)
        self.attack_sound.set_volume(self.volume)
        self.collect_coin_sound.set_volume(self.volume)
        self.projectile_collide_sound.set_volume(self.volume)
        self.hurt_sound.set_volume(self.volume)
        

    def check_invencibility(self):
        '''
        Brief:
        Este método de clase verifica si el jugador está en estado de invencibilidad y actualiza su estado en consecuencia.

        Parametros:
        No tiene parámetros.

        Retorno: 
        No retorna ningún valor.

        '''
        if self.is_invencible:
            current_time = pg.time.get_ticks()
            if current_time - self.colition_time_enemy_or_trap >= 2000:
                self.is_invencible = False


    def update(self,screen,platform_list,coin_list,enemy_list,trap_list,potion_list,sounds_volume):
        '''
        Brief:
        Este método de clase actualiza el estado del jugador en el juego, gestionando eventos del jugador, acciones, colisiones con plataformas, invencibilidad, daño de trampas y enemigos, y colisiones con monedas y pociones.

        Parametros:
        - screen: Superficie de la pantalla.
        - platform_list: Lista de instancias de la clase "Platform".
        - coin_list: Lista de instancias de la clase "Reward" representando monedas.
        - enemy_list: Lista de instancias de la clase "Enemy".
        - trap_list: Lista de instancias de la clase "Trap".
        - potion_list: Lista de instancias de la clase "Reward" representando pociones.
        - sounds_volume: Volumen de los sonidos.

        Retorno: 
        No retorna ningún valor.

        '''
        self.set_sound_volume(sounds_volume)
        self.verify_screen_limit(ANCHO_VENTANA)
        self.verify_player_events()
        self.do_actions()
        self.verify_colission_platforms(platform_list)
        self.check_invencibility()
        self.verify_colition_body_damage(trap_list)
        self.verify_colition_body_damage(enemy_list)
        self.verify_colition_coin(coin_list)
        self.verify_colition_coin(potion_list)

        self.move_x()
        super().update(screen,platform_list,enemy_list)


