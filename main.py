import random
import matplotlib
class Query:
    def __init__(self, isSafe, surroundingMines, neighbor_safe, neighbor_mine, neighbor_unqueried):
            self.isSafe = isSafe
            self.surroundingMines = surroundingMines
            self.neighbor_safe = neighbor_safe
            self.neighbor_mine = neighbor_mine
            self.neighbor_unqueried = neighbor_unqueried

# board_gen generates a list of list of integers
# integer is -1 for mine, else the number of surrounding mines
# dim is the dimension of the board
# n is the number of mines
def board_gen(dim, n):
    # populate board with 0s
    board = []
    for i in range(dim):
        r = []
        for j in range(dim):
            r.append(0)
        board.append(r)

    # populate board with mines
    while n > 0:
        i = random.randint(0, dim - 1)
        j = random.randint(0, dim - 1)
        if board[i][j] == 0:
            board[i][j] = -1
            n -= 1

    # populate rest of board with numbers
    for i in range(dim):
        for j in range(dim):
            if board[i][j] != -1:
                n = check_nearest_inc(board, i, j)
                board[i][j] = n
                #print_board(board)

    return board

def print_board(board):
    print("printing board")
    for r in board:
        for s in r:
            if s == -1:
                print("M ", end='')
            else:
                print(str(s) + " ", end='')
        print()
def check_nearest_inc(board, x, y):
    n = 0
    try:
        if board[x][y + 1] == -1:
            #print("mine at right")
            n += 1
    except IndexError:
        pass
    try:
        if y != 0 and board[x][y - 1] == -1:
            #print("mine at left")
            n += 1
    except IndexError:
        pass
    try:
        if x != 0 and y != 0 and board[x - 1][y - 1] == -1:
            #print("mine at top left")
            n += 1
    except IndexError:
        pass
    try:
        if x != 0 and board[x - 1][y + 1] == -1:
            #print("mine at top right")
            n += 1
    except IndexError:
        pass
    try:
        if x != 0 and board[x - 1][y] == -1:
            #print("mine at top")
            n += 1
    except IndexError:
        pass
    try:
        if y != 0 and board[x + 1][y - 1] == -1:
            #print("mine at bottom left")
            n += 1
    except IndexError:
        pass
    try:
        if board[x + 1][y + 1] == -1:
            #print("mine at bottom right")
            n += 1
    except IndexError:
        pass
    try:
        if board[x + 1][y] == -1:
            #print("mine at bottom")
            n += 1
    except IndexError:
        pass
    return n
def check_nearest(board, info, safe, unvisited,  x, y, func):
    try:
        func(board, info, safe, unvisited,  x, y + 1)
    except IndexError:
        pass
    try:
        func(board, info, safe, unvisited,  x, y - 1)
    except IndexError:
        pass
    try:
        func(board, info, safe, unvisited,  x - 1, y + 1)
    except IndexError:
        pass
    try:
        func(board, info, safe, unvisited,  x - 1, y - 1)
    except IndexError:
        pass
    try:
        func(board, info, safe, unvisited,  x - 1, y)
    except IndexError:
        pass
    try:
        func(board, info, safe, unvisited,  x + 1, y + 1)
    except IndexError:
        pass
    try:
        func(board, info, safe, unvisited,  x + 1, y - 1)
    except IndexError:
        pass
    try:
        func(board, info, safe, unvisited,  x + 1, y)
    except IndexError:
        pass
def neighborsAreMines(board, info, safe, x, y):
    if info[x][y].isSafe == 0:
        info[x][y].isSafe == -1
def neighborsAreSafe(board, info, safe, x, y):
    if info[x][y].isSafe == 0:
        info[x][y].isSafe == 1
        safe.append((x, y))
def print_info(info):
    print("printing info")
    for i in info:
        for j in i:
            if j.isSafe == 0:
                print(". ", end="")
            elif j.isSafe == -1:
                print("M ", end="")
            else:
                print(str(j.neighbor_mine) + " ", end="")
            # j is a Query
            # if status is unknown, print period
            # if is mine, print M
            # else print surrounding_mines
        print()
def basic_agent(board, n):
    # initialize info
    # info is a list of list of Query
    info = []
    for i in range(len(board)):
        r = []
        for j in range(len(board)):
            r.append(Query(0, 0, 0, 0, 8))
        info.append(r)
    print_info(info)

    # list of tripped mines
    tripped = []

    unvisited = []
    for i in range(len(board)):
        for j in range(len(board)):
            unvisited.append((i, j))

    visited = []

    # safe is the queue containing all coordinates known to be safe
    # if it becomes empty, it will be populated by a random space not known to be a mine
    safe = []
    print(unvisited)
    while len(unvisited) > 0:
        # randomly pick a coordinate and append to safe
        while True:
            coord = unvisited[random.randint(0, len(unvisited) - 1)]
            # if coord known to be a mine, reset the random coordinate
            if info[coord[0]][coord[1]].isSafe != -1:
                break
        print(str(coord) + " randomly chosen")
        safe.append(coord)
        #print(safe)
        while len(safe) > 0:
            print(safe)
            c = safe.pop()

            # query the cell
            query_cell_basic(board, info, c, safe, visited, unvisited, tripped)

            print("tripped is " + str(tripped))
    print("final score is " + str(n - len(tripped)))
    print_board(board)
    print_info(info)
            
def query_cell_basic(board, info, coord, safe, visited, unvisited, tripped):
    if coord in unvisited:
        unvisited.remove(coord)
        print(str(coord) + " removed from unvisited")
    visited.append(coord)
    x = coord[0]
    y = coord[1]
    if board[x][y] == -1:
        print("mine hit!")
        tripped.append(coord)
        info[x][y].isSafe = -1
    else:
        info[x][y].isSafe = 1
    print_info(info)
    # update cell info and append newly safe
    update_cell_info(board, info, safe, unvisited, x, y)
    #check_nearest(board, info, safe, unvisited, x, y, update_cell_info)
# resets the information for a cell and checks all its neighbors once more to update the information
# returns the unqueried spaces next to it that are known to be safe
def update_cell_info(board, info, safe, unvisited, x, y):
    if tuple((x, y)) in unvisited:
        return
    q = info[x][y]
    print("updating info on (" + str(x) + ", " + str(y) + ")")
    neighbors = 8
    if x == 0 or x == len(board) - 1:
        if y == 0 or y == len(board) - 1:
            neighbors = 3
        else:
            neighbors = 5
    elif y == 0 or y == len(board) - 1:
        if x == 0 or x == len(board) - 1:
            neighbors = 3
        else:
            neighbors = 5

    print("there are " + str(neighbors) + " neighbors")
    qunq = []

    q.neighbor_unqueried = 0
    q.neighbor_mine = 0
    q.neighbor_safe = 0

    # if neighbor is a mine/safe, increase number for q
    # if neighbor is unqueried, add to qunq list for possible safe append
    try:
        if y != 0:
            neighbor = info[x][y - 1]
            if neighbor.isSafe == -1:
                q.neighbor_mine += 1
            elif neighbor.isSafe == 1:
                q.neighbor_safe += 1
            else:
                q.neighbor_unqueried += 1
                qunq.append((x, y - 1))
    except IndexError:
        pass
    try:
        neighbor = info[x][y + 1]
        if neighbor.isSafe == -1:
            q.neighbor_mine += 1
        elif neighbor.isSafe == 1:
            q.neighbor_safe += 1
        else:
            q.neighbor_unqueried += 1
            qunq.append((x, y + 1))
    except IndexError:
        pass
    try:
        if x != 0 and y != 0:
            neighbor = info[x - 1][y - 1]
            if neighbor.isSafe == -1:
                q.neighbor_mine += 1
            elif neighbor.isSafe == 1:
                q.neighbor_safe += 1
            else:
                q.neighbor_unqueried += 1
                qunq.append((x - 1, y - 1))
    except IndexError:
        pass
    try:
        if x != 0:
            neighbor = info[x - 1][y + 1]
            if neighbor.isSafe == -1:
                q.neighbor_mine += 1
            elif neighbor.isSafe == 1:
                q.neighbor_safe += 1
            else:
                q.neighbor_unqueried += 1
                qunq.append((x - 1, y + 1))
    except IndexError:
        pass
    try:
        if x != 0:
            neighbor = info[x - 1][y]
            if neighbor.isSafe == -1:
                q.neighbor_mine += 1
            elif neighbor.isSafe == 1:
                q.neighbor_safe += 1
            else:
                q.neighbor_unqueried += 1
                qunq.append((x - 1, y))
    except IndexError:
        pass
    try:
        if y != 0:
            neighbor = info[x + 1][y - 1]
            if neighbor.isSafe == -1:
                q.neighbor_mine += 1
            elif neighbor.isSafe == 1:
                q.neighbor_safe += 1
            else:
                q.neighbor_unqueried += 1
                qunq.append((x + 1, y - 1))
    except IndexError:
        pass
    try:
        neighbor = info[x + 1][y + 1]
        if neighbor.isSafe == -1:
            q.neighbor_mine += 1
        elif neighbor.isSafe == 1:
            q.neighbor_safe += 1
        else:
            q.neighbor_unqueried += 1
            qunq.append((x + 1, y + 1))
    except IndexError:
        pass
    try:
        neighbor = info[x + 1][y]
        if neighbor.isSafe == -1:
            q.neighbor_mine += 1
        elif neighbor.isSafe == 1:
            q.neighbor_safe += 1
        else:
            q.neighbor_unqueried += 1
            qunq.append((x + 1, y))
    except IndexError:
        pass
    print("qunq is " + str(qunq))
    # change unqueried neighbors if you know for sure that they're all safe/mines
    # additionally, if unqueried are safe, append for search
    # and if unqueried are mines, remove from unvisited (as we don't want to search them)
    if q.neighbor_unqueried != 0 and q.neighbor_unqueried == board[x][y] - q.neighbor_mine:
        print("oops, all mines")
        for u in qunq:
            info[u[0]][u[1]].isSafe = -1
            if u in unvisited:
                unvisited.remove(u)
    elif q.neighbor_unqueried + q.neighbor_safe + board[x][y] == neighbors:
        print("yay, all safe")
        for u in qunq:
            info[u[0]][u[1]].isSafe = 1
            if u in unvisited:
                safe.append(u)
            #print("safe is now " + str(safe))
    print("after update, safe is " + str(safe))
    print_info(info)

n = 2
board = board_gen(4, n)
print_board(board)
basic_agent(board, n)
