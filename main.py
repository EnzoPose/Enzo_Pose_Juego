import pygame as pg
from auxiliar.modo import *
from auxiliar.animaciones import diccionario_animaciones_personaje,coin_dict,saw_dict,enemy_dict
from models.object_game.Class_object import Object
from models.platform.class_patform import Platform
from models.Items.class_item import Item
from models.Enemy.class_enemy import Enemy

from models.constantes import (
    ALTO_VENTANA, ANCHO_VENTANA, FPS
)
from models.player.class_player import Player

pg.init()

screen = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
clock = pg.time.Clock()

back_img = pg.image.load(r'assets\img\Backgrounds\forest\1920x1080.jpg')
back_img = pg.transform.scale(back_img, (ANCHO_VENTANA, ALTO_VENTANA))

vegeta = Player(diccionario_animaciones_personaje["idle"][0],(150,700),diccionario_animaciones_personaje,10,(40,80),100,20)


floor = Platform("assets\img\Platforms\Metal_floor.png",(0,ALTO_VENTANA-100),None,10,(ANCHO_VENTANA,100))
platform_1 = Platform("assets\img\Platforms\metal_platform.png",(250,300),None,10,(200,40))
platform_2 = Platform("assets\img\Platforms\metal_platform.png",(700,450),None,10,(200,40))
platform_3 = Platform("assets\img\Platforms\metal_platform.png",(1100,300),None,10,(200,40))
platform_4 = Platform("assets\img\Platforms\metal_platform.png",(700,150),None,10,(200,40))
platform_5 = Platform("assets\img\Platforms\metal_platform.png",(250,620),None,10,(200,40))
platform_6 = Platform("assets\img\Platforms\metal_platform.png",(1100,620),None,10,(200,40))
column_1 = Platform("assets\img\Platforms\metal_column.png",(0,200),None,10,(100,700))
column_2 = Platform("assets\img\Platforms\metal_column.png",(ANCHO_VENTANA-100,200),None,10,(100,700))


platform_list = [floor,platform_1,platform_2,platform_3,platform_4,platform_5,platform_6,column_1,column_2]

coin_1 = Item(coin_dict["idle"][0],(40,10),coin_dict,0,(30,30))
coin_2 = Item(coin_dict["idle"][0],(1540,10),coin_dict,0,(30,30))
coin_3 = Item(coin_dict["idle"][0],(780,10),coin_dict,0,(30,30))
coin_4 = Item(coin_dict["idle"][0],(780,300),coin_dict,0,(30,30))
coin_6 = Item(coin_dict["idle"][0],(340,140),coin_dict,0,(30,30))
coin_5 = Item(coin_dict["idle"][0],(340,450),coin_dict,0,(30,30))
coin_7 = Item(coin_dict["idle"][0],(1190,140),coin_dict,0,(30,30))
coin_8 = Item(coin_dict["idle"][0],(1190,450),coin_dict,0,(30,30))

coin_list = [coin_1,coin_2,coin_3,coin_4,coin_5,coin_6,coin_7,coin_8]

trap = Item(saw_dict["idle"][0],(600,600),saw_dict,0,(40,40))

juego_ejecutandose = True

enemy = Enemy(enemy_dict["walk"][0], (750,300),enemy_dict,10,(100,100),100,20)

enemy_2 = Enemy(enemy_dict["walk"][0], (500,400),enemy_dict,10,(100,100),100,20)
enemy_3 = Enemy(enemy_dict["walk"][0], (800,400),enemy_dict,10,(100,100),100,20)
enemy_list = [enemy,enemy_2,enemy_3]
while juego_ejecutandose:
    lista_eventos = pg.event.get()
    for event in lista_eventos:
        match event.type:
            case pg.KEYDOWN:
                if event.key == pg.K_TAB:
                    cambiar_modo()
            case pg.QUIT:
                print('Estoy CERRANDO el JUEGO')
                juego_ejecutandose = False
                break
    
    screen.blit(back_img, back_img.get_rect())

    for platform in platform_list:
        platform.update(screen)    

    vegeta.update(screen,platform_list,coin_list,enemy_list)
    trap.animate(trap.actions["idle"])

    for enemy in enemy_list:
        if enemy.life <= 0:
            enemy_list.remove(enemy)
        else:
            enemy.update(screen,platform_list,[vegeta])


    for coin in coin_list:
        if not coin.colition:
            coin.animate(coin.actions["idle"])
            coin.update(screen)

    if get_mode():
        for collider_side in vegeta.colliders:
            pg.draw.rect(screen,"Purple",vegeta.colliders[collider_side],2)

        for platform in platform_list:
            for side_collider_key in platform.colliders:
                pg.draw.rect(screen,"Red",platform.colliders[side_collider_key],2)
                pg.draw.rect(screen,"Red",platform.rect_for_collide_enemy_r)
                pg.draw.rect(screen,"Red",platform.rect_for_collide_enemy_l)
        
        for projectile in vegeta.projectile_list:
            for side in projectile.colliders:
                pg.draw.rect(screen,"Yellow",projectile.colliders[side],2)
        
        for coin in coin_list:
            pg.draw.rect(screen,"Red",coin.rect,2)
    
        for enemy in enemy_list:
            pg.draw.rect(screen,"Red",enemy.colliders["main"],2)
            pg.draw.rect(screen,"Red",enemy.pov_rect,2)
    clock.tick(FPS)
    pg.display.update()

pg.quit()