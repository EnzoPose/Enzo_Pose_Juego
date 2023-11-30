import pygame

def resize_images(image_list,W,H):
    for i in range(len(image_list)):
        image_list[i] = pygame.transform.scale(image_list[i],(W,H))

def flip_images(lista,flip_x,flip_y = False):
    flipped_list = []
    for image in lista:
        flipped_list.append(pygame.transform.flip(image,flip_x,flip_y))
    return flipped_list



# def transform_images_in_list(path:str):
#     image_list = []
#     for image in os.listdir(path):
#         image_list.append(pygame.image.load(image))
#     return image_list

