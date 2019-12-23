import pygame
from classes import Grid, Tile, Button
import time
import backtrack

pygame.init()

easy = [[5, 4, 3, 9, 2, 6, 8, 7, 1],
        [6, 2, 7, 8, 5, 1, 3, 4, 9],
        [1, 9, 8, 4, 7, 3, 2, 5, 6],
        [3, 1, 9, 5, 6, 8, 4, 2, 7],
        [7, 8, 6, 3, 4, 2, 9, 1, 5],
        [4, 5, 2, 1, 9, 7, 6, 8, 3],
        [8, 3, 5, 2, 1, 9, 7, 6, 4],
        [2, 6, 1, 7, 3, 4, 5, 9, 8],
        [9, 7, 4, 6, 8, 5, 1, 3, 0]]
easy1 = [[5, 4, 3, 0, 0, 0, 0, 0, 0],
        [0, 2, 7, 0, 5, 1, 0, 0, 0],
        [0, 0, 8, 0, 7, 0, 2, 5, 6],
        [0, 0, 9, 5, 6, 0, 4, 0, 0],
        [0, 8, 0, 3, 0, 2, 9, 1, 5],
        [0, 0, 2, 1, 0, 7, 6, 8, 0],
        [0, 3, 0, 0, 0, 9, 0, 6, 0],
        [2, 0, 0, 7, 0, 0, 0, 9, 8],
        [0, 0, 4, 0, 8, 5, 0, 3, 0]]
hardest = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 3, 6, 0, 0, 0, 0, 0],
           [0, 7, 0, 0, 9, 0, 2, 0, 0],
           [0, 5, 0, 0, 0, 7, 0, 0, 0],
           [0, 0, 0, 0, 4, 5, 7, 0, 0],
           [0, 0, 0, 1, 0, 0, 0, 3, 0],
           [0, 0, 1, 0, 0, 0, 0, 6, 8],
           [0, 0, 8, 5, 0, 0, 0, 1, 0],
           [0, 9, 0, 0, 0, 0, 4, 0, 0]]

pygame.display.set_caption("Sudoku")
WIN_DIMENSIONS = (650, 480)
WIN_COLOUR = (255, 255, 255)
win = pygame.display.set_mode(WIN_DIMENSIONS)
win.fill(WIN_COLOUR)

GRID_WIDTH = 425
grid = Grid(hardest, (25, 25), GRID_WIDTH)
grid.drawGrid(win)

BUTTON_START_X = 475
BUTTON_START_Y = 150
LARGE_WIDTH = 129
LARGE_HEIGHT = 50
LARGE_FONT = 28
SMALL_WIDTH = 40
SMALL_HEIGHT = 25
SMALL_FONT = 18
GAP = 8
newGameButton = Button((BUTTON_START_X, BUTTON_START_Y),
        LARGE_WIDTH, LARGE_HEIGHT, LARGE_FONT, "New Game", GRID_WIDTH, False)
easyButton = Button((BUTTON_START_X, BUTTON_START_Y + LARGE_HEIGHT),
        SMALL_WIDTH, SMALL_HEIGHT, SMALL_FONT, "Easy", GRID_WIDTH, False)
easyButton.clicked = True
mediumButton = Button((BUTTON_START_X + SMALL_WIDTH, BUTTON_START_Y + LARGE_HEIGHT),
        SMALL_WIDTH + 9, SMALL_HEIGHT, SMALL_FONT, "Medium", GRID_WIDTH, False)
hardButton = Button((BUTTON_START_X + 2*SMALL_WIDTH + 9, BUTTON_START_Y + LARGE_HEIGHT),
        SMALL_WIDTH, SMALL_HEIGHT, SMALL_FONT, "Hard", GRID_WIDTH, False)
checkBoardButton = Button((BUTTON_START_X, BUTTON_START_Y + LARGE_HEIGHT + SMALL_HEIGHT + GAP),
        LARGE_WIDTH, LARGE_HEIGHT, LARGE_FONT, "Check Board", GRID_WIDTH, False)
checkMoveButton = Button((BUTTON_START_X, BUTTON_START_Y + 2*LARGE_HEIGHT + SMALL_HEIGHT + 2*GAP),
        LARGE_WIDTH, LARGE_HEIGHT, LARGE_FONT, "Check Move", GRID_WIDTH, True)
solveButton = Button((BUTTON_START_X, BUTTON_START_Y + 3*LARGE_HEIGHT + SMALL_HEIGHT + 3*GAP),
        LARGE_WIDTH, LARGE_HEIGHT, LARGE_FONT, "Solve", GRID_WIDTH, False)
pygame.display.update()


def solve(grid):
    r, c = backtrack.nextOpenSpot(grid.grid)
    if r == -1:
        return True
    for num in range(1, 10):
        if backtrack.validMove(grid.grid, r, c, num):
            grid.grid[r][c] = num
            grid.tiles[r][c].update(num)
            grid.tiles[r][c].click(win, False, grid.pos, grid.lineWidth)
            pygame.display.update()
            pygame.time.delay(5)

            if solve(grid):
                return True

            grid.grid[r][c] = 0
            grid.tiles[r][c].update(0)
            grid.tiles[r][c].click(win, False, grid.pos, grid.lineWidth)
            pygame.display.update()
            pygame.time.delay(5)
    return False


def formatTime(seconds):
    sec = seconds % 60
    min = seconds // 60
    hour = min // 60

    time = " "
    if hour < 10:
        time += "0"
    time += str(hour) + ":"
    if min < 10:
        time += "0"
    time += str(min) + ":"
    if sec < 10:
        time += "0"
    time += str(sec)
    return time

def displayTime(time):
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render(time, True, Button.TEXT_COLOUR)
    win.blit(text, (BUTTON_START_X, BUTTON_START_Y - 75))

def clearTime():
    pygame.draw.rect(win, WIN_COLOUR, (BUTTON_START_X, BUTTON_START_Y - 100, WIN_DIMENSIONS[0] - BUTTON_START_X, 100))

run = True
start = time.time()
currTime = ''
while run:
    key = None
    playTime = round(time.time() - start)
    oldTime = currTime
    currTime = formatTime(playTime)
    if time != oldTime:
        clearTime()
        displayTime(currTime)
        pygame.display.update()

    pygame.display.update()
    event = pygame.event.poll()

    if event.type == pygame.QUIT:
        run = False

    # mouse hovered over button
    mouse = pygame.mouse.get_pos()
    if newGameButton.hover(win, mouse):
        pygame.display.update()
    elif not easyButton.clicked and easyButton.hover(win, mouse):
        pygame.display.update()
    elif not mediumButton.clicked and mediumButton.hover(win, mouse):
        pygame.display.update()
    elif not hardButton.clicked and hardButton.hover(win, mouse):
        pygame.display.update()
    elif checkBoardButton.hover(win, mouse):
        pygame.display.update()
    elif not checkMoveButton.clicked and checkMoveButton.hover(win, mouse):
        pygame.display.update()
    elif solveButton.hover(win, mouse):
        pygame.display.update()
    # mouse not hovered over any buttons, draw them normally
    else:
        newGameButton.draw(win, False, newGameButton.clicked)
        easyButton.draw(win, False, easyButton.clicked)
        mediumButton.draw(win, False, mediumButton.clicked)
        hardButton.draw(win, False, hardButton.clicked)
        checkBoardButton.draw(win, False, checkBoardButton.clicked)
        checkMoveButton.draw(win, False, checkMoveButton.clicked)
        solveButton.draw(win, False, solveButton.clicked)
        pygame.display.update()

    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        tile = grid.clicked(pos)
        # tile clicked
        if tile:
            grid.click(win, tile[0], tile[1])
            pygame.display.update()
        # button clicked
        elif newGameButton.click(win, pos):
            pygame.display.update()
        elif easyButton.click(win, pos):
            grid.difficulty = 'easy'
            easyButton.clicked = True
            mediumButton.clicked = False
            hardButton.clicked = False
            pygame.display.update()
        elif mediumButton.click(win, pos):
            grid.difficulty = 'medium'
            easyButton.clicked = False
            mediumButton.clicked = True
            hardButton.clicked = False
            pygame.display.update()
        elif hardButton.click(win, pos):
            grid.difficulty = 'hard'
            easyButton.clicked = False
            mediumButton.clicked = False
            hardButton.clicked = True
            pygame.display.update()
        elif checkBoardButton.click(win, pos):
            if backtrack.checkWin(grid.grid):
                grid.drawState(win, 2)
                pygame.display.update()
                pygame.time.delay(1000)
                grid.drawState(win, 0)
                pygame.display.update()
            else:
                grid.drawState(win, 1)
                pygame.display.update()
                pygame.time.delay(1500)
                grid.drawState(win, 0)
                pygame.display.update()
        elif checkMoveButton.click(win, pos):
            pygame.display.update()
        elif solveButton.click(win, pos):
            solve(grid)
            pygame.display.update()

    # user enters a key
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
            key = 1
        if event.key == pygame.K_2:
            key = 2
        if event.key == pygame.K_3:
            key = 3
        if event.key == pygame.K_4:
            key = 4
        if event.key == pygame.K_5:
            key = 5
        if event.key == pygame.K_6:
            key = 6
        if event.key == pygame.K_7:
            key = 7
        if event.key == pygame.K_8:
            key = 8
        if event.key == pygame.K_9:
            key = 9
        if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
            key = 0

    # only make changes to the grid if key pressed and tile clicked
    if grid.tileClicked and key != None:
        grid.updateTile(win, key, tile[0], tile[1])
        pygame.display.update()
