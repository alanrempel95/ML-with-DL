# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 19:55:09 2020

@author: Alan
"""
# Simple pygame program

# Import and initialize the pygame library
import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN,
)

pygame.init()

#scale variable
canvas_width = 300
cross_check = (False, "empty")
nought_check = (False, "empty")

# Set up the drawing window
screen = pygame.display.set_mode([canvas_width, canvas_width])
pygame.display.set_caption("The Tick-Tackiest!")
font = pygame.font.SysFont("Arial", 18)
c_string = ""

board_tiles = [["e", "e", "e"], ["e", "e", "e"], ["e", "e", "e"]]
current_piece = "nought" #what is currently being placed onclick

def drawNought(x_ind, y_ind):
    # Draw a nought. x_ind e in [0, 1, 2]
    x_coord = canvas_width * (x_ind / 3 + 1 / 6)
    y_coord = canvas_width * (y_ind / 3 + 1 / 6)
    pygame.draw.circle(screen, (0, 0, 255), (x_coord, y_coord), canvas_width / 8)
    pygame.draw.circle(screen, (255, 255, 255), (x_coord, y_coord), canvas_width / 12)

def drawCross(x_ind, y_ind):
    # Draw a cross. x_ind e in [0, 1, 2]
    outer_width = canvas_width / 8
    inner_width = canvas_width / 20
    x_coord = canvas_width * (x_ind / 3 + 1 / 6)
    y_coord = canvas_width * (y_ind / 3 + 1 / 6)
    #points are clockwise from top left
    pygame.draw.polygon(screen, (0, 0, 255), [(x_coord - outer_width, y_coord - outer_width),(x_coord, y_coord - inner_width),(x_coord + outer_width, y_coord - outer_width),(x_coord + inner_width, y_coord),(x_coord + outer_width, y_coord + outer_width),(x_coord, y_coord + inner_width),(x_coord - outer_width, y_coord + outer_width),(x_coord - inner_width, y_coord)])   

def checkVictory(piece_type):
    #there is certainly a more elegant way to do this
    victory = False
    victory_index = "empty"
    if board_tiles[0][0] == piece_type and board_tiles[0][1] == piece_type and board_tiles[0][2] == piece_type:
        #top row victory
        victory = True
        victory_index = "top row"
    if board_tiles[1][0] == piece_type and board_tiles[1][1] == piece_type and board_tiles[1][2] == piece_type:
        #center row victory
        victory = True
        victory_index = "center row"
    if board_tiles[2][0] == piece_type and board_tiles[2][1] == piece_type and board_tiles[2][2] == piece_type:
        #bottom row victory
        victory = True
        victory_index = "bottom row"
    if board_tiles[0][0] == piece_type and board_tiles[1][0] == piece_type and board_tiles[2][0] == piece_type:
        #left column victory
        victory = True
        victory_index = "left column"
    if board_tiles[0][1] == piece_type and board_tiles[1][1] == piece_type and board_tiles[2][1] == piece_type:
        #center column victory
        victory = True
        victory_index = "center column"
    if board_tiles[0][2] == piece_type and board_tiles[1][2] == piece_type and board_tiles[2][2] == piece_type:
        #right column victory
        victory = True
        victory_index = "right column"
    if board_tiles[0][0] == piece_type and board_tiles[1][1] == piece_type and board_tiles[2][2] == piece_type:
        #down diagonal victory
        victory = True
        victory_index = "down diagonal"
    if board_tiles[2][0] == piece_type and board_tiles[1][1] == piece_type and board_tiles[0][2] == piece_type:
        #up diagonal victory
        victory = True
        victory_index = "up diagonal"
    return victory, victory_index

def celebrate(piece_type, victory_index):
    bar_width = canvas_width / 10
    celebrate_string = ""
    if victory_index == "top row":
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0, canvas_width / 6 - bar_width / 2, canvas_width, bar_width))
    elif victory_index == "center row":
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0, canvas_width / 2 - bar_width / 2, canvas_width, bar_width))
    elif victory_index == "bottom row":
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0, canvas_width * 5 / 6 - bar_width / 2, canvas_width, bar_width))
    elif victory_index == "left column":
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(canvas_width / 6 - bar_width / 2, 0, bar_width, canvas_width))
    elif victory_index == "center column":
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(canvas_width / 2 - bar_width / 2, 0, bar_width, canvas_width))
    elif victory_index == "right column":
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(canvas_width * 5 / 6 - bar_width / 2, 0, bar_width, canvas_width))
    elif victory_index == "down diagonal":
        pygame.draw.polygon(screen, (255, 0, 0), [(bar_width / 2, 0), (canvas_width, canvas_width - bar_width / 2), (canvas_width - bar_width / 2, canvas_width), (0, bar_width / 2)])
    elif victory_index == "up diagonal":
        pygame.draw.polygon(screen, (255, 0, 0), [(canvas_width - bar_width / 2, 0), (0, canvas_width - bar_width / 2), (bar_width / 2, canvas_width), (canvas_width, bar_width / 2)])
    celebrate_string = piece_type + " wins with " + victory_index
    return celebrate_string
    #print(celebrate_string)

def restart():
    for i in range(3):
        for j in range(3):
            board_tiles[i][j] = "e"
    #why are these global variables considered local
    c_string = ""
    cross_check = (False, "")
    nought_check = (False, "")

# Run until the user asks to quit
running = True
while running:
    
    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw game grid lines
    pygame.draw.line(screen, (0,0,0), (canvas_width / 3, 0), (canvas_width / 3, canvas_width))
    pygame.draw.line(screen, (0,0,0), (canvas_width * 2 / 3, 0), (canvas_width * 2 / 3, canvas_width))
    pygame.draw.line(screen, (0,0,0), (0, canvas_width / 3), (canvas_width, canvas_width / 3))
    pygame.draw.line(screen, (0,0,0), (0, canvas_width * 2 / 3), (canvas_width, canvas_width * 2 / 3))

    #drawNought(1, 2)
    #drawCross(0, 1)
    
    for i in range(3):
        for j in range(3):
            if(board_tiles[i][j] == "nought"):
                drawNought(j, i)
            elif(board_tiles[i][j] == "cross"):
                drawCross(j, i)
                
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                restart()
        elif event.type == MOUSEBUTTONDOWN:
            #based on mouse position, assign piece location
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] < canvas_width / 3:
                piece_x = 0
            elif mouse_pos[0] >= canvas_width / 3 and mouse_pos[0] <= canvas_width * 2 / 3:
                piece_x = 1
            else:
                piece_x = 2
            if mouse_pos[1] < canvas_width / 3:
                piece_y = 0
            elif mouse_pos[1] >= canvas_width / 3 and mouse_pos[1] <= canvas_width * 2 / 3:
                piece_y = 1
            else:
                piece_y = 2
            #if the location is empty, place & switch turn
            if board_tiles[piece_y][piece_x] == "e":
                board_tiles[piece_y][piece_x] = current_piece
                if current_piece == "nought":
                    current_piece = "cross"
                else:
                    current_piece = "nought"
                    
            cross_check = checkVictory("cross")
            nought_check = checkVictory("nought")
    
    #render victory text to the screen
    if cross_check[0]:
        #print("Cross Wins in " + cross_check[1])
        c_string = celebrate("cross", cross_check[1])
    elif nought_check[0]:
        #print("Nought Wins in " + nought_check[1])
        c_string = celebrate("nought", nought_check[1])
    
    text = font.render(c_string, True, (0, 255, 0))
    textRect = text.get_rect()
    textRect.center = (canvas_width / 2, canvas_width / 2)
    screen.blit(text, textRect)
    
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()