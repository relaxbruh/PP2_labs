import pygame
from pygame.locals import *

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MENU_HEIGHT = 70
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("paint task")

FPS = pygame.time.Clock()

active_brush = 0
active_color = 'white'
painting = []
active_shape = None
drawing_shape = False
shape_start_pos = (0, 0)

# Draw menu and return interactive buttons
def draw_menu():
    pygame.draw.rect(screen, 'gray', (0, 0, SCREEN_WIDTH, MENU_HEIGHT))
    pygame.draw.line(screen, 'black', (0, MENU_HEIGHT), (SCREEN_WIDTH, MENU_HEIGHT), 3)

    # Brush sizes
    XL_brush = pygame.draw.rect(screen, 'black', (10, 10, 50, 50))
    pygame.draw.circle(screen, 'white', (35, 35), 20)
    L_brush = pygame.draw.rect(screen, 'black', (70, 10, 50, 50))
    pygame.draw.circle(screen, 'white', (95, 35), 15)
    M_brush = pygame.draw.rect(screen, 'black', (130, 10, 50, 50))
    pygame.draw.circle(screen, 'white', (155, 35), 10)
    S_brush = pygame.draw.rect(screen, 'black', (190, 10, 50, 50))
    pygame.draw.circle(screen, 'white', (215, 35), 5)
    brush_list = [XL_brush, L_brush, M_brush, S_brush]

    # Shapes
    circle = pygame.draw.circle(screen, 'black', (SCREEN_WIDTH - 187.5, 22.5), 12,5)
    pygame.draw.circle(screen, 'gray', (SCREEN_WIDTH - 187.5, 22.5), 10)
    rectangle = pygame.draw.rect(screen, 'gray', (SCREEN_WIDTH - 200, 40, 30, 25))
    pygame.draw.rect(screen, 'black', (SCREEN_WIDTH - 200, 40, 30, 25), 2)

    square = pygame.draw.rect(screen, 'gray', (SCREEN_WIDTH - 240, 40, 25, 25))
    pygame.draw.rect(screen, 'black', (SCREEN_WIDTH - 240, 40, 25, 25), 2)
    rhombus = pygame.draw.polygon(screen, 'gray', [(SCREEN_WIDTH - 240, 22.5), (SCREEN_WIDTH - 227.5, 35), (SCREEN_WIDTH - 215, 22.5), (SCREEN_WIDTH - 227.5, 10)])
    pygame.draw.polygon(screen, 'black', [(SCREEN_WIDTH - 240, 22.5), (SCREEN_WIDTH - 227.5, 35), (SCREEN_WIDTH - 215, 22.5), (SCREEN_WIDTH - 227.5, 10)], 2)

    right_triangle = pygame.draw.polygon(screen, 'gray', [(SCREEN_WIDTH - 280, 10), (SCREEN_WIDTH - 255, 35), (SCREEN_WIDTH - 280, 35)])
    pygame.draw.polygon(screen, 'black', [(SCREEN_WIDTH - 280, 10), (SCREEN_WIDTH - 255, 35), (SCREEN_WIDTH - 280, 35)], 2)
    equilateral_triangle = pygame.draw.polygon(screen, 'gray', [(SCREEN_WIDTH - 265, 40), (SCREEN_WIDTH - 250, 65), (SCREEN_WIDTH - 280, 65)])
    pygame.draw.polygon(screen, 'black', [(SCREEN_WIDTH - 265, 40), (SCREEN_WIDTH - 250, 65), (SCREEN_WIDTH - 280, 65)], 2)
    
    shape_list = [circle, rectangle, square, right_triangle, equilateral_triangle, rhombus]

    # Colors
    blue = pygame.draw.rect(screen, 'blue', (SCREEN_WIDTH - 35, 10, 25, 25))
    red = pygame.draw.rect(screen, 'red', (SCREEN_WIDTH - 65, 10, 25, 25))
    green = pygame.draw.rect(screen, 'green', (SCREEN_WIDTH - 95, 10, 25, 25))
    yellow = pygame.draw.rect(screen, 'yellow', (SCREEN_WIDTH - 125, 10, 25, 25))
    teal = pygame.draw.rect(screen, 'teal', (SCREEN_WIDTH - 35, 40, 25, 25))
    purple = pygame.draw.rect(screen, 'purple', (SCREEN_WIDTH - 65, 40, 25, 25))
    black = pygame.draw.rect(screen, 'black', (SCREEN_WIDTH - 95, 40, 25, 25))
    white = pygame.draw.rect(screen, 'white', (SCREEN_WIDTH - 125, 40, 25, 25))
    color_list = [blue, red, green, yellow, teal, purple, black, white]
    rgb_list = ['blue', 'red', 'green', 'yellow', 'teal', 'purple', 'black', 'white']

    # Clear button
    clear_btn = pygame.draw.rect(screen, 'darkred', (270, 20, 80, 30))
    font = pygame.font.SysFont(None, 24)
    text = font.render("Clear", True, 'white')
    screen.blit(text, (290, 26))

    return brush_list, shape_list, color_list, rgb_list, clear_btn

def draw_painting(paints):
    for item in paints:
        if item[0] == 'circle':
            pygame.draw.circle(screen, item[1], item[2], item[3], 2)
        elif item[0] == 'rect':
            pygame.draw.rect(screen, item[1], pygame.Rect(item[2], item[3]), 2)

        elif item[0] == 'square':
            pygame.draw.rect(screen, item[1], pygame.Rect(item[2], (item[3], item[3])), 2)
            
        elif item[0] in ('right_triangle', 'equilateral_triangle', 'rhombus'):
            pygame.draw.polygon(screen, item[1], item[2], 2)

        else:
            pygame.draw.circle(screen, item[0], item[1], item[2])

running = True
while running:
    screen.fill('white')
    mouse_pos = pygame.mouse.get_pos()
    LCM = pygame.mouse.get_pressed()[0]

    draw_painting(painting)

    # Drawing with the brush(if no shape is selected)
    if active_shape is None and mouse_pos[1] > MENU_HEIGHT:
        if LCM:
            painting.append((active_color, mouse_pos, active_brush))
        pygame.draw.circle(screen, active_color, mouse_pos, active_brush)

    # Drawing shapes
    elif drawing_shape and mouse_pos[1] > MENU_HEIGHT:

        x0, y0 = shape_start_pos
        x1, y1 = mouse_pos
        width = x1 - x0
        height = y1 - y0


        if active_shape == 'circle':
            radius = int(((mouse_pos[0] - shape_start_pos[0]) ** 2 + (mouse_pos[1] - shape_start_pos[1]) ** 2) ** 0.5)
            pygame.draw.circle(screen, active_color, shape_start_pos, radius, 2)
        elif active_shape == 'rectangle':
            width = mouse_pos[0] - shape_start_pos[0]
            height = mouse_pos[1] - shape_start_pos[1]
            pygame.draw.rect(screen, active_color, pygame.Rect(shape_start_pos, (width, height)), 2)
        elif active_shape == 'square':
            side = min(abs(width), abs(height))
            pygame.draw.rect(screen, active_color, pygame.Rect(shape_start_pos, (side, side)), 2)

        elif active_shape == 'right_triangle':
            points = [shape_start_pos, (x1, y1), (x0, y1)]
            pygame.draw.polygon(screen, active_color, points, 2)

        elif active_shape == 'equilateral_triangle':
            side = min(abs(width), abs(height))
            x_top = x0 + side // 2
            y_top = y0
            points = [
                (x_top, y_top),
                (x_top - side // 2, y_top + int(side * (3 ** 0.5) / 2)),
                (x_top + side // 2, y_top + int(side * (3 ** 0.5) / 2))
            ]
            pygame.draw.polygon(screen, active_color, points, 2)

        elif active_shape == 'rhombus':
            center_x = (x0 + x1) // 2
            center_y = (y0 + y1) // 2
            dx = abs(x1 - x0) // 2
            dy = abs(y1 - y0) // 2
            points = [
                (center_x, y0),
                (x1, center_y),
                (center_x, y1),
                (x0, center_y)
            ]
            pygame.draw.polygon(screen, active_color, points, 2)


    brushes, shapes, colors, rgbs, clear_button = draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # brush's buttons
            for i in range(len(brushes)):
                if brushes[i].collidepoint(event.pos):
                    active_brush = 20 - i * 5
                    active_shape = None

            # colors
            for i in range(len(colors)):
                if colors[i].collidepoint(event.pos):
                    active_color = rgbs[i]

            # shapes
            shape_names = ['circle', 'rectangle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']
            for i in range(len(shapes)):
                if shapes[i].collidepoint(event.pos):
                    active_shape = shape_names[i]


            # clear button
            if clear_button.collidepoint(event.pos):
                painting.clear()

            # start drawing shape
            if active_shape and event.pos[1] > MENU_HEIGHT:
                drawing_shape = True
                shape_start_pos = event.pos

        # stop drawing shape
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing_shape and mouse_pos[1] > MENU_HEIGHT:
                shape_end_pos = event.pos
                if active_shape == 'circle':
                    radius = int(((shape_end_pos[0] - shape_start_pos[0]) ** 2 + (shape_end_pos[1] - shape_start_pos[1]) ** 2) ** 0.5)
                    painting.append(('circle', active_color, shape_start_pos, radius))
                
                elif active_shape == 'rectangle':
                    width = shape_end_pos[0] - shape_start_pos[0]
                    height = shape_end_pos[1] - shape_start_pos[1]
                    painting.append(('rect', active_color, shape_start_pos, (width, height)))
                
                elif active_shape == 'square':
                    side = min(abs(shape_end_pos[0] - shape_start_pos[0]), abs(shape_end_pos[1] - shape_start_pos[1]))
                    painting.append(('square', active_color, shape_start_pos, side))

                elif active_shape == 'right_triangle':
                    x0, y0 = shape_start_pos
                    x1, y1 = shape_end_pos
                    points = [shape_start_pos, (x1, y1), (x0, y1)]
                    painting.append(('right_triangle', active_color, points))

                elif active_shape == 'equilateral_triangle':
                    x0, y0 = shape_start_pos
                    x1, y1 = shape_end_pos
                    side = min(abs(x1 - x0), abs(y1 - y0))
                    x_top = x0 + side // 2
                    y_top = y0
                    points = [
                        (x_top, y_top),
                        (x_top - side // 2, y_top + int(side * (3 ** 0.5) / 2)),
                        (x_top + side // 2, y_top + int(side * (3 ** 0.5) / 2))
                    ]
                    painting.append(('equilateral_triangle', active_color, points))

                elif active_shape == 'rhombus':
                    x0, y0 = shape_start_pos
                    x1, y1 = shape_end_pos
                    center_x = (x0 + x1) // 2
                    center_y = (y0 + y1) // 2
                    dx = abs(x1 - x0) // 2
                    dy = abs(y1 - y0) // 2
                    points = [
                        (center_x, y0),
                        (x1, center_y),
                        (center_x, y1),
                        (x0, center_y)
                    ]
                    painting.append(('rhombus', active_color, points))
                drawing_shape = False

    pygame.display.update()
    FPS.tick(1000000)

pygame.quit()