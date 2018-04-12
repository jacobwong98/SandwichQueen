import pygame, sys, time, random
from pygame.locals import *
from leastCostPath import *
from characters import *
from environment import *

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
        # Draw the player and environment after each time delay in playGame
        self.player.draw()
        self.environment.draw()
        # Update the pygame display with these new drawings
        pygame.display.update()

    # This function will play the game
    def playGame(self):
        self.draw() # Draw initial environment and player in case it isn't already drawn
        while not self.exit:
            if self.cont:
                self.events() # Check if the mouse has been clicked
                self.update() # Update the timer on screen
            self.draw() # Redraw any changed conditions
            time.sleep(0.01) # Delay for 0.01 seconds

    # Function will handle the events that occur in pygame
    def events(self):
        # Get the events that occur in pygame
        for event in pygame.event.get():
            # User has clicked on the exit sign of the window
            if event.type == QUIT:
                self.exit = True
                pygame.quit()
                sys.exit()
            # User has clicked somewhere on the game board
            if event.type == MOUSEBUTTONUP and self.cont:
                # Get the least cost path from user's click
                self.getPath()

    # Function will determine the least cost path from the user's selected destination
    def getPath(self):
        start = None
        end = None
        startCoord = [self.player.startX, self.player.startY]
        x, y = pygame.mouse.get_pos() # Get the user's selected destination
        x -= (x % 100) - 2 # Performs math that will get the top left corner
        y -= (y % 100) - 2 # Same as above line of code but for y-coordinate
        endCoord = [int(x), int(y)]
        # Find the nearest vertices from the country-roads.txt file and returns
        # the unique identifiers of the start and end vertices
        start, end = findmin(startCoord, endCoord, self.location)
        # Find the least cost path from the identifiers that were found above
        reached = least_cost_path(self.graph, start, end, self.cost)
        # If the length of reached is 0, no path is found or we are already at
        # our destination so we don't need to go anywhere
        if len(reached) > 0:
            # Go through the reached list and draw the next location
            for i in range(len(reached)):
                # Draw a black square over the current players location
                pygame.draw.rect(self.surface,Game.backColor,self.player.rect)
                # Get the coordinates of the next vertex to travel to
                point = self.location[reached.pop(0)]
                # Change the variables to the new location
                self.player.startX = point[0]
                self.player.startY = point[1]
                self.player.rect = [self.player.startX, self.player.startY, 98, 98]
                # Draw the player in this new location
                self.player.draw()
        self.checkTile(x, y)

    def checkTile(self, x, y):
        # Handles which square has been clicked on
        # Check if the square that was clicked on is the Plate
        if self.environment.matrix[int((x-2)/100)][int((y-2)/100)] == 9:
            # Check if the player is holding anything
            if self.player.holding:
                # Add whatever they are holding onto the plate
                self.plate.append(self.player.inHands)
                # "Empty" the player's hands
                self.player.holding = False
                self.player.inHands = None
            # Else they are not holding anything
            else:
                # Add whatever is on the plate right now into the player's hands
                self.player.inHands = self.plate
                # Clear the plate
                self.plate = []
                self.player.holding = True
        # Check if the square that was clicked on is the Customer
        elif self.environment.matrix[int((x-2)/100)][int((y-2)/100)] == 8:
            # Check if the player is holding anything
            if self.player.holding:
                counter = 0
                # Sort the customer's order and the item(s) in the player's hands
                sortedPlate = sorted(self.player.inHands)
                sortedOrder = sorted(self.customerOrder)
                # If their length's don't match, we already know the order and
                # what the player brings will not match anyways
                if len(sortedPlate) != len(sortedOrder):
                    pass
                else:
                    # Go through the length of the customer's plate(the length should match)
                    for i in range(len(sortedPlate)):
                        # If the item we are looking at match, increase counter
                        if sortedPlate[i] == sortedOrder[i]:
                            counter += 1
                            # If our counter equals the length of the order
                            # then the order and plate match
                            if counter == len(sortedOrder):
                                # Should break out of our infinite loop
                                self.exit = True
                        # If the elements don't match then stop counting because
                        # order doesn't match
                        else:
                            break
        # If the square that was clicked on was not the Customer or Plate
        # need to determine what the player has clicked on
        else:
            # Need to determine the type of square that the user has clicked on
            self.player.temp = self.environment.getClass(int((x-2)/100), int((y-2)/100))
            # Add/Remove whatever the user has clicked on to their hands if it
            # was an ingredient, garbage or an empty tile
            self.player.inHands, self.player.holding = self.player.temp.addHands(self.player.inHands, self.player.holding)
        # Print what the user is holding
        print(self.player.inHands)

    # Function will update any other elements that we need to update
    def update(self):
        # Update the timer a.k.a the score
        self.environment.drawTimer(self.customerOrder)
def main():
    # Initialize pygame
    pygame.init()

    mode = 1
    # Create the window
    surface = pygame.display.set_mode((800, 600), 0, 0)
    pygame.display.set_caption('Sandwich Queen (Not copyright)')
    while True:
        # Mode 1: Game play mode
        if mode == 1:
            # create and initialize objects
            environment = Environment(surface)
            game = Game(surface)
            # Draw the game board grid
            environment.drawBoard()
            # Start cooking
            game.playGame()
            # Change to the Win Screen Mode
            mode = 0
        # Mode should equal 0 which represents the Win Screen
        else:
            mode = environment.displayWin()
            # Once the user presses the enter key to play again, the mode
            # will change to the game play mode and we want to redraw the game
            # board just in case 
            if mode == 1:
                environment.drawBoard()
main()
