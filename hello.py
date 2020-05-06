import pygame

countdown = 50  # adjustable

font_path = 'fonts/Titillium-Bold.otf'
pig_color = (255, 80, 80)
background_color = (50, 50, 50)
black_color = (0, 0, 0)
gold_color = (255, 215, 0)
start_x = 250  # pig center position
start_y = 400
step = 150  # pig step
pi = 3.141592653


def set_font_size(size):
    return pygame.font.Font(font_path, size)


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


pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("hello... pyg... ame... :=)")
clock = pygame.time.Clock()

font = set_font_size(30)
text = font.render('Countdown: ', True, background_color, black_color)
textRect = text.get_rect()
textRect.center = (100, 50)  # text position
font_help = set_font_size(18)
text_help = font_help.render('Play with arrows', True, black_color)
helpRect = text_help.get_rect()
helpRect.center = (80, 480)


terminated = False
trigger = 0
x = start_x
y = start_y
while not terminated and trigger < 4 and countdown > 0:  # main cycle
    clock.tick(10)
    for event in pygame.event.get():
        def trigger_add(sign):
            global trigger
            global countdown
            if sign == '+':
                trigger += 1
            else:
                trigger -= 1
            countdown -= 1

        if event.type == pygame.QUIT:  # 'close' button event
            terminated = True
        elif event.type == pygame.KEYDOWN:  # key down events
            if event.key == pygame.K_LEFT:
                x -= step
                trigger_add("+")
            elif event.key == pygame.K_RIGHT:
                x += step
                trigger_add("+")
            elif event.key == pygame.K_DOWN:
                y -= step
                trigger_add("+")
            elif event.key == pygame.K_UP:
                y -= step
                trigger_add("+")
        elif event.type == pygame.KEYUP:  # key up events
            if event.key == pygame.K_LEFT:
                x += step
                trigger_add("-")
            elif event.key == pygame.K_RIGHT:
                x -= step
                trigger_add("-")
            elif event.key == pygame.K_DOWN:
                y += step
                trigger_add("-")
            elif event.key == pygame.K_UP:
                y += step
                trigger_add("-")
    text = font.render(f'Countdown: {countdown}', True, background_color, black_color)
    screen.fill(background_color)
    draw_pig(x, y)
    pygame.draw.circle(screen, gold_color, (start_x, start_y - step*2), 48, 2)  # gold circle
    screen.blit(text, textRect)  # draw text and help text
    screen.blit(text_help, helpRect)
    pygame.display.update()  # redraw

if terminated:  # if window closed
    pygame.quit()
    quit()

screen.fill(black_color)  # game over screen
font = set_font_size(64)
textRect.center = (220, 250)
if countdown > 0:
    text = font.render('You WIN!', True, pig_color, background_color)
    draw_pig(start_x, start_y - step*2)
    pygame.draw.circle(screen, gold_color, (start_x, start_y - step*2), 50, 4)
    pygame.display.set_caption("Congratulations!")
else:
    text = font.render('You LOSE!', True, background_color, black_color)
    draw_pig(start_x, start_y, reverse=True)
    pygame.display.set_caption("Try again")
screen.blit(text, textRect)
pygame.display.update()

while not terminated:  # wait for quit
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminated = True
