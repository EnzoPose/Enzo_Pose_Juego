import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ejemplo de Pausa en Pygame")

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Jugador
player_size = 50
player_x = screen_width // 2 - player_size // 2
player_y = screen_height - 2 * player_size
player_speed = 5

# Reloj para controlar la velocidad de actualización
clock = pygame.time.Clock()

# Variable para controlar el estado de pausa
paused = False

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                # Cambiar el estado de pausa al presionar la tecla 'P'
                paused = not paused

    # Actualizar el juego solo si no está en modo de pausa
    if not paused:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
            player_x += player_speed

    # Dibujar el fondo
    screen.fill(white)

    # Dibujar al jugador
    pygame.draw.rect(screen, red, (player_x, player_y, player_size, player_size))

    # Dibujar el mensaje de pausa si está en modo de pausa
    if paused:
        font = pygame.font.SysFont(None, 55)
        text = font.render("Pausado", True, black)
        screen.blit(text, (screen_width // 2 - 100, screen_height // 2 - 30))

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de actualización
    clock.tick(60)
