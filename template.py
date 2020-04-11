import pygame as pg
from os import environ
from random import randrange

window_w = 1225
window_h = 875
frame_rate = 20
window_position = '675, 125'
black = pg.Color('black')  # (0, 0, 0, 255)
brown = pg.Color('brown')
white = pg.Color('white')
red = pg.Color('red')

font_path = 'fonts/Ritalin.ttf'
environ['SDL_VIDEO_WINDOW_POS'] = window_position

pg.init()
screen = pg.display.set_mode((window_w, window_h))
pg.display.set_caption('PET THAT CAT')
clock = pg.time.Clock()

background_image = pg.image.load('images/cat.jpg')
background_image = pg.transform.scale(background_image, (window_w, window_h))


def draw_text(string: str, position: tuple, size=32, color=black, background=None, center=True):
    font = pg.font.Font(font_path, size)
    text = font.render(string, True, color, background)
    text_rect = text.get_rect()
    text_height = text_rect[3] - text_rect[1]
    text_weight = text_rect[2] - text_rect[0]
    if center:
        screen.blit(text, ((int(position[0] - text_weight/2), int(position[1] - text_height/2)), (0, 0)))
    else:
        screen.blit(text, ((int(position[0]), int(position[1])), (0, 0)))


while True:
    clock.tick(frame_rate)
    screen.blit(background_image, (0, 0))

    pressed = pg.key.get_pressed()
    alt_held = pressed[pg.K_LALT] or pressed[pg.K_RALT]
    ctrl_held = pressed[pg.K_LCTRL] or pressed[pg.K_RCTRL]
    for event in pg.event.get():
        if event.type == pg.QUIT:  # close button
            quit()
        if event.type == pg.KEYDOWN:
            if (event.key == pg.K_F4 and alt_held) or (event.key == pg.K_w and ctrl_held):  # alt+f4 or ctrl+w
                quit()
        if event.type == pg.MOUSEBUTTONDOWN:
            coordinates = pg.mouse.get_pos()
            if 0 <= coordinates[0] <= 1 and 0 <= coordinates[1] <= 1:
                pass

    pg.draw.rect(screen, white, ((100, 200), (300, 400)))
    draw_text('CAT', (600, 300), 48, black)

    pg.display.update()  # redraw
