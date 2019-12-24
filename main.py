import pygame
from classes import Grid, Tile, Button, Clock
import backtrack
import time
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

# setup window
pygame.display.set_caption("Sudoku")
WIN_DIMENSIONS = (650, 480)
WIN_COLOUR = (255, 255, 255)
win = pygame.display.set_mode(WIN_DIMENSIONS)
win.fill(WIN_COLOUR)

# setup grid
GRID_WIDTH = 425
GRID_POS = (25, 25)
grid = Grid(GRID_POS, GRID_WIDTH, 'easy', win)
grid.draw('default')

# setup button
BUTTON_START_X = 475
BUTTON_START_Y = 120
LARGE_WIDTH = 129
LARGE_HEIGHT = 50
LARGE_FONT = 28
SMALL_WIDTH = 40
SMALL_HEIGHT = 25
SMALL_FONT = 18
GAP = 8
newGameButton = Button((BUTTON_START_X, BUTTON_START_Y),
        LARGE_WIDTH, LARGE_HEIGHT, LARGE_FONT, "New Game", GRID_WIDTH, win)
easyButton = Button((BUTTON_START_X, BUTTON_START_Y + LARGE_HEIGHT),
        SMALL_WIDTH, SMALL_HEIGHT, SMALL_FONT, "Easy", GRID_WIDTH, win)
easyButton.clicked = True
mediumButton = Button((BUTTON_START_X + SMALL_WIDTH, BUTTON_START_Y + LARGE_HEIGHT),
        SMALL_WIDTH + 9, SMALL_HEIGHT, SMALL_FONT, "Medium", GRID_WIDTH, win)
hardButton = Button((BUTTON_START_X + 2*SMALL_WIDTH + 9, BUTTON_START_Y + LARGE_HEIGHT),
        SMALL_WIDTH, SMALL_HEIGHT, SMALL_FONT, "Hard", GRID_WIDTH, win)
checkBoardButton = Button((BUTTON_START_X, BUTTON_START_Y + LARGE_HEIGHT + SMALL_HEIGHT + GAP),
        LARGE_WIDTH, LARGE_HEIGHT, LARGE_FONT, "Check Board", GRID_WIDTH, win)
checkMoveButton = Button((BUTTON_START_X, BUTTON_START_Y + 2*LARGE_HEIGHT + SMALL_HEIGHT + 2*GAP),
        LARGE_WIDTH, LARGE_HEIGHT, LARGE_FONT, "Check Move", GRID_WIDTH, win)
solveButton = Button((BUTTON_START_X, BUTTON_START_Y + 3*LARGE_HEIGHT + SMALL_HEIGHT + 3*GAP),
        LARGE_WIDTH, LARGE_HEIGHT, LARGE_FONT, "Solve", GRID_WIDTH, win)
clearButton = Button((BUTTON_START_X, BUTTON_START_Y + 4*LARGE_HEIGHT + SMALL_HEIGHT + 4*GAP),
        LARGE_WIDTH, LARGE_HEIGHT, LARGE_FONT, "Clear", GRID_WIDTH, win)

# setup clock
clock = Clock((BUTTON_START_X, BUTTON_START_Y - 75), time.time(), win, WIN_COLOUR,
            WIN_DIMENSIONS[0] - BUTTON_START_X, 100)


def solve(grid):
    r, c = backtrack.nextOpenSpot(grid.grid)
    if r == -1:
        return True
    for num in range(1, 10):
        if backtrack.validMove(grid.grid, r, c, num):
            grid.grid[r][c] = num
            grid.tiles[r][c].changeValue(num)
            grid.tiles[r][c].drawSquare(False, grid.pos, grid.lineWidth)
            pygame.display.update()
            pygame.time.delay(50)

            if solve(grid):
                return True

            grid.grid[r][c] = 0
            grid.tiles[r][c].changeValue(0)
            grid.tiles[r][c].drawSquare(False, grid.pos, grid.lineWidth)
            pygame.display.update()
            pygame.time.delay(50)
    return False

run = True
currTime = ''
while run:
    key = None
    event = pygame.event.poll()

    if event.type == pygame.QUIT:
        run = False

    mouse = pygame.mouse.get_pos()
    # mouse hovered over button
    newGameButton.hover(mouse)
    easyButton.hover(mouse)
    mediumButton.hover(mouse)
    hardButton.hover(mouse)
    checkBoardButton.hover(mouse)
    checkMoveButton.hover(mouse)
    solveButton.hover(mouse)
    clearButton.hover(mouse)

    newGameButton.draw(newGameButton.clicked)
    easyButton.draw(easyButton.clicked)
    mediumButton.draw(mediumButton.clicked)
    hardButton.draw(hardButton.clicked)
    checkBoardButton.draw(checkBoardButton.clicked)
    checkMoveButton.draw(checkMoveButton.clicked)
    solveButton.draw(solveButton.clicked)
    clearButton.draw(clearButton.clicked)

    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        tile = grid.clicked(pos)
        # tile clicked
        if tile:
            grid.click(tile[0], tile[1])
        else:
            grid.tileClicked = False
            row = grid.prevClicked[0]
            col = grid.prevClicked[1]
            grid.updateTile(grid.tiles[row][col].value, row, col, False)
        # button clicked
        if newGameButton.click(pos):
            difficulty = grid.difficulty
            grid = Grid(GRID_POS, GRID_WIDTH, grid.difficulty, win)
            grid.draw('default')
        elif easyButton.click(pos):
            grid.difficulty = 'easy'
            easyButton.clicked = True
            mediumButton.clicked = False
            hardButton.clicked = False
        elif mediumButton.click(pos):
            grid.difficulty = 'medium'
            easyButton.clicked = False
            mediumButton.clicked = True
            hardButton.clicked = False
        elif hardButton.click(pos):
            grid.difficulty = 'hard'
            easyButton.clicked = False
            mediumButton.clicked = False
            hardButton.clicked = True
        elif checkBoardButton.click(pos):
            if backtrack.checkWin(grid.grid):
                grid.draw('win')
                pygame.display.update()
                pygame.time.delay(1000)
                grid.draw('default')
            else:
                grid.draw('loss')
                pygame.display.update()
                pygame.time.delay(1500)
                grid.draw('default')
        elif checkMoveButton.click(pos):
            checkMoveButton.clicked = not checkMoveButton.clicked
            if checkMoveButton.clicked:
                grid.checkMoveValid()
            else:
                for i in range(9):
                    for j in range(9):
                        grid.tiles[i][j].wrong = False

            grid.drawTiles()
            grid.checkMove = checkMoveButton.clicked
        elif solveButton.click(pos):
            solve(grid)
        elif clearButton.click(pos):
            grid.clear()

    # user enters a key
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
            key = 1
        elif event.key == pygame.K_2:
            key = 2
        elif event.key == pygame.K_3:
            key = 3
        elif event.key == pygame.K_4:
            key = 4
        elif event.key == pygame.K_5:
            key = 5
        elif event.key == pygame.K_6:
            key = 6
        elif event.key == pygame.K_7:
            key = 7
        elif event.key == pygame.K_8:
            key = 8
        elif event.key == pygame.K_9:
            key = 9
        elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE or event.key == pygame.K_0:
            key = 0

    # only make changes to the grid if key pressed and tile clicked
    if grid.tileClicked and key != None:
        grid.updateTile(key, tile[0], tile[1], True)

    clock.displayTime(time.time())
    pygame.display.update()
