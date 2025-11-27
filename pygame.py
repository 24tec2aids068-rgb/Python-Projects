import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paddle Ball Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

paddle_width = 120
paddle_height = 15
paddle_x = WIDTH // 2 - paddle_width // 2
paddle_y = HEIGHT - 40
paddle_speed = 8

ball_size = 15
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 5
ball_dy = -5

clock = pygame.time.Clock()

run = True
while run:
    clock.tick(60)  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
        paddle_x += paddle_speed

    
    ball_x += ball_dx
    ball_y += ball_dy

   
    if ball_x <= 0 or ball_x >= WIDTH - ball_size:
        ball_dx *= -1
    if ball_y <= 0:
        ball_dy *= -1

    
    if (paddle_y <= ball_y + ball_size <= paddle_y + 10) and \
       (paddle_x <= ball_x <= paddle_x + paddle_width):
        ball_dy *= -1

   
    if ball_y > HEIGHT:
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_dx = 5
        ball_dy = -5

    
    screen.fill(BLACK)

    
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))

    
    pygame.draw.rect(screen, WHITE, (ball_x, ball_y, ball_size, ball_size))

    pygame.display.update()
