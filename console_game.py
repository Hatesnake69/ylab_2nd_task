import random


def check_five(example_list: list) -> bool:
    """this function checks if where are any of 5 same elements in a row"""
    fst_elem = example_list[0]
    counter = 1
    for index in range(1, len(example_list)):
        if example_list[index] == fst_elem:
            counter += 1
            if counter == 5:
                return True
        else:
            counter = 1
            fst_elem = example_list[index]
    return False


class Draw(Exception):
    pass


class Win(Exception):
    pass


class Board:
    """this class is a field for playing tic-tac-toe"""
    def __init__(self, number):
        self.board = [[i for i in range(j, j + number)] for j in range(1, number ** 2, number)]

    def __str__(self):
        board_image = '-'*80 + '\n'
        for i_line in self.board:
            line = ''
            for j_elem in i_line:
                line += f'| {j_elem} | \t'
            line += '\n' + '-'*80 + '\n'
            board_image += line
        return board_image

    def mark_check(self, number: int) -> bool:
        """this method checks is it possible to add a mark in the cell of the board with required number"""
        for i_line in self.board:
            for j_elem in i_line:
                if number == j_elem:
                    return True
        return False

    def field_fillment_check(self) -> bool:
        """this method checks is where any empty cell left"""
        for i_line in self.board:
            for i_elem in i_line:
                if str(i_elem).isdigit():
                    return True
        return False

    def add_mark(self, player) -> None:
        """this method adds mark in the empty cell of the board"""
        print(self)
        while True:
            try:
                number = int(input(f'{player.name}, enter the number of a free cell in the board: '))
            except ValueError:
                number = None
                continue
            if self.mark_check(number):
                break
        for i_index, i_list in enumerate(self.board):
            for j_index, j_value in enumerate(i_list):
                if j_value == number:
                    self.board[i_index][j_index] = player.mark
                    print(self)

    def end_game_check(self):
        """this method checks whether the game is over"""
        for index, line in enumerate(self.board):
            if check_five(line):
                return True
            col = [self.board[i_index][index] for i_index, i_line in enumerate(self.board)]
            if check_five(col):
                return True
        diagonal1 = [self.board[index][index] for index, i_line in enumerate(self.board)]
        if check_five(diagonal1):
            return True
        diagonal2 = [self.board[len(self.board) - index - 1][index] for index, i_line in enumerate(self.board)]
        if check_five(diagonal2):
            return True
        return False

    @classmethod
    def choose_turn(cls, player1, player2) -> None:
        """this method sets turn order"""
        while True:
            choice = input(f'{player1.name}, do you want to be the first?(y/n): ')
            if choice in {'y', 'n'}:
                player1.turn = choice == 'y'
                player2.turn = not player1.turn
                player1.mark = 'X' if player1.turn else 'O'
                player2.mark = 'O' if player1.turn else 'X'
                break

    def turn(self, player1, player2) -> None:
        if player1.turn:
            self.add_mark(player1)
        else:
            self.computer_turn(player2)
        if not self.end_game_check():
            if self.field_fillment_check():
                player1.turn, player2.turn = not player1.turn, not player2.turn
            else:
                raise Draw
        else:
            raise Win

    def game(self, player1, player2):
        self.choose_turn(player1, player2)
        while True:
            try:
                self.turn(player1, player2)
            except Draw:
                print('Draw')
                break
            except Win:
                print(f'{player1.name if not player1.turn else player2.name} won')
                break

    def computer_turn(self, computer):
        list_of_possible_moves = [j_elem for i_line in self.board for j_elem in i_line if str(j_elem).isdigit()]
        number = random.choice(list_of_possible_moves)
        for i_index, i_list in enumerate(self.board):
            for j_index, j_value in enumerate(i_list):
                if j_value == number:
                    self.board[i_index][j_index] = computer.mark
                    print(self)


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.mark = None
        self.turn = None


if __name__ == '__main__':
    board = Board(10)
    name = input('enter your name: ')
    player1 = Player(name)
    player2 = Player('computer')
    while True:
        board.game(player1, player2)
        choice = input('do you want to play again?(y/n): ')
        if choice == 'y':
            board = Board(10)
        else:
            break


