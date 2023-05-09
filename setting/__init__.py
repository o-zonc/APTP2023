WIDTH = 800
HEIGHT = 600

SPLASHWIDTH = 600
SPLASHHEIGHT = 400

pretendardblack = './src/font/Pretendard-Black.ttf'
pretendardmedium = './src/font/Pretendard-Medium.ttf'


class sound():
    def __init__(self):
        self.background = './src/sound/02_digital_love.mp3'
        self.wall = './src/sound/03_wallhit.mp3'
        self.brick = './src/sound/04_brickhit.mp3'
        self.paddle = './src/sound/05_paddlehit.mp3'
        self.gameover = './src/sound/14_game_over.wav'


__all__ = ['WIDTH', 'HEIGHT', 'SPLASHWIDTH', 'SPLASHHEIGHT',
           'pretendardblack', 'pretendardmedium', 'sound']
