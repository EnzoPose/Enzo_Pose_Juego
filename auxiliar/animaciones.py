from models.auxiliar import SurfaceManager as sf 
import pygame
from auxiliar.configuraciones import flip_images
import os

def obtain_animations(dict:dict[str]):
        loaded_images = {}
        for key,values in dict.values():
                loaded_frames = []
                for frame in values:
                        loaded_frames.append(pygame.image.load(fr"{frame}"))
                loaded_images[key] = loaded_frames


coin = [pygame.image.load(r"assets\img\Items\Coin\0.png"),
                pygame.image.load(r"assets\img\Items\Coin\1.png"),
                pygame.image.load(r"assets\img\Items\Coin\2.png"),
                pygame.image.load(r"assets\img\Items\Coin\3.png"),
                pygame.image.load(r"assets\img\Items\Coin\4.png"),
                pygame.image.load(r"assets\img\Items\Coin\5.png"),
                pygame.image.load(r"assets\img\Items\Coin\6.png"),
                pygame.image.load(r"assets\img\Items\Coin\7.png"),
                pygame.image.load(r"assets\img\Items\Coin\8.png"),
                pygame.image.load(r"assets\img\Items\Coin\9.png"),
                pygame.image.load(r"assets\img\Items\Coin\10.png"),
                pygame.image.load(r"assets\img\Items\Coin\11.png"),
                pygame.image.load(r"assets\img\Items\Coin\12.png"),
                pygame.image.load(r"assets\img\Items\Coin\13.png"),
                pygame.image.load(r"assets\img\Items\Coin\14.png")]

coin_dict = {}
coin_dict["idle"] = coin

saw = [pygame.image.load(r"assets\img\Trap\Saw\0.png"),
        pygame.image.load(r"assets\img\Trap\Saw\1.png"),
        pygame.image.load(r"assets\img\Trap\Saw\2.png"),
        pygame.image.load(r"assets\img\Trap\Saw\3.png"),
        pygame.image.load(r"assets\img\Trap\Saw\4.png")]

saw_dict = {}
saw_dict["idle"] = saw

personaje_idle = [pygame.image.load(r"assets\img\Player\Idle\0.png"),
                pygame.image.load(r"assets\img\Player\Idle\1.png"),
                pygame.image.load(r"assets\img\Player\Idle\2.png")]
personaje_idle_l = flip_images(personaje_idle,True)

personaje_walk = [pygame.image.load(r"assets\img\Player\Walk\0.png"),
                pygame.image.load(r"assets\img\Player\Walk\1.png"),
                pygame.image.load(r"assets\img\Player\Walk\2.png"),
                pygame.image.load(r"assets\img\Player\Walk\3.png"),
                pygame.image.load(r"assets\img\Player\Walk\4.png"),
                pygame.image.load(r"assets\img\Player\Walk\5.png"),
                pygame.image.load(r"assets\img\Player\Walk\6.png"),
                pygame.image.load(r"assets\img\Player\Walk\7.png")]
personaje_walk_l = flip_images(personaje_walk,True)

personaje_jump = [pygame.image.load(r"assets\img\Player\Jump\0.png"),
                pygame.image.load(r"assets\img\Player\Jump\1.png")]
personaje_jump_l = flip_images(personaje_jump,True)

personaje_attack = [pygame.image.load(r"assets\img\Player\Attack\0.png"),
                pygame.image.load(r"assets\img\Player\Attack\1.png")]
personaje_attack_l = flip_images(personaje_attack,True)



diccionario_animaciones_personaje = {}

diccionario_animaciones_personaje["idle"] = personaje_idle
diccionario_animaciones_personaje["idle_l"] = personaje_idle_l
diccionario_animaciones_personaje["walk"] = personaje_walk
diccionario_animaciones_personaje["walk_l"] = personaje_walk_l
diccionario_animaciones_personaje["jump"] = personaje_jump
diccionario_animaciones_personaje["jump_l"] = personaje_jump_l
diccionario_animaciones_personaje[r"attack"] = personaje_attack
diccionario_animaciones_personaje[r"attack_l"] = personaje_attack_l


enemy_walk_l = [pygame.image.load(r"assets\img\Enemy\Walk\0.png"),
                pygame.image.load(r"assets\img\Enemy\Walk\1.png"),
                pygame.image.load(r"assets\img\Enemy\Walk\2.png"),
                pygame.image.load(r"assets\img\Enemy\Walk\3.png"),
                pygame.image.load(r"assets\img\Enemy\Walk\4.png"),
                pygame.image.load(r"assets\img\Enemy\Walk\5.png"),
                pygame.image.load(r"assets\img\Enemy\Walk\6.png"),
                pygame.image.load(r"assets\img\Enemy\Walk\7.png"),
                pygame.image.load(r"assets\img\Enemy\Walk\8.png"),
                pygame.image.load(r"assets\img\Enemy\Walk\9.png"),
                pygame.image.load(r"assets\img\Enemy\Walk\10.png"),
                pygame.image.load(r"assets\img\Enemy\Walk\11.png"),
                pygame.image.load(r"assets\img\Enemy\Walk\12.png"),
                pygame.image.load(r"assets\img\Enemy\Walk\13.png"),
                pygame.image.load(r"assets\img\Enemy\Walk\14.png"),
                pygame.image.load(r"assets\img\Enemy\Walk\15.png"),]

enemy_walk = flip_images(enemy_walk_l,True)
enemy_attack_l = [pygame.image.load(r"assets\img\Enemy\Attack\0.png"),
                pygame.image.load(r"assets\img\Enemy\Attack\1.png"),
                pygame.image.load(r"assets\img\Enemy\Attack\2.png"),
                pygame.image.load(r"assets\img\Enemy\Attack\3.png"),
                pygame.image.load(r"assets\img\Enemy\Attack\4.png")]

enemy_attack = flip_images(enemy_attack_l,True) 

enemy_dict = {}


enemy_dict["walk"] = enemy_walk
enemy_dict["walk_l"] = enemy_walk_l
enemy_dict["attack"] = enemy_attack
enemy_dict["attack_l"] = enemy_attack_l