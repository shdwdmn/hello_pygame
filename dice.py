import pygame as pg
from os import environ
from random import randrange

window_w = 1600
window_h = 900
frame_rate = 8
roll_frames = 10  # frames amount for dice animation
win = 50  # score to win
board_border = int(window_h / 5 * 4)
message_border = int(window_w / 5 * 1)
players_border = int(window_w / 5 * 4)
window_position = '300, 50'
black_color = pg.Color('black')  # (0, 0, 0, 255)
score_color = pg.Color('darkolivegreen4')
background_color = pg.Color('white')
background_image = pg.image.load('images/background_draft.png')
background_image = pg.transform.scale(background_image, (window_w, board_border))
char_size = (80, 80)
char_images = [pg.image.load('images/char1.jpg'),
               pg.image.load('images/char2.jpg'),
               pg.image.load('images/char3.jpg'),
               pg.image.load('images/char4.jpg')]
dice_images = [pg.image.load('images/Alea_1.png'),
               pg.image.load('images/Alea_2.png'),
               pg.image.load('images/Alea_3.png'),
               pg.image.load('images/Alea_4.png'),
               pg.image.load('images/Alea_5.png'),
               pg.image.load('images/Alea_6.png')]
throw_image = pg.image.load('images/throw_dice_f.png')
throw_image = pg.transform.scale(throw_image, (message_border, window_h - board_border))
for i in range(0, len(char_images)):
    char_images[i] = pg.transform.scale(char_images[i], char_size)

font_path = 'fonts/Ritalin.ttf'
environ['SDL_VIDEO_WINDOW_POS'] = window_position

pg.init()
screen = pg.display.set_mode((window_w, window_h))
pg.display.set_caption('FISHECHKI')
clock = pg.time.Clock()
coord_list = ((1372, 517), (1397, 367), (1407, 244), (1377, 131), (1273, 41), (1086, 61), (987, 168), (938, 308),
              (934, 433), (960, 555), (831, 635), (772, 413), (799, 255), (762, 133), (628, 63), (467, 128),
              (402, 257), (396, 438), (394, 576), (292, 649), (225, 501), (233, 353), (243, 181))
start = (1352, 642)
finish = (161, 80)
goal_score = len(coord_list)
wait_phrases = ('Кости летят как хлебушек с паштетом...',
                'Кости летят как шлюхи с небоскреба...',
                'Эх кости мои кости...',
                'Ах если бы не кости, кости-костюшки мои...',
                'Мы идем. а кости летят',
                'Кости летят, а они сидят',
                'Любишь кости, люби и летать',
                'Не те кости летают, что в стакане',
                'Стакан без костей хорош лишь только промежутками',
                'Что кости, а что бросает, где грань, и где же потолок?',
                'Чем кость не тешилась, лишь бы летала')
states_list = ('first move', 'dice throw', 'dice wait', 'dice done', 'moving', 'player change', 'victory')


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
        self.state = 'first move'
        print('=+', self.state)
        self.dice = Dice()
        self.board = Board()
        self.message = Message()
        self.player1 = Player(1)
        self.player2 = Player(2)
        self.player3 = Player(3)
        self.player4 = Player(4)
        self.players = [self.player1, self.player2, self.player3, self.player4]
        self.current = self.players[0]

    @staticmethod
    def draw_main_elements():
        screen.fill(background_color)
        screen.blit(background_image, (0, 0))
        pg.draw.line(screen, black_color, (0, board_border), (window_w, board_border), 4)
        pg.draw.line(screen, black_color, (message_border, board_border), (message_border, window_h), 4)
        pg.draw.line(screen, black_color, (players_border, board_border), (players_border, window_h), 4)

    def change_player(self):
        if self.current == self.player1:
            self.current = self.player2
        elif self.current == self.player2:
            self.current = self.player3
        elif self.current == self.player3:
            self.current = self.player4
        elif self.current == self.player4:
            self.current = self.player1

    def update(self):
        while not self.terminated:  # main cycle
            dice = self.dice
            board = self.board
            message = self.message
            player = self.current

            clock.tick(frame_rate)

            self.draw_main_elements()

            if self.state == 'moving':  # TODO: use bonuses, it don't apply now
                print(f'Player {player.number}: score={player.score}')
                player.score += dice.number + 1
                player.draw()
                node = board.nodes_list[player.score]
                print(f'New score is {player.score}')
                print(f'Moving: surprise is {node.surprise}, bonus={node.bonus}')
                self.state = 'new cell'
                print('=+', self.state)
            self.player1.draw()
            self.player2.draw()
            self.player3.draw()
            self.player4.draw()

            self.state = dice.update(self.state)

            node = board.nodes_list[player.score]
            message.update(self.state, player.number, player.score, player.phrase,
                           dice.number, node.surprise, node.bonus)

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
                    # print(coordinates)
                    if 0 <= coordinates[0] <= message_border and board_border <= coordinates[1]:  # dice area
                        if self.state == 'first move' or self.state == 'player change':
                            self.state = 'dice throw'
                            print('=+', self.state)
                        elif self.state == 'dice done':
                            self.state = 'moving'
                            print('=+', self.state)
                    elif 0 <= coordinates[1] <= board_border:  # board area
                        if self.state == 'dice done':
                            self.state = 'moving'
                            print('=+', self.state)
                        elif self.state == 'player change' or self.state == 'first move':
                            self.state = 'dice throw'
                            print('=+', self.state)
                        elif self.state == 'new cell':
                            self.state = 'player change'
                            self.change_player()
                            print('=+', self.state)
                            print(f'Player {self.current.number} is moving')
                    elif message_border <= coordinates[0] <= players_border \
                            and board_border <= coordinates[1]:  # messages
                        message.update('message click', self.current.number, dice.number)
                    elif players_border <= coordinates[0] and board_border <= coordinates[1]:  # players
                        if self.state == 'player change':
                            self.state = 'dice throw'
                            print('=+', self.state)
                        elif self.state == 'new cell':
                            self.state = 'player change'
                            print('=+', self.state)
                        elif self.state == 'dice done':
                            self.state = 'moving'
                            print('=+', self.state)

            pg.display.update()  # redraw


class Board:

    def __init__(self):
        self.nodes_list = []
        self.nodes_list.append(Node(start[0], start[1], 'start'))
        for node in range(1, goal_score):
            self.nodes_list.append(Node(coord_list[node][0], coord_list[node][1], 'regular'))
            print(f'node #{node}, bonus: {self.nodes_list[node].bonus}, surprise: {self.nodes_list[node].surprise}')
        self.nodes_list.append(Node(finish[0], finish[1], 'finish'))


class Node:

    def __init__(self, x: int, y: int, kind: str):
        self.coordinates = (x, y)
        self.kind = kind

        if randrange(5) < 1:  # 20% chance
            if randrange(2) == 1:
                self.bonus = 4
            else:
                self.bonus = -4
        else:
            self.bonus = 0

        if randrange(5) < 1:
            self.surprise = True
            if randrange(5) == 0:
                self.bonus = 8
            elif randrange(5) == 1:
                self.bonus = -8
            elif randrange(5) == 2:
                pass
            elif randrange(5) == 3:
                self.bonus = 0
            elif randrange(5) == 4:
                self.bonus = 6
        else:
            self.surprise = False


class Message:

    def __init__(self):
        self.string_no = 0
        self.border = 20
        self.position = (message_border + self.border, board_border + self.border)
        self.step = self.border

    def display(self, string: str, size=32, color=black_color, background=None, center=True):
        text, text_height, text_weight = render_text(string, size, color, background)
        if not center:
            self.position = (message_border + self.border, board_border + self.step)
        else:
            self.position = (message_border + int((players_border - message_border) / 2) - int(text_weight / 2),
                             board_border + self.step)
        draw_text(text, self.position)
        self.step += text_height

    def update(self, state: str, player: int, score: int, phrase='', number=None, surprise=False, bonus=0):
        self.step = self.border
        self.position = (message_border + self.border, board_border + self.border)
        if state == 'first move':
            self.display('Ходит Игрок №1')
            self.display('')
            self.display('Кидай КУБИК (КУБИК это слева)')
        elif state == 'dice wait':
            self.display(phrase)
        elif state == 'dice done' and number:
            self.display(f'Выброшено {number + 1} костей')
        elif state == 'moving':
            self.display('Передвигаемся...')
        elif state == 'new cell':
            self.display(f'Клетка {score}')
            if surprise:
                self.display(f'СЮР-ПРИЗ!')
            else:
                self.display('')
            self.display(f'Бонус: {bonus}')
        elif state == 'player change':
            self.display(f'Ход игрока №{str(player)}')
        elif state == 'message click':
            self.display('')
            self.display('КЛЕК')


class Dice:

    def __init__(self):
        self.position = (0, board_border + 3)
        self.sprite = throw_image
        self.rolled_count = 0  # dice rolled count (for internal use)
        self.number = 5  # initial dice number
        self.state = 'player select'
        self.blink = False

    def update(self, state: str):
        self.state = state
        if state == 'first move':
            self.sprite = throw_image
            screen.blit(self.sprite, self.position)
        elif state == 'dice throw':
            self.number = randrange(5)
            self.rolled_count = 1
            self.state = 'dice wait'
            print('=+', self.state)
            self.sprite = dice_images[self.number]
        elif state == 'dice wait':
            if self.rolled_count < roll_frames:
                self.number = randrange(5)
                self.rolled_count += 1
                self.state = 'dice wait'
            else:
                self.state = 'dice done'
                print('=+', self.state)
                print(f'dice == {self.number+1}')
            self.sprite = dice_images[self.number]
        # elif state == 'dice done':
        #     pass

        if state == 'dice wait' and not self.blink:
            self.blink = True
        else:
            self.blink = False
        if not self.blink:
            screen.blit(self.sprite, self.position)

        return self.state


class Player:

    def __init__(self, number: int):
        self.border = 3
        self.number = number
        self.score = 0
        self.sprite = char_images[number - 1]
        self.initial_pos = (players_border + char_size[0] * (self.number - 1) + self.border, board_border + self.border)
        # self.new_cell()
        self.phrase = ''

    def draw(self):
        if self.score == 0:
            position = self.initial_pos
        elif 0 < self.score < goal_score:
            position = [coord_list[self.score - 1][0], coord_list[self.score - 1][1]]  # converting tuple to list
            position[0] -= int(char_size[0] / 2)
            position[1] -= int(char_size[1] / 2)
        else:
            position = finish

        text, text_height, text_weight = render_text(f'{self.score}', 24, pg.Color('red'), background_color)
        if self.score > 0:
            draw_text(text, self.initial_pos)  # score in players area
        screen.blit(self.sprite, position)
    #
    # def new_cell(self, bonus=0, surprise=False):
    #     self.score += bonus
    #     if self.score < 0:
    #         self.score = 0


main_screen = MainScreen()
main_screen.update()
