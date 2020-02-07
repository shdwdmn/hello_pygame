import os
import random
import pygame as pg

window_w = 1600
window_h = 900
frame_rate = 10
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
throw_image = pg.image.load('images/throw_dice_f.png')
throw_image = pg.transform.scale(throw_image, (text_split, window_h-bar_split))
for i in range(0, len(char_images)):
    char_images[i] = pg.transform.scale(char_images[i], char_size)

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
        self.terminated = False
        self.player1 = Player(1)
        self.player2 = Player(2)
        self.player3 = Player(3)
        self.player4 = Player(4)
        # self.score = Score()
        self.dice = Dice()
        self.message = Message()

    @staticmethod
    def main_elements():
        screen.fill(background_color)
        screen.blit(background_image, (0, 0))
        pg.draw.line(screen, black_color, (0, bar_split), (window_w, bar_split), 4)
        pg.draw.line(screen, black_color, (text_split, bar_split), (text_split, window_h), 4)
        pg.draw.line(screen, black_color, (character_split, bar_split), (character_split, window_h), 4)

    def update(self):
        while not self.terminated:  # main cycle
            clock.tick(frame_rate)

            dice = self.dice
            dice.update()

            message = self.message
            message.reset()

            player1 = self.player1
            player2 = self.player2
            player3 = self.player3
            player4 = self.player4

            self.main_elements()

            for event in pg.event.get():  # TODO: catch alt+f4 also
                if event.type == pg.QUIT:  # 'close' button event
                    self.terminated = True

            coordinates = (-1, -1)
            if pg.mouse.get_pressed()[0]:  # 0 for left mouse button, 1 for mid, 2 for right
                coordinates = pg.mouse.get_pos()
                # print(coordinates)
            if 0 <= coordinates[0] <= text_split and bar_split <= coordinates[1] <= window_h:
                dice.left_click()
            if not pg.mouse.get_pressed()[0]:
                dice.dice_wait = True

            message.display('Первый раунд.')
            message.display('Бросайте свои кости!')
            message.display('И будь что будет......... )')
            # message.display('GAME OVER', 99, background=background_color)

            # dice.throw()

            player1.update()
            player2.update()
            player3.update()
            player4.update()

            pg.display.update()  # redraw


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

    def reset(self):
        self.step = self.border
        self.position = (text_split + self.border, bar_split + self.border)


class Score:
    def __init__(self):
        self.position = (30, bar_split + 30)

    def update(self, count):
        draw_text(f'ОЧКОВ: {count}', 64, self.position, background_color, score_color)


class Dice:
    def __init__(self):
        self.position = (0, bar_split + 3)
        self.sprite = throw_image
        # self.blink = False  # if blink: sprite is not displayed
        self.dice_wait = True  # initial state of dice image displaying
        self.roll_frames = 10  # frames amount for dice animation
        self.rolled_count = 0  # dice rolled count (for internal use)
        self.number = 5  # initial dice number
        self.update()

    def update(self):
        if self.dice_wait:
            self.sprite = throw_image
            screen.blit(self.sprite, self.position)  # TODO: fix image displaying
        else:
            if self.rolled_count < self.roll_frames:
                self.number = random.randrange(5)
                self.rolled_count += 1
            self.sprite = dice_images[self.number]
            screen.blit(self.sprite, self.position)
            # if not self.blink:
            #     screen.blit(self.sprite, self.position)
            #     self.blink = True
            # else:
            #     self.blink = False

    def throw(self):
        self.rolled_count = 0
        self.dice_wait = False
        self.update()

    def left_click(self):
        self.throw()


class Player:
    def __init__(self, num):
        self.border = 3
        self.num = num
        self.sprite = char_images[num-1]
        self.update()

    def update(self):
        screen.blit(self.sprite, (character_split + char_size[0]*(self.num-1) + self.border, bar_split + self.border))


main_screen = MainScreen()
main_screen.update()

pg.quit()
quit()
