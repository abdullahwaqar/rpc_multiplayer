import pygame
from network import Network
from player import Player

#* Config
pygame.font.init()
width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

class Button:

    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(slice, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('comicsans', 40)
        text = font.render(self.text, 1, (255, 255, 255))
        #* Center the button on the window
        win.blit(text, (
            self.x + round(self.width / 2) - round(text.get_width() / 2),
            self.y + round(self.height / 2) - round(text.get_height() / 2),
            ))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            False

def redraw_window(win, player, player1):
    win.fill((128, 128, 128))
    pass

btns = [
    Button('Rock', 50, 500, (0, 0, 0)),
    Button('Paper', 250, 500, (0, 255, 0)),
    Button('Scissors', 450, 500, (255, 0, 0)),
    ]

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.get_p())
    print("You are player", player)

    #* Main game loop
    while run:
        clock.tick(60)
        try:
            game = n.send('get')
        except:
            run = False
            print('Game not found')
            break
        if game.both_went():
            redraw_window()
            pygame.time.delay(500)
            try:
                game = n.send('reset')
            except:
                run = False
                print('Game not found')
                break

            font =  pygame.font.SysFont('comicsans', 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render('You Won!', 1, (255, 0, 0))
            elif game.winner() == -1:
                text = font.render('Tie Game!', 1, (255, 0, 0))
            else:
                text = font.render('You Lost!', 1, (255, 0, 0))

            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():

if __name__ == '__main__':
    main()