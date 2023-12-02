import pygame as pg
from models.charapter.charapter import Charapter
from models.platform.class_patform import Platform
from models.constantes import ANCHO_VENTANA

class Enemy(Charapter):
    def __init__(self, surface: pg.surface, initial_position: list, animations: dict, rect_diference: int, size: list,life:int,damage:int):
        super().__init__(surface, initial_position, animations, rect_diference, size,life,damage)
        
        self.last_shot = 0
        self.is_doing = "walk"
        self.previous_action = None
        self.is_jumping = True
        self.is_alive = True
        self.is_looking_player = False
        self.pov_rect = pg.rect.Rect(self.colliders["main"].left - 200, self.colliders["main"].top + 50 , 500,self.height) if not self.is_loking_right else \
        pg.rect.Rect(self.colliders["main"].right + 200, self.colliders["main"].top + 50 , 500,self.height)

    def kill(self):
        self.is_alive = False

    def check_collition_platform(self,platform_list:list[Platform]):
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
        if self.pov_rect.colliderect(player.colliders["main"]):
            self.is_looking_player = True
            self.is_doing = "attack"
        else:
            self.is_looking_player = False
            if self.is_loking_right:
                self.is_doing = "walk"
            else: self.is_doing = "walk_l"


    def do_attack(self):
        now = pg.time.get_ticks()
        if self.is_loking_right:
            self.animate(self.animations["attack"])
        else:
            self.animate(self.animations["attack_l"])
        if now -self.last_shot > 1500:
            self.create_projectile(r"assets\img\Enemy\Attack\bullet.png",(60,40))
            self.last_shot = now

    def event_management(self):
        match self.is_doing:
            case "walk":
                self.speed_x = 3
                self.move_x()
                self.pov_rect.left =  self.colliders["main"].right
                self.pov_rect.top = self.colliders["main"].top
                self.animate(self.animations["walk"])
            case "walk_l":
                self.speed_x = -3
                self.move_x()
                self.pov_rect.right = self.colliders["main"].left
                self.pov_rect.top = self.colliders["main"].top
                self.animate(self.animations["walk_l"])
            case "attack":
                if self.is_looking_player:
                    self.speed_x = 0
                    self.do_attack()


    def update(self,screen,platform_list,enemy_list):
        self.gravity_fall()
        self.verify_is_looking_player(enemy_list[0])
        self.event_management()
        self.check_collition_platform(platform_list)
        # super().verify_colission_platforms(platform_list)
        super().update(screen,platform_list,enemy_list)