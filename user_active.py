import gen_dino_game as gdg
import pygame

def active_player(DINO):
    keys = pygame.key.get_pressed()
    
    # Do nothing
    move = [1,0,0,0]

    # Go left
    if keys[pygame.K_LEFT] and DINO.x > DINO.vel:
        move = [0,1,0,0]
   
    # Go Right
    elif keys[pygame.K_RIGHT] and DINO.x < gdg.G_screen_width - (DINO.w + DINO.vel):
        move = [0,0,1,0]

    if not DINO.jumping:
        # Jump if you can jump
        if keys[pygame.K_UP]:
            move = [0,0,0,1]

    return move
