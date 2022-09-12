import pygame
import random

pygame.init()

# This is setting the screen size to 500 by 700, setting the game to running, and setting the clock.
screen = pygame.display.set_mode((500, 700))
clock = pygame.time.Clock()
game_font = "freesansbold.ttf"
title = pygame.font.SysFont(game_font, 100)


class Button:
    def __init__(self, x_pos, y_pos, width, height, text, background_color, text_color, font, font_size, hover_color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.text = text
        self.background_color = background_color
        self.text_color = text_color
        self.font = font
        self.font_size = font_size
        self.hover_color = hover_color

    def draw(self):
        pygame.draw.rect(screen, self.background_color, (self.x_pos, self.y_pos, self.width, self.height))
        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=(self.x_pos + self.width / 2, self.y_pos + self.height / 2))
        screen.blit(text, text_rect)

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.x_pos < mouse_pos[0] < self.x_pos + self.width and self.y_pos < mouse_pos[1] < self.y_pos + self.height:
            self.background_color = self.hover_color
            return True
        else:
            self.background_color = (0, 0, 0)
            return False

    def is_clicked(self):
        click = pygame.mouse.get_pressed()
        if click[0] == 1 and self.is_hovered():
            return True
        else:
            return False


def menu():
    pygame.display.set_caption("Project F")
    titleText = title.render("Project F", True, (0, 0, 200))
    titleRect = titleText.get_rect(center=(250, 100))
    play_button = Button(150, 225, 200, 100, "Play", (0, 0, 0), (255, 255, 255),
                         pygame.font.SysFont(game_font, 70), 70, (0, 0, 150))
    score_button = Button(150, 375, 200, 100, "Score", (0, 0, 0), (255, 255, 255),
                          pygame.font.SysFont(game_font, 70), 70, (0, 0, 150))
    quit_button = Button(150, 525, 200, 100, "Quit", (0, 0, 0), (255, 255, 255),
                         pygame.font.SysFont(game_font, 70), 70, (0, 0, 150))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill((25, 25, 35))
        screen.blit(titleText, titleRect)
        play_button.draw()
        play_button.is_hovered()
        # if play_button.is_clicked():
        # game()
        score_button.draw()
        score_button.is_hovered()
        # if score_button.is_clicked():
        # score()
        quit_button.draw()
        quit_button.is_hovered()
        if quit_button.is_clicked():
            pygame.quit()
            quit()
        pygame.display.update()
        clock.tick(60)


menu()
