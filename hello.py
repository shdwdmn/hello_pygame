import pygame

countdown = 50

window_size = (500, 500)
window_caption = "hello... pyg... ame... :=)"
start_x = 250
start_y = 400
step = 150
pig_color = (255, 80, 80)
background_color = (50, 50, 50)
black_color = (0, 0, 0)
gold_color = (255, 215, 0)
pi = 3.141592653

pygame.init()
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption(window_caption)

font = pygame.font.Font('impact.ttf', 32)
font_help = pygame.font.Font('impact.ttf', 18)
text = font.render('Countdown: ', True, background_color, black_color)
textRect = text.get_rect()
textRect.center = (100, 50)
text_help = font_help.render('Play with arrows', True, black_color)
helpRect = text_help.get_rect()
helpRect.center = (70, 480)


def draw_pig(_x, _y, color1=pig_color, color2=black_color, reverse=False):
    pygame.draw.polygon(screen, color1, [(_x, _y - 40), (_x - 60, _y - 50), (_x - 45, _y)])  # triangle ears
    pygame.draw.polygon(screen, color1, [(_x, _y - 40), (_x + 60, _y - 50), (_x + 45, _y)])
    pygame.draw.circle(screen, color1, (_x, _y), 52)  # circle face
    pygame.draw.circle(screen, color2, (_x, _y), 50)
    pygame.draw.circle(screen, color1, (_x, _y), 48)
    pygame.draw.ellipse(screen, color2, [(_x - 18, _y), (36, 24)])  # ellipse nose
    pygame.draw.circle(screen, color1, (_x - 7, _y + 10), 3)
    pygame.draw.circle(screen, color1, (_x + 7, _y + 10), 3)
    pygame.draw.circle(screen, color2, (_x - 20, _y - 15), 6)  # circle eyes
    pygame.draw.circle(screen, color2, (_x + 20, _y - 15), 6)
    if not reverse:
        pygame.draw.arc(screen, color2, [(_x - 25, _y + 10), (50, 35)], pi, pi * 2, 4)  # arc smile =)
    else:
        pygame.draw.arc(screen, color2, [(_x - 25, _y + 27), (50, 35)], 0, pi, 4)  # arc reverse =(


terminated = False
trigger = 0
x = start_x
y = start_y
while not terminated and trigger < 2 and countdown > 0:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminated = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= step
                trigger += 0.5
                countdown -= 1
            elif event.key == pygame.K_RIGHT:
                x += step
                trigger += 0.5
                countdown -= 1
            elif event.key == pygame.K_DOWN:
                y -= step
                trigger += 0.5
                countdown -= 1
            elif event.key == pygame.K_UP:
                y -= step
                trigger += 0.5
                countdown -= 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                x += step
                trigger -= 0.5
                countdown -= 1
            elif event.key == pygame.K_RIGHT:
                x -= step
                trigger -= 0.5
                countdown -= 1
            elif event.key == pygame.K_DOWN:
                y += step
                trigger -= 0.5
                countdown -= 1
            elif event.key == pygame.K_UP:
                y += step
                trigger -= 0.5
                countdown -= 1
    text = font.render(f'Countdown: {countdown}', True, background_color, black_color)
    screen.fill(background_color)
    draw_pig(x, y)
    pygame.draw.circle(screen, gold_color, (start_x, start_y - step*2), 48, 2)
    screen.blit(text, textRect)
    screen.blit(text_help, helpRect)
    pygame.display.update()

if terminated:
    pygame.quit()
    quit()

screen.fill(black_color)
font = pygame.font.Font('impact.ttf', 64)
textRect.center = (220, 250)
if countdown > 0:
    text = font.render('You WIN!', True, pig_color, background_color)
    draw_pig(start_x, start_y - step*2)
    pygame.draw.circle(screen, gold_color, (start_x, start_y - step*2), 50, 4)
else:
    text = font.render('You LOSE!', True, background_color, black_color)
    draw_pig(start_x, start_y, reverse=True)
screen.blit(text, textRect)
pygame.display.update()

while not terminated:
    pygame.time.delay(200)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminated = True
