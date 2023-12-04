import json
import pygame as pg
from models.player.class_player import Player
from models.Enemy.class_enemy import Enemy
from models.platform.class_patform import Platform
from models.Items.class_item import Item
from auxiliar.modo import *
from auxiliar.animaciones import player_animations,coin_animations,saw_animations,enemy_animations

class Stage:
    def __init__(self,screen,w,h,stage_name) -> None:
        self.stage_name = stage_name
        self.stage_configs = self.get_configs()
        self.bgd = self.stage_configs.get("Scenario").get("Background")
        self.bgd_surface = pg.image.load(self.bgd)
        self.font = pg.font.SysFont("consolas",30)
        self.player_configs = self.stage_configs.get("Player")
        self.enemy_configs = self.stage_configs.get("Enemies")
        # self.saw_configs = self.stage_configs.get("Saw")
        self.coin_configs = self.stage_configs.get("Items").get("Coins")

        self.w = w
        self.h = h
        self.screen = screen
        background_surface = pg.image.load(self.stage_configs.get("Scenario").get("Background"))
        self.background_img = pg.transform.scale(background_surface,(self.w,self.h))
        self.win = False
        self.is_paused = False

        self.player = Player(player_animations["idle"][0],self.player_configs.get("Coords"),player_animations,10,self.player_configs.get("Size"),self.player_configs.get("Life"),
                            self.player_configs.get("Damage"))

        self.enemies = self.set_enemies()
        self.coins = self.set_coins()
        self.platforms = self.set_platforms()
        # self.traps = self.set_traps()

    def get_configs(self):
        with open('configs\configs.json', 'r',encoding="utf-8") as configs:
            return json.load(configs)[self.stage_name]
            #print(self.__stage_configs)

    def set_enemies(self)-> list[Enemy]:
        enemy_list = []
        for i in range(self.enemy_configs.get("Amount")):
            enemy_list.append(Enemy(enemy_animations["walk"][0],self.enemy_configs.get("Coords")[i],
                                    enemy_animations,10,self.enemy_configs.get("Size"),self.enemy_configs.get("Life"),
                                    self.enemy_configs.get("Damage")))
        return enemy_list

    def set_coins(self)-> list[Item]:
        coin_configs = self.stage_configs.get("Items").get("Coins")
        coin_list = []
        for i in range(coin_configs.get("Amount")):
            coin_list.append(Item(coin_animations["idle"][0],coin_configs.get("Coords")[i],coin_animations,10,coin_configs.get("Size")))
        return coin_list

    def set_platforms(self) -> list[Platform]:
        platform_configs = self.stage_configs.get("Platforms")
        platform_list = []
        for i in range(platform_configs.get("Amount")): #platform_configs.get("Surface")
            platform_list.append(Platform(platform_configs.get("Surface")[i],platform_configs.get("Coords")[i],None,10,platform_configs.get("Size")[i]))
        return platform_list

    def set_traps(self)-> list[Item]:
        trap_configs = self.stage_configs.get("Traps")
        trap_list = []
        for i in range(trap_configs.get("Amount")):
            trap_list.append()


    def stage_passed(self):
        if self.win:
            return self.win


    
    def check_win(self) -> bool:
        match self.stage_name:
            case 'Stage_1' | 'Stage_2' | 'Stage_3' | 'Stage_4':
                if len(self.enemies) == 0 and len(self.coins) == 0:
                    self.win = True 


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
        
        self.screen.blit(score_txt,(0,0))
        self.screen.blit(life_txt,(0,30))

        for platform in self.platforms:
            platform.update(self.screen)

        self.player.update(self.screen,self.platforms,self.coins,self.enemies)

        for enemy in self.enemies:
            if enemy.life <= 0:
                self.enemies.remove(enemy)
            else:
                enemy.update(self.screen,self.platforms,[self.player])
        
        for coin in self.coins:
            if not coin.colition:
                coin.animate(coin.actions["idle"])
                coin.update(self.screen)
        
        if get_mode():
            self.draw_debug_mode()



    def run(self):
        if not self.is_paused:
            self.update_screen()
            self.check_win()
