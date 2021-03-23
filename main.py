import copy
import random
import matplotlib.pyplot as plt
class Query:
    def __init__(self, isSafe, surroundingMines, neighbor_safe, neighbor_mine, neighbor_unqueried):
            self.isSafe = isSafe
            self.surroundingMines = surroundingMines
            self.neighbor_safe = neighbor_safe
            self.neighbor_mine = neighbor_mine
            self.neighbor_unqueried = neighbor_unqueried

class ImprovedQuery:
    def __init__(self, isSafe, qunq, remaining_mines):
        # isSafe is the same, decides whether safe, mine, or unknown
        self.isSafe = isSafe
        # qunq is a list of all the unqueried neighbors
        self.qunq = qunq
        # remaining_mines is the number of all the remaining mines (originally just board.val)
        self.remaining_mines = remaining_mines


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
            query_cell_basic(board, info, c, safe, unvisited, tripped)

            print("tripped is " + str(tripped))
    print("final score is " + str(n - len(tripped)))
    print_board(board)
    print_info(info)
            
def query_cell_basic(board, info, coord, safe, unvisited, tripped):
    if coord in unvisited:
        unvisited.remove(coord)
        print(str(coord) + " removed from unvisited")
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
    update_cell_info_basic(board, info, safe, unvisited, x, y)
    #check_nearest(board, info, safe, unvisited, x, y, update_cell_info_basic)
# resets the information for a cell and checks all its neighbors once more to update the information
# returns the unqueried spaces next to it that are known to be safe
def update_cell_info_basic(board, info, safe, unvisited, x, y):
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

def improved_agent(board, n):
    # initialize info
    info = []
    for i in range(len(board)):
        r = []
        info.append(r)
        for j in range(len(board)):
            #print(str(i) + " and " + str(j))
            r.append(ImprovedQuery(0, [], 0))
            try:
                info[i][j].qunq.append((i, j + 1))
            except IndexError:
                pass
            try:
                if j != 0:
                    info[i][j].qunq.append((i, j - 1))
            except IndexError:
                pass
            try:
                if i != 0 and j != 0:
                    info[i][j].qunq.append((i - 1, j - 1))
            except IndexError:
                pass
            try:
                if i != 0:
                    info[i][j].qunq.append((i - 1, j + 1))
            except IndexError:
                pass
            try:
                if i != 0:
                    info[i][j].qunq.append((i - 1, j))
            except IndexError:
                pass
            try:
                if j != 0:
                    info[i][j].qunq.append((i + 1, j - 1))
            except IndexError:
                pass
            try:
                info[i][j].qunq.append((i + 1, j + 1))
            except IndexError:
                pass
            try:
                info[i][j].qunq.append((i + 1, j))
            except IndexError:
                pass
            #print(info[i][j].qunq)

    # list of tripped mines
    tripped = []
    
    # initialize list of unvisited spaces
    unvisited = []
    for i in range(len(info)):
        for j in range(len(info)):
            unvisited.append((i, j))

    while len(unvisited) > 0:
        # randomly pick a coordinate and recurse it
        while True:
            coord = unvisited[random.randint(0, len(unvisited) - 1)]
            if info[coord[0]][coord[1]].isSafe == 0:
                break
        print("randomly picked " + str(coord))
        query_cell(board, info, coord, unvisited, tripped)
    print("tripped: " + str(tripped))


def query_cell(board, info, coord, unvisited, tripped):
    x = coord[0]
    y = coord[1]
    if board[x][y] == -1:
        print("mine randomly hit!")
        tripped.append(coord)
        info[x][y].isSafe = -1
    else:
        print("safe randomly hit!")
        info[x][y].isSafe = 1
        #info[x][y].remaining_mines += board[x][y]
    update_cell_info(board, info, unvisited, coord)

# full info refresh based on the new information in coord
def update_cell_info_old(board, info, border, coord):
    print("updating info")
    border = border_gen(info)
    print_border(info, border)
    print_info_improved(info)
    q = info[coord[0]][coord[1]]
    toVisit = []
    # val is a conversion of isSafe into a number relevant for the equation i.e. 1 -> 0 and -1 -> 1
    val = 0
    if q.isSafe == -1:
        val = 1
    for v in border:
        cell = info[v[0]][v[1]]
        cunq = cell.qunq
        print("cell qunq is " + str(cunq))

        # if the cell in question borders q, then remove q from its qunq
        # also update the corresponding remaining mines if q is a mine
        if coord in cunq:
            cunq.remove(coord)
            cell.remaining_mines -= val
        # all are safe
        if cell.remaining_mines <= 0:
            print("all are safe!")
            for c in cunq:
                info[c[0]][c[1]].isSafe = 1
                info[c[0]][c[1]].remaining_mines += board[c[0]][c[1]]
                toVisit.append(c)
        # all are mines
        if cell.remaining_mines == len(cunq):
            for c in cunq:
                info[c[0]][c[1]].isSafe = -1
                toVisit.append(c)
    for t in toVisit:
        update_cell_info_old(board, info, border, t)
def print_info_improved(info):
    for i in info:
        for j in i:
            if j.isSafe == -1:
                print("M ", end="")
            elif j.isSafe == 0:
                print(". ", end="")
            else:
                print(str(j.remaining_mines) + " ", end="")
        print()
def border_gen(info):
    border = []
    for i in range(len(info)):
        for j in range(len(info)):
            if len(info[i][j].qunq) > 0 and info[i][j].isSafe == 1:
                border.append((i, j))
    return border
def print_border(info, border):
    for i in range(len(info)):
        for j in range(len(info)):
            if tuple((i, j)) in border:
                print("B ", end="")
            else:
                print("X ", end="")
        print()
def update_cell_info(board, info, unvisited, coord):
    print("updating info")
    print_info_improved(info)
    x = coord[0]
    y = coord[1]
    # q is the known position already queried that we are basing this update around
    q = info[x][y]
    unvisited.remove(coord)
    if q.isSafe == 1:
        print("add on value")
        q.remaining_mines += board[x][y]
    # queue
    toVisit = []
    # now change every neighbor of q based on q's new value
    try:
        if y != 0:
            neighbor = info[x][y - 1]
            #print(neighbor.qunq)
            neighbor.qunq.remove(coord)
            if q.isSafe == -1:
                neighbor.remaining_mines -= 1
            if neighbor.remaining_mines == 0:
                neighbor.isSafe = 1
                toVisit.append((x, y - 1))
            elif neighbor.remaining_mines == len(neighbor.qunq):
                neighbor.isSafe = -1
                toVisit.append((x, y - 1))
    except IndexError:
        pass
    try:
        neighbor = info[x][y + 1]
        #print(neighbor.qunq)
        neighbor.qunq.remove(coord)
        if q.isSafe == -1:
            neighbor.remaining_mines -= 1
        if neighbor.remaining_mines == 0:
            neighbor.isSafe = 1
            toVisit.append((x, y + 1))
        elif neighbor.remaining_mines == len(neighbor.qunq):
            neighbor.isSafe = -1
            toVisit.append((x, y + 1))
    except IndexError:
        pass
    try:
        if x != 0 and y != 0:
            neighbor = info[x - 1][y - 1]
            neighbor.qunq.remove(coord)
            if q.isSafe == -1:
                neighbor.remaining_mines -= 1
            if neighbor.remaining_mines == 0:
                neighbor.isSafe = 1
                toVisit.append((x - 1, y - 1))
            elif neighbor.remaining_mines == len(neighbor.qunq):
                neighbor.isSafe = -1
                toVisit.append((x - 1, y - 1))
    except IndexError:
        pass
    try:
        if x != 0:
            neighbor = info[x - 1][y + 1]
            neighbor.qunq.remove(coord)
            if q.isSafe == -1:
                neighbor.remaining_mines -= 1
            if neighbor.remaining_mines == 0:
                neighbor.isSafe = 1
                toVisit.append((x - 1, y + 1))
            elif neighbor.remaining_mines == len(neighbor.qunq):
                neighbor.isSafe = -1
                toVisit.append((x - 1, y + 1))
    except IndexError:
        pass
    try:
        if x != 0:
            neighbor = info[x - 1][y]
            neighbor.qunq.remove(coord)
            if q.isSafe == -1:
                neighbor.remaining_mines -= 1
            if neighbor.remaining_mines == 0:
                neighbor.isSafe = 1
                toVisit.append((x - 1, y))
            elif neighbor.remaining_mines == len(neighbor.qunq):
                neighbor.isSafe = -1
                toVisit.append((x - 1, y))
    except IndexError:
        pass
    try:
        if y != 0:
            neighbor = info[x + 1][y - 1]
            neighbor.qunq.remove(coord)
            if q.isSafe == -1:
                neighbor.remaining_mines -= 1
            if neighbor.remaining_mines == 0:
                neighbor.isSafe = 1
                toVisit.append((x + 1, y - 1))
            elif neighbor.remaining_mines == len(neighbor.qunq):
                neighbor.isSafe = -1
                toVisit.append((x + 1, y - 1))
    except IndexError:
        pass
    try:
        neighbor = info[x + 1][y + 1]
        neighbor.qunq.remove(coord)
        if q.isSafe == -1:
            neighbor.remaining_mines -= 1
        if neighbor.remaining_mines == 0:
            neighbor.isSafe = 1
            toVisit.append(neighbor)
        elif neighbor.remaining_mines == len(neighbor.qunq):
            neighbor.isSafe = -1
            toVisit.append((x + 1, y + 1))
    except IndexError:
        pass
    try:
        neighbor = info[x + 1][y]
        neighbor.qunq.remove(coord)
        if q.isSafe == -1:
            neighbor.remaining_mines -= 1
        if neighbor.remaining_mines == 0:
            neighbor.isSafe = 1
            toVisit.append(neighbor)
        elif neighbor.remaining_mines == len(neighbor.qunq):
            neighbor.isSafe = -1
            toVisit.append((x + 1, y))
    except IndexError:
        pass

    for t in toVisit:
        update_cell_info(board, info, unvisited, t)

n = 2
board = board_gen(4, n)
print_board(board)
#basic_agent(board, n)
improved_agent(board, n)
