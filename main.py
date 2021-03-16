import random

# space object
class Space:
    def __init__(self, val):
        self.val = val

# info object
class SpaceQuery:
    def __init__(self, isSafe, surroundingMines, visibleSafeNeighbors, visibleMineNeighbors, visibleUnqueriedNeighbors):
        self.isSafe = isSafe
        self.surroundingMines = surroundingMines
        self.visibleSafeNeighbors = visibleSafeNeighbors
        self.visibleMineNeighbors = visibleMineNeighbors
        self.visibleUnqueriedNeighbors = visibleUnqueriedNeighbors

# check_nearest finds how many mines are next to a specified position on the board
# board is a list of list of spaces
# x is the row we are searching
# y is the column we are searching
def check_nearest(board, x, y):
    n = 0
    try:
        if board[x][y + 1].val == -1:
            n += 1
    except IndexError:
        pass
    try:
        if board[x][y - 1].val == -1:
            n += 1
    except IndexError:
        pass
    try:
        if board[x - 1][y - 1].val == -1:
            n += 1
    except IndexError:
        pass
    try:
        if board[x - 1][y + 1].val == -1:
            n += 1
    except IndexError:
        pass
    try:
        if board[x - 1][y].val == -1:
            n += 1
    except IndexError:
        pass
    try:
        if board[x + 1][y - 1].val == -1:
            n += 1
    except IndexError:
        pass
    try:
        if board[x + 1][y + 1].val == -1:
            n += 1
    except IndexError:
        pass
    try:
        if board[x + 1][y].val == -1:
            n += 1
    except IndexError:
        pass
    return n
def board_gen(d, n):
    # simple generation of all 0s
    board = []
    for i in range(d):
        r = []
        for j in range(d):
            s = Space(False, 0)
            r.append(s)
        board.append(r)

    # add mines
    while n > 0:
        #print(n)
        i = random.randint(0, d - 1)
        j = random.randint(0, d - 1)
        if board[i][j].val == 0:
            board[i][j].val = -1
            n -= 1
            #print_board(board)

    # environment
    for i in range(d):
        for j in range(d):
            if board[i][j].val != -1:
                n = check_nearest(board, i, j)
                board[i][j].val = n
                print_board(board)

    return board

def print_board(board):
    print("printing board")
    for r in board:
        for s in r:
            if s.val == -1:
                print("M ", end='')
            else:
                print(str(s.val) + " ", end='')
        print()

def update_info(board, info, unvisited, stk, x, y):
    # updates info based on what's around it
    if board[x][y].val == info[x][y].visibleUnqueriedNeighbors:
        # all hidden spaces are mines
        try:
            if info[x][y + 1].isSafe == 0:
                info[x][y + 1].isSafe = -1
                unvisited.remove((x, y + 1))
        except IndexError:
            pass
        try:
            if info[x][y - 1].isSafe == 0:
                info[x][y - 1].isSafe = -1
                unvisited.remove((x, y - 1))
        except IndexError:
            pass
        try:
            if info[x - 1][y - 1].isSafe == 0:
                info[x - 1][y - 1].isSafe = -1
                unvisited.remove((x - 1, y - 1))
        except IndexError:
            pass
        try:
            if info[x - 1][y + 1].isSafe == 0:
                info[x - 1][y + 1].isSafe = -1
                unvisited.remove((x - 1, y + 1))
        except IndexError:
            pass
        try:
            if info[x - 1][y].isSafe == 0:
                info[x - 1][y].isSafe = -1
                unvisited.remove((x - 1, y))
        except IndexError:
            pass
        try:
            if info[x + 1][y - 1].isSafe == 0:
                info[x][y + 1].isSafe = -1
                unvisited.remove((x + 1, y - 1))
        except IndexError:
            pass
        try:
            if info[x + 1][y + 1].isSafe == 0:
                info[x + 1][y + 1].isSafe = -1
                unvisited.remove((x + 1, y + 1))
        except IndexError:
            pass
        try:
            if info[x + 1][y].isSafe == 0:
                info[x + 1][y].isSafe = -1
                unvisited.remove((x + 1, y))
        except IndexError:
            pass
    elif board[x][y].val + info[x][y].visibleUnqueriedNeighbors == 8:
        # all hidden spaces are safe
        try:
            if info[x][y + 1].isSafe == 0:
                info[x][y + 1].isSafe = 1
                stk.append((x, y + 1))
        except IndexError:
            pass
        try:
            if info[x][y - 1].isSafe == 0:
                info[x][y - 1].isSafe = 1
                stk.append((x, y - 1))
        except IndexError:
            pass
        try:
            if info[x - 1][y - 1].isSafe == 0:
                info[x - 1][y - 1].isSafe = 1
                stk.append((x - 1, y - 1))
        except IndexError:
            pass
        try:
            if info[x - 1][y + 1].isSafe == 0:
                info[x - 1][y + 1].isSafe = 1
                stk.append((x - 1, y + 1))
        except IndexError:
            pass
        try:
            if info[x - 1][y].isSafe == 0:
                info[x - 1][y].isSafe = 1
                stk.append((x - 1, y))
        except IndexError:
            pass
        try:
            if info[x + 1][y - 1].isSafe == 0:
                info[x + 1][y - 1].isSafe = 1
                stk.append((x + 1, y - 1))
        except IndexError:
            pass
        try:
            if info[x + 1][y + 1].isSafe == 0:
                info[x + 1][y + 1].isSafe = 1
                stk.append((x + 1, y + 1))
        except IndexError:
            pass
        try:
            if info[x + 1][y].isSafe == 0:
                info[x + 1][y].isSafe = 1
                stk.append((x + 1, y))
        except IndexError:
            pass
def basic_agent(board):
    counter = 0
    info = []
    for i in range(len(board)):
        r = []
        for j in range(len(board)):
            sq = SpaceQuery(0, 0, 0, 0, 8)
            r.append(sq)
        info.append(r)

    # list of positions that are definitely known
    safe = []
    mines = []
    unvisited = []
    stk = []

    # populate unvisited
    for i in range(len(board)):
        for j in range(len(board)):
            unvisited.append((i, j))

    while len(unvisited) > 0:
        # v is a random unvisited space
        while True:
            v = random.randint(0, len(unvisited) - 1)
            # make sure that the random hidden space isn't known to be a mine
            if info[x][y].isSafe != -1:
                break
        x = v[0]
        y = v[1]
        # stk will contain all safe, unvisited searches
        while True:
            unvisited.remove(x, y)
            if board[x][y].val == -1:
                # oops, mine exploded
                counter += 1
                info[x][y].isSafe = -1
                mines.append((x, y))
            else:
                # okay, no mine here
                info[x][y].isSafe = 1
                safe.append((x, y))

                # will update spaces around
                update_info(board, info, unvisited, stk, x, y)
            if len(stk) > 0:
                p = stk.pop()
                x = p[0]
                y = p[1]
            else:
                break






d = 5
n = 10
print_board(board_gen(d, n))