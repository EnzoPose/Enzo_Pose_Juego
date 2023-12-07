import pygame
from models.auxiliar import resize_images

class Object:
    def __init__(self,surface: pygame.Surface, initial_position: list, actions:dict, rect_diference:int , size:list):
        self.width = size[0]
        self.height = size[1]


        self.surface = pygame.transform.scale(surface,(size[0],size[1]))

        if actions is not None:
            for key,value in actions.items():
                actions[key] = resize_images(actions[key],size[0],size[1])

        self.rect = self.surface.get_rect()
        self.rect.x = initial_position[0]
        self.rect.y = initial_position[1]
        self.colliders = self.obtain_rects(self.rect, rect_diference)
        self.actions = actions

        self.step_counter = 0



    def animate(self, animation_list,count_amountt):
        '''
        Brief:
        Este método de clase anima el objeto cambiando su superficie en función de una lista de animaciones.

        Parametros:
        - animation_list: Lista de imágenes representando las animaciones.
        - count_amount: Cantidad a incrementar en cada paso de la animación.

        Retorno: 
        No retorna ningún valor.
        '''
        length = len(animation_list)
        if self.step_counter >= length:
            self.step_counter = 0
        self.surface = animation_list[int(self.step_counter)]
        self.step_counter += count_amountt

    def move_x(self, speed):
        '''
        Brief:
        Este método de clase mueve el objeto en el eje X ajustando las coordenadas de sus colisionadores.

        Parametros:
        - speed: Velocidad de movimiento en el eje X.

        Retorno: 
        No retorna ningún valor.

        '''
        for side in self.colliders:
            self.colliders[side].x += speed
    
    def update(self,screen):
        '''
        Brief:
        Este método de clase actualiza la representación gráfica del objeto en la pantalla.

        Parametros:
        - screen: Superficie de la pantalla.

        Retorno: 
        No retorna ningún valor.

        '''
        screen.blit(self.surface,self.rect)

    def obtain_rects(self,main:pygame.Rect,rect_diference_value)->dict:
        '''
        Brief:
        Este método de clase obtiene un diccionario de rectángulos asociados a diferentes lados del objeto.

        Parametros:
        - main: Rectángulo principal.
        - rect_diference_value: Valor de diferencia para ajustar los rectángulos adicionales.

        Retorno: 
        Diccionario con rectángulos asociados a diferentes lados del objeto.
        '''
        dictionary = {}
        dictionary["main"] = main ##(left: float, top: float, width: float, height: float) -> None
        dictionary["bottom"] = pygame.Rect(main.left,main.bottom-rect_diference_value,main.width,rect_diference_value)
        dictionary["right"] = pygame.Rect(main.right -rect_diference_value, main.top, rect_diference_value, main.height)
        dictionary["left"] = pygame.Rect(main.left, main.top, rect_diference_value, main.height)
        dictionary["top"] = pygame.Rect(main.left, main.top, main.width, rect_diference_value) ## la suma de los 2 tiene que ser mayor a la velocidad de caida para que no se vaya del piso
        return dictionary
