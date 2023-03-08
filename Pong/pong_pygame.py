import pygame
import os
pygame.font.init()

FPS = 60
VEL = 5
BALL_VEL = 5
BALL_VELX = 5

WIDTH, HEIGHT = 1000, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Set how big the window is
pygame.display.set_caption("Pong Game")  # Title of the application

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

SCORE_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)


RECT_WIDTH, RECT_HEIGHT = 20, 100
BALL_SIZE = 20

SPACE_IMAGE = pygame.image.load(os.path.join('Assets', 'space.png'))
SPACE = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))

BALL_IMAGE = pygame.image.load(os.path.join('Assets', 'circle.png'))
BALL = pygame.transform.scale(BALL_IMAGE, (BALL_SIZE, BALL_SIZE))



def draw_window(RECTANGLE_LEFT, RECTANGLE_RIGHT, BALL_HITBOX):
    WIN.fill(BLACK)  # Fills the window a certain colour. Use WIN.blit for text and images
    WIN.blit(SPACE, (0, 0))
    score_text = SCORE_FONT.render(f"Player 1: {p1}  | Player 2: {p2}", True, WHITE)
    WIN.blit(score_text, ((WIDTH//2) - score_text.get_width()//2, 10))
    pygame.draw.rect(WIN, WHITE, RECTANGLE_LEFT)
    pygame.draw.rect(WIN, WHITE, RECTANGLE_RIGHT)
    WIN.blit(BALL, BALL_HITBOX)
    pygame.display.update()  # Updates the game so the above appear on the screen


def ball_movement(BALL_HITBOX, winner_text):
    global BALL_VEL
    if BALL_HITBOX.y - BALL_VEL < 0:
        BALL_VEL = BALL_VEL * -1
        BALL_HITBOX.y = 0
        # print(f"AA: {BALL_VEL}")

    if BALL_HITBOX.y + BALL_VEL > HEIGHT - BALL_SIZE:
        BALL_VEL = BALL_VEL * -1
        BALL_HITBOX.y = HEIGHT - BALL_SIZE
        # print(f"BB: {BALL_VEL}")

    if winner_text == "":
        # BALL_VEL = BALL_VEL
        BALL_HITBOX.x += BALL_VELX
        BALL_HITBOX.y += BALL_VEL



def handle_pong_hit(RECTANGLE_LEFT, RECTANGLE_RIGHT, BALL_HITBOX):
    global BALL_VELX
    if RECTANGLE_LEFT.colliderect(BALL_HITBOX):
        BALL_VELX = BALL_VELX * -1.05 # Multiply with -1 to change direction
        BALL_HITBOX.x = 40 # Enable this if there are any bugs with the paddle and ball
        print(f"PONG: {BALL_VELX}")


    if RECTANGLE_RIGHT.colliderect(BALL_HITBOX):
        BALL_VELX = BALL_VELX * -1.05
        BALL_HITBOX.x = (WIDTH - 20) - RECT_WIDTH - 20 # Can be disabled but may cause issues with the paddle and ball
        print(f"PONG: {BALL_VELX}")


def score(BALL_HITBOX):
    global p1, p2, BALL_VELX # Made global, so I can reset it back to 5 once the user scores

    # I made the ball go further than the screen to get a point as it looked nicer when playing
    if BALL_HITBOX.x + BALL_VELX > WIDTH + BALL_SIZE and p1 == END_SCORE - 1: # Right edge
        BALL_VELX = 5 # Reset ball x velocity to 5 after each point
        BALL_HITBOX.x = 10 # Puts ball at top left for the final point
        BALL_HITBOX.y = 10
        p1 += 1
        # print(f"p1: {p1}")
        pygame.time.delay(400)

    if BALL_HITBOX.x - BALL_VELX < -20 and p2 == END_SCORE - 1: # Left edge
        BALL_VELX = 5 # Reset ball x velocity to 5 after each point
        BALL_HITBOX.x = 10 # Puts ball at top left for the final point
        BALL_HITBOX.y = 10
        p2 += 1
        # print(f"p1: {p1}")
        pygame.time.delay(400)

    if BALL_HITBOX.x + BALL_VELX > WIDTH + BALL_SIZE: # Right edge
        BALL_VELX = -5 # Resets ball and makes ball go to person who scored
        BALL_HITBOX.x = WIDTH//2 - BALL_SIZE
        BALL_HITBOX.y = HEIGHT//2 - BALL_SIZE
        p1 += 1
        pygame.time.delay(400)

    if BALL_HITBOX.x - BALL_VELX < -20: # Left edge
        BALL_VELX = 5 # Reset to minus
        BALL_HITBOX.x = WIDTH//2 - BALL_SIZE//2
        BALL_HITBOX.y = HEIGHT//2 - BALL_SIZE//2
        p2 += 1
        pygame.time.delay(400)


def draw_winner(result):
    draw_win_results = WINNER_FONT.render(result, True, WHITE)
    WIN.blit(draw_win_results, (WIDTH//2 - draw_win_results.get_width()//2, HEIGHT//2 - draw_win_results.get_height()//2))
    pygame.display.update() # Display text above
    pygame.time.delay(3000) # Pause at the win results for a few seconds


def pong_left_movement(keys_pressed, RECTANGLE_LEFT):
    if keys_pressed[pygame.K_w] and RECTANGLE_LEFT.y - VEL > 0: # up
        RECTANGLE_LEFT.y -= VEL

    if keys_pressed[pygame.K_s] and RECTANGLE_LEFT.y + VEL < HEIGHT - RECT_HEIGHT: # down
        RECTANGLE_LEFT.y += VEL

def pong_right_movement(keys_pressed, RECTANGLE_RIGHT):
    if keys_pressed[pygame.K_UP] and RECTANGLE_RIGHT.y - VEL > 0: # Up arrow
        RECTANGLE_RIGHT.y -= VEL

    if keys_pressed[pygame.K_DOWN] and RECTANGLE_RIGHT.y + VEL < HEIGHT - RECT_HEIGHT: # Down arrow
        RECTANGLE_RIGHT.y += VEL


def main():
    global p1, p2, END_SCORE
    RECTANGLE_LEFT = pygame.Rect(20, HEIGHT // 2 - RECT_HEIGHT // 2, RECT_WIDTH, RECT_HEIGHT)
    RECTANGLE_RIGHT = pygame.Rect((WIDTH - 20) - RECT_WIDTH, HEIGHT // 2 - RECT_HEIGHT // 2, RECT_WIDTH, RECT_HEIGHT)
    BALL_HITBOX = pygame.Rect(WIDTH // 2 - BALL_SIZE, HEIGHT // 2 - BALL_SIZE, BALL_SIZE, BALL_SIZE)
    # score
    p1, p2 = 0, 0
    END_SCORE = 5 # How many points to win
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) # Run game at 60fps
        for event in pygame.event.get():  # Loops through all the events
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        winner_text = ""
        if p1 >= END_SCORE:
            winner_text = "Player 1 Wins!"

        if p2 >= END_SCORE:
            winner_text = "Player 2 Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        pong_left_movement(keys_pressed, RECTANGLE_LEFT) # Movement for left rectangle
        pong_right_movement(keys_pressed, RECTANGLE_RIGHT) # Movement for right rectangle
        ball_movement(BALL_HITBOX, winner_text) # Ball hitting Y axis border
        handle_pong_hit(RECTANGLE_LEFT, RECTANGLE_RIGHT, BALL_HITBOX) # Ball and pong collision
        score(BALL_HITBOX) # Scoring system
        draw_window(RECTANGLE_LEFT, RECTANGLE_RIGHT, BALL_HITBOX)

    # pygame.quit()
    main() # call main to restart the game, once it breaks out of loop



if __name__ == "__main__":
    main()
