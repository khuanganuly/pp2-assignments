import pygame
import datetime

pygame.init()

screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

surface = pygame.Surface((640, 480))
surface.fill((255, 255, 255))

mode = 'black'
tool = 'brush'
radius = 5

drawing = False
start_pos = None
last_pos = None
preview_surface = surface.copy()

text_mode = False
text_input = ""
text_pos = (0, 0)
font = pygame.font.SysFont(None, 24)

def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))

    if target_color == new_color:
        return

    stack = [(x, y)]

    while stack:
        px, py = stack.pop()

        if px < 0 or px >= surface.get_width() or py < 0 or py >= surface.get_height():
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), new_color)

        stack.append((px + 1, py))
        stack.append((px - 1, py))
        stack.append((px, py + 1))
        stack.append((px, py - 1))

def get_color(mode):
    if mode == 'black':
        return (0, 0, 0)
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
            

            # цвета
            if event.key == pygame.K_r:
                mode = 'red'
            elif event.key == pygame.K_g:
                mode = 'green'
            elif event.key == pygame.K_b:
                mode = 'black'

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
            elif event.key == pygame.K_9:
                tool = 'line'
            elif event.key == pygame.K_0:
                tool = 'fill'
            elif event.key == pygame.K_t:
                tool = 'text'


            # размер кисти
            elif event.key == pygame.K_z:
                radius = 2
            elif event.key == pygame.K_x:
                radius = 5
            elif event.key == pygame.K_c:
                radius = 10

            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"paint_{now}.png"
                pygame.image.save(surface, filename)
                print("Saved:", filename)



            if text_mode:
                if event.key == pygame.K_RETURN:
                    # сохранить текст
                    text_surface = font.render(text_input, True, get_color(mode))
                    surface.blit(text_surface, text_pos)
                    text_mode = False

                    continue

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                else:
                    text_input += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
            last_pos = event.pos

            if tool == 'line':
                preview_surface = surface.copy()
            if tool == 'fill':
                flood_fill(surface, event.pos[0], event.pos[1], get_color(mode))
            if tool == 'text':
                text_mode = True
                text_input = ""
                text_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if tool == 'rect':
                pygame.draw.rect(
                    surface,
                    get_color(mode),
                    pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1])),
                    radius
                )

            elif tool == 'circle':
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                r = min(100, int((dx**2 + dy**2) ** 0.5))
                pygame.draw.circle(surface, get_color(mode), start_pos, r, radius)

            elif tool == 'square':  # square drawing based on mouse drag
                size = min(abs(end_pos[0]-start_pos[0]), abs(end_pos[1]-start_pos[1]))
                pygame.draw.rect(
                    surface,
                    get_color(mode),
                    pygame.Rect(start_pos[0], start_pos[1], size, size),
                    radius
                )

            elif tool == 'triangle_right':  # right triangle using 3 points
                points = [
                    start_pos,
                    (end_pos[0], start_pos[1]),
                    end_pos
                ]
                pygame.draw.polygon(surface, get_color(mode), points, radius)

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
                pygame.draw.polygon(surface, get_color(mode), points, radius)

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
                pygame.draw.polygon(surface, get_color(mode), points, radius)

            elif tool == 'line':
                pygame.draw.line(surface, get_color(mode), start_pos, end_pos, radius)

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if tool == 'brush':
                    pygame.draw.line(surface, get_color(mode), last_pos, event.pos, radius)
                    last_pos = event.pos

                elif tool == 'eraser':
                    pygame.draw.circle(surface, (255,255,255), event.pos, 10)

                elif tool == 'line':
                    preview_surface = surface.copy()
                    pygame.draw.line(preview_surface, get_color(mode), start_pos, event.pos, radius)
    
    if text_mode:
        temp_surface = surface.copy()
        text_surface = font.render(text_input, True, get_color(mode))
        temp_surface.blit(text_surface, text_pos)
        screen.blit(temp_surface, (0,0))
    else:
        if tool == 'line' and drawing:
            screen.blit(preview_surface, (0,0))
        else:
            screen.blit(surface, (0,0))

    pygame.display.flip()
    clock.tick(60)