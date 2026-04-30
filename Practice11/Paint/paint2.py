import pygame

pygame.init()

screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

surface = pygame.Surface((640, 480))
surface.fill((255, 255, 255))

mode = 'blue'
tool = 'brush'
radius = 5

drawing = False
start_pos = None
last_pos = None

def get_color(mode):
    if mode == 'blue':
        return (0, 0, 255)
    elif mode == 'red':
        return (255, 0, 0)
    elif mode == 'green':
        return (0, 255, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

            # цвета
            if event.key == pygame.K_r:
                mode = 'red'
            elif event.key == pygame.K_g:
                mode = 'green'
            elif event.key == pygame.K_b:
                mode = 'blue'

            # инструменты
            elif event.key == pygame.K_1:
                tool = 'brush'
            elif event.key == pygame.K_2:
                tool = 'rect'
            elif event.key == pygame.K_3:
                tool = 'circle'
            elif event.key == pygame.K_4:
                tool = 'eraser'
            elif event.key == pygame.K_5:
                tool = 'square'
            elif event.key == pygame.K_6:
                tool = 'triangle_right'
            elif event.key == pygame.K_7:
                tool = 'triangle_eq'
            elif event.key == pygame.K_8:
                tool = 'rhombus'

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
            last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if tool == 'rect':
                pygame.draw.rect(
                    surface,
                    get_color(mode),
                    pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1])),
                    2
                )

            elif tool == 'circle':
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                r = min(100, int((dx**2 + dy**2) ** 0.5))
                pygame.draw.circle(surface, get_color(mode), start_pos, r, 2)

            elif tool == 'square':  # square drawing based on mouse drag
                size = min(abs(end_pos[0]-start_pos[0]), abs(end_pos[1]-start_pos[1]))
                pygame.draw.rect(
                    surface,
                    get_color(mode),
                    pygame.Rect(start_pos[0], start_pos[1], size, size),
                    2
                )

            elif tool == 'triangle_right':  # right triangle using 3 points
                points = [
                    start_pos,
                    (end_pos[0], start_pos[1]),
                    end_pos
                ]
                pygame.draw.polygon(surface, get_color(mode), points, 2)

            elif tool == 'triangle_eq': # equilateral triangle using math formula
                x1, y1 = start_pos
                x2, y2 = end_pos

                base = abs(x2 - x1)
                height = int((3**0.5 / 2) * base)

                points = [
                    (x1, y1),
                    (x1 + base, y1),
                    (x1 + base//2, y1 - height)
                ]
                pygame.draw.polygon(surface, get_color(mode), points, 2)

            elif tool == 'rhombus': # rhombus using center and diagonals
                x1, y1 = start_pos
                x2, y2 = end_pos

                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                points = [
                    (cx, y1),
                    (x2, cy),
                    (cx, y2),
                    (x1, cy)
                ]
                pygame.draw.polygon(surface, get_color(mode), points, 2)

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if tool == 'brush':
                    pygame.draw.line(surface, get_color(mode), last_pos, event.pos, radius)
                    last_pos = event.pos

                elif tool == 'eraser':
                    pygame.draw.circle(surface, (255,255,255), event.pos, 10)

    screen.blit(surface, (0,0))
    pygame.display.flip()
    clock.tick(60)