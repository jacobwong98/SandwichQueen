import pygame, sys, time, random
from pygame.locals import *
from leastCostPath import *
from characters import *

class Game:
    charColor = pygame.Color('red')
    backColor = pygame.Color('black')
    def __init__(self, surface):
        self.surface = surface
        self.exit = False
        self.cont = True
        self.player = Player(self.surface)
        self.environment = Environment(self.surface)
        self.plate = []
        self.customer = Customer()
        self.customerOrder = self.customer.createOrder()
        self.graph, self.location = load_graph('country-roads.txt')
        self.cost = CostDistance(self.location)

    def draw(self):
        self.player.draw(Game.charColor)
        self.environment.draw()
        pygame.display.update()

    def playGame(self):
        self.draw()
        while not self.exit:
            if self.cont:
                self.events()
                self.update()
                # Check cond??
            self.draw()
            time.sleep(0.01)

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.exit = True
            if event.type == MOUSEBUTTONUP and self.cont:
                self.getPath()

    def getPath(self):
        start = None
        end = None
        startCoord = [self.player.startX, self.player.startY]
        x, y = pygame.mouse.get_pos()
        x -= (x % 100) - 2
        y -= (y % 100) - 2
        endCoord = [int(x), int(y)]
        start, end = findmin(startCoord, endCoord, self.location)
        reached = least_cost_path(self.graph, start, end, self.cost)

        if len(reached) > 0:
            for i in range(len(reached)):
                self.player.draw(Game.backColor)
                point = self.location[reached.pop(0)]
                self.player.startX = point[0]
                self.player.startY = point[1]
                self.player.rect = [self.player.startX, self.player.startY, 98, 98]
                self.player.draw(Game.charColor)

        if self.environment.matrix[int((x-2)/100)][int((y-2)/100)] == 9:
            #Plate
            if self.player.holding:
                self.plate.append(self.player.inHands)
                self.player.holding = False
                self.player.inHands = None
            else:
                self.player.inHands = self.plate
                self.plate = []
                self.player.holding = True
        elif self.environment.matrix[int((x-2)/100)][int((y-2)/100)] == 8:
            #Customer
            print(self.customerOrder)
            if self.player.holding:
                counter = 0
                sortedPlate = sorted(self.player.inHands)
                sortedOrder = sorted(self.customerOrder)
                if len(sortedPlate) != len(sortedOrder):
                    pass
                else:
                    for i in range(len(sortedPlate)):
                        if sortedPlate[i] == sortedOrder[i]:
                            counter += 1
                            if counter == len(sortedOrder):
                                self.exit = True
                        else:
                            break
        else:
            self.player.temp = self.environment.getClass(int((x-2)/100), int((y-2)/100))
            self.player.inHands, self.player.holding = self.player.temp.addHands(self.player.inHands, self.player.holding)
        print(self.player.inHands, self.player.holding)
    def update(self):
        self.draw()
        self.environment.drawTimer(self.customerOrder)
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
    # pygame.quit()

main()
