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
        for item in item_list:
            if self.colliders["main"].colliderect(item.colliders["main"]) and item.get_colition() == False:
                item.set_colition(True)
                item.kill(item_list)
                self.collect_coin_sound.play()
                self.score += item.score * random.randint(1,3)
                self.life += item.health

    def verify_colition_body_damage(self,item_list:list):
        for item in item_list:
            if self.colliders["main"].colliderect(item.colliders["main"]):
                if not self.is_invencible:
                    self.colition_time_enemy_or_trap = pg.time.get_ticks()
                    self.is_invencible = True
                    self.life -= item.damage_colition
                    self.hurt_sound.play()


    
    def verify_colission_platforms(self, platforms_list:list[Platform]):
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
        self.volume = sound_volume
        self.jump_sound.set_volume(self.volume)
        self.attack_sound.set_volume(self.volume)
        self.collect_coin_sound.set_volume(self.volume)
        self.projectile_collide_sound.set_volume(self.volume)
        self.hurt_sound.set_volume(self.volume)
        

    def check_invencibility(self):
        if self.is_invencible:
            current_time = pg.time.get_ticks()
            if current_time - self.colition_time_enemy_or_trap >= 2000:
                self.is_invencible = False


    def update(self,screen,platform_list,coin_list,enemy_list,trap_list,sounds_volume):
        self.set_sound_volume(sounds_volume)
        self.verify_screen_limit(ANCHO_VENTANA)
        self.verify_player_events()
        self.do_actions()
        self.verify_colission_platforms(platform_list)
        self.check_invencibility()
        self.verify_colition_body_damage(trap_list)
        self.verify_colition_body_damage(enemy_list)
        self.verify_colition_coin(coin_list)

        self.move_x()
        super().update(screen,platform_list,enemy_list)


