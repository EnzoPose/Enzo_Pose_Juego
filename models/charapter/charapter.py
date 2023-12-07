from models.object_game.Class_object import Object
from models.Projectile.class_projectile import Projectile
from auxiliar.configuraciones import resize_images
from models.constantes import ANCHO_VENTANA
import pygame as pg

class Charapter(Object):

    def __init__(self, surface:pg.surface, initial_position: list ,animations:dict,rect_diference:int,size:list,life:int,damage:int):
        super().__init__(surface,initial_position,animations,rect_diference, size)
        
        self.life = life
        self.damage = damage
        ##Movement 
        self.speed_x = 0

        self.gravity = 1
        self.jump_power = -20
        self.drop_speed_limit = 20
        self.displacement_y = 0
        self.is_jumping = False

        ##Attack
        self.is_shooting = False
        self.projectile_list:list[Projectile] = []
        self.cadence = 200


        self.is_loking_right = True
        self.right_limit = False
        self.left_limit = False
        self.animations = animations
        self.resize_animations()

        self.colliders_thickness = rect_diference

        self.projectile_collide_sound = pg.mixer.Sound("assets\img\Sounds\lasser_collide.mp3")

    
    def resize_animations(self):
        '''
        Brief:
        Este método de clase redimensiona todas las animaciones de la instancia de la clase "Charapter" utilizando la función "resize_images".
        Parametros:
        No tiene parámetros.

        Retorno: 
        No retorna ningún valor.
        '''
        for key in self.animations: ## por cada key en el diccionario de animations del objeto
            resize_images(self.animations[key],self.width,self.height)## llamo a la función de reescalar imagen


    def gravity_fall(self):
        '''
        Brief:
        Este método de clase aplica la gravedad a la instancia de la clase "Character" cuando está en el proceso de caída (no está saltando). Actualiza la posición vertical según la gravedad, pero solo hasta el límite de velocidad de caída establecido.

        Parametros:
        No tiene parámetros.

        Retorno: 
        No retorna ningún valor.
        '''
        if self.is_jumping:
            self.jump()
            if self.displacement_y + self.gravity < self.drop_speed_limit:
                self.displacement_y += self.gravity

    def jump(self):
        '''
        Brief:
        Este método de clase actualiza las posiciones verticales de los colliders de la instancia de la clase "Character" durante un salto.

        Parametros:
        No tiene parámetros.

        Retorno: 
        No retorna ningún valor.
        '''
        for side in self.colliders:
            self.colliders[side].y += self.displacement_y



    def move_x(self):
        '''
        Brief:
        Este método de clase mueve horizontalmente la instancia de la clase "Character" utilizando el metodo "move_x" de la clase Object, con una velocidad específica.
        Parametros:
        No tiene parámetros.

        Retorno: 
        No retorna ningún valor.
        '''
        super().move_x(self.speed_x)


    def projectile_rain(self,image_path,size,who_created_it):
        '''
        Brief:
        Este método de clase crea una lluvia de proyectiles (instancias de la clase "Projectile") con una imagen específica, tamaño y creador.

        Parametros:
        - image_path: Ruta de la imagen para los proyectiles.
        - size: Tamaño de los proyectiles.
        - who_created_it: Identificador del creador de los proyectiles.

        Retorno: 
        No retorna ningún valor.
        '''
        surface = pg.transform.scale(pg.image.load(image_path),size)
        projectile_distance_x = ANCHO_VENTANA // 20

        initial_x = 0
        for i in range(19):
            projectile = Projectile(surface,(initial_x + projectile_distance_x,0),None,0,size,self.damage,who_created_it)
            projectile.speed_y = 18
            initial_x += projectile_distance_x
            self.projectile_list.append(projectile)

    def create_projectile(self,image_path,size,who_created_it):
        '''
        Brief:
        Este método de clase crea un proyectil (instancia de la clase "Projectile") con una imagen específica, tamaño y creador, y lo agrega a la lista de proyectiles.

        Parametros:
        - image_path: Ruta de la imagen para el proyectil.
        - size: Tamaño del proyectil.
        - who_created_it: Identificador del creador del proyectil.

        Retorno: 
        No retorna ningún valor.
        '''
        surface = pg.transform.scale(pg.image.load(image_path),size)
        if self.is_loking_right:
            projectile = Projectile(surface,(self.rect.right, self.rect.centery - 20),None,0,size,self.damage,who_created_it)
            projectile.speed = 20
        else:
            surface = pg.transform.flip(surface,True,False)
            projectile = Projectile(surface,(self.rect.left, self.rect.centery - 20),None,0,size,self.damage,who_created_it)
            projectile.speed = -20
        self.projectile_list.append(projectile)


    def update_projectiles(self,screen,platform_list,enemy_list):
        '''
        Brief:
        Este método de clase actualiza todos los proyectiles en la lista de proyectiles de la instancia de la clase "TuClase", verificando colisiones y reproduciendo un sonido cuando ocurre una colisión.

        Parametros:
        - screen: Objeto que representa la pantalla en la que se realiza la actualización.
        - platform_list: Lista de instancias de la clase "Platform".
        - enemy_list: Lista de instancias de la clase "Enemy" si Player creo el proyectil O "Player" si Enemy creo el proyectil.

        Retorno: 
        No retorna ningún valor.
        '''
        for projectile in self.projectile_list:
            projectile.update(screen,platform_list,self.projectile_list,enemy_list)
            if projectile.colition:
                self.projectile_collide_sound.play()
                projectile.kill(self.projectile_list)



    def update(self,screen,platform_list,enemy_list):
        '''
        Brief:
        Este método de clase actualiza la instancia de la clase "Character" y los proyectiles asociados, utilizando la función "update" de la clase Object y el método "update_projectiles".

        Parametros:
        - screen: Objeto que representa la pantalla en la que se realiza la actualización.
        - platform_list: Lista de instancias de la clase "Platform".
        - enemy_list: Lista de instancias de la clase "Enemy".

        Retorno: 
        No retorna ningún valor.
        '''
        super().update(screen)
        self.update_projectiles(screen,platform_list,enemy_list)


