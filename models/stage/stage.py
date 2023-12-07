import json
import pygame as pg
from models.player.class_player import Player
from models.Enemy.class_enemy import Enemy
from models.Boss.class_boss import Boss
from models.platform.class_patform import Platform
from models.reward.reward import Reward
from models.trap.trap import Trap
from auxiliar.modo import *
from auxiliar.animaciones import player_animations,coin_animations,saw_animations,enemy_animations,potion_animations,boss_animations
from models.constantes import ANCHO_VENTANA,ALTO_VENTANA
from models.values import Values
from db_functions import get_player_id, update_row_in_db
import random

class Stage:
    def __init__(self,screen,w,h,stage_name,values:Values) -> None:

        self.stage_name = stage_name
        self.values = values
        self.values.current_level = stage_name
        self.stage_configs = self.get_configs()
        self.bgd = self.stage_configs.get("Scenario").get("Background")
        self.bgd_surface = pg.image.load(self.bgd)
        self.bgd_surface = pg.transform.scale(self.bgd_surface,(ANCHO_VENTANA,ALTO_VENTANA))
        self.font = pg.font.SysFont("consolas",30)
        self.player_configs = self.stage_configs.get("Player")
        self.enemy_configs = self.stage_configs.get("Enemies")
        self.trap_configs = self.stage_configs.get("Traps")
        self.coin_configs = self.stage_configs.get("Items").get("Coins")
        self.potion_configs = self.stage_configs.get("Items").get("Potions")
        
        self.w = w
        self.h = h
        self.screen = screen
        background_surface = pg.image.load(self.stage_configs.get("Scenario").get("Background"))
        self.background_img = pg.transform.scale(background_surface,(self.w,self.h))


        self.win = False
        self.lost = False
        self.initial_time = pg.time.get_ticks()
        self.time = 60

        # self.sounds_volume = 0.1

        self.player = Player(player_animations["idle"][0],self.player_configs.get("Coords"),player_animations,10,self.player_configs.get("Size"),self.player_configs.get("Life"),
                            self.player_configs.get("Damage"))

        if self.stage_name != "Stage_3":
            self.enemies = self.set_enemies() 
            self.score_enemies = 300
        else:
            self.enemies = [Boss(boss_animations["walk"][0],self.enemy_configs.get("Coords"),boss_animations,10,self.enemy_configs.get("Size"),
                self.enemy_configs.get("Life"),self.enemy_configs.get("Damage"),self.enemy_configs.get("Cadence"),self.enemy_configs.get("Damage_colition"))]
            self.score_enemies = 5000
    
        self.coins = self.set_coins()
        self.platforms = self.set_platforms()
        self.traps = self.set_traps()
        self.potions = self.set_potions()



    def get_configs(self):
        with open('configs\configs.json', 'r',encoding="utf-8") as configs:
            return json.load(configs)[self.stage_name]

    def set_enemies(self)-> list[Enemy]:
        enemy_list = []
        for i in range(self.enemy_configs.get("Amount")):
            enemy_list.append(Enemy(enemy_animations["walk"][0],self.enemy_configs.get("Coords")[i],
                                    enemy_animations,10,self.enemy_configs.get("Size"),self.enemy_configs.get("Life"),
                                    self.enemy_configs.get("Damage"),self.enemy_configs.get("Cadence"),self.enemy_configs.get("Damage_colition")))
        return enemy_list

    def set_coins(self)-> list[Reward]:
        coin_configs = self.stage_configs.get("Items").get("Coins")
        coin_list = []
        for i in range(coin_configs.get("Amount")):
            coin_list.append(Reward(coin_animations["idle"][0],coin_configs.get("Coords")[i],coin_animations,0,coin_configs.get("Size"),coin_configs.get("Score")))
        return coin_list

    def set_platforms(self) -> list[Platform]:
        platform_configs = self.stage_configs.get("Platforms")
        platform_list = []
        for i in range(platform_configs.get("Amount")): #platform_configs.get("Surface")
            platform_list.append(Platform(platform_configs.get("Surface")[i],platform_configs.get("Coords")[i],None,10,platform_configs.get("Size")[i]))
        return platform_list

    def set_traps(self)-> list[Trap]:
        trap_list = []
        for i in range(self.trap_configs.get("Amount")):
            trap_list.append(Trap(saw_animations["idle"][0],self.trap_configs.get("Coords")[i],saw_animations,0,self.trap_configs.get("Size"),self.trap_configs.get("Damage")))
        return trap_list

    def set_potions(self)-> list[Reward]:
        potion_configs = self.stage_configs.get("Items").get("Potion")
        potion_list = []
        for i in range(potion_configs.get("Amount")):
            potion_list.append(Reward(potion_animations["idle"][0],potion_configs.get("Coords")[i],potion_animations,0,potion_configs.get("Size"),0,potion_configs.get("Health")))
        return potion_list

    def check_win(self):
        match self.stage_name:
            case 'Stage_1' | 'Stage_2' | 'Stage_3':
                if len(self.enemies) == 0 and len(self.coins) == 0:
                    self.win = True
                    self.values.player_score[self.values.player_name][self.values.current_level] = self.player.score
                    current_player_id = get_player_id(self.values.player_name) 
                    update_row_in_db(current_player_id,self.values.obtain_total_score())



    def draw_debug_mode(self):
        for collider_side in self.player.colliders:
            pg.draw.rect(self.screen,"Purple",self.player.colliders[collider_side],2)

        for platform in self.platforms:
            for side_collider_key in platform.colliders:
                pg.draw.rect(self.screen,"Red",platform.colliders[side_collider_key],2)
                pg.draw.rect(self.screen,"Red",platform.rect_for_collide_enemy_r)
                pg.draw.rect(self.screen,"Red",platform.rect_for_collide_enemy_l)
        
        for projectile in self.player.projectile_list:
            for side in projectile.colliders:
                pg.draw.rect(self.screen,"Yellow",projectile.colliders[side],2)
        

        for coin in self.coins:
            pg.draw.rect(self.screen,"Red",coin.rect,2)
    
        for potion in self.potions:
            pg.draw.rect(self.screen,"Red",potion.rect,2)

        for trap in self.traps:
            pg.draw.rect(self.screen,"Red",trap.rect,2)

        for enemy in self.enemies:
            pg.draw.rect(self.screen,"Red",enemy.colliders["main"],2)
            pg.draw.rect(self.screen,"Red",enemy.pov_rect,2)

            for projectile in enemy.projectile_list:
                for side in projectile.colliders:
                    pg.draw.rect(self.screen,"Yellow",projectile.colliders[side],2)

    def update_screen(self):
        self.screen.blit(self.bgd_surface,(0,0))

        score_txt = self.font.render(f"Score: {self.player.score}",False,"Red")
        life_txt = self.font.render(f"Life: {self.player.life}",False,"Green")
        timer_txt = self.font.render(f"Time: {self.time}",False,"White")


        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.initial_time
        if  elapsed_time >= 1000:
            self.time -= 1
            self.initial_time = current_time


        for platform in self.platforms:
            platform.update(self.screen)


        for enemy in self.enemies:
            if enemy.life <= 0:
                self.player.score += self.score_enemies * random.randint(1,5)
                self.enemies.remove(enemy)
            else:
                if self.stage_name != "Stage_3":
                    enemy.update(self.screen,self.platforms,[self.player],self.sounds_volume)
                else:
                    enemy.update(self.screen,self.platforms,[self.player])
        for trap in self.traps:
            trap.animate(trap.actions["idle"],1)
            trap.update(self.screen)

        self.player.update(self.screen,self.platforms,self.coins,self.enemies,self.traps,self.potions,self.sounds_volume)
        
        for coin in self.coins:
            if not coin.colition:
                coin.animate(coin.actions["idle"],1)
                coin.update(self.screen)
        

        for potion in self.potions:
            potion.animate(potion.actions["idle"],0.3)
            potion.update(self.screen)

        if get_mode():
            self.draw_debug_mode()

        self.screen.blit(score_txt,(100,0))
        self.screen.blit(life_txt,(300,0))
        self.screen.blit(timer_txt,(500,0))

    def update_volume(self):
        self.sounds_volume = self.values.sound_volume

    def check_lost(self):
        if self.player.life <= 0 or self.time <= 0:
            self.lost = True


    def run(self):
        self.update_volume()
        self.check_lost()
        self.check_win()
        self.update_screen()
