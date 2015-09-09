from pprint import pprint
from random import randint, choice

print(chr(27) + "[2J")

fleet_dict = {1: 4,
              2: 3,
              3: 2,
              4: 1
              }

player_fleet_dict_for_ai = fleet_dict


class Board(object):
    def __init__(self, length):
        self.length = length
        self.board = []
        for i in range(length):
            self.board.append(["~ "] * length)

    def __repr__(self):
        field_y = self.length
        field_x = ' 0 '
        for i in self.board:
            print(str(field_y).rjust(2, ' '), ' '.join(i))
            field_y -= 1
        for xx in range(1, self.length + 1):
            field_x += (str(xx).ljust(3, ' '))
        print(field_x)
        print('\n')


battleBoard = Board(10)
board_length = len(battleBoard.board)


# Checking if point is allowed to place ship
def point_ok(board, xx, yy):
    ok = False
    for xxx in range(max(0, xx - 1), min(board_length, xx + 2)):
        for yyy in range(max(0, yy - 1), min(board_length, yy + 2)):
            if board.board[xxx][yyy] != "~ ":
                ok = False
                break
        else:
            ok = True
        if not ok:
            break
    return ok


def place_ship(board, size, number, player_fleet_in):
    # checking horizontal placing availability
    def point_hor_ok(check_board, check_x, check_y, check_size):
        cnt = 0
        for check_xx in range(check_x, min(board_length, check_x + check_size)):
            if check_board.board[check_y][check_xx] != "~ ":
                ok = False
                break
            else:
                cnt += 1
        else:
            if cnt == check_size:
                ok = True
            else:
                ok = False
        return ok

    # checking vertical placing availability
    def point_vert_ok(check_board, check_x, check_y, check_size):
        cnt = 0
        for check_yy in range(check_y, min(board_length, check_y + check_size)):
            if check_board.board[check_yy][check_x] != "~ ":
                ok = False
                break
            else:
                cnt += 1
        else:
            if cnt == check_size:
                ok = True
            else:
                ok = False
        return ok

    result = False
    result_board = Board(board_length)
    init_board = Board(board_length)
    for xx in range(board_length):
        for yy in range(board_length):
            if not point_ok(board, xx, yy):
                result_board.board[xx][yy] = 'X'
                init_board.board[xx][yy] = 'X'

    # building placing variants map
    for xx in range(board_length):
        for yy in range(board_length):
            if point_vert_ok(init_board, yy, xx, size) and point_hor_ok(init_board, yy, xx, size):
                result_board.board[xx][yy] = 'd'
            elif point_vert_ok(init_board, yy, xx, size):
                result_board.board[xx][yy] = 'v'
            elif point_hor_ok(init_board, yy, xx, size):
                result_board.board[xx][yy] = 'h'
            else:
                result_board.board[xx][yy] = 'xx'

    # check if there free cell in board
    for xx in range(board_length):
        for yy in range(board_length):
            if result_board.board[xx][yy] in 'dvh':
                result = True
                break
        if result:
            break
    else:
        result = False
        print('ERROR!!! Placing result: {}, ship: {} \n'.format(result, number))
    # log
    player_fleet_in[number]['coordinates'] = []

    def dict_fill(player_fleet_for_fill, ship_x, ship_y):
        player_fleet_for_fill[number]['coordinates'].append((ship_x, ship_y))

    # placing ship
    if result:
        in_progress = True
        while in_progress:
            rand_x = randint(0, board_length - 1)
            rand_y = randint(0, board_length - 1)
            if result_board.board[rand_x][rand_y] == 'v':
                for xx in range(rand_x, rand_x + size):
                    board.board[xx][rand_y] = str(number)
                    dict_fill(player_fleet_in, xx, rand_y)
                in_progress = False
            elif result_board.board[rand_x][rand_y] == 'h':
                for yy in range(rand_y, rand_y + size):
                    board.board[rand_x][yy] = str(number)
                    dict_fill(player_fleet_in, rand_x, yy)
                in_progress = False
            elif result_board.board[rand_x][rand_y] == 'd':
                if choice(['v', 'h']) == 'v':
                    for xx in range(rand_x, rand_x + size):
                        board.board[xx][rand_y] = str(number)
                        dict_fill(player_fleet_in, xx, rand_y)
                else:
                    for yy in range(rand_y, rand_y + size):
                        board.board[rand_x][yy] = str(number)
                        dict_fill(player_fleet_in, rand_x, yy)
                in_progress = False
                # print('Placing result: {}, x:y [{}:{}], ship: {} \n'.format(result, rand_x, rand_y, number))
    return result  # rand_x, rand_y, result_board.__repr__(), board.__repr__()


def board_init(board, fleet_dict_in, player_fleet_in):
    quit_init_flag = False
    try_cnt = 0
    while not quit_init_flag:
        battleBoard.__init__(10)
        for size in fleet_dict_in:
            for count in range(0, fleet_dict_in[size]):
                player_fleet_in[size * 10 + count + 1] = {}
                player_fleet_in[size * 10 + count + 1]['size'] = size
                # print('\nShip {} added to player_fleet_dict, success: {}'.format(size * 10 + count + 1, success))
                if not place_ship(board, int(size), size * 10 + count + 1, player_fleet_in):
                    print('Place ship returned False, not success for count loop')
                    success = False
                    break
            else:
                success = True
            if not success:
                break
        else:
            check_board_init(board, fleet_dict_in)
            quit_init_flag = True
        try_cnt += 1
        # print('Try_cnt: {}'.format(try_cnt))
        if try_cnt == 10:
            print('Fail to init battle board')
            break


# diagnostics
def check_board_init(board, fleet_dict_input):
    board_check_cnt = 0
    for xx in range(0, board_length):
        for yy in range(0, board_length):
            if board.board[xx][yy] == "~ ":
                board_check_cnt += 1
    fleet_sum = 0
    for key in fleet_dict_input:
        fleet_sum += (key * fleet_dict_input[key])
    if board_check_cnt == board_length ** 2 - fleet_sum:
        print('Init successful')
    else:
        print('Init failed')


# print X for sunken ship
def sunk_ship(fleet_name, ship_name, board_name):
    for xxx in fleet_name[ship_name]['coordinates']:
        board_name.board[xxx[0]][xxx[1]] = 'X '
        player_fleet_dict_for_ai[int(str(ship_name)[0])] -= 1


ai_board = Board(10)
player_board = Board(10)

ai_fleet = {'total': sum(fleet_dict.values())}
player_fleet = {'total': sum(fleet_dict.values())}

print(battleBoard.__repr__())
# print(ai_fleet)

quit_flag = False
is_players_turn = True

positive_answer = ['YES', 'YEP', 'YEAH', 'Y', '1']
negative_answer = ['NO', 'NOPE', 'NONE', 'N', '0']

ai_level = 0


def game_invitation():
    int_ai_level = 0
    internal_quit_flag = False
    while True:
        # answer = 'Y'
        answer = input('Would you like to play Battleship? (yes/no)\n').upper()
        if answer in negative_answer:
            print('Well, goodbye!')
            internal_quit_flag = True
            break
        elif answer in positive_answer:
            # refactor for try
            int_ai_level = int(input('Please choose difficulty level:\n'
                                     '1 - Normal\n'
                                     '2 - Hardcore'))
            print('Well, let\'s begin!')
            break
        else:
            print('I don\'t understand you, let\'s try again:')
    return internal_quit_flag, int_ai_level


def check_shot(xx, yy):
    if is_players_turn:
        if ai_board.board[xx][yy] not in str(ai_fleet.keys().__str__()):
            if ai_board.board[xx][yy] in ['* ', 'm ', 'xx ']:
                print('Don\'t repeat')
            else:
                ai_board.board[xx][yy] = 'm '
                battleBoard.board[xx][yy] = 'm '
                print('You missed')
        else:
            ai_fleet[int(ai_board.board[xx][yy])]['size'] -= 1
            if ai_fleet[int(ai_board.board[xx][yy])]['size'] == 0:
                ai_fleet['total'] -= 1
                print('Oh no! you sank myy ship!')
                sunk_ship(ai_fleet, int(ai_board.board[xx][yy]), battleBoard)
                ai_board.board[xx][yy] = 'xx '
                # battleBoard.board[xx][yy] = 'xx '
            else:
                print('You\'ve got me')
                ai_board.board[xx][yy] = '* '
                battleBoard.board[xx][yy] = '* '


def get_shot_coordinates():
    if is_players_turn:
        while True:
            try:
                # converting human coordinates to alien logic system
                xx = abs(board_length - int(input('Type x: ')))
                yy = int(input('Type y: ')) - 1
                if (xx not in range(0, board_length)) or (yy not in range(0, board_length)):
                    raise BaseException
                break
            except ValueError:
                print('Please type correct coordinates')
            except BaseException:
                print('Oops, that\'s not even in the ocean')
                # check hit/missed
    else:
        # call to ai logic
        pass
    return xx, yy


# game cycle
while not quit_flag:
    quit_flag, ai_level = game_invitation()
    if quit_flag:
        break

    # init boards
    ai_board.__init__(10)
    player_board.__init__(10)
    board_init(ai_board, fleet_dict, ai_fleet)
    board_init(player_board, fleet_dict, player_fleet)

    # debug only
    print(ai_board.__repr__())
    pprint(ai_fleet, width=95)
    print(battleBoard.__repr__())
    print(player_fleet)
    round_quit_flag = False

    while not round_quit_flag:
        while ai_fleet['total'] * player_fleet['total'] != 0:
            print('Entered game loop')

            # getting shot coordinates
            x, y = get_shot_coordinates()

            # checking result of shot and switching turn if needed
            is_players_turn = check_shot(x, y)

            battleBoard.__repr__()
            if ai_fleet['total'] == 0:
                print('Congratulations! You won!')
                round_quit_flag = True
                break
            elif player_fleet['total'] == 0:
                print('Bad news: I won')
                round_quit_flag = True
                break
        if round_quit_flag:
            break
