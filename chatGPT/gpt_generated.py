import pygame
import random

# Set up the game window
pygame.init()
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Set up the game objects
paddle_width = 100
paddle_height = 20
paddle_x = WIDTH // 2 - paddle_width // 2
paddle_y = HEIGHT - 50
paddle_speed = 30 # originally it was 5, but now it is 30 due to the hardness
paddle = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)

ball_width = 20
ball_height = 20
ball_x = random.randint(ball_width, WIDTH - ball_width)
ball_y = HEIGHT // 2 - ball_height // 2
ball_speed_x = random.choice([-5, 5])
ball_speed_y = -5
ball = pygame.Rect(ball_x, ball_y, ball_width, ball_height)

brick_width = 80
brick_height = 30
brick_gap = 10
brick_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
bricks = []
for row in range(3):
    brick_color = brick_colors[row]
    for col in range(10):
        brick_x = col * (brick_width + brick_gap) + brick_gap
        brick_y = row * (brick_height + brick_gap) + brick_gap
        brick = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
        bricks.append((brick, brick_color))

# Set up the game loop
clock = pygame.time.Clock()
game_over = False

while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle.x -= paddle_speed
            elif event.key == pygame.K_RIGHT:
                paddle.x += paddle_speed

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Check for collisions with walls
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        ball_speed_y = -ball_speed_y

    # Check for collisions with paddle
    if ball.colliderect(paddle):
        ball_speed_y = -ball_speed_y

    # Check for collisions with bricks
    for brick, color in bricks:
        if ball.colliderect(brick):
            bricks.remove((brick, color))
            ball_speed_y = -ball_speed_y
            break

    # Draw the game objects
    window.fill((255, 255, 255))
    pygame.draw.rect(window, (0, 0, 0), paddle)
    pygame.draw.circle(window, (0, 0, 0), (ball.x, ball.y), ball.width // 2)
    for brick, color in bricks:
        pygame.draw.rect(window, color, brick)
    pygame.display.update()

    # Check for game over
    if ball.bottom >= HEIGHT:
        game_over = True

    # Set the game clock
    clock.tick(60)

# Clean up
pygame.quit()
