import pygame as pg
import json

class SurfaceManager:

    @staticmethod
    def get_surface_from_spritesheet(img_path: str, cols: int, rows: int, step = 1, flip: bool = False) -> list[pg.surface.Surface]:
        sprites_list = list()
        surface_img = pg.image.load(img_path)
        frame_width = int(surface_img.get_width()/cols)
        frame_height = int(surface_img.get_height()/rows)

        for row in range(rows):

            for column in range(0, cols, step):
                x_axis = column * frame_width
                y_axis = row * frame_height

                frame_surface = surface_img.subsurface(
                    x_axis, y_axis, frame_width, frame_height
                )

                if flip:
                    frame_surface = pg.transform.flip(frame_surface, True, False)
                sprites_list.append(frame_surface)
        return sprites_list
    

def resize_images(image_list,W,H):
    for i in range(len(image_list)):
        image_list[i] = pg.transform.scale(image_list[i],(W,H))
    return image_list

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