import pygame as pg
from os import environ
from math import sin, cos, pi
from random import randrange, shuffle

# TODO:
#  - difficulties
#  - boxing hand on hover
win_score = 20
start_timer = 10
clown_size = 150
star_edges = 9
star_rotate = pi/300
star_gauge = 3

window_w = 1225
window_h = 875
frame_rate = 60
window_position = '675, 125'
black = pg.Color('black')  # (0, 0, 0, 255)
brown = pg.Color('brown')
white = pg.Color('white')
red = pg.Color('red')

font_path = 'fonts/Ritalin.ttf'
environ['SDL_VIDEO_WINDOW_POS'] = window_position

pg.init()
screen = pg.display.set_mode((window_w, window_h))
pg.display.set_caption('PUNCH THAT CLOWN')
pg.mixer_music.load('midi/fast.mid')
pg.mixer_music.play(-1)
clock = pg.time.Clock()

big_button = ((int(window_w/5*2), int(window_h/5*2)), (int(window_w/5), int(window_h/5)))
score = 0

background_image = pg.image.load('images/room.jpg')
background_image = pg.transform.scale(background_image, (window_w, window_h))
clowns = [pg.image.load('images/clown1.jpg'),
          pg.image.load('images/clown2.jpg'),
          pg.image.load('images/clown3.jpg'),
          pg.image.load('images/clown4.jpg'),
          pg.image.load('images/clown5.jpg'),
          pg.image.load('images/clown6.jpg'),
          pg.image.load('images/clown7.jpg'),
          pg.image.load('images/clown8.jpg'),
          pg.image.load('images/clown9.jpg'),
          pg.image.load('images/clown10.jpg')]
for clown_num in range(len(clowns)):
    clowns[clown_num] = pg.transform.scale(clowns[clown_num], (clown_size, clown_size))


def draw_text(string: str, position=(0, 0), size=32, color=black, background=None, center=True):
    font = pg.font.Font(font_path, size)
    text = font.render(string, True, color, background)
    text_rect = text.get_rect()
    text_height = text_rect[3] - text_rect[1]
    text_weight = text_rect[2] - text_rect[0]
    if center:
        screen.blit(text, ((int(position[0] - text_weight/2), int(position[1] - text_height/2)), (0, 0)))
    else:
        screen.blit(text, ((int(position[0]), int(position[1])), (0, 0)))


def draw_score(_score: int):
    position = (window_w*1/25, window_h*9/10)
    draw_text(f'SCORE::{_score}', position, 48, brown, black, center=False)


def draw_timer(_timer: int):
    position = (window_w*8/10, window_h*9/10)
    draw_text(f'TIMER::{_timer:.2f}', position, 48, brown, black, center=False)


def get_clown():
    random = randrange(100)
    if 0 <= random <= 1:
        clown_number = 9
    elif 2 <= random <= 4:
        clown_number = 8
    elif 5 <= random <= 8:
        clown_number = 7
    elif 9 <= random <= 13:
        clown_number = 6
    elif 14 <= random <= 19:
        clown_number = 5
    elif 20 <= random <= 26:
        clown_number = 4
    elif 27 <= random <= 37:
        clown_number = 3
    elif 38 <= random <= 59:
        clown_number = 2
    elif 60 <= random <= 75:
        clown_number = 1
    else:
        clown_number = 0
    clown_image = clowns[clown_number]
    return clown_image, clown_number


def random_color():
    rgb = [255, 0, 0]
    shuffle(rgb)
    return tuple(rgb)


def start_over():
    global is_start, is_reset, timer, score
    is_start = True
    is_reset = True
    timer = start_timer
    score = 0
    pg.mixer_music.play()


class Star:
    def __init__(self, edges):
        self.edges = edges
        self.radius = 0
        self.points = []
        self.angle_step = 2 * pi / self.edges
        self.start_angle = 0
        self.color = random_color()

    def calc(self):
        self.points = []
        for edge in range(self.edges):
            angle = self.angle_step * edge + self.start_angle
            int_angle = self.angle_step * (edge + 0.5)
            point = (int(cos(angle) * self.radius + window_w/2),
                     int(sin(angle) * self.radius + window_h/2))
            int_point = (int(cos(int_angle) * self.radius * 0.6 + window_w / 2),
                         int(sin(int_angle) * self.radius * 0.6 + window_h / 2))
            self.points.append(point)
            self.points.append(int_point)

        self.radius += 5
        self.start_angle += star_rotate


class Background:
    def __init__(self):
        self.stars = []
        self.stars.append(Star(star_edges))

    def draw(self):
        screen.fill(white)
        for star in self.stars:
            star.calc()
            pg.draw.polygon(screen, star.color, star.points, star_gauge)
            if star.radius == 25:
                self.stars.append(Star(star_edges))
            if star.radius >= window_w:
                self.stars.pop(0)


timer = start_timer
is_start = True
is_reset = True
clown_position = (-1, -1)
clown = clowns[0]
back = Background()

while True:
    clock.tick(frame_rate)
    big_button_pressed = False
    # screen.blit(background_image, (0, 0))
    back.draw()

    if is_reset:
        clown, clown_num = get_clown()
        clown_position = (randrange(clown_size, window_w - clown_size),
                          randrange(clown_size, window_h - clown_size))
        is_reset = False

    pressed = pg.key.get_pressed()
    alt_held = pressed[pg.K_LALT] or pressed[pg.K_RALT]
    ctrl_held = pressed[pg.K_LCTRL] or pressed[pg.K_RCTRL]
    for event in pg.event.get():
        if event.type == pg.QUIT:  # close button
            quit()
        if event.type == pg.KEYDOWN:
            if (event.key == pg.K_F4 and alt_held) or (event.key == pg.K_w and ctrl_held):  # alt+f4 or ctrl+w
                quit()
            if event.key == pg.K_r or pg.K_F5:
                start_over()
        if event.type == pg.MOUSEBUTTONDOWN:
            coordinates = pg.mouse.get_pos()
            if big_button[0][0] <= coordinates[0] <= big_button[0][0] + big_button[1][0] and \
                    big_button[0][1] <= coordinates[1] <= big_button[0][1] + big_button[1][1]:
                big_button_pressed = True
            if clown_position[0] - clown_size/2 <= coordinates[0] <= clown_position[0] + clown_size/2 and \
               clown_position[1] - clown_size/2 <= coordinates[1] <= clown_position[1] + clown_size/2 and \
               score < win_score and timer > 0:  # CLOWN hit
                score += 1
                is_reset = True

    if score >= win_score:  # WIN screen
        pg.draw.rect(screen, white, big_button)
        pg.draw.rect(screen, red, big_button, 3)
        draw_text('YOU WIN !!!', (window_w/2, window_h/2), 50, red)
        draw_text(f'TIME::{start_timer - timer:.2f}', (window_w/2, window_h/2 + 50), 38, red)
    elif timer <= 0:  # LOSE screen
        pg.draw.rect(screen, black, big_button)
        pg.draw.rect(screen, red, big_button, 3)
        draw_text('YOU LOSE...', (window_w/2, window_h/2), 50, brown)
        draw_text(f'SCORE::{score}', (window_w/2, window_h/2 + 50), 38, brown)
    elif is_start:  # START screen
        pg.draw.rect(screen, brown, big_button)
        pg.draw.rect(screen, red, big_button, 3)
        draw_text('PUSH IT HARD', (window_w/2, window_h/2), 38)
        draw_text(f'get {win_score} for {timer} sec', (window_w/2, window_h/2 + 50), 32)
        if big_button_pressed:
            is_start = False
    else:  # GAME screen
        timer -= 1 / frame_rate
        draw_timer(timer)
        draw_score(score)
        screen.blit(clown, (int(clown_position[0] - clown_size/2), int(clown_position[1] - clown_size/2)))

    pg.display.update()  # redraw
