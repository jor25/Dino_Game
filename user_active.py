# File made for human players to use and play the game.
# Controls are in this file
# 11-22-2019
import gen_dino_game as gdg
import pygame


def active_player(dino):
    keys = pygame.key.get_pressed()
    
    # Do nothing
    move = [1,0,0,0]

    # Go left
    if keys[pygame.K_LEFT] and dino.x > dino.vel:
        move = [0,1,0,0]
   
    # Go Right
    elif keys[pygame.K_RIGHT] and dino.x < gdg.G_screen_width - (dino.w + dino.vel):
        move = [0,0,1,0]

    #if dino.jumping:    # Testing this case...
    #    move = [0,0,0,1]
    if not dino.jumping:
        # Jump if you can jump
        if keys[pygame.K_UP]:
            move = [0,0,0,1]

    return move
