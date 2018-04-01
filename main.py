import pygame, sys, time, random
from pygame.locals import *
# from graph import Graph
# from binaryHeap import BinaryHeap
from leastCostPath import *

# User-defined classes
class Player:
    chefColor = pygame.Color('white')
    width = 100
    height = 100
    startX = 100
    startY = 100
    def __init__(self, surface):
        self.surface = surface
        self.rect = [Player.startX, Player.startY, Player.width, Player.height]
        self.color = Player.chefColor
        self.holding = False

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect, 0)

    def isHolding(self):
        self.holding = True

    def notHolding(self):
        self.holding = False

class Game:
    backColor = pygame.Color('black')

    def __init__(self, surface):
        self.surface = surface

    def draw(self):
        player = Player(self.surface)
        player.draw()

    def update(self):
        if False:
            return True
        else:
            self.draw()
            return False
def main():
    # Initialize pygame
    pygame.init()

    # Set window size and title, and frame delay
    surfaceSize = (800, 600)
    Title = 'Sandwich Queen (Not copyright)'
    pauseTime = 0.01 # smaller is faster game

    # Create the window
    surface = pygame.display.set_mode(surfaceSize, 0, 0)
    pygame.display.set_caption(Title)

    # create and initialize objects
    gameOver = False
    game = Game(surface)
    player = Player(surface)
    game.draw()
    pygame.display.update()

    # Draw the game board grid
    for i in range(1, 8):
        pygame.draw.line(surface, pygame.Color('white'), (100*i, 0), (100*i, 600), 2)
    for j in range(0, 6):
        pygame.draw.line(surface, pygame.Color('white'), (0, 100*j), (800, 100*j), 2)

    # Refresh the display
    pygame.display.update()

    # Loop forever
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Handle additional events
            if event.type == MOUSEBUTTONUP and not gameOver:
                pygame.draw.rect(surface, pygame.Color('black'),[player.startX + 2, player.startY + 2, player.width - 2, player.height - 2], 0)
                x, y = pygame.mouse.get_pos()
                x -= (x % 100) - 50
                y -= (y % 100) - 50
                player.startX = x - 50
                player.startY = y - 50
                player.draw()

        # Update and draw objects for next frame
        gameOver = game.update()

        # Refresh the display
        pygame.display.update()

        # Set the frame speed by pausing between frames
        time.sleep(pauseTime)

main()
