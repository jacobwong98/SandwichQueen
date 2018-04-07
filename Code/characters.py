import pygame, sys, time, random
# import numpy
from pygame.locals import *

class Player:
    def __init__(self, surface):
        self.surface = surface
        self.startX = 102
        self.startY = 102
        self.rect = [self.startX, self.startY, 98, 98]
        self.color = pygame.Color('white')
        self.holding = False
        self.inHands = set()

    def draw(self, Color):
        pygame.draw.rect(self.surface, Color, self.rect)

    def isHolding(self):
        self.holding = True

    def notHolding(self):
        self.holding = False

class Environment:
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
        # self.matrix = numpy.full((6,8), 0)

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

    def drawTimer(self):
        # print(self.matrix)
        pass
