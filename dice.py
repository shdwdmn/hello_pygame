import pygame as pg
from os import environ
from random import randrange

window_w = 1600
window_h = 900
frame_rate = 8
roll_frames = 15  # frames amount for dice animation
win = 50  # score to win
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
environ['SDL_VIDEO_WINDOW_POS'] = window_position

pg.init()
screen = pg.display.set_mode((window_w, window_h))
pg.display.set_caption('FISHECHKI')
clock = pg.time.Clock()
states_list = ('player select', 'player change', 'first move', 'invitation', 'dice throw', 'dice wait', 'dice done')


def draw_text(text_object, position):
    screen.blit(text_object, (position, (0, 0)))


def render_text(text, size, color, background):
    font = pg.font.Font(font_path, size)
    text = font.render(text, True, color, background)
    text_rect = text.get_rect()
    text_height = text_rect[3] - text_rect[1]
    text_weight = text_rect[2] - text_rect[0]
    return text, text_height, text_weight


class MainScreen:
    def __init__(self):
        self.terminated = False
        self.state = states_list[0]
        self.dice = Dice()
        self.board = Board()
        self.message = Message()
        self.player1 = Player(1)
        self.player2 = Player(2)
        self.player3 = Player(3)
        self.player4 = Player(4)
        self.current = self.player1

    @staticmethod
    def draw_main_elements():
        screen.fill(background_color)
        screen.blit(background_image, (0, 0))
        pg.draw.line(screen, black_color, (0, bar_split), (window_w, bar_split), 4)
        pg.draw.line(screen, black_color, (text_split, bar_split), (text_split, window_h), 4)
        pg.draw.line(screen, black_color, (character_split, bar_split), (character_split, window_h), 4)

    def update(self):
        while not self.terminated:  # main cycle
            dice = self.dice
            message = self.message
            player1 = self.player1
            player2 = self.player2
            player3 = self.player3
            player4 = self.player4

            clock.tick(frame_rate)

            # start drawing
            self.draw_main_elements()

            player1.update()
            player2.update()
            player3.update()
            player4.update()

            self.state = dice.update(self.state)
            message.update(self.state, dice.number)

            pressed = pg.key.get_pressed()
            alt_held = pressed[pg.K_LALT] or pressed[pg.K_RALT]
            ctrl_held = pressed[pg.K_LCTRL] or pressed[pg.K_RCTRL]
            for event in pg.event.get():
                if event.type == pg.QUIT:  # close button
                    self.terminated = True
                if event.type == pg.KEYDOWN:
                    if (event.key == pg.K_F4 and alt_held) or (event.key == pg.K_w and ctrl_held):  # alt+f4 or ctrl+w
                        self.terminated = True
                if event.type == pg.MOUSEBUTTONDOWN:
                    coordinates = pg.mouse.get_pos()
                    print(coordinates)
                    print(self.state)
                    if 0 <= coordinates[0] <= text_split and bar_split <= coordinates[1]:  # dice
                        if self.state == 'first move' or self.state == 'invitation':
                            self.state = 'dice throw'
                    elif text_split <= coordinates[0] <= character_split and bar_split <= coordinates[1]:  # messages
                        message.update('message click', dice.number)
                    elif character_split <= coordinates[0] and bar_split <= coordinates[1]:  # players
                        if character_split+char_size[0]*0 <= coordinates[0] <= character_split+char_size[0]*1:
                            player1.score += 1
                        elif character_split+char_size[0]*1 <= coordinates[0] <= character_split+char_size[0]*2:
                            player2.score += 1
                        elif character_split+char_size[0]*2 <= coordinates[0] <= character_split+char_size[0]*3:
                            player3.score += 1
                        elif character_split+char_size[0]*3 <= coordinates[0] <= character_split+char_size[0]*4:
                            player4.score += 1

                        if self.state == 'player select':
                            self.state = 'first move'
                        if self.state == 'dice done':
                            self.state = 'player change'

            pg.display.update()  # redraw


class Grid:
    def __init__(self):
        for x in range(0, window_w, 100):
            pg.draw.line(screen, black_color, (x, 0), (x, window_h))
        for y in range(0, window_h, 100):
            pg.draw.line(screen, black_color, (0, y), (window_w, y))


class Board:
    def __init__(self):
        pass

    def something(self):
        pass


class Message:
    def __init__(self):
        self.string_no = 0
        self.border = 20
        self.position = (text_split + self.border, bar_split + self.border)
        self.step = self.border

    def display(self, string, size=32, color=black_color, background=None, center=True):
        text, text_height, text_weight = render_text(string, size, color, background)
        if not center:
            self.position = (text_split + self.border, bar_split + self.step)
        else:
            self.position = (text_split + int((character_split - text_split)/2) - int(text_weight/2),
                             bar_split + self.step)
        draw_text(text, self.position)
        self.step += text_height

    def update(self, state, number=None):
        self.step = self.border
        self.position = (text_split + self.border, bar_split + self.border)
        if state == 'player select':
            self.display('ДОБРОПОЖ')
            self.display('Это ИГРА в ФИШЕЧКИ')
            self.display('Выбирай ИГРОКА (ИГРОК это справа)')
        if state == 'first move':
            self.display('Ходит Игрок №1')
            self.display('И не важно, что ты там нажал')
            self.display('Кидай КУБИК (КУБИК это слева)')
        elif state == 'dice wait':
            self.display('Кости летят как шлюхи с небоскреба...')
        elif state == 'dice done' and number:
            self.display(f'Выброшено {number + 1} костей')
        elif state == 'message click':
            self.display('')
            self.display('КЛЕК')


class Dice:
    def __init__(self):
        self.position = (0, bar_split + 3)
        self.sprite = throw_image
        # self.dice_wait = True  # initial state of dice image displaying
        self.roll_frames = roll_frames  # frames amount for dice animation
        self.rolled_count = 0  # dice rolled count (for internal use)
        self.number = 5  # initial dice number
        self.state = 'player select'

    def update(self, state):
        self.state = state
        if state == 'player select':
            # self.sprite = throw_image
            # screen.blit(self.sprite, self.position)
            pass
        if state == 'first move':
            self.sprite = throw_image
            screen.blit(self.sprite, self.position)
        elif state == 'dice throw':
            self.number = randrange(5)
            self.rolled_count = 1
            self.state = 'dice wait'
            self.sprite = dice_images[self.number]
        elif state == 'dice wait':
            if self.rolled_count < self.roll_frames:
                self.number = randrange(5)
                self.rolled_count += 1
                self.state = 'dice wait'
            else:
                self.state = 'dice done'
            self.sprite = dice_images[self.number]
        elif state == 'dice done':
            pass
        screen.blit(self.sprite, self.position)
        return self.state


class Player:
    def __init__(self, number):
        self.border = 3
        self.number = number
        self.score = 0
        self.sprite = char_images[number - 1]
        self.initial_pos = (character_split + char_size[0] * (self.number - 1) + self.border, bar_split + self.border)
        self.update()

    def update(self):
        position = self.initial_pos
        if self.score > 0:
            start = (position[0], position[1] - self.border - char_size[1])
            end = (position[0] - character_split, char_size[1])
            path_x = end[0] - start[0]
            path_y = end[1] - start[1]
            position = (start[0] + int(path_x/win*self.score), start[1] + int(path_y/win*self.score))
        text, text_height, text_weight = render_text(f'{self.score}', 24, pg.Color('red'), background_color)
        draw_text(text, position)  # TODO: fix drawing score text
        screen.blit(self.sprite, position)


main_screen = MainScreen()
main_screen.update()

quit()
