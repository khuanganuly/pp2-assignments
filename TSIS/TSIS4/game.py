import pygame, random, json
from db import save_score, get_best

WIDTH, HEIGHT = 600, 600
CELL = 20


def load_settings():
    with open("settings.json") as f:
        return json.load(f)

def run_game(username):
    pygame.init()

    settings = load_settings()

    if settings["sound"]:
        pygame.mixer.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)
    
    snake_color = tuple(settings["color"])

    snake = [(100,100),(80,100),(60,100)]
    direction = (20,0)

    def gen_food():
        while True:
            f = (random.randrange(0,WIDTH,CELL), random.randrange(0,HEIGHT,CELL))
            if f not in snake:
                return f

    food = gen_food()
    food_spawn_time = pygame.time.get_ticks()
    food_lifetime = 8000   # 5 секунд

    poison = gen_food()
    poison_spawn_time = pygame.time.get_ticks()
    poison_lifetime = 8000   # 5 секунд
    
    power = None
    power_time = 0
    obstacles = []

    score = 0
    level = 1
    speed = 10
    best = get_best(username)

    shield = False
    effect_end_time = 0
    effect_type = None

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "menu"

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and direction!=(0,20): direction=(0,-20)
                if e.key == pygame.K_DOWN and direction!=(0,-20): direction=(0,20)
                if e.key == pygame.K_LEFT and direction!=(20,0): direction=(-20,0)
                if e.key == pygame.K_RIGHT and direction!=(-20,0): direction=(20,0)

        head = (snake[0][0]+direction[0], snake[0][1]+direction[1])

        current_time = pygame.time.get_ticks()

        # исчезновение еды
        if current_time - food_spawn_time > food_lifetime:
            food = gen_food()
            food_spawn_time = current_time

        current_time = pygame.time.get_ticks()

        # исчезновение poison
        if current_time - poison_spawn_time > poison_lifetime:
            poison = gen_food()
            poison_spawn_time = current_time

        snake.insert(0, head)

        # collisions
        if head in snake[1:] or head in obstacles or head[0]<0 or head[1]<0 or head[0]>=WIDTH or head[1]>=HEIGHT:
            if shield:
                shield=False
            else:
                save_score(username, score, level)

                result = game_over_screen(screen, score, level, best)

                if result == "retry":
                    return "retry"
                else:
                    return "menu"

        # food
        if head == food:
            if settings["sound"]:
                pygame.mixer.Sound("eat.mp3").play()
            score+=1
            food = gen_food()
            food_spawn_time = pygame.time.get_ticks()

            if score % 3 == 0:
                level+=1
                speed+=2

                if level>=3:
                    for _ in range(5):
                        obstacles.append(gen_food())
        else:
            snake.pop()

        # poison
        if head == poison:
            if len(snake)>2:
                snake.pop()
                snake.pop()
            else:
                save_score(username, score, level)

                result = game_over_screen(screen, score, level, best)

                if result == "retry":
                    return "retry"
                else:
                    return "menu"
            poison = gen_food()
            poison_spawn_time = pygame.time.get_ticks()

        # power-up
        now = pygame.time.get_ticks()
        if not power:
            if random.random()<0.01:
                power = gen_food()
                power_time = now
                power_type = random.choice(["speed","slow","shield"])

        if power and now-power_time>8000:
            power=None

        if head == power:
            now = pygame.time.get_ticks()

            if power_type == "speed":
                speed += 5
                effect_type = "speed"
                effect_end_time = now + 5000

            elif power_type == "slow":
                speed = max(5, speed - 5)
                effect_type = "slow"
                effect_end_time = now + 5000

            elif power_type == "shield":
                shield = True

            power = None

        screen.fill((0,0,0))

        now = pygame.time.get_ticks()

        if effect_type and now > effect_end_time:
            speed = 10 + (level - 1) * 2
            effect_type = None

        for s in snake:
            pygame.draw.rect(screen, snake_color, (*s,CELL,CELL))

        pygame.draw.rect(screen, (255,0,0), (*food,CELL,CELL))
        pygame.draw.rect(screen, (150,0,0), (*poison,CELL,CELL))

        if power:
            if power_type == "speed":
                color = (0, 255, 255)   # голубой (ускорение)
            elif power_type == "slow":
                color = (255, 165, 0)   # оранжевый (замедление)
            elif power_type == "shield":
                color = (0, 0, 255)     # синий (щит)

            pygame.draw.rect(screen, color, (*power, CELL, CELL))

        for o in obstacles:
            pygame.draw.rect(screen, (100,100,100), (*o,CELL,CELL))

        text = font.render(f"Score:{score} Level:{level} Best:{best}", True, (255,255,255))
        screen.blit(text, (10,10))


        if settings["grid"]:
            for x in range(0, WIDTH, CELL):
                pygame.draw.line(screen, (40,40,40), (x,0), (x,HEIGHT))
            for y in range(0, HEIGHT, CELL):
                pygame.draw.line(screen, (40,40,40), (0,y), (WIDTH,y))


        pygame.display.flip()
        clock.tick(speed)






def game_over_screen(screen, score, level, best):
    font_big = pygame.font.SysFont(None, 60)
    font = pygame.font.SysFont(None, 40)

    while True:
        screen.fill((0,0,0))

        title = font_big.render("GAME OVER", True, (255,0,0))
        s_text = font.render(f"Score: {score}", True, (255,255,255))
        l_text = font.render(f"Level: {level}", True, (255,255,255))
        b_text = font.render(f"Best: {best}", True, (255,255,255))

        retry = font.render("R - Retry", True, (0,255,0))
        menu = font.render("M - Menu", True, (0,255,255))

        screen.blit(title, (150,150))
        screen.blit(s_text, (200,250))
        screen.blit(l_text, (200,300))
        screen.blit(b_text, (200,350))
        screen.blit(retry, (200,420))
        screen.blit(menu, (200,470))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "menu"

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return "retry"
                if e.key == pygame.K_m:
                    return "menu"   