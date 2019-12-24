def nextOpenSpot(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return -1, -1

def checkWin(grid):
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == 0:
                return False
            else:
                temp = grid[i][j]
                grid[i][j] = 0
                valid = validMove(grid, i, j, temp)
                grid[i][j] = temp
                if not valid:
                    return False
    return True

def validGrid(grid):
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] != 0:
                temp = grid[i][j]
                grid[i][j] = 0
                valid = validMove(grid, i, j, temp)
                grid[i][j] = temp
                if not valid:
                    return False
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
