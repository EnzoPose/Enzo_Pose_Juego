import pygame
from auxiliar.configuraciones import flip_images
from models.auxiliar import import_json


data_animations = import_json(r"auxiliar\animations.json")

def obtain_animations(dictionary:dict):
        '''
        Brief:
        Esta función toma un diccionario que contiene claves (keys) como nombres de animaciones y valores como listas de rutas de archivos de imagen. Luego, carga las imágenes correspondientes y las organiza en un diccionario donde las claves incluyen sufijos "_l" para indicar la versión invertida de la animación.

        Parámetros:
        - dictionary: Diccionario que contiene nombres de animaciones como claves y listas de rutas de archivos de imagen como valores.

        Retorno: 
        Un diccionario que mapea nombres de animaciones a listas de imágenes correspondientes, incluyendo versiones invertidas para animaciones orientadas hacia la izquierda.
        '''
        loaded_images = {}
        for key,values in dictionary.items():
                loaded_frames = []
                for frame in values:
                        loaded_frames.append(pygame.image.load(fr"{frame}"))
                loaded_images[key] = loaded_frames
                loaded_images[key + "_l"] = flip_images(loaded_frames,True)
        return loaded_images


player_animations = obtain_animations(data_animations.get("Player"))
enemy_animations = obtain_animations(data_animations.get("Enemy"))
enemy_animations["walk"],enemy_animations["walk_l"] = enemy_animations["walk_l"],enemy_animations["walk"]
enemy_animations["attack"],enemy_animations["attack_l"] = enemy_animations["attack_l"],enemy_animations["attack"]
coin_animations = obtain_animations(data_animations.get("Items").get("Coin"))
saw_animations = obtain_animations(data_animations.get("Items").get("Saw"))
potion_animations = obtain_animations(data_animations.get("Items").get("Potion"))
boss_animations = obtain_animations(data_animations.get("Boss"))