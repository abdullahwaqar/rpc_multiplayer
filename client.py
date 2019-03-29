import pygame
from network import Network
from player import Player

#* Config
width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

def redraw_window(win, player, player1):
    win.fill((255, 255, 255))
    player.draw(win)
    player1.draw(win)
    pygame.display.update()

def main():
    run = True
    n = Network()
    p = n.get_p()
    while run:
        p2 = n.send(p)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.mov()
        redraw_window(win, p, p2)

if __name__ == '__main__':
    main()