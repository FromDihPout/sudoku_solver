import pygame
pygame.init()

class Grid:
    BIG_LINE_COLOUR = (57, 71, 91)
    SMALL_LINE_COLOUR = (212, 217, 230)
    WHITE = (255, 255, 255)
    GREEN = (190, 235, 190)
    RED = (235, 190, 190)
    def __init__(self, grid, pos, gridWidth):
        self.grid = grid
        self.pos = pos
        self.smallWidth = gridWidth // 9
        self.largeWidth = self.smallWidth * 3
        self.lineWidth = gridWidth // 150
        self.tiles = [[Tile(self.smallWidth, j, i, grid[i][j], True, gridWidth) for j in range(9)] for i in range(9)]
        for i in range(9):
            for j in range(9):
                if self.tiles[i][j].value == 0:
                    self.tiles[i][j].given = False
        self.prevClicked = (0,0)
        self.tileClicked = False
        self.difficulty = 'easy'

    def drawGrid(self, surface):
        # vertical small lines
        for i in range(10):
            pygame.draw.line(surface, Grid.SMALL_LINE_COLOUR,
                (i * self.smallWidth + self.pos[0], self.pos[1]),
                (i * self.smallWidth + self.pos[0], self.pos[1] + 3 * self.largeWidth),
                self.lineWidth)
        # horizontal small lines
        for i in range(10):
            pygame.draw.line(surface, Grid.SMALL_LINE_COLOUR,
                (self.pos[0], i * self.smallWidth + self.pos[1]),
                (self.pos[0] + 3 * self.largeWidth, i * self.smallWidth + self.pos[1]),
                self.lineWidth)
        # vertical big lines
        for i in range(4):
            pygame.draw.line(surface, Grid.BIG_LINE_COLOUR,
                (i * self.largeWidth + self.pos[0], self.pos[1]),
                (i * self.largeWidth + self.pos[0], self.pos[1] + 3 * self.largeWidth),
                self.lineWidth)
        # horizontal big lines
        for i in range(4):
            pygame.draw.line(surface, Grid.BIG_LINE_COLOUR,
                (self.pos[0], i * self.largeWidth + self.pos[1]),
                (self.pos[0] + 3 * self.largeWidth, i * self.largeWidth + self.pos[1]),
                self.lineWidth)

        # draw tiles
        for i in range(9):
            for j in range(9):
                self.tiles[i][j].displayContent(surface, self.pos, self.lineWidth)

    def updateTile(self, surface, value, row, col):
        if not self.tiles[row][col].given:
            self.grid[row][col] = value
            self.tiles[row][col].update(value)
            self.tiles[row][col].click(surface, True, self.pos, self.lineWidth)

    def clicked(self, pos):
        if (self.pos[0] < pos[0] < self.pos[0]+3*self.largeWidth) and (self.pos[1] < pos[1] < self.pos[1]+3*self.largeWidth):
            return ((pos[1]-self.pos[1]) // self.smallWidth, (pos[0]-self.pos[0]) // self.smallWidth)
        else:
            return None

    def click(self, surface, row, col):
        # unclick previous tile
        self.tiles[self.prevClicked[0]][self.prevClicked[1]].click(surface, False, self.pos, self.lineWidth)
        self.prevClicked = (row, col)
        self.tileClicked = True
        # click current tile
        self.tiles[row][col].click(surface, True, self.pos, self.lineWidth)

    def drawState(self, surface, state):
        # reset board colour
        if state == 0:
            colour = Grid.WHITE
        # player lost
        if state == 1:
            colour = Grid.RED
        # player won
        if state == 2:
            colour = Grid.GREEN
        pygame.draw.rect(surface, colour, (self.pos[0], self.pos[1], self.largeWidth * 3, self.largeWidth * 3))
        self.drawGrid(surface)


class Tile:
    WHITE = (255, 255, 255)
    GIVEN_COLOUR = (57, 71, 91)
    USER_COLOUR = (147, 182, 210)
    CLICK_COLOUR = (187, 222, 250)

    def __init__(self, size, row, col, value, given, gridWidth):
        self.size = size
        self.update(value)
        self.row = row
        self.col = col
        self.given = given
        self.fontSize = gridWidth // 10
        self.font = pygame.font.SysFont("comicsans", self.fontSize)

    def update(self, value):
        self.value = value
        if value == 0:
            self.display = ''
        else:
            self.display = ('%d' %value)

    def displayContent(self, surface, gridPos, lineWidth):
        # value is preset by board
        if self.given:
            text = self.font.render(self.display, True, Tile.GIVEN_COLOUR)
        # user entered value
        else:
            text = self.font.render(self.display, True, Tile.USER_COLOUR)
        x = self.row * self.size + gridPos[0] + lineWidth
        y = self.col * self.size + gridPos[1] + lineWidth

        textRect = text.get_rect()
        textRect.center = (x + self.size // 2, y + self.size // 2)
        surface.blit(text, textRect)

    def click(self, surface, click, gridPos, lineWidth):
        x = self.row * self.size + gridPos[0] + lineWidth
        y = self.col * self.size + gridPos[1] + lineWidth
        width = self.size - lineWidth
        # user clicked a square
        if click:
            pygame.draw.rect(surface, Tile.CLICK_COLOUR, (x, y, width, width))
            self.displayContent(surface, gridPos, lineWidth)
        # undo previous click
        else:
            pygame.draw.rect(surface, Tile.WHITE, (x, y, width, width))
            self.displayContent(surface, gridPos, lineWidth)


class Button:
    LINE_COLOUR = (212, 217, 230)
    WHITE = (255, 255, 255)
    CLICKED_COLOUR = (187, 222, 250)
    HOVER_COLOUR = (232, 237, 250)
    TEXT_COLOUR = (57, 71, 91)

    def __init__(self, pos, width, height, fontSize, text, gridWidth, hold):
        self.pos = pos
        self.width = width
        self.height = height
        self.lineWidth = gridWidth // 150
        self.font = pygame.font.SysFont("comicsans", fontSize)
        self.text = self.font.render(text, True, Button.TEXT_COLOUR)
        self.textRect = self.text.get_rect()
        self.textRect.center = (pos[0] + width// 2, pos[1] + height // 2)
        self.clicked = False
        self.hold = hold

    def draw(self, surface, hover, click):
        if click:
            pygame.draw.rect(surface, Button.CLICKED_COLOUR, (self.pos[0], self.pos[1], self.width, self.height))
        elif hover:
            pygame.draw.rect(surface, Button.HOVER_COLOUR, (self.pos[0], self.pos[1], self.width, self.height))
        else:
            pygame.draw.rect(surface, Button.WHITE, (self.pos[0], self.pos[1], self.width, self.height))
        pygame.draw.line(surface, Button.LINE_COLOUR, (self.pos[0], self.pos[1]), (self.pos[0]+self.width, self.pos[1]), self.lineWidth)
        pygame.draw.line(surface, Button.LINE_COLOUR, (self.pos[0], self.pos[1]+self.height), (self.pos[0]+self.width, self.pos[1]+self.height), self.lineWidth)
        pygame.draw.line(surface, Button.LINE_COLOUR, (self.pos[0], self.pos[1]), (self.pos[0], self.pos[1]+self.height), self.lineWidth)
        pygame.draw.line(surface, Button.LINE_COLOUR, (self.pos[0]+self.width, self.pos[1]), (self.pos[0]+self.width, self.pos[1]+self.height), self.lineWidth)

        surface.blit(self.text, self.textRect)

    def hover(self, surface, pos):
        if self.pos[0] < pos[0] < self.pos[0] + self.width and self.pos[1] < pos[1] < self.pos[1] + self.height:
            self.draw(surface, True, False)
            return True
        else:
            return False

    def click(self, surface, pos):
        if self.pos[0] < pos[0] < self.pos[0] + self.width and self.pos[1] < pos[1] < self.pos[1] + self.height:
            if self.hold:
                self.clicked = True
            return True
        else:
            return False
