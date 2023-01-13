from board import boards
import pygame
import math

pygame.init()

WIDTH = 750
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()            #Control the speed at which the game runs
fps = 60           #Maximum speed at which the game can be played
font = pygame.font.Font('freesansbold.ttf',20)
level = boards          #The board can be changed for different levels
color = 'blue'
PI = math.pi            #Used for radial commands

def draw_board():            #Specificatoins of the board itself
    num1 = ((HEIGHT - 50)//32)          #-50 to get a boarder and divide by 32 to get how tall each piece should be
    num2 = (WIDTH // 30)            #Floor division (//) always makes it a integer
    for i in range(len(level)):            #A loop that iterates through every single row in the level
        for j in range(len(level[i])):          #A loop that iterates through every single column in the level (easiers way to go through every single tile in the program)
            if level[i][j] == 1:            #Little dot
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)          #(surface, colour, the colunm number + the middle of the spot, the row number + the middle of the spot, radius)
            if level[i][j] == 2:            #Big dot
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)         #(surface, colour, the colunm number + the middle of the spot, the row number + the middle of the spot, radius)
            if level[i][j] == 3:            #Vertical line
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1), (j * num2 + (0.5 * num2), i * num1 + num1), 3)         #(surface, color variable, start the line at the top of the tile, going from the top of the square to the bottom of the square, line thickness)
            if level[i][j] == 4:            #Horizontal line
                pygame.draw.line(screen, color, (j * num2 , i * num1 + (0.5 * num1)), ((j * num2 + num2), i * num1 + (0.5 * num1)), 3)         #(surface, color variable, start the line at the top of the tile, going from the top of the square to the bottom of the square, line thickness)
            if level[i][j] == 5:            #Top Right corner
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4) - 2), (i * num1 + (0.5 * num1)), num2, num1], 0, PI/2, 3)            #(surface, color, starting position of the arc, statrting part of the circle, ending part of the circle, line thickness)
            if level[i][j] == 6:            #Top Left corner
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI/2, PI, 3)            #(surface, color, starting position of the arc, statrting part of the circle, ending part of the circle, line thickness)
            if level[i][j] == 7:            #Bottom Left corner
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI, 3*PI/2, 3)            #(surface, color, starting position of the arc, statrting part of the circle, ending part of the circle, line thickness)
            if level[i][j] == 8:            #Bottom Right corner
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4) - 2), (i * num1 - (0.4 * num1)), num2, num1], 3*PI/2, 2*PI, 3)            #(surface, color, starting position of the arc, statrting part of the circle, ending part of the circle, line thickness)
            if level[i][j] == 9:            #Horizontal line (ghost door)
                pygame.draw.line(screen, 'white', (j * num2 , i * num1 + (0.5 * num1)), ((j * num2 + num2), i * num1 + (0.5 * num1)), 3)         #(surface, color variable, start the line at the top of the tile, going from the top of the square to the bottom of the square, line thickness)

run = True
while run:
     timer.tick(fps)
     screen.fill('black')
     draw_board()

     for event in pygame.event.get():           #Event handling that the pi game has which gets everything happening to your computer
         if event.type == pygame.QUIT:
             run = False
     pygame.display.flip()          #Let everything drawn on the screen be iterated
pygame.quit