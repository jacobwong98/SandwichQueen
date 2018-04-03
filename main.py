import pygame, sys, time, random
from pygame.locals import *
from leastCostPath import *

# User-defined classes
class Player:
    def __init__(self, surface):
        self.surface = surface
        self.rect = Rect(102, 102, 98, 98)
        self.color = pygame.Color('white')
        self.holding = False

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)

    def isHolding(self):
        self.holding = True

    def notHolding(self):
        self.holding = False

class Game:
    def __init__(self, surface, charColor, backColor):
        self.surface = surface
        self.exit = False
        self.cont = True
        self.charcolor = charColor
        self.backcolor = backColor
        self.player = Player(self.surface)

    def draw(self):
        self.player.draw()
        pygame.display.update()

    def playGame(self):
        self.draw()
        # clock = pygame.time.Clock()
        # counter, text = 60, '60'.rjust(2)
        # pygame.time.set_timer(pygame.USEREVENT, 1000)
        # font = pygame.font.SysFont('Consolas', 10)
        while not self.exit:
            self.events()
            if self.cont:
                # for event in pygame.event.get():
                #     if event.type == pygame.USEREVENT:
                #         counter -= 1
                #         if counter > 0:
                #             text = str(counter).rjust(2)
                #         else:
                #             text = 'game'.rjust(2)
                #         self.surface.blit(font.render(text, True, (255,255,255)), (750,50))
                #         pygame.display.flip()
                #         clock.tick(60)
                self.update()
                # Check cond??
            self.draw()
            time.sleep(0.01)

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.exit = True
            if event.type == MOUSEBUTTONUP and self.cont:
                pygame.draw.rect(self.surface, self.backcolor,self.player.rect, 0)
                x, y = pygame.mouse.get_pos()
                x -= (x % 100) - 50
                y -= (y % 100) - 50
                # self.player.startX = x - 48
                # self.player.startY = y - 48
                # self.player.draw(self.charcolor)

    def update(self):
        # Put the customers timer here
        # Put the cooking/cutting timer here
        pass
def main():
    # Initialize pygame
    pygame.init()

    # Create the window
    surface = pygame.display.set_mode((800, 600), 0, 0)
    backColor = pygame.Color('red')
    charColor = pygame.Color('white')
    pygame.display.set_caption('Sandwich Queen (Not copyright)')
    # Draw the game board grid
    for i in range(1, 8):
        pygame.draw.line(surface, pygame.Color('white'), (100*i, 0), (100*i, 600), 2)
    for j in range(0, 6):
        pygame.draw.line(surface, pygame.Color('white'), (0, 100*j), (800, 100*j), 2)

    # create and initialize objects
    gameOver = False
    game = Game(surface, charColor, backColor)
    # Start cooking
    game.playGame()
    # Quit if we get to this point
    pygame.quit()

main()
