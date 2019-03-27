import pygame

# Config
width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

client_number = 0

def redraw_window():
    win.fill((255, 255, 255))
    pygame.display.update()