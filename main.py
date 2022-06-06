import pygame
import random

pygame.init()

# This is setting the screen size to 500 by 700, setting the game to running, and setting the clock.
screen = pygame.display.set_mode((500, 700))
running = True
clock = pygame.time.Clock()


# This is creating a red square that is 100 by 100 pixels. It is setting the red square's x and y coordinates to
# 100 and 250. It is also setting the red square's y change to 0.
redSquare = pygame.Surface((100, 100))
redSquare.fill((255, 0, 0))
redSquareX = 100
redSquareY = 250
redSquareYChange = 0


def displayRedSquare(x, y):
    """
    "Display the red square at the given x and y coordinates."

    :param x: The x coordinate of the top left corner of the square
    :param y: The y coordinate of the top left corner of the square
    """
    screen.blit(redSquare, (x, y))


# Creating the obstacle.
obstacleWidth = 60
obstacleHeight = random.randint(150, 450)
obstacleColor = (0, 255, 0)
obstacleXChange = -5
obstacleX = 500


def displayObstacle(topObstacleHeight):
    """
    It draws two rectangles, one on the top and one on the bottom, to create the illusion of a single obstacle

    :param topObstacleHeight: The height of the top obstacle
    """
    pygame.draw.rect(screen, obstacleColor, (obstacleX, 0, obstacleWidth, topObstacleHeight))
    bottomObstacleY = topObstacleHeight + 250
    bottomObstacleHeight = 700 - bottomObstacleY
    pygame.draw.rect(screen, obstacleColor, (obstacleX, bottomObstacleY, obstacleWidth, bottomObstacleHeight))


def detectCollision(topObstacleHeight, bottomObstacleHeight):
    """
    If the red square is within the obstacle's x-coordinate range and the red square's y-coordinate is either above the top
    obstacle or below the bottom obstacle, then the red square has collided with the obstacle

    :param topObstacleHeight: The height of the top obstacle
    :param bottomObstacleHeight: The height of the bottom obstacle
    :return: a boolean value.
    """
    if 100 <= obstacleX <= 200:
        if redSquareY <= topObstacleHeight or redSquareY >= (bottomObstacleHeight - 100):
            return True
    return False


# Creating a variable called score and setting it to 0. It is also creating a variable called scoreText and
# setting it to a font.
score = 0
scoreText = pygame.font.Font('freesansbold.ttf', 32)


def displayScore():
    """
    It creates a surface with the text "Score: [score]" and then blits it to the screen at the coordinates (10, 10)
    """
    scoreTextSurface = scoreText.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(scoreTextSurface, (10, 10))


# This is the main game loop. It is checking for events, updating the game, and displaying the game.
while running:
    clock.tick(60)
    screen.fill((0, 0, 0))

    # This is checking for events. If the event is the user closing the window, it will stop the game. If the event
    # is the user pressing the space bar, it will move the red square up. If the event is the user releasing the
    # space bar, it will move the red square down.
    for event in pygame.event.get():

        # This is checking if the user has closed the window. If they have, it will stop the game.
        if event.type == pygame.QUIT:
            running = False

        # This is checking if the space bar is pressed. If it is, the red square will move up.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                redSquareYChange = -9

        # This is checking if the space bar is released. If it is, the red square will move down.
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                redSquareYChange = 5

    # This is checking if the red square is going out of bounds. If it is, it will set the red square to the edge of the
    # screen.
    redSquareY += redSquareYChange
    if redSquareY > 600:
        redSquareY = 600
    if redSquareY < 0:
        redSquareY = 0

    # This is moving the obstacle to the left and resetting it when it goes off the screen.
    obstacleX += obstacleXChange
    if obstacleX < -100:
        obstacleX = 500
        obstacleHeight = random.randint(200, 400)
        score += 1

    # Displaying the obstacle, the red square, and the score.
    displayObstacle(obstacleHeight)
    displayRedSquare(redSquareX, redSquareY)
    displayScore()

    # This is checking if the red square has collided with the obstacle. If it has, it will print "Collision!" and
    # stop the game.
    collision = detectCollision(obstacleHeight, obstacleHeight + 250)
    if collision:
        print("Collision!")
        running = False

    # Updating the display.
    pygame.display.update()

# Quitting pygame.
pygame.quit()
