import pygame

window_w = 800
window_h = 800
black_color = (0, 0, 0)
score_color = (165, 165, 0)
background_color = (200, 200, 255)
font_path = 'fonts/Ritalin.ttf'

pygame.init()
screen = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("MAP")
clock = pygame.time.Clock()


class MainScreen:
    def __init__(self):
        pass


class TextScreen:
    def __init__(self):
        pygame.draw.line(screen, black_color, (0, window_h/4*3), (window_w, window_h/4*3))


def display_text(string):
    pass


class ScreenOneCharacter:
    def __init__(self):
        pass


def draw_text(text, size, position=(150, 50), color=background_color, background=score_color):
    font = pygame.font.Font(font_path, size)
    text = font.render(text, True, color, background)
    text_rect = text.get_rect()
    text_rect.center = position


def choose_your_character():
    pass

# def update_score(score):


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
    if keys[pygame.K_LEFT]:
        x -= step
    if keys[pygame.K_RIGHT]:
        x += step
    if keys[pygame.K_DOWN]:
        y += step
    if keys[pygame.K_UP]:
        y -= step

    # text = font.render(f'ОЧКОВ: {score}', True, background_color, score_color)
    screen.fill(background_color)
    turtle = pygame.image.load('images/chika.png')
    # pygame.draw.circle(screen, gold_color, (start_x, start_y - step*2), 48, 2)  # gold circle
    screen.blit(turtle, (x, y))
    # screen.blit(text, textRect)  # draw text and help text
    # screen.blit(text_help, helpRect)
    draw_text(f'ОЧКОВ: {score}', 64)
    pygame.display.update()  # redraw

# if terminated:  # if window closed
pygame.quit()
quit()
