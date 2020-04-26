import pygame as pg
from os import environ
from random import randrange

window_w = 600
window_h = 900
frame_rate = 60
grid = int(window_w / 20)
grid_h = int(window_h / grid)
speed_hor = int(grid / 3)
speed_ver = int(grid / 3)
window_position = '1275, 125'
black = pg.Color('black')  # (0, 0, 0, 255)
brown = pg.Color('brown')
white = pg.Color('white')
red = pg.Color('red')

font_path = 'fonts/Ritalin.ttf'
environ['SDL_VIDEO_WINDOW_POS'] = window_position

pg.init()
screen = pg.display.set_mode((window_w, window_h))
pg.display.set_caption('MOON SHUTTLE')
# pg.mixer_music.load('midi/fast.mid')
# pg.mixer_music.play()
clock = pg.time.Clock()

background_image = pg.image.load('images/cat.jpg')
background_image = pg.transform.scale(background_image, (window_w, window_h))


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


class Shuttle:
    def __init__(self):
        self.width = grid * 2
        self.height = grid * 4
        self.x = window_w / 2 - grid
        self.y = window_h - grid - self.height

    def draw(self):
        pg.draw.rect(screen, pg.Color('darkred'), ((int(self.x - self.width/2), self.y), (self.width, self.height)))

    def move(self, side):
        if side == 'left':
            if self.x > grid * 2:
                self.x -= speed_hor
        else:
            if self.x < window_w - grid * 2:
                self.x += speed_hor


class Border:
    def __init__(self, side):
        if side == 'left':
            self.left = True
        else:
            self.left = False
        self.map = []
        self.size = 1
        for n in range(grid_h + 2):
            self.step(fill=True)

    def step(self, fill=False):
        self.size += randrange(-1, 2)
        if self.size > 9:
            self.size = 9
        elif self.size < 1:
            self.size = 1
        if not fill:
            self.map.pop(0)
        self.map.append(((0, 0), (grid * self.size, grid)))

    def draw(self):
        if self.left:
            for n in range(grid_h + 2):
                pg.draw.rect(screen, black, ((0, window_h - n * grid + step),
                                             (self.map[n][1][0], self.map[n][1][1])))
        else:
            for n in range(grid_h + 2):
                pg.draw.rect(screen, black, ((window_w - self.map[n][1][0], window_h - n * grid + step),
                                             (self.map[n][1][0], self.map[n][1][1])))


score = 0
step = 0
shuttle = Shuttle()
move_left = False
move_right = False
left_border = Border('left')
right_border = Border('right')

while True:
    clock.tick(frame_rate)
    # screen.blit(background_image, (0, 0))
    screen.fill(pg.Color('cornsilk3'))

    pressed = pg.key.get_pressed()
    alt_held = pressed[pg.K_LALT] or pressed[pg.K_RALT]
    ctrl_held = pressed[pg.K_LCTRL] or pressed[pg.K_RCTRL]
    for event in pg.event.get():
        if event.type == pg.QUIT:  # close button
            quit()
        if event.type == pg.KEYDOWN:
            if (event.key == pg.K_F4 and alt_held) or (event.key == pg.K_w and ctrl_held):  # alt+f4 or ctrl+w
                quit()
            if event.key == pg.K_LEFT:
                move_left = True
            elif event.key == pg.K_RIGHT:
                move_right = True
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                move_left = False
            elif event.key == pg.K_RIGHT:
                move_right = False
        # if event.type == pg.MOUSEBUTTONDOWN:
        #     coordinates = pg.mouse.get_pos()
        #     if 0 <= coordinates[0] <= 1 and 0 <= coordinates[1] <= 1:
        #         pass

    # draw_text('CAT', (600, 300), 48, black)
    # pg.draw.rect(screen, white, ((grid, grid), (grid, grid)))
    left_border.draw()
    right_border.draw()

    if move_left:
        shuttle.move('left')
    elif move_right:
        shuttle.move('right')
    shuttle.draw()

    score += speed_ver
    step = int(score % grid)

    if step == 0:
        left_border.step()
        right_border.step()

    pg.display.update()  # redraw
