import pygame, sys, time, random
from pygame.locals import *

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

class Environment:
    upArrow = pygame.image.load('arrowup.png')
    downArrow = pygame.image.load('arrowdown.png')
    leftArrow = pygame.image.load('arrowleft.png')
    rightArrow = pygame.image.load('arrowright.png')
    def __init__(self, surface):
        self.surface = surface

    def draw(self):
        self.surface.blit(Environment.downArrow, (102,302))
        self.surface.blit(Environment.rightArrow, (2,102))
        self.surface.blit(Environment.rightArrow, (202,102))
        self.surface.blit(Environment.rightArrow, (402,102))
        self.surface.blit(Environment.rightArrow, (202,102))
        self.surface.blit(Environment.rightArrow, (402,402))
