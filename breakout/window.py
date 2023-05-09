import pygame

from breakout import sprites
from setting import *


def splash():
    pygame.init()
    start_time = pygame.time.get_ticks()

    window = pygame.display.set_mode((SPLASHWIDTH, SPLASHHEIGHT))
    window.fill((0, 0, 0))

    while pygame.time.get_ticks() < start_time + 3000:
        pygame.display.update()


def main():
    # Set up the game window
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Breakout")

    # Set up the sound
    sfx = sound()
    background_sound = pygame.mixer.Sound(sfx.background)
    background_sound.set_volume(0.5)
    background_sound.play(-1)
    wall_hit_sound = pygame.mixer.Sound(sfx.wall)
    brick_hit_sound = pygame.mixer.Sound(sfx.brick)
    paddle_hit_sound = pygame.mixer.Sound(sfx.paddle)
    paddle_hit_sound.set_volume(1.5)
    game_over_sound = pygame.mixer.Sound(sfx.gameover)

    # Set key repeat interval
    delay = 100
    interval = 50
    pygame.key.set_repeat(delay, interval)

    # Set up the game objects
    botpad = sprites.paddle()
    paddle = pygame.Rect(botpad.x, botpad.y, botpad.width, botpad.height)

    mball = sprites.ball()
    ball = pygame.Rect(mball.x, mball.y, mball.width, mball.height)

    blocks = sprites.brick()
    bricks = []
    for row in range(9):  # originally 3 rows
        blocks.color = blocks.colors[row]
        for col in range(10):
            blocks.x = col * (blocks.width + blocks.gap) + blocks.gap
            blocks.y = row * (blocks.height + blocks.gap) + blocks.gap
            brick = pygame.Rect(blocks.x, blocks.y,
                                blocks.width, blocks.height)
            bricks.append((brick, blocks.color))

    game_font = pygame.font.Font(pretendardblack, 40)

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
                    paddle.x -= botpad.speed
                elif event.key == pygame.K_RIGHT:
                    paddle.x += botpad.speed

        # Move the ball
        ball.x += mball.speed_x
        ball.y += mball.speed_y

        # Check for collisions with walls
        if ball.left <= 0 or ball.right >= WIDTH:
            mball.speed_x = -mball.speed_x
            wall_hit_sound.play()
        if ball.top <= 0:
            mball.speed_y = -mball.speed_y
            wall_hit_sound.play()

        # Check for collisions with paddle
        if ball.colliderect(paddle):
            mball.speed_y = -mball.speed_y
            paddle_hit_sound.play()

        # Check for collisions with bricks
        for brick, color in bricks:
            if ball.colliderect(brick):
                bricks.remove((brick, color))
                mball.speed_y = -mball.speed_y
                brick_hit_sound.play()
                break

        # Draw the game objects
        window.fill((0, 0, 0))
        pygame.draw.rect(window, (165, 165, 165), paddle)
        pygame.draw.circle(window, (255, 255, 255), (ball.x, ball.y),
                           ball.width // 2)
        for brick, color in bricks:
            pygame.draw.rect(window, color, brick)
        pygame.display.update()

        # Check for game over
        if ball.bottom >= HEIGHT:
            game_over = True

        # Set the game clock
        clock.tick(60)

    msg = game_font.render("Game Over!", True, (255, 255, 255))
    background_sound.stop()
    game_over_sound.play()
    msg_rect = msg.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 2)))
    window.blit(msg, msg_rect)
    pygame.display.update()

    # 2초 대기
    pygame.time.delay(2000)

    # Clean up
    pygame.quit()
