import pygame, sys, time, random
from pygame.locals import *
from characters import *


# Class deals with any elements in the environment of the game
class Environment:
    # Load all the images that are used
    upArrow = pygame.image.load('../Images/arrowup.png')
    downArrow = pygame.image.load('../Images/arrowdown.png')
    leftArrow = pygame.image.load('../Images/arrowleft.png')
    rightArrow = pygame.image.load('../Images/arrowright.png')
    lettuce = pygame.image.load('../Images/Lettuce.png')
    tomato = pygame.image.load('../Images/tomato.png')
    customer = pygame.image.load('../Images/customer.png')
    meat = pygame.image.load('../Images/meat.png')
    plate = pygame.image.load('../Images/plate.png')
    grill = pygame.image.load('../Images/grill.png')
    cheese = pygame.image.load('../Images/cheese.png')
    garbage = pygame.image.load('../Images/garbage.png')
    cuttingboard = pygame.image.load('../Images/cuttingboard.png')
    def __init__(self, surface):
        self.surface = surface
        # This matrix represents the game board in terms of each items identifier
        # that is defined in the dictionary
        self.matrix = [[9,0,0,0,0,0],[0,0,0,0,0,0],[0,0,1,2,0,5],[0,0,0,3,0,0],
        [0,0,0,4,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[8,0,6,0,0,7]]
        self.dict = dict([(0,Empty()),(1,Meat()),(2, Cheese()),
        (3, Lettuce()),(4, Tomato()),(5, Grill()),(6, Board()),
        (7, Garbage())])
    # Draw all the ingredients, arrows and other aspects on the screen
    def draw(self):
        self.surface.blit(Environment.downArrow, (102,302))
        self.surface.blit(Environment.rightArrow, (2,102))
        self.surface.blit(Environment.rightArrow, (202,102))
        self.surface.blit(Environment.rightArrow, (402,102))
        self.surface.blit(Environment.rightArrow, (402,402))
        self.surface.blit(Environment.lettuce, (302, 302))
        self.surface.blit(Environment.tomato, (402,302))
        self.surface.blit(Environment.customer, (702, 2))
        self.surface.blit(Environment.meat, (202, 202))
        self.surface.blit(Environment.plate, (2,2))
        self.surface.blit(Environment.grill, (202, 502))
        self.surface.blit(Environment.cheese, (202, 302))
        self.surface.blit(Environment.garbage, (702, 502))
        self.surface.blit(Environment.cuttingboard, (702,202))
        self.surface.blit(Environment.leftArrow, (402,2))
    # This function will determine the type of tile that was clicked on by the user
    def getClass(self, x, y):
        # Based on the coordinates x,y index into the 2D matrix to determine the type of tile selected
        k = self.matrix[x][y]
        for key, val in self.dict.items():
            # If our selected id matches the key from the dictionary we found our class
            if k == key:
                # Return the class that was selected
                return val
    # This function will draw the timer on board as well as the customer's order
    def drawTimer(self, order):
        # Determine a font size
        font = pygame.font.SysFont(None, 60, True)
        # Get the current time
        time = pygame.time.get_ticks() // 1000
        # Create a text surface that is to be drawn on the screen
        textSurface = font.render(str(time), True, pygame.Color('white'), pygame.Color('black'))
        # Draw the timer on the screen
        self.surface.blit(textSurface, (510,10))
        # Determine a font size for the customer's order
        fontOrder = pygame.font.SysFont(None, 15, True)
        # Go through the customer's print each ingredient
        for i in range(len(order)):
            textSurfaceOrder = fontOrder.render(order[i], True, pygame.Color('white'), pygame.Color('black'))
            self.surface.blit(textSurfaceOrder, (602, i*10+2))
    # This function will draw the game board which is a grid
    def drawBoard(self):
        # Draw the column lines
        for i in range(1, 8):
            pygame.draw.line(self.surface, pygame.Color('white'), (100*i, 0), (100*i, 600), 2)
        # Draw the row lines
        for j in range(0, 6):
            pygame.draw.line(self.surface, pygame.Color('white'), (0, 100*j), (800, 100*j), 2)
