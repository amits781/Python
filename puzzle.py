import random
from copy import deepcopy
from os import system, name
from time import sleep 


# for clearing the screen
def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

# for printing animated loading progress
def loading_message(message_to_print):
    for i in range (5):
        clear() 
        print(message_to_print + "."*(i+1))
        sleep(0.5) 
    clear()


# printing rules of the game
def print_rules():
    print("Here are the rules for the game:")
    print("\tYou'll need to select a level, easy gives you 3x3 board and hard gives you 4x4 board")
    print("\tYour goal is to arrange the jumbled up numbers in the order shown in the board before shuffling")
    print("\tFor moving the blank space you will use the keys W/S/A/D that represents up/down/left/right motion respectively")
    print("\tTry to keep your moves minimum to score high")
    input("Press enter to continue")
    clear()

# creates a new board in order of given size
def render_board (size):
    loading_message("Loading Board")
    my_new_board = []
    for num in range(0,size):
        my_new_sub_list = []
        for number in range(1,size + 1):
            if num == size - 1 and number == size:
                my_new_sub_list.append('     ')
                continue
            my_new_sub_list.append(format(num * size + number," ^5,d"))
        my_new_board.append(my_new_sub_list)
    return my_new_board


# to find the inversion count
# used for determining if puzzle is solvable
def find_inversion_count(elements_array):
    count = 0
    for i in range (len(elements_array)-1):
        for j in range (i+1,len(elements_array)):
            if elements_array[i] != '     ' and elements_array[j] != '     ' and elements_array[i] > elements_array[j]:
                count += 1
    
    return count

# creates a new shuffled board
# ensures that the puzzle is solvable
def shuffle_board(board):
    loading_message("Shuffling")
    all_elements = []
    shuffled_board = []
    board_is_solvable = False
    for row in board:
        for item in row:
            all_elements.append(item)

    while board_is_solvable == False:
        random.shuffle(all_elements)
        inversion_count = find_inversion_count(all_elements)
        space_index = all_elements.index('     ')
        space_row =len(board) - (( space_index // len(board) ) + 1) +1
        if len(board)%2 != 0 and inversion_count%2 == 0:
            board_is_solvable = True
        elif len(board)%2 == 0 and inversion_count%2 == 0 and space_row%2 != 0:
            board_is_solvable = True
        elif len(board)%2 == 0 and inversion_count%2 != 0 and space_row%2 == 0:
            board_is_solvable = True

    for i in range(len(board)):
        inner_list = []
        for j in range(len(board)):
            inner_list.append(all_elements[i*len(board)+j])
        shuffled_board.append(inner_list)

    return shuffled_board

# returns the index of space
def find_space(board):
    blank_index = {'row_index': -1, 'col_index': -1}
    flag = False
    for i, row in enumerate(board):
        for index, num in enumerate(row):
            if num == '     ':
                blank_index['row_index'] = i
                blank_index['col_index'] = index
                flag = True
                break
        if flag:
            break
    return int(blank_index['row_index']),int(blank_index['col_index'])


# prints the board
def print_board(board):
    for row in board:
        print(row)

# checks for valid move and implements it on board
def cal_move(move , old_space_pos, board):
    clear()
    v_pos , h_pos = old_space_pos
    invalid_move = False
    if move == "s":
        new_space_pos = (v_pos+1 , h_pos)
    elif move == "w":
        new_space_pos = (v_pos -1, h_pos)
    elif move == "d":
        new_space_pos = (v_pos, h_pos+1)
    elif move == "a":
        new_space_pos = (v_pos, h_pos-1)
    else:
        new_space_pos = (v_pos, h_pos)
        invalid_move = True

    new_v_pos , new_h_pos = new_space_pos

    if new_h_pos < 0 or new_v_pos < 0 or new_h_pos >= len(board) or new_v_pos >= len(board) or invalid_move:
        print("Invalid Move!! Please try again...")
        invalid_move = False
        return old_space_pos

    board[v_pos][h_pos] , board[new_v_pos][new_h_pos] = board[new_v_pos][new_h_pos] , board[v_pos][h_pos]
    return new_space_pos

# game starts here
clear()
print("Welcome to puzzle game")
print_rules()
print("Choose your level: Easy or Hard")
level = input()
level = level.lower()
if level == "easy":
    size = 3
elif level == "hard":
    size = 4
values = render_board(size)
print("Your board is below:")
print_board(values)
input("Press enter to continue")
new_board = deepcopy(values)
new_board = shuffle_board(new_board)
counter_steps = 0
print("Total number of steps: {0}".format(counter_steps))
print_board(new_board)
x,y = find_space(new_board)
space_pos = (x,y)

while True:
    move = input("Enter Move: ")
    move = move.lower()
    if move == "q" or move == "quit":
        break
    new_space_pos = cal_move(move, space_pos, new_board)
    if new_space_pos != space_pos:
        counter_steps +=1
    space_pos = new_space_pos
    print("Total number of steps: {0}".format(counter_steps))
    print_board(new_board)
    if new_board == values:
        print("Puzzle Completed!!")
        print("Number of steps {0}".format(counter_steps))
        break
    

    