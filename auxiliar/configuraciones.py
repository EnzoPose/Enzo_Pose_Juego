import pygame
import json
def resize_images(image_list,W,H):
    for i in range(len(image_list)):
        image_list[i] = pygame.transform.scale(image_list[i],(W,H))

def flip_images(lista,flip_x,flip_y = False):
    flipped_list = []
    for image in lista:
        flipped_list.append(pygame.transform.flip(image,flip_x,flip_y))
    return flipped_list

def import_json(path):
    try:
        with open(path,"r",encoding="utf-8") as archivo_json:
            data = json.load(archivo_json)
        print("Se cargaron los datos")
        return data
    except FileNotFoundError:
        print(f"El {path} no se encontro")
    except Exception as e:
        print(f"Error al cargar el archivo {str(e)}")

# def transform_images_in_list(path:str):
#     image_list = []
#     for image in os.listdir(path):
#         image_list.append(pygame.image.load(image))
#     return image_list

