import pygame as pg
from pygame import midi
from os import environ
from random import randrange

window_w = 600
window_h = 900
frame_rate = 60
grid = int(window_w / 20)
grid_hor = int(window_w / grid)
grid_ver = int(window_h / grid)
speed_hor = int(grid / 6)
speed_ver = int(grid / 3)
window_position = '1275, 125'
black = pg.Color('black')  # (0, 0, 0, 255)
white = pg.Color('white')
red = pg.Color('red')
silk = pg.Color('cornsilk3')
brown = pg.Color('sandybrown')
dark_red = pg.Color('darkred')

font_path = 'fonts/Ritalin.ttf'
environ['SDL_VIDEO_WINDOW_POS'] = window_position

pg.init()
midi.init()
screen = pg.display.set_mode((window_w, window_h))
pg.display.set_caption('MOON SHUTTLE')
pg.mixer_music.load('midi/nemesis.mid')
pg.mixer_music.play(-1)
clock = pg.time.Clock()

# background_image = pg.image.load('images/cat.jpg')
# background_image = pg.transform.scale(background_image, (window_w, window_h))


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


def draw_hud():
    draw_text('HEALTH', (50, 20), 32, red, True)
    draw_text(f'{health}', (50, 52), 32, red, True)
    draw_text('SCORE', (window_w - 50, 20), 32, red, True)
    draw_text(f'{score}', (window_w - 50, 52), 32, red, True)
    if health > 0:
        draw_text('HIGH SCORE', (window_w - 50, 84), 16, dark_red, True)
        draw_text(f'{high_score}', (window_w - 50, 100), 16, dark_red, True)
    else:
        if score == high_score:
            draw_text('HIGH SCORE', (window_w/2, 100), 64, red, True)
            draw_text(f'{high_score}', (window_w/2, 160), 64, red, True)
        else:
            draw_text('HIGH SCORE', (window_w / 2, 80), 32, red, True)
            draw_text(f'{high_score}', (window_w / 2, 112), 32, red, True)
        draw_text('Press R to start over', (window_w/2, window_h - grid), center=True)


def draw_start_screen():
    draw_text('Press  <left or right arrow>  to move', (window_w/2, window_h/2), 32, dark_red, None, center=True)
    draw_text('Press  <down arrow>  to start', (window_w/2, window_h/2 + 50), 32, dark_red, None, center=True)


def draw_background():
    # screen.blit(background_image, (0, 0))
    if not is_started:
        screen.fill(silk)
    elif health > 0:
        screen.fill(brown)
    elif score == high_score:
        screen.fill(dark_red)
    else:
        screen.fill(silk)


def read_high_score():
    save_file = open('shuttle.sav', 'r')
    read_score = int(save_file.read())
    save_file.close()
    return read_score


def update_high_score():
    global score, high_score, high_score_updated
    if not high_score_updated:
        if score > high_score:
            high_score = score
            save_file = open('shuttle.sav', 'w')
            save_file.write(str(high_score))
            save_file.close()
        high_score_updated = True


class Shuttle:
    def __init__(self):
        self.width = grid * 2
        self.height = grid * 4
        self.x = window_w / 2 - grid
        self.y = window_h - grid - self.height

    def draw(self):
        if (not move_left and not move_right) or (move_left and move_right):
            pg.draw.rect(screen, red, ((int(self.x - self.width/4), int(self.y + self.height/8)),
                                       (int(self.width/2), int(self.height*3/4))))
            pg.draw.rect(screen, dark_red, ((int(self.x - self.width / 2), self.y),
                                            (int(self.width/4), int(self.height/8))))
            pg.draw.rect(screen, dark_red, ((int(self.x + self.width / 4), self.y),
                                            (int(self.width/4), int(self.height/8))))
            pg.draw.rect(screen, dark_red, ((int(self.x - self.width / 2), int(self.y + self.height * 7 / 8)),
                                            (int(self.width/4), int(self.height/8))))
            pg.draw.rect(screen, dark_red, ((int(self.x + self.width / 4), int(self.y + self.height * 7 / 8)),
                                            (int(self.width/4), int(self.height/8))))
        elif move_right:
            if self.x < window_w - grid * 2:
                self.x += speed_hor
            pg.draw.polygon(screen, red,
                            ((int(self.x - self.width / 4), int(self.y + self.height / 8)),
                             (int(self.x + self.width / 4), int(self.y + self.height / 8)),
                             (int(self.x + self.width / 4 - speed_hor), int(self.y + self.height * 7 / 8)),
                             (int(self.x - self.width / 4 - speed_hor), int(self.y + self.height * 7 / 8))))
            pg.draw.rect(screen, dark_red, ((int(self.x - self.width / 2), self.y),
                                            (int(self.width/4), int(self.height/8))))
            pg.draw.rect(screen, dark_red, ((int(self.x + self.width / 4), self.y),
                                            (int(self.width/4), int(self.height/8))))
            pg.draw.rect(screen, dark_red, ((int(self.x - self.width / 2 - speed_hor),
                                             int(self.y + self.height*7/8)),
                                            (int(self.width/4), int(self.height/8))))
            pg.draw.rect(screen, dark_red, ((int(self.x + self.width / 4 - speed_hor),
                                             int(self.y + self.height*7/8)),
                                            (int(self.width/4), int(self.height/8))))
        elif move_left:
            if self.x > grid * 2:
                self.x -= speed_hor
            pg.draw.polygon(screen, red,
                            ((int(self.x - self.width / 4), int(self.y + self.height / 8)),
                             (int(self.x + self.width / 4), int(self.y + self.height / 8)),
                             (int(self.x + self.width / 4 + speed_hor), int(self.y + self.height * 7 / 8)),
                             (int(self.x - self.width / 4 + speed_hor), int(self.y + self.height * 7 / 8))))
            pg.draw.rect(screen, dark_red, ((int(self.x - self.width / 2), self.y),
                                            (int(self.width/4), int(self.height/8))))
            pg.draw.rect(screen, dark_red, ((int(self.x + self.width / 4), self.y),
                                            (int(self.width/4), int(self.height/8))))
            pg.draw.rect(screen, dark_red, ((int(self.x - self.width / 2 + speed_hor),
                                             int(self.y + self.height*7/8)),
                                            (int(self.width/4), int(self.height/8))))
            pg.draw.rect(screen, dark_red, ((int(self.x + self.width / 4 + speed_hor),
                                             int(self.y + self.height*7/8)),
                                            (int(self.width/4), int(self.height/8))))


class Borders:
    def __init__(self):
        self.map = []
        self.l_size = 1
        self.r_size = 1
        self.window = 1
        for n in range(grid_ver + 2):
            self.step(fill=True)

    def step(self, fill=False):
        self.l_size += randrange(-1, 2)
        self.r_size += randrange(-1, 2)
        self.window = grid_hor - self.l_size - self.r_size

        if self.window <= 3:
            self.l_size -= 1
            self.r_size -= 1
        elif self.window >= 12 and len(self.map) >= grid_ver:
            self.l_size += 1
            self.r_size += 1
        if self.l_size < 1:
            self.l_size = 1
        if self.r_size < 1:
            self.r_size = 1

        if not fill:
            self.map.pop(0)
        self.map.append((((0, 0),
                          (grid * self.l_size, grid)),
                         ((window_w - grid * self.r_size, (grid * self.r_size, grid)),
                          (window_w, grid))))

    def draw(self, is_hit):
        if is_hit:
            border_color = red
        else:
            border_color = black
        for n in range(grid_ver + 2):
            pg.draw.rect(screen, border_color, ((0,                    window_h - n * grid + step),
                                                (self.map[n][0][1][0], self.map[n][0][1][1])))
            pg.draw.rect(screen, border_color, ((self.map[n][1][0][0], window_h - n * grid + step),
                                                (self.map[n][1][1][0], self.map[n][1][1][1])))


step = 0
score = 0
health = 100
borders = Borders()
shuttle = Shuttle()
move_left = False
move_right = False
high_score = read_high_score()
high_score_updated = False
is_started = False

while True:
    clock.tick(frame_rate)
    draw_background()

    pressed = pg.key.get_pressed()
    alt_held = pressed[pg.K_LALT] or pressed[pg.K_RALT]
    ctrl_held = pressed[pg.K_LCTRL] or pressed[pg.K_RCTRL]
    for event in pg.event.get():
        if event.type == pg.QUIT:  # close button
            quit()
        if event.type == pg.KEYDOWN:
            if (event.key == pg.K_F4 and alt_held) or (event.key == pg.K_w and ctrl_held):  # alt+f4 or ctrl+w
                quit()
            if event.key == pg.K_DOWN:
                is_started = True
            if event.key == pg.K_LEFT:
                move_left = True
            elif event.key == pg.K_RIGHT:
                move_right = True
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                move_left = False
            elif event.key == pg.K_RIGHT:
                move_right = False
            if event.key == pg.K_r:
                step = 0
                score = 0
                health = 100
                borders = Borders()
                shuttle = Shuttle()
                high_score_updated = False
                is_started = False

    if not is_started:
        draw_start_screen()
    elif health > 0:
        hit = 0
        if shuttle.x - shuttle.width/2 < borders.map[6][0][1][0]:
            hit = 5
        if shuttle.x - shuttle.width/2 < borders.map[6][0][1][0] - grid:
            hit = 20
        if shuttle.x + shuttle.width/2 > borders.map[6][1][0][0]:
            hit = 5
        if shuttle.x + shuttle.width/2 > borders.map[6][1][0][0] + grid:
            hit = 20
        health -= hit
        if hit > 0:
            clock.tick(frame_rate/2)

        borders.draw(hit)
        shuttle.draw()
        draw_hud()

        score += speed_ver
        step = int(score % grid)

        if step == 0:
            borders.step()
    else:
        update_high_score()
        draw_hud()

    pg.display.update()  # redraw
