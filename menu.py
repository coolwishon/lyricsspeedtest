import pygame
import sys

def main_menu():
    pygame.init()
    
    SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Menu główne")
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 102, 204)
    BLUE2 = (0, 153, 255)  
    try:
        font = pygame.font.Font("arial.ttf", 80)  
        button_font = pygame.font.Font("arial.ttf", 50)
    except:
        font = pygame.font.SysFont("Arial", 80)  
        button_font = pygame.font.SysFont("Arial", 50)
    title_text = font.render("Jak szybko napiszesz tekst swojej ulubionej piosenki??", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 - 50))
    play_btn = pygame.Rect(SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 30, 320, 80)
    exit_btn = pygame.Rect(SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 140, 320, 80)
    running = True
    while running:
        screen.fill(BLACK)
        screen.blit(title_text, title_rect)
        mouse_x, mouse_y = pygame.mouse.get_pos()       
        play_color = BLUE2 if play_btn.collidepoint((mouse_x, mouse_y)) else BLUE
        exit_color = BLUE2 if exit_btn.collidepoint((mouse_x, mouse_y)) else BLUE
        pygame.draw.rect(screen, play_color, play_btn, border_radius=15)
        pygame.draw.rect(screen, exit_color, exit_btn, border_radius=15)
        play_text = button_font.render("Graj", True, WHITE)
        exit_text = button_font.render("Wyjście", True, WHITE)
        screen.blit(play_text, play_text.get_rect(center=play_btn.center))
        screen.blit(exit_text, exit_text.get_rect(center=exit_btn.center))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_ESCAPE:
                screen.fill((0, 0, 0))  
                text_surface = font.render("Zagraj ponownie", True, (255, 255, 255))
                screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 
                                           SCREEN_HEIGHT // 2 - text_surface.get_height() // 2))
                pygame.display.update() 
                pygame.time.delay(3000) 
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):
                    running = False 
                if exit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.flip()


if __name__ == "__main__":
    main_menu()
