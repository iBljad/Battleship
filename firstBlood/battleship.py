print(chr(27) + "[2J")


from random import randint

board = []

for x in range(5):
    board.append(["~"] * 5)


def print_board(brd):
    for row in brd:
        print(" ".join(row))

print("Let's play Battleship!")
print_board(board)


def random_row(brd):
    return randint(0, len(brd) - 1)


def random_col(brd):
    return randint(0, len(brd[0]) - 1)

ship_row = random_row(board)
ship_col = random_col(board)

# Everything from here on should go in your for loop!
# Be sure to indent four spaces!
for turn in range(4):
    print('Turn', turn + 1)
    guess_row = int(input("Guess Row: "))-1
    guess_col = int(input("Guess Col: "))-1

    if guess_row == ship_row and guess_col == ship_col:
        print("Congratulations! You sunk my battleship!")
        break
    else:
        if (guess_row < 0 or guess_row > 4) or (guess_col < 0 or guess_col > 4):
            print("Oops, that's not even in the ocean.")
        elif board[guess_row][guess_col] == "X":
            print("You guessed that one already.")
        else:
            print("You missed my battleship!")
            board[guess_row][guess_col] = "X"
            print_board(board)
        if turn == 3:
            print('Game Over, my ship was here:')
            board[ship_row][ship_col] = "S"
            print_board(board)



