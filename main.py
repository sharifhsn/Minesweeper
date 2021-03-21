# import random
#
# # space object
# class Space:
#     def __init__(self, val):
#         self = val
#
# # info object
# class SpaceQuery:
#     def __init__(self, isSafe, surroundingMines, neighbor_safe, neighbor_mine, neighbor_unqueried):
#         self.isSafe = isSafe
#         self.surroundingMines = surroundingMines
#         self.neighbor_safe = neighbor_safe
#         self.neighbor_mine = neighbor_mine
#         self.neighbor_unqueried = neighbor_unqueried
#
# # check_nearest finds how many mines are next to a specified position on the board
# # board is a list of list of spaces
# # x is the row we are searching
# # y is the column we are searching
# def check_nearest(board, x, y):
#     n = 0
#     try:
#         if board[x][y + 1] == -1:
#             n += 1
#     except IndexError:
#         pass
#     try:
#         if board[x][y - 1] == -1:
#             n += 1
#     except IndexError:
#         pass
#     try:
#         if board[x - 1][y - 1] == -1:
#             n += 1
#     except IndexError:
#         pass
#     try:
#         if board[x - 1][y + 1] == -1:
#             n += 1
#     except IndexError:
#         pass
#     try:
#         if board[x - 1][y] == -1:
#             n += 1
#     except IndexError:
#         pass
#     try:
#         if board[x + 1][y - 1] == -1:
#             n += 1
#     except IndexError:
#         pass
#     try:
#         if board[x + 1][y + 1] == -1:
#             n += 1
#     except IndexError:
#         pass
#     try:
#         if board[x + 1][y] == -1:
#             n += 1
#     except IndexError:
#         pass
#     return n
# def board_gen(d, n):
#     # simple generation of all 0s
#     board = []
#     for i in range(d):
#         r = []
#         for j in range(d):
#             s = Space(False, 0)
#             r.append(s)
#         board.append(r)
#
#     # add mines
#     while n > 0:
#         #print(n)
#         i = random.randint(0, d - 1)
#         j = random.randint(0, d - 1)
#         if board[i][j] == 0:
#             board[i][j] = -1
#             n -= 1
#             #print_board(board)
#
#     # environment
#     for i in range(d):
#         for j in range(d):
#             if board[i][j] != -1:
#                 n = check_nearest(board, i, j)
#                 board[i][j] = n
#                 print_board(board)
#
#     return board
#
# def print_board(board):
#     print("printing board")
#     for r in board:
#         for s in r:
#             if s == -1:
#                 print("M ", end='')
#             else:
#                 print(str(s) + " ", end='')
#         print()
#
# def update_info(board, info, unvisited, stk, x, y):
#     # updates info based on what's around it
#     if board[x][y] == info[x][y].neighbor_unqueried:
#         # all hidden spaces are mines
#         try:
#             if info[x][y + 1].isSafe == 0:
#                 info[x][y + 1].isSafe = -1
#                 unvisited.remove((x, y + 1))
#         except IndexError:
#             pass
#         try:
#             if info[x][y - 1].isSafe == 0:
#                 info[x][y - 1].isSafe = -1
#                 unvisited.remove((x, y - 1))
#         except IndexError:
#             pass
#         try:
#             if info[x - 1][y - 1].isSafe == 0:
#                 info[x - 1][y - 1].isSafe = -1
#                 unvisited.remove((x - 1, y - 1))
#         except IndexError:
#             pass
#         try:
#             if info[x - 1][y + 1].isSafe == 0:
#                 info[x - 1][y + 1].isSafe = -1
#                 unvisited.remove((x - 1, y + 1))
#         except IndexError:
#             pass
#         try:
#             if info[x - 1][y].isSafe == 0:
#                 info[x - 1][y].isSafe = -1
#                 unvisited.remove((x - 1, y))
#         except IndexError:
#             pass
#         try:
#             if info[x + 1][y - 1].isSafe == 0:
#                 info[x][y + 1].isSafe = -1
#                 unvisited.remove((x + 1, y - 1))
#         except IndexError:
#             pass
#         try:
#             if info[x + 1][y + 1].isSafe == 0:
#                 info[x + 1][y + 1].isSafe = -1
#                 unvisited.remove((x + 1, y + 1))
#         except IndexError:
#             pass
#         try:
#             if info[x + 1][y].isSafe == 0:
#                 info[x + 1][y].isSafe = -1
#                 unvisited.remove((x + 1, y))
#         except IndexError:
#             pass
#     elif board[x][y] + info[x][y].neighbor_unqueried == 8:
#         # all hidden spaces are safe
#         try:
#             if info[x][y + 1].isSafe == 0:
#                 info[x][y + 1].isSafe = 1
#                 stk.append((x, y + 1))
#         except IndexError:
#             pass
#         try:
#             if info[x][y - 1].isSafe == 0:
#                 info[x][y - 1].isSafe = 1
#                 stk.append((x, y - 1))
#         except IndexError:
#             pass
#         try:
#             if info[x - 1][y - 1].isSafe == 0:
#                 info[x - 1][y - 1].isSafe = 1
#                 stk.append((x - 1, y - 1))
#         except IndexError:
#             pass
#         try:
#             if info[x - 1][y + 1].isSafe == 0:
#                 info[x - 1][y + 1].isSafe = 1
#                 stk.append((x - 1, y + 1))
#         except IndexError:
#             pass
#         try:
#             if info[x - 1][y].isSafe == 0:
#                 info[x - 1][y].isSafe = 1
#                 stk.append((x - 1, y))
#         except IndexError:
#             pass
#         try:
#             if info[x + 1][y - 1].isSafe == 0:
#                 info[x + 1][y - 1].isSafe = 1
#                 stk.append((x + 1, y - 1))
#         except IndexError:
#             pass
#         try:
#             if info[x + 1][y + 1].isSafe == 0:
#                 info[x + 1][y + 1].isSafe = 1
#                 stk.append((x + 1, y + 1))
#         except IndexError:
#             pass
#         try:
#             if info[x + 1][y].isSafe == 0:
#                 info[x + 1][y].isSafe = 1
#                 stk.append((x + 1, y))
#         except IndexError:
#             pass
# def basic_agent(board):
#     counter = 0
#     info = []
#     for i in range(len(board)):
#         r = []
#         for j in range(len(board)):
#             sq = SpaceQuery(0, 0, 0, 0, 8)
#             r.append(sq)
#         info.append(r)
#
#     # list of positions that are definitely known
#     safe = []
#     mines = []
#     unvisited = []
#     stk = []
#
#     # populate unvisited
#     for i in range(len(board)):
#         for j in range(len(board)):
#             unvisited.append((i, j))
#
#     while len(unvisited) > 0:
#         # v is a random unvisited space
#         while True:
#             v = random.randint(0, len(unvisited) - 1)
#             # make sure that the random hidden space isn't known to be a mine
#             if info[x][y].isSafe != -1:
#                 break
#         x = v[0]
#         y = v[1]
#         # stk will contain all safe, unvisited searches
#         while True:
#             unvisited.remove(x, y)
#             if board[x][y] == -1:
#                 # oops, mine exploded
#                 counter += 1
#                 info[x][y].isSafe = -1
#                 mines.append((x, y))
#             else:
#                 # okay, no mine here
#                 info[x][y].isSafe = 1
#                 safe.append((x, y))
#
#                 # will update spaces around
#                 update_info(board, info, unvisited, stk, x, y)
#             if len(stk) > 0:
#                 p = stk.pop()
#                 x = p[0]
#                 y = p[1]
#             else:
#                 break
# def jav_basic_agent(board, minesWalkedInto, unvisited, visited, safe, unsafe):
#     info = []
#     for i in range(len(board)):
#         r = []
#         for j in range(len(board)):
#             sq = SpaceQuery(0, 0, 0, 0, 8)
#             r.append(sq)
#         info.append(r)
#
#     while len(unvisited) > 0:
#         int x = random.randInt(0, len(unvisited))
#         coord = unvisited[x]
#
# def queryCellBasic(board, info, unvisited, visited, coord):
#     if info[coord[0]][coord[1]].isSafe != 0:
#         return
#
#     unvisited.remove(coord)
#     visited.append(coord)
#
#     if board[coord[0]][coord[1]] == -1
#
#
#
# d = 5
# n = 10
# print_board(board_gen(d, n))





import random

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
def check_nearest(board, info, safe, x, y, func):
    try:
        func(board, info, safe, x, y + 1)
    except IndexError:
        pass
    try:
        func(board, info, safe, x, y - 1)
    except IndexError:
        pass
    try:
        func(board, info, safe, x - 1, y + 1)
    except IndexError:
        pass
    try:
        func(board, info, safe, x - 1, y - 1)
    except IndexError:
        pass
    try:
        func(board, info, safe, x - 1, y)
    except IndexError:
        pass
    try:
        func(board, info, safe, x + 1, y + 1)
    except IndexError:
        pass
    try:
        func(board, info, safe, x + 1, y - 1)
    except IndexError:
        pass
    try:
        func(board, info, safe, x + 1, y)
    except IndexError:
        pass
def neighborsAreMines(board, info, safe, x, y):
    if info[x][y].isSafe == 0:
        info[x][y].isSafe == -1
def neighborsAreSafe(board, info, safe, x, y):
    if info[x][y].isSafe == 0:
        info[x][y].isSafe == 1
        safe.append((x, y))

def basic_agent(board):
    # initialize info
    # info is a list of list of Query
    info = []
    for i in range(len(board)):
        r = []
        for j in range(len(board)):
            r.append(Query(0, 0, 0, 0, 8))
        info.append(r)
    print(info)

    # list of tripped mines
    tripped = []

    unvisited = []
    for i in range(len(board)):
        for j in range(len(board)):
            unvisited.append((i, j))

    visited = []
    safe = []
    print(unvisited)
    while len(unvisited) > 0:
        coord = unvisited[random.randint(0, len(unvisited) - 1)]
        safe.append(coord)
        print(safe)
        while len(safe) > 0:
            c = safe.pop()
            x = c[0]
            y = c[1]

            # query cell
            unvisited.remove(coord)
            visited.append(coord)
            if board[x][y] == -1:
                tripped.append(coord)
                info[x][y].isSafe = -1
            else:
                info[x][y].isSafe = 1

            # update cell info and append newly safe
            update_cell_info(board, info, safe, x, y)
            check_nearest(board, info, safe, x, y, update_cell_info)
            print(tripped)
            

# resets the information for a cell and checks all its neighbors once more to update the information
# returns the unqueried spaces next to it that are known to be safe
def update_cell_info(board, info, safe, x, y):
    q = info[x][y]
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
    qunq = []

    q.neighbor_unqueried = 0
    q.neighbor_mine = 0
    q.neighbor_safe = 0

    # if neighbor is a mine/safe, increase number for q
    # if neighbor is unqueried, add to qunq list for possible safe append
    try:
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
    
    # change unqueried neighbors if you know for sure that they're all safe/mines
    # additionally, if unqueried are safe, append for search
    if q.neighbor_unqueried == board[x][y]:
        for u in qunq:
            info[u[0]][u[1]].isSafe = -1
    elif q.neighbor_unqueried + q.neighbor_safe + board[x][y] == neighbors:
        for u in qunq:
            info[u[0]][u[1]].isSafe = 1
            safe.append(u)

board = board_gen(6, 4)
print_board(board)
basic_agent(board)


























