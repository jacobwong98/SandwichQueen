import pygame, sys, time, random
from pygame.locals import *
from leastCostPath import *

# User-defined classes
class Player:
    def __init__(self, surface):
        self.surface = surface
        self.startX = 102
        self.startY = 102
        self.rect = [self.startX, self.startY, 98, 98]
        self.color = pygame.Color('white')
        self.holding = False

    def draw(self, Color):
        pygame.draw.rect(self.surface, Color, self.rect)

    def isHolding(self):
        self.holding = True

    def notHolding(self):
        self.holding = False

class Game:
    backColor = pygame.Color('red')
    charColor = pygame.Color('blue')
    def __init__(self, surface):
        self.surface = surface
        self.exit = False
        self.cont = True
        self.player = Player(self.surface)
        self.graph, self.location = load_graph('country-roads.txt')
        self.cost = CostDistance(self.location)

    def draw(self):
        self.player.draw(Game.backColor)
        pygame.display.update()

    def playGame(self):
        self.draw()
        # clock = pygame.time.Clock()
        # counter, text = 60, '60'.rjust(2)
        # pygame.time.set_timer(pygame.USEREVENT, 1000)
        # font = pygame.font.SysFont('Consolas', 10)
        while not self.exit:
            if self.cont:
                self.events()
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
                # graph, location = load_graph('country-roads.txt')
                # cost = CostDistance(location)
                start = None
                end = None
                startCoord = [self.player.startX, self.player.startY]
                x, y = pygame.mouse.get_pos()
                x -= (x % 100) - 2
                y -= (y % 100) - 2
                endCoord = [int(x), int(y)]
                start, end = findmin(startCoord, endCoord, self.location)
                reached = least_cost_path(self.graph, start, end, self.cost)
                print(reached)
                if len(reached) > 0:
                    for i in range(len(reached)):
                        self.player.draw(Game.charColor)
                        point = self.location[reached.pop(0)]
                        self.player.startX = point[0]
                        self.player.startY = point[1]
                        self.player.rect = [self.player.startX, self.player.startY, 98, 98]
                        self.player.draw(Game.backColor)
                # self.player.startX = x + 2
                # self.player.startY = y + 2
                # self.player.rect = [self.player.startX, self.player.startY, 98, 98]
                # self.player.draw(Game.backColor)

    def update(self):
        # Put the customers timer here
        # Put the cooking/cutting timer here
        self.draw()
def main():
    # Initialize pygame
    pygame.init()

    # Create the window
    surface = pygame.display.set_mode((800, 600), 0, 0)
    pygame.display.set_caption('Sandwich Queen (Not copyright)')
    # Draw the game board grid
    for i in range(1, 8):
        pygame.draw.line(surface, pygame.Color('white'), (100*i, 0), (100*i, 600), 2)
    for j in range(0, 6):
        pygame.draw.line(surface, pygame.Color('white'), (0, 100*j), (800, 100*j), 2)

    # create and initialize objects
    gameOver = False
    game = Game(surface)
    # Start cooking
    game.playGame()
    # Quit if we get to this point
    pygame.quit()

main()
