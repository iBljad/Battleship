from random import randint, choice

fleet_dict = {1: 4,
              2: 3,
              3: 2,
              4: 1,
              }


class Board(object):
    def __init__(self, length):
        self.board = []
        for i in range(length):
            self.board.append(['~'] * length)

    def __repr__(self):
        for i in self.board:
            print(' '.join(i))
        print('\n')


battleBoard = Board(10)

battleBoard.__repr__()


def point_ok(board, x, y):
    ok = False
    for xx in range(max(0, x - 1), min(len(board.board), x + 2)):
        for yy in range(max(0, y - 1), min(len(board.board), y + 2)):
            if board.board[xx][yy] != '~':
                ok = False
                break
        else:
            ok = True
        if not ok:
            break
    return ok


def point_hor_ok(board, x, y, size):
    ok = False
    cnt = 0
    for xx in range(x, min(len(board.board), x + size)):
        if board.board[y][xx] != '~':
            ok = False
            break
        else:
            cnt += 1
    else:
        if cnt == size:
            ok = True
        else:
            ok = False
    return ok


def point_vert_ok(board, x, y, size):
    ok = False
    cnt = 0
    for yy in range(y, min(len(board.board), y + size)):
        if board.board[yy][x] != '~':
            ok = False
            break
        else:
            cnt += 1
    else:
        if cnt == size:
            ok = True
        else:
            ok = False
    return ok


print()
battleBoard.board[8][8] = '2'
battleBoard.board[8][7] = '2'
battleBoard.__repr__()

print(point_ok(battleBoard, 0, 0))


def place_ship(board, size):
    result = False
    result_board = Board(len(board.board))
    init_board = Board(len(board.board))
    for x in range(len(board.board)):
        for y in range(len(board.board)):
            if not point_ok(board, x, y):
                result_board.board[x][y] = 'X'
                init_board.board[x][y] = 'X'

    # building placing variants map
    for x in range(len(init_board.board)):
        for y in range(len(init_board.board)):
            if point_vert_ok(init_board, y, x, size) and point_hor_ok(init_board, y, x, size):
                result_board.board[x][y] = 'd'
            elif point_vert_ok(init_board, y, x, size):
                result_board.board[x][y] = 'v'
            elif point_hor_ok(init_board, y, x, size):
                result_board.board[x][y] = 'h'
            else:
                result_board.board[x][y] = 'X'

    # check if there free cell in board
    for x in range(len(board.board)):
        for y in range(len(board.board)):
            if result_board.board[x][y] in 'dvh':
                result = True
                break
        if result:
            break
    else:
        result = False

    # placing ship
    if result:
        in_progress = True
        while in_progress:
            rand_x = randint(0, len(board.board) - 1)
            rand_y = randint(0, len(board.board) - 1)
            print(rand_x, rand_y, result_board.board[rand_x][rand_y])
            if result_board.board[rand_x][rand_y] == 'v':
                for xx in range(rand_x, rand_x + size):
                    board.board[xx][rand_y] = str(size)
                in_progress = False
            elif result_board.board[rand_x][rand_y] == 'h':
                for yy in range(rand_y, rand_y + size):
                    board.board[rand_x][yy] = str(size)
                in_progress = False
            elif result_board.board[rand_x][rand_y] == 'd':
                if choice(['v', 'h']) == 'v':
                    for xx in range(rand_x, rand_x + size):
                        board.board[xx][rand_y] = str(size)
                else:
                    for yy in range(rand_y, rand_y + size):
                        board.board[rand_x][yy] = str(size)
                in_progress = False

    return result  # rand_x, rand_y, result_board.__repr__(), board.__repr__()


"""for i in range(0,9):
    place_ship(battleBoard, 3)"""

# while place_ship(battleBoard, 9):
#     pass

quit_flag = False
success_cnt = 0
while quit_flag ^ (success_cnt <= 100):
    success = False
    battleBoard.__repr__()
    for size in fleet_dict:
        for count in range(0, fleet_dict[size]):
            if not place_ship(battleBoard, int(size)):
                break
        else:
            success = True
        if not success:
            break
    else:
        quit_flag = True
    success_cnt += 1
else:
    print('Fail to init battle board')


print(battleBoard.__repr__())
