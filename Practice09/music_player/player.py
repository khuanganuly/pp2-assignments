import pygame

playlist = [
    "musics/Mac_DeMarco - No_Other_Heart.mp3",
    "musics/Mac_Demarco - moonlight_on_the_river.mp3",
    "musics/The_Cure - Lovesong.mp3"
]

current_track = 0



def play_track():
    pygame.mixer.music.load(playlist[current_track])
    pygame.mixer.music.play()


def stop_track():
    pygame.mixer.music.stop()


def next_track():
    global current_track
    current_track = (current_track + 1) % len(playlist)
    play_track()


def previous_track():
    global current_track
    current_track = (current_track - 1) % len(playlist)
    play_track()


def get_track_name():
    return playlist[current_track].split("/")[-1]