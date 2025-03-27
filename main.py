# MIT License
# Copyright (c) 2025 coolwishon
import pygame
import sys
import requests
from bs4 import BeautifulSoup
import pyperclip
import re
import time 
import menu

pygame.init()
pygame.mixer.init() 
pygame.mixer.music.load("blad.mp3") 

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jak szybko napiszesz tekst swojej ulubionej piosenki?") 

bialy = (255, 255, 255)
szary = (150, 150, 150)
czarny = (0, 0, 0)
ziel = (0, 255, 0)
czerw = (255, 0, 0)

font = pygame.font.Font(None, 36)

def bezpol(text):
    replacements = {'ą': 'a', 'ć': 'c', 'Ć': 'C', 'ę': 'e', 'ł': 'l', 'Ł': 'L', 'ń': 'n','ó': 'o', 'ś': 's', 'Ś': 'S', 'ź': 'z', 'Ź': 'Z', 'Ż': 'Z', 'ż': 'z'}

    return ''.join(replacements.get(char, char) for char in text)
def url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        link = soup.find('div', class_='inner-text')
        if link:
            return '\n'.join(line.strip() for line in link.get_text("\n").split('\n') if line.strip())
        else:
            print("Nie znaleziono tekstu")
            return None
    except Exception as e:
        print(f"Bład pobierania tekstu: {e}")
        return None
def bezsym(text):
    text = re.sub(r'\[.*?\]|\{.*?\}|\(.*?\)', '', text) 
    text = re.sub(r'[^a-zA-Z0-9ąćęłńóśźżĄĆĘŁŃÓŚŹŻ ]', '', text) 
    return text.lower().strip()
def end_screen(bledy_ile, game_time):
    screen.fill(czarny)
    formatted_time = f"{int(game_time // 60)}:{int(game_time % 60):02}:{int((game_time % 1) * 1000):03}"
    messages = [
        ("Wynik koncowy", bialy),
        (f"Suma błedów: {bledy_ile}", bialy),
        (f"Łaczny czas: {formatted_time}", bialy)
    ]
    y_offset = SCREEN_HEIGHT // 2 - 50
    for text, color in messages:
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - 200, y_offset))
        y_offset += 50
    pygame.display.flip()
    pygame.time.delay(5000) 
def start_game():
    global adres
    running = True
    lines = [bezsym(line) for line in adres.split('\n')]
    lines = [line for line in lines if line.strip()]  

    line_index = 0
    char_index = 0
    bledy_ile = 0
    start_time = None

    while running:
        screen.fill(czarny) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if event.key == pygame.K_ESCAPE:
                        screen.fill(czarny)  
                        message = "Dzięki za zagranie w grę!"
                        text_surface = font.render(message, True, pygame.Color('white'))
                        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                        screen.blit(text_surface, text_rect)
                        pygame.display.flip()
                        pygame.time.wait(2000) 
                        pygame.quit()
                        sys.exit()
                if event.key == pygame.K_BACKSPACE:
                    char_index = max(0, char_index - 1)
                elif event.unicode.isprintable():
                    typed_char = bezpol(event.unicode)
                    current_line = bezpol(lines[line_index])
                    while char_index < len(current_line) and current_line[char_index] == ' ': 
                          char_index += 1  
                    if char_index < len(current_line) and typed_char == current_line[char_index]:
                        if start_time is None:
                            start_time = time.time()
                        char_index += 1
                        if char_index == len(current_line):
                            line_index += 1
                            char_index = 0
                            if line_index >= len(lines):
                                running = False
                    else:
                        if typed_char != ' ':  
                          bledy_ile += 1  
                          pygame.mixer.music.play()  
                          pygame.mixer.music.set_volume(0.01)
        timer = time.time() - start_time if start_time else 0
        formatted_time = f"{int(timer // 60)}:{int(timer % 60):02}:{int((timer % 1) * 1000):03}"
        bledy = font.render(f"Błędy: {bledy_ile}", True, czerw)
        time_text = font.render(f"Czas: {formatted_time}", True, bialy)
        screen.blit(bledy, (SCREEN_WIDTH - 250, 20))
        screen.blit(time_text, (SCREEN_WIDTH - 250, 60))
        y_offset = SCREEN_HEIGHT // 2 - 60
        for i in range(max(0, line_index - 3), min(line_index + 4, len(lines))):
            color = bialy if i == line_index else szary
            if i == line_index:
                correct_text_surface = font.render(lines[i][:char_index], True, ziel)
                remaining_text_surface = font.render(lines[i][char_index:], True, bialy)
                screen.blit(correct_text_surface, (50, y_offset))
                screen.blit(remaining_text_surface, (50 + correct_text_surface.get_width(), y_offset))
                char_x = font.size(lines[i][:char_index])[0]
                pygame.draw.rect(screen, ziel, (50 + char_x, y_offset, 2, font.get_height()))
            else:
                text_surface = font.render(lines[i], True, color)
                screen.blit(text_surface, (50, y_offset))
            y_offset += 40
        pygame.display.flip()
    end_screen(bledy_ile, timer) 
    pygame.quit()
    sys.exit()
def start_screen():
    global adres
    input_box = pygame.Rect(SCREEN_WIDTH // 4 - 200, SCREEN_HEIGHT // 2 - 50, 1300, 40)
    color = pygame.Color('lightskyblue3')
    active = False
    text = ''
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screen.fill(czarny)  
                    message = "Dzięki za zagranie w grę!"
                    text_surface = font.render(message, True, pygame.Color('white'))
                    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                    screen.blit(text_surface, text_rect)
                    pygame.display.flip()
                    pygame.time.wait(2000) 
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    text = pyperclip.paste()
                elif event.key == pygame.K_RETURN:
                    adres = url(text)
                    if adres:
                        adres = adres.strip()
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        screen.fill(czarny)
        txt_surface = font.render(text, True, color)
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

menu.main_menu()
start_screen()
start_game()
