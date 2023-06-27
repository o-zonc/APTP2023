import pygame
import math
import webbrowser

from breakout import sprites
from setting import *

# Define global properties
clock = pygame.time.Clock()
sfx = sound()
pygame.mixer.init()
click_sound = pygame.mixer.Sound(sfx.click)
quit_sound = pygame.mixer.Sound(sfx.quit)


def splash():
    # Initialize game
    pygame.init()
    readout.readstatus()

    # Define background image and splash chime
    splashimage = pygame.image.load('./src/image/splash.png')
    splash_sound = pygame.mixer.Sound(sfx.splash)
    pygame.display.set_caption('Breakout')
    splash_sound.play()

    # Draw window
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    window.blit(splashimage, [0, 0])
    pygame.display.flip()
    pygame.time.delay(2000)


def home():
    # Create Pygame window and sound property
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    home_ambient_sound = pygame.mixer.Sound(sfx.homebackground)
    aistart_sound = pygame.mixer.Sound(sfx.aistart)
    aistart_sound.set_volume(50)
    home_ambient_sound.play(-1)
    pygame.display.set_caption("Breakout")
    running = True

    # Define button properties
    button_width, button_height = 250, 50
    start_button_x, start_button_y = (WIDTH - button_width) // 2, (HEIGHT - button_height) // 2
    start_button_text = "Start"
    mode_button_x, mode_button_y = (WIDTH - button_width) // 2, (HEIGHT - button_height) // 2 + PADDING + button_height
    mode_button_text = "Settings"
    save_button_x, save_button_y = (WIDTH - button_width) // 2, \
                                   (HEIGHT - button_height) // 2 + 2 * (PADDING + button_height)
    save_button_text = "Save"
    no_button_x, no_button_y = (WIDTH - button_width) // 2, \
                               (HEIGHT - button_height) // 2 + 3 * (PADDING + button_height)
    no_button_text = "Hell Mode"
    quit_button_x, quit_button_y = (WIDTH - button_width) // 2, (HEIGHT - button_height) // 2 + 4 * (PADDING
                                                                                                     + button_height)
    quit_button_text = "Quit"

    hiscore_x, hiscore_y = PADDING, (HEIGHT - button_height) // 2 + 4 * (PADDING + button_height)

    # Create font object
    font = pygame.font.Font(pretendardblack, 36)

    pulse = 0

    while running:
        sfx.monochrome()
        pulse -= 1
        hiscore_text = "HI : " + str(mode.highscore)

        # Define header image
        header = 0
        if mode.monochrome == 0:
            header = pygame.image.load('./src/image/Header.png')
        elif mode.monochrome == 1:
            header = pygame.image.load('./src/image/Header_monochrome.png')
        header_width, header_height = 780, 110
        header = pygame.transform.scale(header, (header_width, header_height))
        header_x, header_y = (WIDTH - header_width) // 2, HEIGHT // 2 - 1.5 * header_height
        window.blit(header, (header_x, header_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitpage()
                pygame.display.set_caption("Breakout")

            # Check for mouse button down event
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_x <= mouse_pos[0] <= start_button_x + button_width and \
                        start_button_y <= mouse_pos[1] <= start_button_y + button_height:
                    if mode.modeset == 0:
                        # Button is clicked
                        if mode.sfxon == 1:
                            click_sound.play()
                        home_ambient_sound.stop()
                        main()
                        window.fill(chroma.BLACK)
                        return True
                    elif mode.modeset == 1:
                        if mode.sfxon == 1:
                            aistart_sound.play()
                        home_ambient_sound.stop()
                        # AI function
                        window.fill(chroma.BLACK)
                        return True
                if mode_button_x <= mouse_pos[0] <= mode_button_x + button_width and \
                        mode_button_y <= mouse_pos[1] <= mode_button_y + button_height:
                    # Button is clicked
                    if mode.sfxon == 1:
                        click_sound.play()
                    modeset()
                    pygame.display.set_caption("Breakout")
                if save_button_x <= mouse_pos[0] <= save_button_x + button_width and \
                        save_button_y <= mouse_pos[1] <= save_button_y + button_height:
                    if mode.sfxon == 1:
                        click_sound.play()
                    pulse = 7
                    mode.mod += 1
                    readout.savestatus()
                if no_button_x <= mouse_pos[0] <= no_button_x + button_width and \
                        no_button_y <= mouse_pos[1] <= no_button_y + button_height:
                    if mode.nocnt >= 10:
                        if mode.sfxon == 1:
                            click_sound.play()
                        if mode.levelset == 5:
                            mode.levelset = 0
                        else:
                            mode.levelset = 5
                    else:
                        mode.nocnt += 1
                if quit_button_x <= mouse_pos[0] <= quit_button_x + button_width and \
                        quit_button_y <= mouse_pos[1] <= quit_button_y + button_height:
                    if mode.sfxon == 1:
                        click_sound.play()
                    quitpage()
                    pygame.display.set_caption("Breakout")

        # Draw the button rectangle
        if mode.monochrome == 0:
            pygame.draw.rect(window, chroma.ORANGEISTHENEWBLACK, (start_button_x, start_button_y,
                                                                  button_width, button_height))
            pygame.draw.rect(window, chroma.GRAY, (mode_button_x, mode_button_y, button_width, button_height))
            if pulse > 0:
                pygame.draw.rect(window, chroma.GREEN, (save_button_x, save_button_y, button_width, button_height))
            elif pulse <= 0:
                pygame.draw.rect(window, chroma.GRAY, (save_button_x, save_button_y, button_width, button_height))
            if mode.nocnt >= 10:
                if mode.levelset == 5:
                    pygame.draw.rect(window, chroma.RED, (no_button_x, no_button_y, button_width, button_height))
                else:
                    pygame.draw.rect(window, chroma.GRAY, (no_button_x, no_button_y, button_width, button_height))
            else:
                pygame.draw.rect(window, chroma.BLACK, (no_button_x, no_button_y, button_width, button_height))
            pygame.draw.rect(window, chroma.GRAY, (quit_button_x, quit_button_y, button_width, button_height))
        elif mode.monochrome == 1:
            pygame.draw.rect(window, chroma.WHITE, (start_button_x, start_button_y, button_width, button_height))
            pygame.draw.rect(window, chroma.BLACK, (mode_button_x, mode_button_y, button_width, button_height))
            pygame.draw.rect(window, chroma.BLACK, (save_button_x, save_button_y, button_width, button_height))
            if mode.nocnt >= 10:
                pygame.draw.rect(window, chroma.BLACK, (no_button_x, no_button_y, button_width, button_height))
            else:
                pygame.draw.rect(window, chroma.BLACK, (no_button_x, no_button_y, button_width, button_height))
            pygame.draw.rect(window, chroma.BLACK, (quit_button_x, quit_button_y, button_width, button_height))

        # Draw the button text
        start_text_surface = font.render(start_button_text, True, chroma.BLACK)
        mode_text_surface, save_text_surface, no_text_surface, quit_text_surface = 0, 0, 0, 0
        if mode.monochrome == 0:
            mode_text_surface = font.render(mode_button_text, True, chroma.BLACK)
            save_text_surface = font.render(save_button_text, True, chroma.BLACK)
            no_text_surface = font.render(no_button_text, True, chroma.BLACK)
            quit_text_surface = font.render(quit_button_text, True, chroma.BLACK)
        elif mode.monochrome == 1:
            mode_text_surface = font.render(mode_button_text, True, chroma.WHITE)
            if pulse > 0:
                save_text_surface = font.render(save_button_text, True, chroma.GREEN)
            elif pulse <= 0:
                save_text_surface = font.render(save_button_text, True, chroma.WHITE)
            if mode.levelset == 5:
                no_text_surface = font.render(no_button_text, True, chroma.RED)
            else:
                no_text_surface = font.render(no_button_text, True, chroma.WHITE)
            quit_text_surface = font.render(quit_button_text, True, chroma.WHITE)
        start_text_rect = start_text_surface.get_rect(center=(start_button_x + button_width // 2,
                                                              start_button_y + button_height // 2))
        mode_text_rect = mode_text_surface.get_rect(center=(mode_button_x + button_width // 2,
                                                            mode_button_y + button_height // 2))
        save_text_rect = save_text_surface.get_rect(center=(save_button_x + button_width // 2,
                                                            save_button_y + button_height // 2))
        no_text_rect = no_text_surface.get_rect(center=(no_button_x + button_width // 2,
                                                        no_button_y + button_height // 2))
        quit_text_rect = quit_text_surface.get_rect(center=(quit_button_x + button_width // 2,
                                                            quit_button_y + button_height // 2))

        hiscore_text_surface = font.render(hiscore_text, True, chroma.WHITE)
        hiscore_text_rect = hiscore_text_surface.get_rect(center=(hiscore_x + button_width // 2,
                                                                  hiscore_y + button_height // 2))

        window.blit(start_text_surface, start_text_rect)
        window.blit(mode_text_surface, mode_text_rect)
        window.blit(save_text_surface, save_text_rect)
        if mode.nocnt >= 10:
            window.blit(no_text_surface, no_text_rect)
        window.blit(quit_text_surface, quit_text_rect)
        window.blit(hiscore_text_surface, hiscore_text_rect)

        pygame.display.flip()
        clock.tick(60)


def modeset():
    # Create Pygame window
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Select Mode")

    # Define button properties
    button_width, button_height = 250, 50
    upper_left_x, upper_right_x = (WIDTH - button_width) // 4, 3 * (WIDTH - button_width) // 4
    upper_y = []
    mode_center_x, mode_center_y = (WIDTH - button_width) // 4, \
        [(HEIGHT - button_height) // 2, (HEIGHT - button_height) // 2 + PADDING + button_height,
         (HEIGHT - button_height) // 2 + 4 * (PADDING + button_height)]
    level_center_x, level_center_y = 3 * (WIDTH - button_width) // 4, []
    for i in range(5):
        level_center_y.append((HEIGHT - button_height) // 2 + i * (PADDING + button_height))
    for i in range(3):
        upper_y.append((i + 1) * button_height + (i - 1) * PADDING)

    mode_text = ["Manual", "AI", "Reset"]
    mode_color = [0, 1, 2]
    level_text = ["Easy", "Normal", "Hard", "Harder", "Insane"]
    level_color = [0, 1, 2, 3, 4]
    velo_text = ["Slow", "Medium", "Fast"]
    velo_color = [0, 1, 2]
    upper_left_text = ["Back to Menu", "Gyukatsu", "Vivid"]
    upper_left_color = [0, 1, 2]
    upper_right_text = ["Score On", "SFX On", "Quit"]
    upper_right_color = [0, 1, 2]

    monochrome_image = pygame.image.load('./src/image/gradation.png')
    gyukatsu_link = "https://toss.me/8taby/10000"

    # Create font object
    font = pygame.font.Font(pretendardblack, 36)
    label = pygame.font.Font(pretendardmedium, 36)

    # Define the label text
    mode_label_text, level_label_text = "Select mode", "Select level"
    mode_label_surface, level_label_surface = label.render(mode_label_text, True, chroma.WHITE), \
        label.render(level_label_text, True, chroma.WHITE)
    mode_label_rect = mode_label_surface.get_rect(center=(mode_center_x + button_width // 2,
                                                          mode_center_y[0] - PADDING - button_height // 2))
    level_label_rect = level_label_surface.get_rect(
        center=(level_center_x + button_width // 2, level_center_y[0] - PADDING - button_height // 2))

    # Define the button text
    mode_text_surface, level_text_surface, velo_text_surface = [0, 1, 2], [0, 1, 2, 3, 4], [0, 1, 2]
    upper_left_surface, upper_right_surface = [0, 1, 2], [0, 1, 2]
    mode_text_rect, level_text_rect, velo_text_rect = [0, 1, 2], [0, 1, 2, 3, 4], [0, 1, 2]
    upper_left_rect, upper_right_rect = [0, 1, 2], [0, 1, 2]

    moderun = True

    while moderun:
        sfx.monochrome()

        # === Monochrome, Score, Back to main, Buy us gyukatsu controller === #
        if mode.monochrome == 0:
            upper_left_text[2] = "Vivid"
            upper_left_surface = [font.render(upper_left_text[0], True, chroma.BLACK),
                                  font.render(upper_left_text[1], True, chroma.WHITE),
                                  font.render(upper_left_text[2], True, chroma.BLACK)]
            upper_left_color = [chroma.GRAY, chroma.TOSSBLUE, chroma.BLACK]
            upper_right_surface = [font.render(upper_right_text[0], True, chroma.BLACK),
                                   font.render(upper_right_text[1], True, chroma.BLACK),
                                   font.render(upper_right_text[2], True, chroma.BLACK)]
            upper_right_color = [chroma.ORANGEISTHENEWBLACK, chroma.ORANGEISTHENEWBLACK, chroma.GRAY]
            if mode.scron == 0:
                upper_right_color[0] = chroma.GRAY
            if mode.sfxon == 0:
                upper_right_color[1] = chroma.GRAY
        elif mode.monochrome == 1:
            upper_left_text[2] = "Monochrome"
            upper_left_surface = [font.render(upper_left_text[0], True, chroma.WHITE),
                                  font.render(upper_left_text[1], True, chroma.TOSSBLUE),
                                  font.render(upper_left_text[2], True, chroma.BLACK)]
            upper_left_color = [chroma.BLACK, chroma.BLACK, chroma.WHITE]
            upper_right_surface = [font.render(upper_right_text[0], True, chroma.BLACK),
                                   font.render(upper_right_text[1], True, chroma.BLACK),
                                   font.render(upper_right_text[2], True, chroma.WHITE)]
            upper_right_color = [chroma.WHITE, chroma.WHITE, chroma.BLACK]
            if mode.scron == 0:
                upper_right_color[0] = chroma.BLACK
                upper_right_surface[0] = font.render(upper_right_text[0], True, chroma.WHITE)
            if mode.sfxon == 0:
                upper_right_color[1] = chroma.BLACK
                upper_right_surface[1] = font.render(upper_right_text[1], True, chroma.WHITE)

        for i in range(3):
            pygame.draw.rect(window, upper_left_color[i], (upper_left_x, upper_y[i],
                                                           button_width, button_height))
            pygame.draw.rect(window, upper_right_color[i], (upper_right_x, upper_y[i],
                                                            button_width, button_height))
            upper_left_rect[i] = upper_left_surface[i].get_rect(center=(upper_left_x + button_width // 2,
                                                                        upper_y[i] + button_height // 2))
            upper_right_rect[i] = upper_right_surface[i].get_rect(center=(upper_right_x + button_width // 2,
                                                                          upper_y[i] + button_height // 2))

        if mode.monochrome == 0:
            window.blit(monochrome_image, (upper_left_x, upper_y[2]))

        # === Mode, Level, Velocity controller === #
        # Define button properties that might be updated
        for i in range(5):
            if mode.monochrome == 0:
                if i == mode.levelset:
                    level_color[i] = chroma.level[i]
                else:
                    level_color[i] = chroma.GRAY
                level_text_surface[i] = font.render(level_text[i], True, chroma.BLACK)
            elif mode.monochrome == 1:
                if i == mode.levelset:
                    level_color[i] = chroma.levelmonochrome[i]
                    if mode.levelset <= 1:
                        level_text_surface[i] = font.render(level_text[i], True, chroma.WHITE)
                    else:
                        level_text_surface[i] = font.render(level_text[i], True, chroma.BLACK)
                else:
                    level_color[i] = chroma.BLACK
                    level_text_surface[i] = font.render(level_text[i], True, chroma.WHITE)
            level_text_rect[i] = level_text_surface[i].get_rect(center=(level_center_x + button_width // 2,
                                                                        level_center_y[i] + button_height // 2))

        for i in range(3):
            if i == mode.aivelo:
                velo_color[i] = chroma.WHITE
                velo_text_surface[i] = font.render(velo_text[i], True, chroma.BLACK)
            else:
                if mode.monochrome == 0:
                    velo_color[i] = chroma.GRAY
                    velo_text_surface[i] = font.render(velo_text[i], True, chroma.BLACK)
                elif mode.monochrome == 1:
                    velo_color[i] = chroma.BLACK
                    velo_text_surface[i] = font.render(velo_text[i], True, chroma.WHITE)
            velo_text_rect[i] = velo_text_surface[i].get_rect(center=(level_center_x + button_width // 2,
                                                                      level_center_y[i] + button_height // 2))

        for i in range(2):
            if mode.monochrome == 0:
                if i == mode.modeset:
                    mode_color[i] = chroma.ORANGEISTHENEWBLACK
                else:
                    mode_color[i] = chroma.GRAY
                mode_text_surface[i] = font.render(mode_text[i], True, chroma.BLACK)
            elif mode.monochrome == 1:
                if i == mode.modeset:
                    mode_color[i] = chroma.WHITE
                    mode_text_surface[i] = font.render(mode_text[i], True, chroma.BLACK)
                else:
                    mode_color[i] = chroma.BLACK
                    mode_text_surface[i] = font.render(mode_text[i], True, chroma.WHITE)
            mode_text_rect[i] = mode_text_surface[i].get_rect(center=(mode_center_x + button_width // 2,
                                                                      mode_center_y[i] + button_height // 2))
        if mode.monochrome == 0:
            mode_color[2] = chroma.RED
            mode_text_surface[2] = font.render(mode_text[2], True, chroma.WHITE)
        elif mode.monochrome == 1:
            mode_color[2] = chroma.BLACK
            mode_text_surface[2] = font.render(mode_text[2], True, chroma.WHITE)
        mode_text_rect[2] = mode_text_surface[2].get_rect(center=(mode_center_x + button_width // 2,
                                                                  mode_center_y[2] + button_height // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitpage()
                pygame.display.set_caption("Select Mode")

            # Check for mouse button down event
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Mode setting
                if mode_center_x <= mouse_pos[0] <= mode_center_x + button_width and \
                        mode_center_y[0] <= mouse_pos[1] <= mode_center_y[0] + button_height:
                    # Button is clicked
                    if mode.modeset != 0:
                        if mode.sfxon == 1:
                            click_sound.play()
                    mode.modeset = 0
                if mode_center_x <= mouse_pos[0] <= mode_center_x + button_width and \
                        mode_center_y[1] <= mouse_pos[1] <= mode_center_y[1] + button_height:
                    # Button is clicked
                    if mode.modeset != 1:
                        if mode.sfxon == 1:
                            click_sound.play()
                    mode.modeset = 1
                if mode_center_x <= mouse_pos[0] <= mode_center_x + button_width and mode_center_y[2] <= mouse_pos[1] <= \
                        mode_center_y[2] + button_height:
                    # Button is clicked
                    if mode.sfxon == 1:
                        click_sound.play()
                    resetpage()
                    window.fill(chroma.BLACK)
                    pygame.display.set_caption("Select Mode")
                if mode.modeset == 0:
                    # Level setting
                    if level_center_x <= mouse_pos[0] <= level_center_x + button_width and \
                            level_center_y[0] <= mouse_pos[1] <= level_center_y[0] + button_height:
                        # Button is clicked
                        if mode.levelset != 0:
                            if mode.sfxon == 1:
                                click_sound.play()
                        mode.levelset = 0
                    if level_center_x <= mouse_pos[0] <= level_center_x + button_width and \
                            level_center_y[1] <= mouse_pos[1] <= level_center_y[1] + button_height:
                        # Button is clicked
                        if mode.levelset != 1:
                            if mode.sfxon == 1:
                                click_sound.play()
                        mode.levelset = 1
                    if level_center_x <= mouse_pos[0] <= level_center_x + button_width and \
                            level_center_y[2] <= mouse_pos[1] <= level_center_y[2] + button_height:
                        # Button is clicked
                        if mode.levelset != 2:
                            if mode.sfxon == 1:
                                click_sound.play()
                        mode.levelset = 2
                    if level_center_x <= mouse_pos[0] <= level_center_x + button_width and \
                            level_center_y[3] <= mouse_pos[1] <= level_center_y[3] + button_height:
                        # Button is clicked
                        if mode.levelset != 3:
                            if mode.sfxon == 1:
                                click_sound.play()
                        mode.levelset = 3
                    if level_center_x <= mouse_pos[0] <= level_center_x + button_width and \
                            level_center_y[4] <= mouse_pos[1] <= level_center_y[4] + button_height:
                        # Button is clicked
                        if mode.levelset != 4:
                            if mode.sfxon == 1:
                                click_sound.play()
                        mode.levelset = 4
                elif mode.modeset == 1:
                    # Velocity setting
                    if level_center_x <= mouse_pos[0] <= level_center_x + button_width and \
                            level_center_y[0] <= mouse_pos[1] <= level_center_y[0] + button_height:
                        # Button is clicked
                        if mode.aivelo != 0:
                            if mode.sfxon == 1:
                                click_sound.play()
                        mode.aivelo = 0
                    if level_center_x <= mouse_pos[0] <= level_center_x + button_width and \
                            level_center_y[1] <= mouse_pos[1] <= level_center_y[1] + button_height:
                        # Button is clicked
                        if mode.aivelo != 1:
                            if mode.sfxon == 1:
                                click_sound.play()
                        mode.aivelo = 1
                    if level_center_x <= mouse_pos[0] <= level_center_x + button_width and \
                            level_center_y[2] <= mouse_pos[1] <= level_center_y[2] + button_height:
                        # Button is clicked
                        if mode.aivelo != 2:
                            if mode.sfxon == 1:
                                click_sound.play()
                        mode.aivelo = 2
                if upper_left_x <= mouse_pos[0] <= upper_left_x + button_width and \
                        upper_y[0] <= mouse_pos[1] <= upper_y[0] + button_height:
                    if mode.sfxon == 1:
                        if mode.sfxon == 1:
                            click_sound.play()
                    window.fill(chroma.BLACK)
                    return
                if upper_left_x <= mouse_pos[0] <= upper_left_x + button_width and \
                        upper_y[1] <= mouse_pos[1] <= upper_y[1] + button_height:
                    if mode.sfxon == 1:
                        click_sound.play()
                    webbrowser.open(gyukatsu_link)
                if upper_left_x <= mouse_pos[0] <= upper_left_x + button_width and \
                        upper_y[2] <= mouse_pos[1] <= upper_y[2] + button_height:
                    if mode.sfxon == 1:
                        click_sound.play()
                    if mode.monochrome == 0:
                        mode.monochrome = 1
                        upper_left_text[2] = "Monochrome"
                    elif mode.monochrome == 1:
                        mode.monochrome = 0
                        upper_left_text[2] = "Vivid"
                if upper_right_x <= mouse_pos[0] <= upper_right_x + button_width and \
                        upper_y[0] <= mouse_pos[1] <= upper_y[0] + button_height:
                    if mode.sfxon == 1:
                        click_sound.play()
                    if mode.scron == 0:
                        mode.scron = 1
                        upper_right_text[0] = "Score On"
                    elif mode.scron == 1:
                        mode.scron = 0
                        upper_right_text[0] = "Score Off"
                if upper_right_x <= mouse_pos[0] <= upper_right_x + button_width and \
                        upper_y[1] <= mouse_pos[1] <= upper_y[1] + button_height:
                    if mode.sfxon == 0:
                        click_sound.play()
                        mode.sfxon = 1
                        upper_right_text[1] = "SFX On"
                    elif mode.sfxon == 1:
                        mode.sfxon = 0
                        upper_right_text[1] = "SFX Off"
                if upper_right_x <= mouse_pos[0] <= upper_right_x + button_width and \
                        upper_y[2] <= mouse_pos[1] <= upper_y[2] + button_height:
                    if mode.sfxon == 1:
                        click_sound.play()
                    quitpage()
                    pygame.display.set_caption("Select Mode")

        # Draw the label text
        window.blit(mode_label_surface, mode_label_rect)
        window.blit(level_label_surface, level_label_rect)

        # Draw the button rectangle
        # Mode buttons
        for i in range(3):
            pygame.draw.rect(window, mode_color[i], (mode_center_x, mode_center_y[i],
                                                     button_width, button_height))
            window.blit(mode_text_surface[i], mode_text_rect[i])
        if mode.modeset == 0:
            # Level buttons
            for i in range(5):
                pygame.draw.rect(window, level_color[i], ((level_center_x, level_center_y[i],
                                                           button_width, button_height)))
                window.blit(level_text_surface[i], level_text_rect[i])
        elif mode.modeset == 1:
            # Velocity buttons
            for i in range(3):
                pygame.draw.rect(window, velo_color[i], ((level_center_x, level_center_y[i],
                                                          button_width, button_height)))
                window.blit(velo_text_surface[i], velo_text_rect[i])
            pygame.draw.rect(window, chroma.BLACK, ((level_center_x, level_center_y[3],
                                                     button_width, button_height)))
            pygame.draw.rect(window, chroma.BLACK, ((level_center_x, level_center_y[4],
                                                     button_width, button_height)))
        for i in range(3):
            window.blit(upper_left_surface[i], upper_left_rect[i])
            window.blit(upper_right_surface[i], upper_right_rect[i])

        pygame.display.flip()
        clock.tick(60)


def main():
    # Set up the game window
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Breakout")

    # Set key repeat interval
    delay = 100
    interval = 50
    pygame.key.set_repeat(delay, interval)

    # Set sound
    sfx.monochrome()
    background_sound = pygame.mixer.Sound(sfx.background)
    background_sound.set_volume(0.5)
    background_sound.play(-1)
    wall_hit_sound = pygame.mixer.Sound(sfx.wall)
    brick_hit_sound = pygame.mixer.Sound(sfx.brick)
    paddle_hit_sound = pygame.mixer.Sound(sfx.paddle)
    paddle_hit_sound.set_volume(1.5)
    new_hiscore_sound = pygame.mixer.Sound(sfx.newhigh)
    game_over_sound = pygame.mixer.Sound(sfx.gameover)

    # Set up the game objects
    botpad = sprites.paddle()
    botpad.squeeze(math.pow(1.2 + 0.1 * mode.monochrome, mode.levelset + mode.monochrome))
    botpad.speedup(math.pow(1.1 + 0.1 * mode.monochrome, mode.levelset + mode.monochrome))
    paddle = pygame.Rect(botpad.x, botpad.y, botpad.width, botpad.height)

    button_width, button_height = 250, 50
    hiscore_x, hiscore_y = PADDING, (HEIGHT - button_height) // 2 + 4 * (PADDING + button_height)
    hiscore_text = "HI : " + str(mode.highscore)
    nowscore_x, nowscore_y = (WIDTH - button_width - PADDING), (HEIGHT - button_height) // 2 + 4 * (
            PADDING + button_height)

    score = 0
    multi = 0

    mball = sprites.ball()
    mball.speedup(math.pow(1.13 + 0.1 * mode.monochrome, mode.levelset + mode.monochrome))
    ball = pygame.Rect(mball.x, mball.y, mball.width, mball.height)

    blocks = sprites.brick()
    blocks.monochrome()
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
    font = pygame.font.Font(pretendardblack, 36)

    # Set up the game loop
    game_over = False

    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitpage()
                window.fill(chroma.BLACK)
                pygame.display.set_caption("Breakout")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_1:
                    paddle.x -= botpad.speed
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_2:
                    paddle.x += botpad.speed
                elif event.key == pygame.K_ESCAPE:
                    endint = escape()
                    if endint == 0:
                        background_sound.stop()
                        return
                    pygame.display.set_caption("Breakout")
                    pygame.display.flip()

        # Move the ball
        ball.x += mball.speed_x
        ball.y += mball.speed_y

        # Check for collisions with walls
        if ball.left <= 0 or ball.right >= WIDTH:
            mball.speed_x = -mball.speed_x
            if mode.sfxon == 1:
                wall_hit_sound.play()
        if ball.top <= 0:
            mball.speed_y = -mball.speed_y
            if mode.sfxon == 1:
                wall_hit_sound.play()

        # Check for collisions with paddle
        if ball.colliderect(paddle):
            multi = 0
            mball.speed_y = -mball.speed_y
            if mode.sfxon == 1:
                paddle_hit_sound.play()

        # Check for collisions with bricks
        for brick, color in bricks:
            if ball.colliderect(brick):
                bricks.remove((brick, color))
                score += (mode.levelset // 3 + 1) * (mode.levelset + mode.monochrome + multi + 1)
                mball.speed_x *= math.pow(1.002, mode.monochrome + mode.levelset)
                mball.speed_y *= math.pow(1.003, mode.levelset)
                mball.speed_y = -mball.speed_y
                if mode.sfxon == 1:
                    brick_hit_sound.play()
                break

        # Draw the game objects
        window.fill(chroma.BLACK)
        if mode.monochrome == 0:
            pygame.draw.rect(window, chroma.GRAY, paddle)
            pygame.draw.circle(window, chroma.WHITE, (ball.x, ball.y), ball.width // 2)
        elif mode.monochrome == 1:
            pygame.draw.rect(window, chroma.WHITE, paddle)
            pygame.draw.circle(window, chroma.WHITE, (ball.x, ball.y), ball.width // 2)
        for brick, color in bricks:
            pygame.draw.rect(window, color, brick)

        hiscore_text_surface, nowscore_text_surface = font.render(hiscore_text, True, chroma.WHITE), 0
        if mode.monochrome == 0:
            if score <= mode.highscore:
                nowscore_text_surface = font.render("Score : " + str(score), True, chroma.WHITE)
            else:
                nowscore_text_surface = font.render("Score : " + str(score), True, chroma.ORANGEISTHENEWBLACK)
        elif mode.monochrome == 1:
            if score <= mode.highscore:
                nowscore_text_surface = font.render("Score : " + str(score), True, chroma.WHITE)
            else:
                nowscore_text_surface = font.render("Score : " + str(score), True, chroma.GRAY)
        hiscore_text_rect = hiscore_text_surface.get_rect(center=(hiscore_x + button_width // 2,
                                                                  hiscore_y - PADDING - button_height // 2))
        nowscore_text_rect = nowscore_text_surface.get_rect(center=(nowscore_x + button_width // 2,
                                                                    nowscore_y - PADDING - button_height // 2))

        window.blit(hiscore_text_surface, hiscore_text_rect)
        window.blit(nowscore_text_surface, nowscore_text_rect)
        pygame.display.flip()

        # Check for game over
        if ball.bottom >= HEIGHT:
            game_over = True

        # Set the game clock
        clock.tick(60)

    msg = game_font.render("Game Over!", True, chroma.WHITE)
    background_sound.stop()
    if mode.sfxon == 1:
        game_over_sound.play()
    if score > mode.highscore:
        mode.highscore = score
        new_hiscore_sound.play()
        readout.savestatus()
        if mode.monochrome == 0:
            msg = game_font.render("New Highscore!", True, chroma.ORANGEISTHENEWBLACK)
        elif mode.monochrome == 1:
            msg = game_font.render("New Highscore!", True, chroma.WHITE)

    msg_rect = msg.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 2)))
    window.blit(msg, msg_rect)
    pygame.display.update()

    # 2초 대기
    pygame.time.delay(2000)


def quitpage():
    # Create Pygame window
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Quit?")
    alert_sound = pygame.mixer.Sound(sfx.alert)

    font = pygame.font.Font(pretendardblack, 36)

    # Define button properties
    button_width, button_height = 250, 50
    yes_button_x, yes_button_y = (WIDTH - button_width) // 4, (HEIGHT - button_height) // 2
    no_button_x, no_button_y = 3 * (WIDTH - button_width) // 4, (HEIGHT - button_height) // 2
    yes_text_surface, yes_text_rect, no_text_surface, no_text_rect = 0, 0, 0, 0

    # Define label properties
    label = pygame.font.Font(pretendardmedium, 36)
    label_surface = label.render("Do you really want to quit?", True, chroma.WHITE)
    label_rect = label_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - button_height - PADDING))
    window.blit(label_surface, label_rect)

    quitrun = True

    while quitrun:
        sfx.monochrome()

        # Define button properties that might be updated
        if mode.monochrome == 0:
            yes_text_surface = font.render("Yes", True, chroma.BLACK)
            no_text_surface = font.render("No", True, chroma.BLACK)
            pygame.draw.rect(window, chroma.GRAY, ((yes_button_x, yes_button_y,
                                                    button_width, button_height)))
            pygame.draw.rect(window, chroma.ORANGEISTHENEWBLACK, ((no_button_x, no_button_y,
                                                                   button_width, button_height)))
        elif mode.monochrome == 1:
            yes_text_surface = font.render("Yes", True, chroma.WHITE)
            no_text_surface = font.render("No", True, chroma.BLACK)
            pygame.draw.rect(window, chroma.BLACK, ((yes_button_x, yes_button_y,
                                                     button_width, button_height)))
            pygame.draw.rect(window, chroma.WHITE, ((no_button_x, no_button_y,
                                                     button_width, button_height)))
        yes_text_rect = yes_text_surface.get_rect(center=(yes_button_x + button_width // 2,
                                                          yes_button_y + button_height // 2))
        no_text_rect = no_text_surface.get_rect(center=(no_button_x + button_width // 2,
                                                        no_button_y + button_height // 2))
        window.blit(yes_text_surface, yes_text_rect)
        window.blit(no_text_surface, no_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alert_sound.play()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if yes_button_x <= mouse_pos[0] <= yes_button_x + button_width and \
                        yes_button_y <= mouse_pos[1] <= yes_button_y + button_height:
                    if mode.sfxon == 1:
                        click_sound.play()
                    pygame.time.delay(100)
                    if mode.sfxon == 1:
                        quit_sound.play()
                    pygame.time.delay(100)
                    quit()
                    return
                if no_button_x <= mouse_pos[0] <= no_button_x + button_width and \
                        no_button_y <= mouse_pos[1] <= no_button_y + button_height:
                    if mode.sfxon == 1:
                        click_sound.play()
                    window.fill(chroma.BLACK)
                    return

        pygame.display.flip()


def escape():
    # Create Pygame window
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paused")

    font = pygame.font.Font(pretendardblack, 36)

    # Define button properties
    button_width, button_height = 250, 50
    resume_button_x, resume_button_y = (WIDTH - button_width) // 4, \
        [(HEIGHT - button_height) // 2, (HEIGHT - button_height) // 2 + PADDING + button_height]
    quit_button_x, quit_button_y = 3 * (WIDTH - button_width) // 4, \
        [(HEIGHT - button_height) // 2, (HEIGHT - button_height) // 2 + PADDING + button_height]
    resume_text_surface, resume_text_rect, quit_text_surface, quit_text_rect = 0, 0, 0, 0
    github_text_surface, github_text_rect, menu_text_surface, menu_text_rect = 0, 0, 0, 0

    # Define label properties
    label = pygame.font.Font(pretendardmedium, 36)
    label_surface = label.render("Paused. Press Resume to restart.", True, chroma.WHITE)
    label_rect = label_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - button_height - PADDING))
    window.blit(label_surface, label_rect)

    escaperun = True

    while escaperun:
        sfx.monochrome()

        # Define button properties that might be updated
        if mode.monochrome == 0:
            resume_text_surface = font.render("Resume", True, chroma.BLACK)
            quit_text_surface = font.render("Quit", True, chroma.BLACK)
            github_text_surface = font.render("Github", True, chroma.BLACK)
            menu_text_surface = font.render("Back to Menu", True, chroma.BLACK)
            pygame.draw.rect(window, chroma.ORANGEISTHENEWBLACK, ((resume_button_x, resume_button_y[0],
                                                                   button_width, button_height)))
            pygame.draw.rect(window, chroma.GRAY, ((quit_button_x, quit_button_y[0],
                                                    button_width, button_height)))
            pygame.draw.rect(window, chroma.GRAY, ((resume_button_x, resume_button_y[1],
                                                    button_width, button_height)))
            pygame.draw.rect(window, chroma.GRAY, ((quit_button_x, quit_button_y[1],
                                                    button_width, button_height)))
        elif mode.monochrome == 1:
            resume_text_surface = font.render("Resume", True, chroma.BLACK)
            quit_text_surface = font.render("Quit", True, chroma.WHITE)
            github_text_surface = font.render("Github", True, chroma.WHITE)
            menu_text_surface = font.render("Back to Menu", True, chroma.WHITE)
            pygame.draw.rect(window, chroma.WHITE, ((resume_button_x, resume_button_y[0],
                                                     button_width, button_height)))
            pygame.draw.rect(window, chroma.BLACK, ((quit_button_x, quit_button_y[0],
                                                     button_width, button_height)))
            pygame.draw.rect(window, chroma.BLACK, ((resume_button_x, resume_button_y[1],
                                                     button_width, button_height)))
            pygame.draw.rect(window, chroma.BLACK, ((quit_button_x, quit_button_y[1],
                                                     button_width, button_height)))
        resume_text_rect = resume_text_surface.get_rect(center=(resume_button_x + button_width // 2,
                                                                resume_button_y[0] + button_height // 2))
        quit_text_rect = quit_text_surface.get_rect(center=(quit_button_x + button_width // 2,
                                                            quit_button_y[0] + button_height // 2))
        github_text_rect = github_text_surface.get_rect(center=(resume_button_x + button_width // 2,
                                                                resume_button_y[1] + button_height // 2))
        menu_text_rect = menu_text_surface.get_rect(center=(quit_button_x + button_width // 2,
                                                            quit_button_y[1] + button_height // 2))
        window.blit(resume_text_surface, resume_text_rect)
        window.blit(quit_text_surface, quit_text_rect)
        window.blit(github_text_surface, github_text_rect)
        window.blit(menu_text_surface, menu_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitpage()
                pygame.display.set_caption("Paused")

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if resume_button_x <= mouse_pos[0] <= resume_button_x + button_width and \
                        resume_button_y[0] <= mouse_pos[1] <= resume_button_y[0] + button_height:
                    if mode.sfxon == 1:
                        click_sound.play()
                    window.fill(chroma.BLACK)
                    return 1
                if quit_button_x <= mouse_pos[0] <= quit_button_x + button_width and \
                        quit_button_y[0] <= mouse_pos[1] <= quit_button_y[0] + button_height:
                    if mode.sfxon == 1:
                        click_sound.play()
                    quitpage()
                    pygame.display.set_caption("Paused")
                if resume_button_x <= mouse_pos[0] <= resume_button_x + button_width and \
                        resume_button_y[1] <= mouse_pos[1] <= resume_button_y[1] + button_height:
                    if mode.sfxon == 1:
                        click_sound.play()
                    webbrowser.open('https://github.com/o-zonc/APTP2023')
                if quit_button_x <= mouse_pos[0] <= quit_button_x + button_width and \
                        quit_button_y[1] <= mouse_pos[1] <= quit_button_y[1] + button_height:
                    if mode.sfxon == 1:
                        click_sound.play()
                        window.fill(chroma.BLACK)
                    return 0

        pygame.display.flip()


def resetpage():
    # Create Pygame window
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Reset?")

    font = pygame.font.Font(pretendardblack, 36)

    # Define button properties
    button_width, button_height = 250, 50
    yes_button_x, yes_button_y = (WIDTH - button_width) // 4, (HEIGHT - button_height) // 2
    no_button_x, no_button_y = 3 * (WIDTH - button_width) // 4, (HEIGHT - button_height) // 2
    yes_text_surface, yes_text_rect, no_text_surface, no_text_rect = 0, 0, 0, 0

    # Define label properties
    label = pygame.font.Font(pretendardmedium, 36)
    label_surface = label.render("Do you really want to reset?", True, chroma.WHITE)
    label_rect = label_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - button_height - PADDING))
    window.blit(label_surface, label_rect)

    quitrun = True

    while quitrun:
        sfx.monochrome()

        # Define button properties that might be updated
        if mode.monochrome == 0:
            yes_text_surface = font.render("Yes", True, chroma.BLACK)
            no_text_surface = font.render("No", True, chroma.BLACK)
            pygame.draw.rect(window, chroma.GRAY, ((yes_button_x, yes_button_y,
                                                    button_width, button_height)))
            pygame.draw.rect(window, chroma.ORANGEISTHENEWBLACK, ((no_button_x, no_button_y,
                                                                   button_width, button_height)))
        elif mode.monochrome == 1:
            yes_text_surface = font.render("Yes", True, chroma.WHITE)
            no_text_surface = font.render("No", True, chroma.BLACK)
            pygame.draw.rect(window, chroma.BLACK, ((yes_button_x, yes_button_y,
                                                     button_width, button_height)))
            pygame.draw.rect(window, chroma.WHITE, ((no_button_x, no_button_y,
                                                     button_width, button_height)))
        yes_text_rect = yes_text_surface.get_rect(center=(yes_button_x + button_width // 2,
                                                          yes_button_y + button_height // 2))
        no_text_rect = no_text_surface.get_rect(center=(no_button_x + button_width // 2,
                                                        no_button_y + button_height // 2))
        window.blit(yes_text_surface, yes_text_rect)
        window.blit(no_text_surface, no_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitpage()
                pygame.display.set_caption("Reset?")

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if yes_button_x <= mouse_pos[0] <= yes_button_x + button_width and \
                        yes_button_y <= mouse_pos[1] <= yes_button_y + button_height:
                    if mode.sfxon == 1:
                        click_sound.play()
                    readout.init()
                    return
                if no_button_x <= mouse_pos[0] <= no_button_x + button_width and \
                        no_button_y <= mouse_pos[1] <= no_button_y + button_height:
                    if mode.sfxon == 1:
                        click_sound.play()
                    window.fill(chroma.BLACK)
                    return

        pygame.display.flip()
