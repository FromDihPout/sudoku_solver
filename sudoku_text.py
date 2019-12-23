def displayGrid(grid):
    for i in range(9):
        for j in range(9):
            print(' %d ' % grid[i][j], end='')
        print('')

def nextOpenSpot(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return -1, -1

def validGrid(grid):
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] != 0:
                temp = grid[i][j]
                grid[i][j] = 0
                if not validMove(grid, i, j, temp):
                    return False
                grid[i][j] = temp
    return True

def validMove(grid, r, c, num):
    rowValid = all(num != grid[r][i] for i in range(9))
    if rowValid:
        columnValid = all(num != grid[i][c] for i in range(9))
        if columnValid:
            # coordinates of top-left corner of sector
            rSector, cSector = 3* (r//3), 3 * (c//3)
            for i in range(rSector, rSector+3):
                for j in range(cSector, cSector+3):
                    if num == grid[i][j]:
                        return False
            return True
    return False


def solve(grid):
    r, c = nextOpenSpot(grid)
    if r == -1:
        return True
    for num in range(1, 10):
        if validMove(grid, r, c, num):
            grid[r][c] = num
            if solve(grid):
                return True
            grid[r][c] = 0
    return False


easy = [[5, 4, 3, 0, 0, 0, 0, 0, 0],
        [0, 2, 7, 0, 5, 1, 0, 0, 0],
        [0, 0, 8, 0, 7, 0, 2, 5, 6],
        [0, 0, 9, 5, 6, 0, 4, 0, 0],
        [0, 8, 0, 3, 0, 2, 9, 1, 5],
        [0, 0, 2, 1, 0, 7, 6, 8, 0],
        [0, 3, 0, 0, 0, 9, 0, 6, 0],
        [2, 0, 0, 7, 0, 0, 0, 9, 8],
        [0, 0, 4, 0, 8, 5, 0, 3, 0]]

medium = [[8, 0, 2, 4, 9, 0, 0, 0, 7],
          [7, 0, 0, 2, 0, 8, 3, 0, 6],
          [0, 9, 6, 7, 0, 0, 0, 0, 0],
          [0, 0, 0, 8, 0, 7, 0, 0, 0],
          [0, 5, 0, 0, 4, 0, 0, 0, 0],
          [9, 0, 4, 5, 0, 0, 0, 0, 0],
          [3, 0, 0, 9, 0, 0, 0, 1, 0],
          [5, 6, 0, 3, 0, 0, 0, 2, 0],
          [0, 2, 0, 0, 0, 0, 0, 6, 3]]

hardest = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 3, 6, 0, 0, 0, 0, 0],
           [0, 7, 0, 0, 9, 0, 2, 0, 0],
           [0, 5, 0, 0, 0, 7, 0, 0, 0],
           [0, 0, 0, 0, 4, 5, 7, 0, 0],
           [0, 0, 0, 1, 0, 0, 0, 3, 0],
           [0, 0, 1, 0, 0, 0, 0, 6, 8],
           [0, 0, 8, 5, 0, 0, 0, 1, 0],
           [0, 9, 0, 0, 0, 0, 4, 0, 0]]

impossible = [[5, 4, 3, 0, 0, 0, 0, 5, 5],
              [0, 2, 7, 0, 5, 1, 0, 0, 0],
              [0, 0, 8, 0, 7, 0, 2, 5, 6],
              [0, 0, 9, 5, 6, 0, 4, 0, 0],
              [0, 8, 0, 3, 0, 2, 9, 1, 5],
              [0, 0, 2, 1, 0, 7, 6, 8, 0],
              [0, 3, 0, 0, 0, 9, 0, 6, 0],
              [2, 0, 0, 7, 0, 0, 0, 9, 8],
              [0, 0, 4, 0, 8, 5, 0, 3, 0]]

if validGrid(easy):
    solve(easy)
displayGrid(easy)
print('')

if validGrid(medium):
    solve(medium)
displayGrid(medium)
print('')

if validGrid(hardest):
    solve(hardest)
displayGrid(hardest)
print('')

if validGrid(impossible):
    solve(easy)
displayGrid(impossible)
