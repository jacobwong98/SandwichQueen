import pygame, sys, time, random
from pygame.locals import *

class Player:
    chef = pygame.image.load('../Images/chef.png')
    def __init__(self, surface):
        self.surface = surface
        self.startX = 102
        self.startY = 102
        self.rect = [self.startX, self.startY, 98, 98]
        self.color = pygame.Color('white')
        self.holding = False
        self.inHands = None
        self.temp = None
    # Function will draw the player depending on their location
    def draw(self):
        self.surface.blit(Player.chef,(self.startX, self.startY))


class Empty:
    def addHands(self, inHands, holding):
        return inHands, holding
class Meat:
    def addHands(self, inHands, holding):
        if holding:
            return inHands, holding
        else:
            return "rawmeat", True
class Cheese:
    def addHands(self, inHands, holding):
        if holding:
            return inHands, holding
        else:
            return "cheese", True
class Lettuce:
    def addHands(self, inHands, holding):
        if holding:
            return inHands, holding
        else:
            return "lettucehead", True
class Tomato:
    def addHands(self, inHands, holding):
        if holding:
            return inHands, holding
        else:
            return "wholetomato", True
class Grill:
    def addHands(self, inHands, holding):
        if holding:
            if inHands == "rawmeat":
                inHands = "cookedmeat"
        return inHands, holding
class Board:
    def addHands(self, inHands, holding):
        if holding:
            if inHands == "lettucehead":
                inHands = "cutlettuce"
            elif inHands == "wholetomato":
                inHands = "cuttomato"
        return inHands, holding
class Garbage:
    def addHands(self, inHands, holding):
        return None, False
class Customer:
    def __init__(self):
        self.plate = []
        self.ingredients = ["cookedmeat", "cutlettuce", "cuttomato","cheese","rawmeat","lettucehead","wholetomato"]
    def createOrder(self):
        for i in self.ingredients:
            num = random.randint(0, 2398498234)
            if num%2 == random.randint(0, 1):
                self.plate.append(i)
        return self.plate

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
        self.matrix = [[9,0,0,0,0,0],[0,0,0,0,0,0],[0,0,1,2,0,5],[0,0,0,3,0,0],
        [0,0,0,4,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[8,0,6,0,0,7]]
        self.dict = dict([(0,Empty()),(1,Meat()),(2, Cheese()),
        (3, Lettuce()),(4, Tomato()),(5, Grill()),(6, Board()),
        (7, Garbage())])

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

    def getClass(self, x, y):
        k = self.matrix[x][y]
        for key, val in self.dict.items():
            if k == key:
                return val

    def drawTimer(self, order):
        font = pygame.font.SysFont(None, 60, True)
        time = pygame.time.get_ticks() // 1000 # divide to convert to seconds
        textSurface = font.render(str(time), True, pygame.Color('white'), pygame.Color('black'))
        self.surface.blit(textSurface, (510,10))

        fontOrder = pygame.font.SysFont(None, 15, True)
        for i in range(len(order)):
            textSurfaceOrder = fontOrder.render(order[i], True, pygame.Color('white'), pygame.Color('black'))
            self.surface.blit(textSurfaceOrder, (602, i*10+2))

    def drawBoard(self):
        for i in range(1, 8):
            pygame.draw.line(self.surface, pygame.Color('white'), (100*i, 0), (100*i, 600), 2)
        for j in range(0, 6):
            pygame.draw.line(self.surface, pygame.Color('white'), (0, 100*j), (800, 100*j), 2)
