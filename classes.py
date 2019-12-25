import pygame
from random import randrange
import backtrack
import time

pygame.init()

class Grid:
    BIG_LINE_COLOUR = (57, 71, 91)
    SMALL_LINE_COLOUR = (212, 217, 230)
    DEFAULT_COLOUR = (255, 255, 255)
    GREEN = (190, 235, 190)
    RED = (235, 190, 190)
    EASY = (30, 40)
    MEDIUM = (40, 50)
    HARD = (50, 60)
    SOLVE_DELAY = 50

    def __init__(self, pos, gridWidth, difficulty, surface):
        self.pos = pos
        self.gridWidth = gridWidth
        self.smallWidth = gridWidth // 9
        self.largeWidth = self.smallWidth * 3
        self.lineWidth = gridWidth // 150
        self.difficulty = difficulty

        # assigns values to self.grid and self.tiles
        self.grid = []
        self.tiles = []
        self.surface = surface
        self.generateBoard(self.difficulty)

        self.prevClicked = (0,0)
        self.tileClicked = False
        self.checkMove = False

    def generateBoard(self, difficulty):
        # generate first row
        possibilities = [i for i in range(1, 10)]
        grid = [[0 for j in range(9)] for i in range(9)]
        for i in range(9):
            index = randrange(len(possibilities))
            value = possibilities[index]
            grid[0][i] = value
            possibilities.remove(value)

        # fill in board based on first row
        backtrack.randomSolve(grid)

        if difficulty == 'easy':
            removeRange = Grid.EASY
        elif difficulty == 'medium':
            removeRange = Grid.MEDIUM
        else:
            removeRange = Grid.HARD
        spotsToRemove = randrange(removeRange[0], removeRange[1])
        indicies = [i for i in range(9)]

        while spotsToRemove > 0:
            row = indicies[randrange(9)]
            col = indicies[randrange(9)]
            if grid[row][col] != 0:
                grid[row][col] = 0
                spotsToRemove -= 1

        self.grid = grid
        self.tiles = [[Tile(self.smallWidth, j, i, grid[i][j], True, self.gridWidth, self.surface) for j in range(9)] for i in range(9)]
        for i in range(9):
            for j in range(9):
                if self.tiles[i][j].value == 0:
                    self.tiles[i][j].given = False

    def drawTiles(self):
        for i in range(9):
            for j in range(9):
                self.tiles[i][j].drawContent(self.pos, self.lineWidth)

    def draw(self, state):
        # board is incorrect
        if state == 'loss':
            colour = Grid.RED
        # board is solved
        elif state == 'win':
            colour = Grid.GREEN
        # default colour
        else:
            colour = Grid.DEFAULT_COLOUR
        pygame.draw.rect(self.surface, colour, (self.pos[0], self.pos[1], self.largeWidth * 3, self.largeWidth * 3))

        # vertical small lines
        for i in range(10):
            pygame.draw.line(self.surface, Grid.SMALL_LINE_COLOUR,
                (i * self.smallWidth + self.pos[0], self.pos[1]),
                (i * self.smallWidth + self.pos[0], self.pos[1] + 3 * self.largeWidth),
                self.lineWidth)
        # horizontal small lines
        for i in range(10):
            pygame.draw.line(self.surface, Grid.SMALL_LINE_COLOUR,
                (self.pos[0], i * self.smallWidth + self.pos[1]),
                (self.pos[0] + 3 * self.largeWidth, i * self.smallWidth + self.pos[1]),
                self.lineWidth)
        # vertical big lines
        for i in range(4):
            pygame.draw.line(self.surface, Grid.BIG_LINE_COLOUR,
                (i * self.largeWidth + self.pos[0], self.pos[1]),
                (i * self.largeWidth + self.pos[0], self.pos[1] + 3 * self.largeWidth),
                self.lineWidth)
        # horizontal big lines
        for i in range(4):
            pygame.draw.line(self.surface, Grid.BIG_LINE_COLOUR,
                (self.pos[0], i * self.largeWidth + self.pos[1]),
                (self.pos[0] + 3 * self.largeWidth, i * self.largeWidth + self.pos[1]),
                self.lineWidth)

        self.drawTiles()

    def clear(self):
        for i in range(9):
            for j in range(9):
                self.tiles[i][j].wrong = False
                if not self.tiles[i][j].given:
                    self.grid[i][j] = 0
                    self.tiles[i][j].changeValue(0)
                    self.draw('default')
        self.tileClicked = False

    def checkMoveValid(self):
        for i in range(9):
            for j in range(9):
                self.tiles[i][j].wrong = False

        for row in range(9):
            for col in range(9):
                # check for same number in row
                for i in range(9):
                    if self.grid[row][col] == self.grid[row][i] and i != col and self.grid[row][col] != 0:
                        self.tiles[row][i].wrong = True
                        self.tiles[row][col].wrong = True
                # check for same number in column
                for i in range(9):
                    if self.grid[row][col] == self.grid[i][col] and i != row and self.grid[row][col] != 0:
                        self.tiles[i][col].wrong = True
                        self.tiles[row][col].wrong = True
                # check for same number in sector
                rSector, cSector = 3* (row//3), 3 * (col//3)
                for i in range(rSector, rSector+3):
                    for j in range(cSector, cSector+3):
                        if self.grid[row][col] == self.grid[i][j] and row != i and col != j and self.grid[row][col] != 0:
                            self.tiles[i][j].wrong = True
                            self.tiles[row][col].wrong = True

        for i in range(9):
            for j in range(9):
                print(self.tiles[i][j].wrong, end = '')
            print('')
        print('')

    def updateTile(self, value, row, col, clicked):
        if not self.tiles[row][col].given:
            self.grid[row][col] = value
            self.tiles[row][col].changeValue(value)
            if self.checkMove:
                self.checkMoveValid()
                self.drawTiles()
            self.tiles[row][col].drawSquare(clicked, self.pos, self.lineWidth)

    def clicked(self, pos):
        if (self.pos[0] < pos[0] < self.pos[0]+3*self.largeWidth) and (self.pos[1] < pos[1] < self.pos[1]+3*self.largeWidth):
            return ((pos[1]-self.pos[1]) // self.smallWidth, (pos[0]-self.pos[0]) // self.smallWidth)
        else:
            return None

    def click(self, row, col):
        # unclick previous tile
        self.tiles[self.prevClicked[0]][self.prevClicked[1]].drawSquare(False, self.pos, self.lineWidth)
        self.prevClicked = (row, col)
        self.tileClicked = True
        # click current tile
        self.tiles[row][col].drawSquare(True, self.pos, self.lineWidth)

    def solve(self, clock):
        r, c = backtrack.nextOpenSpot(self.grid)
        if r == -1:
            return True
        for num in range(1, 10):
            if backtrack.validMove(self.grid, r, c, num):
                # draw in new value
                self.grid[r][c] = num
                self.tiles[r][c].changeValue(num)
                self.tiles[r][c].drawSquare(False, self.pos, self.lineWidth)
                clock.displayTime(time.time())
                pygame.display.update()
                pygame.time.delay(Grid.SOLVE_DELAY)

                if self.solve(clock):
                    return True

                # delete incorrect value
                self.grid[r][c] = 0
                self.tiles[r][c].changeValue(0)
                self.tiles[r][c].drawSquare(False, self.pos, self.lineWidth)
                clock.displayTime(time.time())
                pygame.display.update()
                pygame.time.delay(Grid.SOLVE_DELAY)
        return False


class Tile:
    DEFAULT_COLOUR = (255, 255, 255)
    GIVEN_COLOUR = (57, 71, 91)
    USER_COLOUR = (90, 115, 185)
    CLICK_COLOUR = (187, 222, 250)
    WRONG_COLOUR = (205, 100, 100)

    def __init__(self, size, row, col, value, given, gridWidth, surface):
        self.size = size
        self.changeValue(value)
        self.row = row
        self.col = col
        self.given = given
        self.fontSize = gridWidth // 10
        self.surface = surface
        self.font = pygame.font.SysFont("comicsans", self.fontSize)
        self.wrong = False

    def changeValue(self, value):
        self.value = value
        if value == 0:
            self.display = ''
        else:
            self.display = str(value)

    def drawContent(self, gridPos, lineWidth):
        # value contradicts with other value
        if self.wrong:
            text = self.font.render(self.display, True, Tile.WRONG_COLOUR)
        # value is preset by board
        elif self.given:
            text = self.font.render(self.display, True, Tile.GIVEN_COLOUR)
        # user entered value
        else:
            text = self.font.render(self.display, True, Tile.USER_COLOUR)

        x = self.row * self.size + gridPos[0] + lineWidth
        y = self.col * self.size + gridPos[1] + lineWidth

        textRect = text.get_rect()
        textRect.center = (x + self.size // 2, y + self.size // 2)
        self.surface.blit(text, textRect)

    def drawSquare(self, clicked, gridPos, lineWidth):
        x = self.row * self.size + gridPos[0] + lineWidth
        y = self.col * self.size + gridPos[1] + lineWidth
        width = self.size - lineWidth
        # user clicked a square
        if clicked:
            pygame.draw.rect(self.surface, Tile.CLICK_COLOUR, (x, y, width, width))
            self.drawContent(gridPos, lineWidth)
        # tile not clicked
        else:
            pygame.draw.rect(self.surface, Tile.DEFAULT_COLOUR, (x, y, width, width))
            self.drawContent(gridPos, lineWidth)


class Button:
    LINE_COLOUR = (212, 217, 230)
    DEFAULT_COLOUR = (255, 255, 255)
    CLICKED_COLOUR = (187, 222, 250)
    HOVER_COLOUR = (232, 237, 250)
    TEXT_COLOUR = (57, 71, 91)

    def __init__(self, pos, width, height, fontSize, text, gridWidth, surface):
        self.pos = pos
        self.width = width
        self.height = height
        self.lineWidth = gridWidth // 150
        self.surface = surface
        self.hovered = False
        self.clicked = False

        self.font = pygame.font.SysFont("comicsans", fontSize)
        self.text = self.font.render(text, True, Button.TEXT_COLOUR)
        self.textRect = self.text.get_rect()
        self.textRect.center = (pos[0] + width// 2, pos[1] + height // 2)

    def draw(self, click):
        if click:
            pygame.draw.rect(self.surface, Button.CLICKED_COLOUR, (self.pos[0], self.pos[1], self.width, self.height))
        elif self.hovered:
            pygame.draw.rect(self.surface, Button.HOVER_COLOUR, (self.pos[0], self.pos[1], self.width, self.height))
        else:
            pygame.draw.rect(self.surface, Button.DEFAULT_COLOUR, (self.pos[0], self.pos[1], self.width, self.height))
        pygame.draw.line(self.surface, Button.LINE_COLOUR, (self.pos[0], self.pos[1]), (self.pos[0]+self.width, self.pos[1]), self.lineWidth)
        pygame.draw.line(self.surface, Button.LINE_COLOUR, (self.pos[0], self.pos[1]+self.height), (self.pos[0]+self.width, self.pos[1]+self.height), self.lineWidth)
        pygame.draw.line(self.surface, Button.LINE_COLOUR, (self.pos[0], self.pos[1]), (self.pos[0], self.pos[1]+self.height), self.lineWidth)
        pygame.draw.line(self.surface, Button.LINE_COLOUR, (self.pos[0]+self.width, self.pos[1]), (self.pos[0]+self.width, self.pos[1]+self.height), self.lineWidth)

        self.surface.blit(self.text, self.textRect)

    def hover(self, pos):
        if self.pos[0] < pos[0] < self.pos[0] + self.width and self.pos[1] < pos[1] < self.pos[1] + self.height:
            self.hovered = True
        else:
            self.hovered = False

    def click(self, pos):
        if self.pos[0] < pos[0] < self.pos[0] + self.width and self.pos[1] < pos[1] < self.pos[1] + self.height:
            return True
        else:
            return False


class Clock:
    def __init__(self, pos, startTime, surface, colour, width, height):
        self.pos = pos
        self.startTime = startTime
        self.surface = surface
        self.surfaceColour = colour
        self.prevTime = ''
        self.width = width
        self.height = height

        self.font = pygame.font.SysFont("comicsans", 40)

    @staticmethod
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

    def displayTime(self, time):
        playTime = round(time - self.startTime)
        currTime = Clock.formatTime(playTime)

        if currTime != self.prevTime:
            self.clearTime()
            self.prevTime = currTime
            text = self.font.render(currTime, True, Button.TEXT_COLOUR)
            self.surface.blit(text, self.pos)

    def clearTime(self):
        pygame.draw.rect(self.surface, self.surfaceColour, (self.pos[0], self.pos[1] - 25, self.width, self.height))
