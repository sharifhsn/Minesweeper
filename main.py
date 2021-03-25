import random


# Query is the object is used for basic_agent's knowledge base
class Query:
    def __init__(self, isSafe, neighbor_safe, neighbor_mine, neighbor_unqueried):
        # isSafe is an integer that is 0 if unqueried, 1 if safe, and -1 if mine
        self.isSafe = isSafe
        # neighbor_safe is the number of neighbors known to be safe
        self.neighbor_safe = neighbor_safe
        # neighbor_mine is the number of neighbors known to be mines
        self.neighbor_mine = neighbor_mine
        # neighbor_unqueried is the number of neighbors that are unknown
        self.neighbor_unqueried = neighbor_unqueried


# ImprovedQuery is the object is used for improved_agent's knowledge base
class ImprovedQuery:
    def __init__(self, isSafe, unq, remaining_mines):
        # isSafe is implemented the same
        self.isSafe = isSafe
        # unq is a list of neighbors that are unqueried
        self.unq = unq
        # remaining_mines is the number of neighboring mines that have not been identified
        self.remaining_mines = remaining_mines

    def eq_gen(self):
        return tuple((self.unq, self.remaining_mines))


# board_gen generates a board for both basic_agent and improved_agent to use
# it is a list of list of integers
# if a cell is a mine, its value is -1
# otherwise, its value is the number of neighboring mines
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
                # print_board(board)

    return board


# check_nearest_inc counts the number of mines that neighbor a cell at (x, y)
def check_nearest_inc(board, x, y):
    n = 0
    if x != 0 and y != 0:
        if board[x - 1][y - 1] == -1:
            n += 1
    if x != 0:
        if board[x - 1][y] == -1:
            n += 1
    if x != 0 and y != len(board) - 1:
        if board[x - 1][y + 1] == -1:
            n += 1
    if y != 0:
        if board[x][y - 1] == -1:
            n += 1
    if y != len(board) - 1:
        if board[x][y + 1] == -1:
            n += 1
    if x != len(board) - 1 and y != 0:
        if board[x + 1][y - 1] == -1:
            n += 1
    if x != len(board) - 1:
        if board[x + 1][y] == -1:
            n += 1
    if x != len(board) - 1 and y != len(board) - 1:
        if board[x + 1][y + 1] == -1:
            n += 1
    return n


def basic_agent(board, n):
    if n == 0:
        return 1.0

    # initialize our knowledge base: info
    # info is a list of list of Query
    info = []
    for i in range(len(board)):
        r = []
        for j in range(len(board)):
            r.append(Query(0, 0, 0, 0, 8))
        info.append(r)

    # number of tripped mines
    tripped = 0

    # maintain list of unvisited cells stored as tuples (x, y)
    # initialized with every cell on the board
    unvisited = []
    for i in range(len(board)):
        for j in range(len(board)):
            unvisited.append((i, j))

    # safe is the queue containing all coordinates known to be safe
    # if it becomes empty, it will be populated by a random space not known to be a mine
    safe = []

    # the loop ends when all cells have been visited (either declared safe, flagged, or tripped mine)
    while len(unvisited) > 0:
        # randomly pick a coordinate and append to safe
        while True:
            coord = unvisited[random.randint(0, len(unvisited) - 1)]
            # if coord known to be a mine, reset the random coordinate
            if info[coord[0]][coord[1]].isSafe != -1:
                break

        # add coord to queue
        safe.append(coord)

        # loop until there are no more conclusively safe cells, then randomly pick
        while len(safe) > 0:

            # pop from safe and remove from unvisited
            c = safe.pop()
            if c in unvisited:
                unvisited.remove(c)

            x = c[0]
            y = c[1]
            if board[x][y] == -1:
                # if the cell is a mine, increment tripped and flag as a mine in info
                tripped += 1
                info[x][y].isSafe = -1
            else:
                # if the cell is safe, flag as safe in info
                info[x][y].isSafe = 1

            # now update our knowledge base
            update_cell_info_basic(board, info, safe, unvisited, x, y)

    # return the number of mines flagged divided by total mines
    return (n - tripped) / n


# updates the cell info
def update_cell_info_basic(board, info, safe, unvisited, x, y):
    if tuple((x, y)) in unvisited:
        return

    # q is the Query we are concerned with
    q = info[x][y]

    # handles neighbors in case of a side or corner cell
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

    # unq is a list of unqueried neighbors
    unq = []

    # reset each cell
    q.neighbor_unqueried = 0
    q.neighbor_mine = 0
    q.neighbor_safe = 0

    # fill them back up with fresh information
    if y != 0:
        neighbor = info[x][y - 1]
        if neighbor.isSafe == -1:
            q.neighbor_mine += 1
        elif neighbor.isSafe == 1:
            q.neighbor_safe += 1
        else:
            q.neighbor_unqueried += 1
            unq.append((x, y - 1))
    if y != len(board) - 1:
        neighbor = info[x][y + 1]
        if neighbor.isSafe == -1:
            q.neighbor_mine += 1
        elif neighbor.isSafe == 1:
            q.neighbor_safe += 1
        else:
            q.neighbor_unqueried += 1
            unq.append((x, y + 1))

    if x != 0 and y != 0:
        neighbor = info[x - 1][y - 1]
        if neighbor.isSafe == -1:
            q.neighbor_mine += 1
        elif neighbor.isSafe == 1:
            q.neighbor_safe += 1
        else:
            q.neighbor_unqueried += 1
            unq.append((x - 1, y - 1))

    if x != 0 and y != len(board) - 1:
        neighbor = info[x - 1][y + 1]
        if neighbor.isSafe == -1:
            q.neighbor_mine += 1
        elif neighbor.isSafe == 1:
            q.neighbor_safe += 1
        else:
            q.neighbor_unqueried += 1
            unq.append((x - 1, y + 1))

    if x != 0:
        neighbor = info[x - 1][y]
        if neighbor.isSafe == -1:
            q.neighbor_mine += 1
        elif neighbor.isSafe == 1:
            q.neighbor_safe += 1
        else:
            q.neighbor_unqueried += 1
            unq.append((x - 1, y))

    if x != len(board) - 1 and y != 0:
        neighbor = info[x + 1][y - 1]
        if neighbor.isSafe == -1:
            q.neighbor_mine += 1
        elif neighbor.isSafe == 1:
            q.neighbor_safe += 1
        else:
            q.neighbor_unqueried += 1
            unq.append((x + 1, y - 1))
    if x != len(board) - 1 and y != len(board) - 1:
        neighbor = info[x + 1][y + 1]
        if neighbor.isSafe == -1:
            q.neighbor_mine += 1
        elif neighbor.isSafe == 1:
            q.neighbor_safe += 1
        else:
            q.neighbor_unqueried += 1
            unq.append((x + 1, y + 1))
    if x != len(board) - 1:
        neighbor = info[x + 1][y]
        if neighbor.isSafe == -1:
            q.neighbor_mine += 1
        elif neighbor.isSafe == 1:
            q.neighbor_safe += 1
        else:
            q.neighbor_unqueried += 1
            unq.append((x + 1, y))

    if q.neighbor_unqueried != 0 and q.neighbor_unqueried == board[x][y] - q.neighbor_mine:
        # if all neighbors are definitely safe
        for u in unq:
            info[u[0]][u[1]].isSafe = -1
            if u in unvisited:
                unvisited.remove(u)
    elif q.neighbor_unqueried + q.neighbor_safe + board[x][y] == neighbors:
        # if all neighbors are definitely mines
        for u in unq:
            info[u[0]][u[1]].isSafe = 1
            if u in unvisited:
                safe.append(u)


def improved_agent(board, n):
    if n == 0:
        return 1.0

    # initialize info and populate unq for each cell
    info = []
    for i in range(len(board)):
        r = []
        info.append(r)
        for j in range(len(board)):
            r.append(ImprovedQuery(0, [], 0))
            if j != len(board) - 1:
                info[i][j].unq.append((i, j + 1))
            if j != 0:
                info[i][j].unq.append((i, j - 1))
            if i != 0 and j != 0:
                info[i][j].unq.append((i - 1, j - 1))
            if i != 0 and j != len(board) - 1:
                info[i][j].unq.append((i - 1, j + 1))
            if i != 0:
                info[i][j].unq.append((i - 1, j))
            if j != 0 and i != len(board) - 1:
                info[i][j].unq.append((i + 1, j - 1))
            if i != len(board) - 1 and j != len(board) - 1:
                info[i][j].unq.append((i + 1, j + 1))
            if i != len(board) - 1:
                info[i][j].unq.append((i + 1, j))

    # number of tripped mines
    tripped = 0

    # maintain list of unvisited cells stored as tuples (x, y)
    # initialized with every cell on the board
    unvisited = []
    for i in range(len(info)):
        for j in range(len(info)):
            unvisited.append((i, j))

    while len(unvisited) > 0:
        # randomly pick an unvisited coordinate
        coord = unvisited[random.randint(0, len(unvisited) - 1)]
        unvisited.remove(coord)
        x = coord[0]
        y = coord[1]
        if board[x][y] == -1:
            tripped += 1
            info[x][y].isSafe = -1
            # decrement the remaining_mines of cells surrounding the identified mine
            dec_r_m(info, x, y)
        else:
            info[x][y].isSafe = 1
            # increase the remaining_mines of the safe cell by the actual value on the board
            info[x][y].remaining_mines += board[x][y]

        # remove the found cell from all unqueried lists
        remove_q(info, coord)

        # update cell information
        update_cell_info(board, info, unvisited, coord)

    return (n - tripped) / n


def update_cell_info(board, info, unvisited, coord):
    # generate a border every iteration
    border = border_gen(info)
    if len(border) == 0:
        return

    # equations is the system of equations corresponding to the knowledge base
    equations = get_list(info, border)

    # run the solvers
    # if they change any information, update cell info once again
    if basic_solver(board, info, equations):
        update_cell_info(board, info, unvisited, coord)
    border = border_gen(info)
    equations = get_list(info, border)
    if systems_solver(board, info, equations):
        update_cell_info(board, info, unvisited, coord)

    # once all solvers are finished, refresh unvisited
    check_unvisited(info, unvisited)


# returns a list of all cells that are both safe and have at least one unqueried neighbor
def border_gen(info):
    border = []
    for i in range(len(info)):
        for j in range(len(info)):
            q = info[i][j]
            if q.isSafe == 1 and len(q.unq) > 0:
                border.append(tuple((i, j)))
    return border


# returns a system of equations (list), with each equation corresponding to a cell in the border
def get_list(info, border):
    equations = []
    for b in border:
        equations.append(info[b[0]][b[1]].eq_gen())
    return equations


# conclusively decides whether cells are safe or mines based on the same algorithm as basic
def basic_solver(board, info, equations):
    # keeps track of whether a change has occurred or not
    change = False
    # for every equation in the system
    for e in equations:
        unq = e[0]
        r_m = e[1]
        if r_m == 0:
            # if there are no mines, all are safe
            change = True
            l = len(unq)
            for i in range(l):
                u = unq[0]
                v = info[u[0]][u[1]]
                v.isSafe = 1
                v.remaining_mines += board[u[0]][u[1]]
                remove_q(info, tuple((u[0], u[1])))
                i -= 1
        elif len(unq) == r_m:
            # if every unqueried neighbor is a mine
            change = True
            l = len(unq)
            for i in range(l):
                u = unq[0]
                v = info[u[0]][u[1]]
                v.isSafe = -1
                dec_r_m(info, u[0], u[1])
                remove_q(info, tuple((u[0], u[1])))
                i -= 1
    return change


# if basic_solver fails to change anything, solve for each possible dual system
def systems_solver(board, info, equations):
    for i in range(len(equations)):
        for j in range(len(equations)):
            e = equations[i]
            f = equations[j]

            # if e is a subset of f, it can be removed
            if len(e[0]) != 0 and set(e[0]).issubset(set(f[0])) and sorted(e[0]) != sorted(f[0]):
                # remove all elements from f that are in e
                unq = [x for x in f[0] if x not in e[0]]

                # subtract the remaining_mines of e from f
                r_m = f[1] - e[1]
                equations[j] = tuple((unq, r_m))

    # run basic_solver again to see if the simplification has created a solution
    return basic_solver(board, info, equations)


# refresh unvisited
def check_unvisited(info, unvisited):
    for i in range(len(info)):
        for j in range(len(info)):
            if info[i][j].isSafe != 0 and tuple((i, j)) in unvisited:
                unvisited.remove(tuple((i, j)))
    return unvisited


# remove a cell from every unqueried list
def remove_q(info, coord):
    for i in range(len(info)):
        for j in range(len(info)):
            q = info[i][j]
            if coord in q.unq:
                q.unq.remove(coord)


# decrement the remaining_mines of all neighbors of the specified cell
def dec_r_m(info, x, y):
    if y != len(info) - 1:
        info[x][y + 1].remaining_mines -= 1
    if y != 0:
        info[x][y - 1].remaining_mines -= 1
    if y != len(info) - 1 and x != 0:
        info[x - 1][y + 1].remaining_mines -= 1
    if y != 0 and x != 0:
        info[x - 1][y - 1].remaining_mines -= 1
    if x != 0:
        info[x - 1][y].remaining_mines -= 1
    if y != len(info) - 1 and x != len(info) - 1:
        info[x + 1][y + 1].remaining_mines -= 1
    if y != 0 and x != len(info) - 1:
        info[x + 1][y - 1].remaining_mines -= 1
    if x != len(info) - 1:
        info[x + 1][y].remaining_mines -= 1
