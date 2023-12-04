import pygame
from pygame.locals import *

from GUI.UI.GUI_button import *
#No se instancia. Es la base de la jerarquia
class Form(Widget):
    def __init__(self, screen, x,y,w,h,color_background = "Black",color_border = "Black", border_size = -1, active = True):
        super().__init__(screen, x,y,w,h, color_background, color_border, border_size)
        self.slave = pygame.Surface((w,h))
        self.slave_rect = self.slave.get_rect()
        self.slave_rect.x = x
        self.slave_rect.y = y
        self.active = active
        self.widget_list = []
        self.hijo = None
        self.dialog_result = None
        self.padre = None
        self.volume = 0.1
    
    def show_dialog(self, formulario):
        self.hijo = formulario
        self.hijo.padre = self

    def end_dialog(self):
        self.dialog_result = "OK"
        self.close()

    def close(self):
        self.active = False

    def verify_dialog_result(self):
        return self.hijo == None or self.hijo.dialog_result != None

    def render(self):
        pass

    def update(self, event_list):
        pass

