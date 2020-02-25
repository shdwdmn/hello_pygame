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
black_color = pg.Color('black')  # (0, 0, 0, 255)
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
coord_list = ((1372, 517), (1397, 367), (1407, 244), (1377, 131), (1273, 41), (1086, 61), (987, 168),
              (938, 308), (934, 433), (960, 555), (831, 635), (772, 413), (799, 255), (762, 133), (628, 63),
              (467, 128), (402, 257), (396, 438), (394, 576), (292, 649), (225, 501), (233, 353), (243, 181))
start = (1352, 642)
finish = (161, 80)
goal_score = len(coord_list)


def draw_text(text_object: object, position: tuple):
    screen.blit(text_object, (position, (0, 0)))


def render_text(text: object, size: int, color, background):
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
            board = self.board
            message = self.message
            player1 = self.player1
            player2 = self.player2
            player3 = self.player3
            player4 = self.player4

            clock.tick(frame_rate)

            # start drawing
            self.draw_main_elements()

            player1.update(board.nodes_list[player1.score].effects)
            player2.update(board.nodes_list[player2.score].effects)
            player3.update(board.nodes_list[player3.score].effects)
            player4.update(board.nodes_list[player4.score].effects)

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
                    if 0 <= coordinates[0] <= text_split and bar_split <= coordinates[1]:  # dice
                        if self.state == 'first move' or self.state == 'invitation':
                            self.state = 'dice throw'
                            print(self.state)
                    elif 0 <= coordinates[1] <= bar_split:  # board
                        if self.state == 'dice throw':
                            self.state = 'first move'
                            print(self.state)
                        if self.state == 'player select':
                            self.state = 'first move'
                            print(self.state)
                    elif text_split <= coordinates[0] <= character_split and bar_split <= coordinates[1]:  # messages
                        message.update('message click', dice.number)
                    elif character_split <= coordinates[0] and bar_split <= coordinates[1]:  # players
                        # if character_split+char_size[0]*0 <= coordinates[0] <= character_split+char_size[0]*1:
                        #     player1.score += 1
                        # elif character_split+char_size[0]*1 <= coordinates[0] <= character_split+char_size[0]*2:
                        #     player2.score += 1
                        # elif character_split+char_size[0]*2 <= coordinates[0] <= character_split+char_size[0]*3:
                        #     player3.score += 1
                        # elif character_split+char_size[0]*3 <= coordinates[0] <= character_split+char_size[0]*4:
                        #     player4.score += 1

                        if self.state == 'player select':
                            self.state = 'first move'
                            print(self.state)
                        if self.state == 'dice done':
                            self.state = 'player change'
                            print(self.state)

            pg.display.update()  # redraw


class Grid:
    def __init__(self):
        for x in range(0, window_w, 100):
            pg.draw.line(screen, black_color, (x, 0), (x, window_h))
        for y in range(0, window_h, 100):
            pg.draw.line(screen, black_color, (0, y), (window_w, y))


class Board:
    def __init__(self):
        self.nodes_list = []
        self.nodes_list.append(Node(start[0], start[1], 'start'))
        for node in range(1, goal_score):
            self.nodes_list.append(Node(coord_list[node][0], coord_list[node][1], 'regular'))
            print(f'node #{node}, effects: {self.nodes_list[node].effects}')
        self.nodes_list.append(Node(finish[0], finish[1], 'finish'))


class Node:
    def __init__(self, x: int, y: int, kind: str):
        effects_list = ('+2 steps', '-2 steps')
        effects_count = 2
        self.coordinates = (x, y)
        self.kind = kind
        self.effects = []
        for count in range(effects_count):
            self.effects.append(effects_list[randrange(len(effects_list))])


class Message:
    def __init__(self):
        self.string_no = 0
        self.border = 20
        self.position = (text_split + self.border, bar_split + self.border)
        self.step = self.border

    def display(self, string: str, size=32, color=black_color, background=None, center=True):
        text, text_height, text_weight = render_text(string, size, color, background)
        if not center:
            self.position = (text_split + self.border, bar_split + self.step)
        else:
            self.position = (text_split + int((character_split - text_split)/2) - int(text_weight/2),
                             bar_split + self.step)
        draw_text(text, self.position)
        self.step += text_height

    def update(self, state: str, number=None, score=0, effects=()):
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
        elif state == 'moving':
            self.display(f'Ячейка {score}')
            self.display(f'{effects}')
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

    def update(self, state: str):
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
    def __init__(self, number: int):
        self.border = 3
        self.number = number
        self.score = 0
        self.sprite = char_images[number - 1]
        self.initial_pos = (character_split + char_size[0] * (self.number - 1) + self.border, bar_split + self.border)
        self.update()

    def update(self, effects=()):
        if '+2 steps' in effects:
            self.score += 2
        if '-2 steps' in effects:
            self.score -= 2

        if self.score == 0:
            position = self.initial_pos
        elif 0 < self.score < goal_score:
            position = coord_list[self.score-1]
        else:
            position = finish

        text, text_height, text_weight = render_text(f'{self.score}', 24, pg.Color('red'), background_color)
        draw_text(text, position)  # TODO: fix drawing score text
        screen.blit(self.sprite, position)


main_screen = MainScreen()
main_screen.update()

quit()
