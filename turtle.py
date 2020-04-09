import pygame

score_color = (0, 200, 0)
background_color = (255, 255, 255)
screen_size = (1600, 800)
font_path = 'fonts/Titillium-Bold.otf'

pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("TURTLE")


# def update_score(score):


terminated = False
x = 1200
y = 600
score = 0
step = 10
font = pygame.font.Font(font_path, 64)
text = font.render(f'SCORE: {score}', True, background_color, score_color)
textRect = text.get_rect()
textRect.center = (100, 50)  # text position
while not terminated:  # main cycle
    pygame.time.delay(50)
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

    text = font.render(f'SCORE: {score}', True, background_color, score_color)
    screen.fill(background_color)
    turtle = pygame.image.load('images/turtle.png')
    # pygame.draw.circle(screen, gold_color, (start_x, start_y - step*2), 48, 2)  # gold circle
    screen.blit(turtle, (x, y))
    # screen.blit(text, textRect)  # draw text and help text
    # screen.blit(text_help, helpRect)
    pygame.display.update()  # redraw

# if terminated:  # if window closed
pygame.quit()
quit()
