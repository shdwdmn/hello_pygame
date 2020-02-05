import os
import random
import pygame as pg

window_w = 1600
window_h = 900
bar_split = int(window_h / 5 * 4)
text_split = int(window_w / 5 * 1)
character_split = int(window_w / 5 * 4)
window_position = '150, 50'
black_color = pg.Color('black')
score_color = pg.Color('darkolivegreen4')
background_color = pg.Color('white')
background_image = pg.image.load('images/background_draft.png')
background_image = pg.transform.scale(background_image, (window_w, bar_split))
char_size = (80, 180)
char_images = [pg.image.load('images/char1.png'),
               pg.image.load('images/char2.png'),
               pg.image.load('images/char3.png'),
               pg.image.load('images/char4.png')]
dice_images = [pg.image.load('images/Alea_1.png'),
               pg.image.load('images/Alea_2.png'),
               pg.image.load('images/Alea_3.png'),
               pg.image.load('images/Alea_4.png'),
               pg.image.load('images/Alea_5.png'),
               pg.image.load('images/Alea_6.png')]
for i in range(0, len(char_images)):
    char_images[i] = pg.transform.scale(char_images[i], char_size)
re_roll_count = 10  # frames count for dice animation

font_path = 'fonts/Ritalin.ttf'
os.environ['SDL_VIDEO_WINDOW_POS'] = window_position

pg.init()
screen = pg.display.set_mode((window_w, window_h))
pg.display.set_caption("MAP")
clock = pg.time.Clock()


def draw_text(text, size, position, color, background):
    font = pg.font.Font(font_path, size)
    text = font.render(text, True, color, background)
    screen.blit(text, (position, (0, 0)))
    text_rect = text.get_rect()
    text_height = text_rect[3]-text_rect[1]
    text_weight = text_rect[2]-text_rect[0]
    return text_height, text_weight


class MainScreen:
    def __init__(self):
        screen.fill(background_color)
        screen.blit(background_image, (0, 0))
        pg.draw.line(screen, black_color, (0, bar_split), (window_w, bar_split), 4)
        pg.draw.line(screen, black_color, (text_split, bar_split), (text_split, window_h), 4)
        pg.draw.line(screen, black_color, (character_split, bar_split), (character_split, window_h), 4)


class Grid:
    def __init__(self):
        for x in range(0, window_w, 100):
            pg.draw.line(screen, black_color, (x, 0), (x, window_h))
        for y in range(0, window_h, 100):
            pg.draw.line(screen, black_color, (0, y), (window_w, y))


class Message:
    def __init__(self):
        self.string_no = 0
        self.border = 20
        self.position = (text_split + self.border, bar_split + self.border)
        self.step = self.border

    def display(self, string, size=32, color=black_color, background=None):
        text_height, text_weight = draw_text(string, size, self.position, color, background)
        self.step += text_height
        self.position = (text_split + self.border, bar_split + self.step)


class Score:
    def __init__(self):
        self.position = (30, bar_split + 30)

    def update(self, _count):
        draw_text(f'ОЧКОВ: {_count}', 64, self.position, background_color, score_color)


class Dice:
    def __init__(self):
        self.border = 25
        self.position = (self.border, bar_split + self.border)
        self.update()

    def update(self):
        global roll_count
        global roll_back
        if roll_count > 0:
            roll_back = random.randrange(5)
        sprite = dice_images[roll_back]
        screen.blit(sprite, self.position)
        roll_count -= 1

    def roll(self):
        global roll_count
        global re_roll_count
        roll_count = re_roll_count
        self.update()


class Player:
    def __init__(self, number):
        border = 3
        sprite = char_images[number-1]
        screen.blit(sprite, (character_split + char_size[0]*(number-1) + border, bar_split + border))


terminated = False
count = 0
roll_count = re_roll_count  # to start animation immediately
roll_back = None
while not terminated:  # main cycle
    clock.tick(5)

    main = MainScreen()
    # g = Grid()
    player1 = Player(1)
    player2 = Player(2)
    player3 = Player(3)
    player4 = Player(4)
    # score = Score()
    dice = Dice()
    message = Message()

    for event in pg.event.get():
        if event.type == pg.QUIT:  # 'close' button event
            terminated = True

    # keys = pg.key.get_pressed()
    # if keys[pg.K_LEFT]:
    #     x -= step
    # if keys[pg.K_RIGHT]:
    #     x += step
    # if keys[pg.K_DOWN]:
    #     y += step
    # if keys[pg.K_UP]:
    #     y -= step

    # score.update(count)

    message.display('Первый раунд.')
    message.display('Бросайте свои кости!')
    message.display('И будь что будет......... )')
    # message.display('GAME OVER', 99, background=background_color)

    # dice.roll()

    pg.display.update()  # redraw

# if terminated:  # if window closed
pg.quit()
quit()
