import random

import pygame

pygame.init()
pygame.display.set_caption("Project F")
screen = pygame.display.set_mode((500, 700))
clock = pygame.time.Clock()


class Button:
    def __init__(self, x_pos, y_pos, width, height, text, background_color, text_color, font, font_size, hover_color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.text = text
        self.background_color = background_color
        self.saved_background_color = background_color
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
            self.background_color = self.saved_background_color
            return False

    def is_clicked(self):
        click = pygame.mouse.get_pressed()
        if click[0] == 1 and self.is_hovered():
            return True
        else:
            return False


def main_menu():
    title_font = pygame.font.SysFont(None, 100)
    game_font = pygame.font.SysFont(None, 70)
    play_button = Button(150, 225, 200, 100, "Play", (0, 0, 0), (255, 255, 255), game_font, 70, (0, 0, 150))
    score_button = Button(150, 375, 200, 100, "Score", (0, 0, 0), (255, 255, 255), game_font, 70, (0, 0, 150))
    quit_button = Button(150, 525, 200, 100, "Quit", (0, 0, 0), (255, 255, 255), game_font, 70, (0, 0, 150))
    while True:
        screen.fill((25, 25, 35))

        titleText = title_font.render("Project F", True, (0, 0, 200))
        titleRect = titleText.get_rect(center=(250, 100))
        screen.blit(titleText, titleRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        play_button.draw()
        play_button.is_hovered()
        if play_button.is_clicked():
            game()

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


def game():
    score = 0
    scoreText = pygame.font.Font('freesansbold.ttf', 32)

    redSquare = pygame.Surface((100, 100))
    redSquare.fill((255, 0, 0))
    redSquareX = 100
    redSquareY = 250
    redSquareYChange = 5

    obstacleWidth = 60
    obstacleHeight = random.randint(150, 450)
    obstacleColor = (0, 255, 0)
    obstacleXChange = -5
    obstacleX = 500

    running = True
    scoreFlag = False
    pauseFlag = False

    while running:
        clock.tick(60)
        screen.fill((0, 0, 0))

        screen.blit(redSquare, (redSquareX, redSquareY))
        displayObstacle(obstacleHeight, obstacleX, obstacleColor, obstacleWidth)
        displayScore(scoreText, score)

        for event in pygame.event.get():

            # This is checking if the user has closed the window. If they have, it will stop the game.
            if event.type == pygame.QUIT:
                running = False

            # This is checking if the space bar is pressed. If it is, the red square will move up.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not pauseFlag:
                        redSquareYChange = -9

            # This is checking if the space bar is released. If it is, the red square will move down.
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if not pauseFlag:
                        redSquareYChange = 5

            # This is checking if the user has pressed the escape key. If they have, it will pause the game.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not pauseFlag:
                        pauseFlag = True
                        pauseFlag = pause_menu()
                        redSquareYChange = 5
                        obstacleXChange = -5

        redSquareY += redSquareYChange
        if redSquareY > 600:
            redSquareY = 600
        if redSquareY < 0:
            redSquareY = 0

        obstacleX += obstacleXChange
        if obstacleX < 40 and not scoreFlag:
            score += 1
            scoreFlag = True

        if obstacleX < -60:
            obstacleX = 500
            obstacleHeight = random.randint(200, 400)
            scoreFlag = False

        if detectCollision(obstacleHeight, obstacleHeight + 250, obstacleX, redSquareY):
            obstacleXChange = 0
            redSquareYChange = 0
        else:
            if score > 20:
                obstacleXChange = -6
            if score > 50:
                obstacleXChange = -7
            if score > 100:
                obstacleXChange = -8

        # Updating the display.
        pygame.display.update()


def displayObstacle(topObstacleHeight, obstacleX, obstacleColor, obstacleWidth):
    pygame.draw.rect(screen, obstacleColor, (obstacleX, 0, obstacleWidth, topObstacleHeight))
    bottomObstacleY = topObstacleHeight + 250
    bottomObstacleHeight = 700 - bottomObstacleY
    pygame.draw.rect(screen, obstacleColor, (obstacleX, bottomObstacleY, obstacleWidth, bottomObstacleHeight))


def detectCollision(topObstacleHeight, bottomObstacleHeight, obstacleX, redSquareY):
    if 40 <= obstacleX <= 200:
        if redSquareY <= topObstacleHeight or redSquareY >= (bottomObstacleHeight - 100):
            return True
    return False


def displayScore(scoreText, score):
    scoreTextSurface = scoreText.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(scoreTextSurface, (10, 10))


def pause_menu():
    pause_font = pygame.font.SysFont(None, 100)
    game_font = pygame.font.SysFont(None, 70)
    resume_button = Button(150, 225, 200, 100, "Resume", (150, 150, 0), (255, 255, 255), game_font, 70, (0, 0, 150))
    quit_button = Button(150, 375, 200, 100, "Quit", (150, 150, 0), (255, 255, 255), game_font, 70, (0, 0, 150))
    while True:

        titleText = pause_font.render("Paused", True, (0, 0, 200))
        titleRect = titleText.get_rect(center=(250, 100))
        screen.blit(titleText, titleRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        resume_button.draw()
        resume_button.is_hovered()
        if resume_button.is_clicked():
            return False

        quit_button.draw()
        quit_button.is_hovered()
        if quit_button.is_clicked():
            main_menu()

        pygame.display.update()
        clock.tick(60)


main_menu()
