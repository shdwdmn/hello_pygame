import os
import pygame

window_w = 800
window_h = 800
black_color = (0, 0, 0)
score_color = (165, 165, 0)
background_color = (200, 200, 255)
font_path = 'fonts/Ritalin.ttf'

os.environ['SDL_VIDEO_WINDOW_POS'] = "1120,180"
pygame.init()
screen = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("MAP")
clock = pygame.time.Clock()


def draw_text(text, size, position, color, background):
    font = pygame.font.Font(font_path, size)
    text = font.render(text, True, color, background)
    screen.blit(text, (position, (0, 0)))
    text_rect = text.get_rect()
    return text_rect


class Grid:
    def __init__(self):
        pass


class MainScreen:
    def __init__(self):
        screen.fill(background_color)
        pygame.draw.line(screen, black_color, (int(window_w/2), 0), (int(window_w/2), window_h))


class Message(object):
    def __init__(self):
        self.position = (20, 500)

    def display(self, string, size=32, color=black_color, background=None):
        draw_text(string, size, self.position, color, background)


class Score:
    def __init__(self):
        self.position = (30, 30)

    def update(self, count):
        draw_text(f'ОЧКОВ: {count}', 64, self.position, background_color, score_color)


class Player:
    def __init__(self):
        player = pygame.image.load('images/chika.png')
        screen.blit(player, (550, 500))


terminated = False
x = 550
y = 500
score = 0
step = 10
while not terminated:  # main cycle
    clock.tick(15)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 'close' button event
            terminated = True

    keys = pygame.key.get_pressed()
    # if keys[pygame.K_LEFT]:
    #     x -= step
    # if keys[pygame.K_RIGHT]:
    #     x += step
    # if keys[pygame.K_DOWN]:
    #     y += step
    # if keys[pygame.K_UP]:
    #     y -= step

    MainScreen.__init__(MainScreen())
    Score.update(Score(), 0)
    Player.__init__(Player())
    Message.display(Message(), 'GAME OVER', 99, background=background_color)

    pygame.display.update()  # redraw

# if terminated:  # if window closed
pygame.quit()
quit()
