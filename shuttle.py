import pygame as pg
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
health_max = 100
ornament_chance = 60
med_chance_start = 50
rock_chance_start = 0
window_position = '1275, 125'
black = pg.Color('black')  # (0, 0, 0, 255)
white = pg.Color('white')
red = pg.Color('red')
silk = pg.Color('cornsilk3')
brown = pg.Color('sandybrown')
green = pg.Color('green')
dark_red = pg.Color('darkred')
border_color = black
hit_color = dark_red
med_color = green

font_path = 'fonts/Ritalin.ttf'
environ['SDL_VIDEO_WINDOW_POS'] = window_position

pg.init()
screen = pg.display.set_mode((window_w, window_h))
pg.display.set_caption('MOON SHUTTLE')
pg.mixer_music.load('midi/nemesis.mid')
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
    draw_text('HEALTH', (50, 20), 32, red)
    draw_text(f'{health}', (50, 52), 32, red)
    draw_text('SCORE', (window_w - 50, 20), 32, red)
    draw_text(f'{score}', (window_w - 50, 52), 32, red)
    if health > 0:
        draw_text('HIGH SCORE', (window_w - 50, 84), 16, dark_red)
        draw_text(f'{max(score, high_score)}', (window_w - 50, 100), 16, dark_red)
    else:
        draw_text('HIGH SCORE', (window_w/2, 200), 64, red)
        draw_text(f'{high_score}', (window_w/2, 260), 64, red)
        draw_text('Press R to start over', (window_w/2, window_h - grid))


def draw_start_screen():
    draw_text('Press  <left or right arrow>  to move', (window_w/2, window_h/2), 32, dark_red)
    draw_text('Press  <up or down arrow>  to start', (window_w/2, window_h/2 + 50), 32, dark_red)
    draw_text('Press M to switch music', (window_w/2, window_h - 50), 24, dark_red)


def draw_background():
    # screen.blit(background_image, (0, 0))
    if start_screen:
        screen.fill(silk)
    elif health > 0:
        screen.fill(brown)
    else:
        screen.fill(dark_red)


def read_high_score():
    save_file = None
    try:
        save_file = open('shuttle.sav', 'r')
        read_score = int(save_file.read())
    except IOError:
        save_file = open('shuttle.sav', 'x')
        read_score = 0
        save_file.write(str(read_score))
    finally:
        if save_file:
            save_file.close()
    return read_score


def update_high_score(new_score):
    global high_score_updated
    save_file = open('shuttle.sav', 'w')
    save_file.write(str(new_score))
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


class Road:
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

        left_rect = ((0, 0), (grid * self.l_size, grid))
        right_rect = ((window_w - grid * self.r_size, 0), (grid * self.r_size, grid))
        if self.window * self.window * ornament_chance/100 >= randrange(100):  # ornament chance grows with \
            random = randrange(self.window) * grid                             # ornament_chance and window^2
            ornament_pos = (((int(left_rect[1][0] + random + grid*1/8), int(left_rect[0][1] + grid*7/8)),
                             (int(left_rect[1][0] + random + grid*7/8), int(left_rect[0][1] + grid*7/8))),
                            ((int(left_rect[1][0] + random + grid*1/3), int(left_rect[0][1] + grid*6/8)),
                             (int(left_rect[1][0] + random + grid*2/3), int(left_rect[0][1] + grid*6/8))))
        else:
            ornament_pos = None
        if self.window > 5 and rock_chance > randrange(100):
            random = randrange(self.window) * grid
            rock_pos = ((int(left_rect[1][0] + random + grid*0/8), int(left_rect[0][1] + grid*8/8)),
                        (int(left_rect[1][0] + random + grid*2/8), int(left_rect[0][1] + grid*4/8)),
                        (int(left_rect[1][0] + random + grid*4/8), int(left_rect[0][1] + grid*5/8)),
                        (int(left_rect[1][0] + random + grid*6/8), int(left_rect[0][1] + grid*2/8)),
                        (int(left_rect[1][0] + random + grid*8/8), int(left_rect[0][1] + grid*8/8)))
        else:
            rock_pos = None
        if med_chance > randrange(1000):
            random = randrange(self.window) * grid
            med_pos = (((left_rect[1][0] + random, int(left_rect[0][1] + grid/3)),
                        (grid, int(grid/3))),
                       ((int(left_rect[1][0] + random + grid/3), left_rect[0][1]),
                        (int(grid/3), grid)))
        else:
            med_pos = None
        if not fill:
            self.map.pop(0)
        self.map.append((left_rect, right_rect, ornament_pos, rock_pos, med_pos))

    def draw(self, is_hit, is_heal):
        block_color = border_color
        if is_hit:
            block_color = hit_color
        if is_heal:
            block_color = med_color
        for n in range(grid_ver + 2):
            left_rect = ((0, window_h - n * grid + step),
                         (self.map[n][0][1][0], self.map[n][0][1][1]))
            right_rect = ((self.map[n][1][0][0], window_h - n * grid + step),
                          (self.map[n][1][1][0], self.map[n][1][1][1]))
            pg.draw.rect(screen, block_color, left_rect)
            pg.draw.rect(screen, block_color, right_rect)
            ornament_pos = self.map[n][2]
            rock_pos = self.map[n][3]
            med_pos = self.map[n][4]
            if ornament_pos:
                pg.draw.line(screen, block_color, (ornament_pos[0][0][0], ornament_pos[0][0][1] + left_rect[0][1]),
                                                  (ornament_pos[0][1][0], ornament_pos[0][1][1] + left_rect[0][1]))
                pg.draw.line(screen, block_color, (ornament_pos[1][0][0], ornament_pos[1][0][1] + left_rect[0][1]),
                                                  (ornament_pos[1][1][0], ornament_pos[1][1][1] + left_rect[0][1]))
            if rock_pos:
                pg.draw.polygon(screen, block_color, ((rock_pos[0][0], rock_pos[0][1] + left_rect[0][1]),
                                                      (rock_pos[1][0], rock_pos[1][1] + left_rect[0][1]),
                                                      (rock_pos[2][0], rock_pos[2][1] + left_rect[0][1]),
                                                      (rock_pos[3][0], rock_pos[3][1] + left_rect[0][1]),
                                                      (rock_pos[4][0], rock_pos[4][1] + left_rect[0][1])))
            if med_pos:
                pg.draw.rect(screen, med_color, ((med_pos[0][0][0], med_pos[0][0][1] + left_rect[0][1]),
                                                 (med_pos[0][1][0], med_pos[0][1][1])))
                pg.draw.rect(screen, med_color, ((med_pos[1][0][0], med_pos[1][0][1] + left_rect[0][1]),
                                                 (med_pos[1][1][0], med_pos[1][1][1])))


step = 0
score = 0
level = 0
health = health_max
med_chance = med_chance_start
rock_chance = rock_chance_start
road = Road()
shuttle = Shuttle()
move_left = False
move_right = False
high_score = read_high_score()
high_score_updated = False
start_screen = True
music_enabled = False

while True:
    clock.tick(frame_rate)
    draw_background()

    pressed = pg.key.get_pressed()
    alt_held = pressed[pg.K_LALT] or pressed[pg.K_RALT]
    ctrl_held = pressed[pg.K_LCTRL] or pressed[pg.K_RCTRL]
    for event in pg.event.get():
        if event.type == pg.QUIT:  # close button
            exit()
        if event.type == pg.KEYDOWN:
            if (alt_held and event.key == pg.K_F4) or (ctrl_held and event.key == pg.K_w):
                exit()
            if ctrl_held and event.key == pg.K_DELETE:
                high_score = 0
                update_high_score(high_score)
                high_score_updated = False
            if event.key == pg.K_UP or event.key == pg.K_DOWN:
                start_screen = False
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
                level = 0
                health = health_max
                road = Road()
                shuttle = Shuttle()
                high_score_updated = False
                start_screen = True
            if event.key == pg.K_m:
                if music_enabled:
                    pg.mixer_music.stop()
                    music_enabled = False
                else:
                    pg.mixer_music.play(-1)
                    music_enabled = True

    if start_screen:
        draw_start_screen()
    elif health > 0:
        med_chance = med_chance_start - level
        rock_chance = rock_chance_start + level
        shuttle_top = road.map[6]
        shuttle_left = shuttle.x - shuttle.width/2
        shuttle_right = shuttle.x + shuttle.width/2
        left_border = shuttle_top[0][1][0]
        right_border = shuttle_top[1][0][0]
        rock = shuttle_top[3]
        med = shuttle_top[4]
        hit = 0
        heal = 0
        if rock:
            rock_left = rock[0][0]
            rock_right = rock[4][0]
            if shuttle_left < rock_right and shuttle_right > rock_left:
                hit = 5
        if med:
            med_left = med[0][0][0]
            med_right = med[0][0][0] + med[0][1][0]
            if shuttle_left < med_right and shuttle_right > med_left:
                heal = 10
        if shuttle_left < left_border or shuttle_right > right_border:
            hit = 5
        if shuttle_left < left_border - grid or shuttle_right > right_border + grid:
            hit = 20
        health -= hit
        health += heal
        if health > health_max:
            health = health_max
        if health < 0:
            health = 0
        if hit or heal:
            clock.tick(frame_rate/2)

        road.draw(hit, heal)
        shuttle.draw()
        draw_hud()

        score += speed_ver
        step = score % grid
        level = int((score - score % 1000) / 1000)

        if step == 0:
            road.step()
    else:
        if score > high_score and not high_score_updated:
            high_score = score
            update_high_score(high_score)
        draw_hud()

    pg.display.update()  # redraw
