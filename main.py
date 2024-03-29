import pygame, random, os

pygame.init()
pygame.display.set_caption("Project F")
screen = pygame.display.set_mode((500, 700))
clock = pygame.time.Clock()
file = open("BestScore.txt", "r")
best_score = int(file.read())
file.close()


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
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered():
                return True
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

        play_button.draw()
        play_button.is_hovered()

        score_button.draw()
        score_button.is_hovered()

        quit_button.draw()
        quit_button.is_hovered()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_hovered():
                    game()
                if score_button.is_hovered():
                    print("Score Clicked")
                    # score_menu()
                if quit_button.is_hovered():
                    pygame.quit()
                    quit()

        pygame.display.update()
        clock.tick(60)


def game():
    global best_score
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
    collisionFLag = False

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

        if obstacleX < 40 and not scoreFlag:
            score += 1
            if score > best_score:
                best_score = score
                if os.path.exists("BestScore.txt"):
                    file = open("BestScore.txt", "w")
                    file.write(str(best_score))
                    file.close()
            print(best_score)
            scoreFlag = True

        if obstacleX < -60:
            obstacleX = 500
            obstacleHeight = random.randint(200, 400)
            scoreFlag = False

        obstacleX += obstacleXChange
        if detectCollision(obstacleHeight, obstacleHeight + 250, obstacleX, redSquareY):
            obstacleXChange = 0
            redSquareYChange = 0
            collisionFLag = True
            loose_menu(score)
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
    if 45 <= obstacleX <= 195:
        if redSquareY <= topObstacleHeight - 3 or redSquareY >= (bottomObstacleHeight - 98):
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

        resume_button.draw()
        resume_button.is_hovered()

        quit_button.draw()
        quit_button.is_hovered()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.is_hovered():
                    return False
                if quit_button.is_hovered():
                    main_menu()

        pygame.display.update()
        clock.tick(60)


def loose_menu(score):
    loose_font = pygame.font.SysFont(None, 100)
    game_font = pygame.font.SysFont(None, 70)
    play_again_button = Button(150, 350, 200, 100, "Retry", (150, 150, 0), (255, 255, 255), game_font, 70, (0, 0, 150))
    quit_button = Button(150, 500, 200, 100, "Quit", (150, 150, 0), (255, 255, 255), game_font, 70, (0, 0, 150))
    while True:

        titleText = loose_font.render("You Loose", True, (0, 0, 200))
        titleRect = titleText.get_rect(center=(250, 100))
        screen.blit(titleText, titleRect)

        scoreText = loose_font.render(f"Score: {score}", True, (0, 0, 200))
        scoreRect = scoreText.get_rect(center=(250, 200))
        screen.blit(scoreText, scoreRect)

        bestScoreText = loose_font.render(f"Best Score: {best_score}", True, (0, 0, 200))
        bestScoreRect = bestScoreText.get_rect(center=(250, 300))
        screen.blit(bestScoreText, bestScoreRect)

        play_again_button.draw()
        play_again_button.is_hovered()

        quit_button.draw()
        quit_button.is_hovered()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.is_hovered():
                    game()
                if quit_button.is_hovered():
                    main_menu()

        pygame.display.update()
        clock.tick(60)


main_menu()
