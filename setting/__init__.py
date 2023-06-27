from .mode import *
from .readout import *
from .chroma import *

WIDTH = 800
HEIGHT = 600
PADDING = 10

pretendardblack = './src/font/Pretendard-Black.ttf'
pretendardmedium = './src/font/Pretendard-Medium.ttf'
dgm = './src/font/DungGeunMo.ttf'


class sound():
    def __init__(self):
        self.splash = './src/sound/01_splash.mp3'
        self.homebackground = './src/sound/02_reflected-light-147979.mp3'
        self.click = './src/sound/03_click.wav'
        self.background = './src/sound/04_digital_love.mp3'
        self.wall = './src/sound/05_wallhit.mp3'
        self.brick = './src/sound/06_brickhit.mp3'
        self.paddle = './src/sound/07_paddlehit.mp3'
        self.newhigh = './src/sound/10_new_high.mp3'
        self.gameover = './src/sound/14_game_over.wav'
        self.quit = './src/sound/15_lego_piece_pressed.mp3'
        self.aistart = './src/sound/17_blaster-2-81267.mp3'
        self.alert = './src/sound/19_error-when-entering-the-game-menu-132111.mp3'

    def monochrome(self):
        if mode.monochrome == 0:
            self.background = './src/sound/04_digital_love.mp3'
            self.gameover = './src/sound/14_game_over.wav'
        else:
            self.background = './src/sound/08_futuristic-beat-146661.mp3'
            self.gameover = './src/sound/18_mixkit-click-error-1110.wav'


__all__ = ['WIDTH', 'HEIGHT', 'PADDING', 'pretendardblack', 'pretendardmedium', 'dgm',
           'sound', 'chroma', 'mode', 'readout']
