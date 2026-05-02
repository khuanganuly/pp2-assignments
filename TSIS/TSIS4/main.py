import pygame, sys
import random
from db import create_tables, get_top10
from game import run_game

pygame.init()
screen = pygame.display.set_mode((600,600))
font = pygame.font.SysFont(None,40)

def input_name():
    name=""
    while True:
        screen.fill((0,0,0))
        txt = font.render("Enter name: "+name, True,(255,255,255))
        screen.blit(txt,(100,250))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type==pygame.QUIT: sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_RETURN:
                    return name
                elif e.key==pygame.K_BACKSPACE:
                    name=name[:-1]
                else:
                    name+=e.unicode

def show_leaderboard():
    data = get_top10()
    while True:
        screen.fill((0,0,0))
        y=100
        for row in data:
            txt = font.render(f"{row[0]} {row[1]}", True,(255,255,255))
            screen.blit(txt,(100,y))
            y+=40

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type==pygame.QUIT: return
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE:
                    return

def menu():
    create_tables()

    while True:
        screen.fill((0,0,0))

        play = font.render("1.Play", True,(255,255,255))
        lb = font.render("2.Leaderboard", True,(255,255,255))
        setb = font.render("3.Settings", True,(255,255,255))
        quitb = font.render("4.Quit", True,(255,255,255))

        
    

        screen.blit(play,(200,200))
        screen.blit(lb,(200,260))
        screen.blit(setb,(200,320))
        screen.blit(quitb,(200,380))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type==pygame.QUIT: sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_1:
                    user = input_name()
                    while True:
                        result = run_game(user)

                        if result == "retry":
                            continue
                        else:
                            break
                            
                if e.key==pygame.K_2:
                    show_leaderboard()
                if e.key==pygame.K_3:
                    settings_menu()
                if e.key==pygame.K_4:
                    sys.exit()

def save_settings(settings):
    import json
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)


def settings_menu():
    import json

    with open("settings.json") as f:
        settings = json.load(f)


    colors = [
        [0, 255, 0],     # зеленый
        [255, 105, 180], # розовый
        [0, 0, 255]      # синий
    ]

    color_names = ["Green", "Pink", "Blue"]

    current_color_index = 0

    for i, c in enumerate(colors):
        if settings["color"] == c:
            current_color_index = i

    

    

    

    selected = 0  # 0=color, 1=grid, 2=sound

    while True:
        screen.fill((0,0,0))

        text1 = font.render(f"Color: {color_names[current_color_index]}", True, (255,255,255))
        text2 = font.render(f"Grid: {settings['grid']}", True, (255,255,255))
        text3 = font.render(f"Sound: {settings['sound']}", True, (255,255,255))
        text4 = font.render("ENTER - change | ESC - save & back", True, (200,200,200))

        screen.blit(text1, (100,200))
        screen.blit(text2, (100,250))
        screen.blit(text3, (100,300))
        screen.blit(text4, (50,400))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    save_settings(settings)
                    return

                if e.key == pygame.K_DOWN:
                    selected = (selected + 1) % 3

                if e.key == pygame.K_UP:
                    selected = (selected - 1) % 3

                if e.key == pygame.K_RETURN:
                    if selected == 0:
                        current_color_index = (current_color_index + 1) % 3
                        settings["color"] = colors[current_color_index]

                    elif selected == 1:
                        settings["grid"] = not settings["grid"]

                    elif selected == 2:
                        settings["sound"] = not settings["sound"]

menu()