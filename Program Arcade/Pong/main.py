import pygame
import ball
import paddle
import random

#colours
WHITE = [255,255,255]
BLACK = [0,0,0]
RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,255,0]

WW = 634
WH = 464

BALL_DIAMETER = 6
BALL_START_POSITION = [(WW/2)-(BALL_DIAMETER/2),(WH/2)-(BALL_DIAMETER/2)]
BALL_MAX_VELOCITYX = 1
BALL_VELOCITYY = 4

PADDLE_WIDTH = 50
PADDLE_HEIGHT = 5
PADDLE_START_POSITIONX = WW/2-PADDLE_WIDTH
PADDLE1_START_POSITIONY = 1
PADDLE2_START_POSITIONY = WH-PADDLE_HEIGHT-1
PADDLE_SPEED = 10

SCORE_SPACING = 50

WIN_LIMIT = 10

def create_objs(game_objs):
    new_ball = ball.ball(BALL_DIAMETER,WHITE,BALL_START_POSITION,BALL_MAX_VELOCITYX,BALL_VELOCITYY)
    paddle1 = paddle.paddle(PADDLE_WIDTH,PADDLE_HEIGHT,WHITE,PADDLE_START_POSITIONX,PADDLE1_START_POSITIONY)
    paddle2 = paddle.paddle(PADDLE_WIDTH,PADDLE_HEIGHT,WHITE,PADDLE_START_POSITIONX,PADDLE2_START_POSITIONY)
    screen = pygame.display.set_mode((WW,WH))
    game_objs['ball'] = new_ball
    game_objs['paddle1'] = paddle1
    game_objs['paddle2'] = paddle2
    game_objs['screen'] = screen
    return game_objs
    
def main():
    
    bg_img = pygame.image.load("megan_fox.jpg")
    ship_img = pygame.image.load("playerShip1_orange.png")
    click_sound = pygame.mixer.Sound("house_lo.ogg")
    
    font = pygame.font.Font(None,50)
    
    player1_score = 0
    player2_score = 0
    
    game_objs = {}
    game_objs = create_objs(game_objs)
    
    #mainloop
    playing = True
    while playing:
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
            elif event.type == pygame.KEYDOWN:
                # Figure out if it was an arrow key. If so
                # adjust speed.
                if event.key == pygame.K_LEFT:
                    game_objs['paddle2'].velocityx = -PADDLE_SPEED
                if event.key == pygame.K_RIGHT:
                    game_objs['paddle2'].velocityx = PADDLE_SPEED
                if event.key == pygame.K_a:
                    game_objs['paddle1'].velocityx = -PADDLE_SPEED
                if event.key == pygame.K_d:
                    game_objs['paddle1'].velocityx = PADDLE_SPEED
                 
            # User let up on a key
            elif event.type == pygame.KEYUP:
                # If it is an arrow key, reset vector back to zero
                if event.key == pygame.K_LEFT:
                    game_objs['paddle2'].velocityx = 0
                if event.key == pygame.K_RIGHT:
                    game_objs['paddle2'].velocityx = 0
                if event.key == pygame.K_a:
                    game_objs['paddle1'].velocityx = 0
                if event.key == pygame.K_d:
                    game_objs['paddle1'].velocityx = 0             
        
        #game logic
        
        next_paddle1_pos = game_objs['paddle1'].positionx + game_objs['paddle1'].velocityx
        next_paddle2_pos = game_objs['paddle2'].positionx + game_objs['paddle2'].velocityx
        
        if next_paddle1_pos < 0:
            game_objs['paddle1'].positionx = 0
        elif next_paddle1_pos > WW-PADDLE_WIDTH:
            game_objs['paddle1'].positionx = WW-PADDLE_WIDTH
        else:
            game_objs['paddle1'].positionx += game_objs['paddle1'].velocityx
            
        if next_paddle2_pos < 0:
            game_objs['paddle2'].positionx = 0
        elif next_paddle2_pos > WW-PADDLE_WIDTH:
            game_objs['paddle2'].positionx = WW-PADDLE_WIDTH
        else:
            game_objs['paddle2'].positionx += game_objs['paddle2'].velocityx

        next_ball_posx = game_objs['ball'].positionx + game_objs['ball'].velocityx
        next_ball_posy = game_objs['ball'].positiony + game_objs['ball'].velocityy  
        
        if next_ball_posy < (PADDLE1_START_POSITIONY + PADDLE_HEIGHT):
            if next_ball_posx > next_paddle1_pos and next_ball_posx < (next_paddle1_pos + PADDLE_WIDTH):
                game_objs['ball'].add_velocityx(game_objs['paddle1'].velocityx)
                game_objs['ball'].velocityy *= -1
                game_objs['ball'].positionx += game_objs['ball'].velocityx
            else:
                player2_score += 1
                if player2_score == WIN_LIMIT:
                    playing = False
                else:
                    game_objs['ball'].reset_ball()
                    
        elif next_ball_posy > (PADDLE2_START_POSITIONY-BALL_DIAMETER):
            if next_ball_posx > next_paddle2_pos and next_ball_posx < (next_paddle2_pos + PADDLE_WIDTH):
                game_objs['ball'].add_velocityx(game_objs['paddle2'].velocityx)
                game_objs['ball'].velocityy *= -1
                game_objs['ball'].positionx += game_objs['ball'].velocityx            
            else:
                player1_score += 1
                if player1_score == WIN_LIMIT:
                    playing = False
                else:
                    game_objs['ball'].reset_ball()
        
        if next_ball_posx < 0 or next_ball_posx > WW-BALL_DIAMETER:
            game_objs['ball'].velocityx *= -1
            game_objs['ball'].positiony += game_objs['ball'].velocityy
        else:
            game_objs['ball'].positionx += game_objs['ball'].velocityx
            game_objs['ball'].positiony += game_objs['ball'].velocityy        
            
        pos = pygame.mouse.get_pos()
        posx = pos[0]
        posy = pos[1]
        
        #drawing
        game_objs['screen'].fill(BLACK)
        
        game_objs['screen'].blit(bg_img,[0,0])
        game_objs['screen'].blit(ship_img,[posx,posy])
        
        text1 = font.render(str(player1_score),True,WHITE)
        text2 = font.render(str(player2_score),True,WHITE)
        
        game_objs['screen'].blit(text1,[(WW/2)-SCORE_SPACING,(WH/2)])
        game_objs['screen'].blit(text2,[(WW/2)+SCORE_SPACING,(WH/2)])
        
        pygame.draw.ellipse(game_objs['screen'],game_objs['ball'].colour,[game_objs['ball'].positionx,game_objs['ball'].positiony,game_objs['ball'].diameter,game_objs['ball'].diameter])
        
        pygame.draw.rect(game_objs['screen'],game_objs['paddle1'].colour,[game_objs['paddle1'].positionx,game_objs['paddle1'].positiony,game_objs['paddle1'].width,game_objs['paddle1'].height])
        
        pygame.draw.rect(game_objs['screen'],game_objs['paddle2'].colour,[game_objs['paddle2'].positionx,game_objs['paddle2'].positiony,game_objs['paddle2'].width,game_objs['paddle2'].height])
        
        pygame.display.flip()
        clock.tick(60)
        
pygame.init()
clock = pygame.time.Clock()

if __name__ == "__main__":
    main()
    
pygame.quit()