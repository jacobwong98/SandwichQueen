import pygame, sys, time, random
from pygame.locals import *

# Class deals with the drawing of the player
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

# These classes will be used to identify what to do depending on which tile was
# selected by the user and will add the desired result to the player's hands
# This class is for the empty tiles and arrow tiles
class Empty:
    def addHands(self, inHands, holding):
        return inHands, holding
# Class for when the user selects the meat tile
class Meat:
    def addHands(self, inHands, holding):
        # Check if the user is holding anything
        if holding:
            # Return whatever they were holding because you can't hold multiple
            # items in your hands
            return inHands, holding
        # Otherwise their hands are empty
        else:
            # Put rawmeat in the player's hands and true that they are holding something
            return "rawmeat", True
# Class for when the user selects the cheese tile
class Cheese:
    def addHands(self, inHands, holding):
        # Check if the user is holding anything
        if holding:
            # Return whatever they are already holding
            return inHands, holding
        # Otherwise their hands are empty
        else:
            # Put cheese in the player's hands and true that they are holding something
            return "cheese", True
# Class for when the user selects the lettuce tile
class Lettuce:
    def addHands(self, inHands, holding):
        # Check if the user is holding anything
        if holding:
            # Return whatever they are already holding
            return inHands, holding
        # Otherwise their hands are empty
        else:
            # Put lettucehead into user's hands and true that they are holding something
            return "lettucehead", True
# Class for when the user selects the tomato tile
class Tomato:
    def addHands(self, inHands, holding):
        # Check if the user is holding anything
        if holding:
            # Return whatever they are already holding
            return inHands, holding
        # Otherwise their hands are empty
        else:
            # Put wholetomato into the user's hands and true that they are holding something
            return "wholetomato", True
# Class for when the user selects the grill tile
class Grill:
    def addHands(self, inHands, holding):
        # Check if the user is holding anything
        if holding:
            # Check if the item in their hands is rawmeat because that is the
            # only ingredient that can be cooked is rawmeat
            if inHands == "rawmeat":
                # "Cook" the raw meat
                inHands = "cookedmeat"
        # Return the result which could be the user's original ingredient or
        # the cooked meat if the conditions match
        return inHands, holding
# Class for when the user selects the cutting board tile
class Board:
    def addHands(self, inHands, holding):
        # Check if the user is holding anything
        if holding:
            # Check if the item the user has in their hands is uncut lettuce a.k.a lettucehead
            if inHands == "lettucehead":
                # "Cut" the lettuce
                inHands = "cutlettuce"
            # Check if the item the user has in their hands is uncut tomato a.k.a wholetomato
            elif inHands == "wholetomato":
                # "Cut" the tomato
                inHands = "cuttomato"
        # Return the user's original ingredient, cutlettuce or cuttomato if the conditions match
        return inHands, holding
# Class for when the user selects the garbage tile
class Garbage:
    def addHands(self, inHands, holding):
        # No matter what is in the user's hands, clear their hands
        return None, False
# Class for when the user selects the customer tile
class Customer:
    def __init__(self):
        self.plate = []
        self.ingredients = ["cookedmeat", "cutlettuce", "cuttomato","cheese","rawmeat","lettucehead","wholetomato"]
    # Create a random order from the ingredients list
    def createOrder(self):
        # Go through the list of ingredients
        for i in self.ingredients:
            # Generate a random number
            num = random.randint(0, 2398498234)
            # Perform the modular on this number and add to the list if it's
            # modular equals the randomly selected value of 0 or 1
            if num%2 == random.randint(0, 1):
                # Add the item to the customer's plate
                self.plate.append(i)
        # Return the customer's order
        return self.plate
