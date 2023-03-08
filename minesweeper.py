import itertools
import random
from tabnanny import check
from unittest.mock import sentinel
from copy import deepcopy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == 0:
            return set()
        elif len(self.cells) == self.count:
            print("mine cells")
            print(self.cells)
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        elif len(self.cells) == self.count:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            print("cell mine")
            print("-------")
            print(self.cells)
            self.cells.remove(cell)
            print(self.cells)
            print("-------")
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            #print("cell safe")
            #print("-------")
            #print(self.cells)
            self.cells.remove(cell)
            #print(self.cells)
            #print("-------")


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        print(cell)
        for sentence in self.knowledge:
            #print(sentence)
            sentence.mark_safe(cell)
            #print(sentence)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        """
        Can't recognize safe spots very well, doesn't properly remove from sets.
        """
        #print("stop")
        #print(len(self.mines))
        def check_knowledge():
            print("check knowledge")
            for sentence in self.knowledge:
                if sentence.known_safes():
                    for safe in sentence.known_safes().copy():
                        #print(safe)
                        #print("safe loop")
                        if safe not in self.safes:
                            print(sentence)
                            self.mark_safe(safe)
                            print(sentence)
                if sentence.known_mines():
                    for mine in sentence.known_mines().copy():      
                        #print("mine",mine)
                        if mine not in self.mines:
                            self.mark_mine(mine)
                
        
        self.moves_made.add(cell)
        self.mark_safe(cell)
        #self.knowledge.append(Sentence(cell, count))
        new_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    new_cells.add((i,j))
        
        if len(new_cells) != 0:
            self.knowledge.append(Sentence(new_cells, count))
        
        check_knowledge()
        #print(len(self.knowledge))
        #print(self.knowledge)
        for sentence_1 in deepcopy(self.knowledge):   
            for sentence_2 in deepcopy(self.knowledge):
                if sentence_2.cells.issubset(sentence_1.cells) and len(sentence_2.cells) != 0 and sentence_1 != sentence_2:

                    combined_set = set()
                    combined_set = sentence_1.cells.difference(sentence_2.cells)
                    #print("start of for")
                    #print(sentence_1)
                    #print(sentence_2)
                    #print(sentence_1.cells.difference(sentence_2.cells))
                    # still inf loop, gets stuck on one sentence pair for some reason
                    new_sentence = Sentence(combined_set, sentence_1.count-sentence_2.count)
                    if new_sentence not in self.knowledge:
                        self.knowledge.append(Sentence(combined_set, sentence_1.count-sentence_2.count))
        check_knowledge()
        # Must make a sentence based on the neighboring cells and their count, not the current cell???
        #print("success")
        print(self.mines)
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        move_set = self.safes.difference(self.moves_made)
        if move_set:
            print(random.choice(tuple(move_set)))
            return random.choice(tuple(move_set))
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    print("random",(i,j))
                    return (i,j)
        # Random for sake of running the function, finish correct implementation

"""
Traceback (most recent call last):
  File "T:\minesweeper\runner.py", line 220, in <module>
    ai.add_knowledge(move, nearby)
  File "T:\minesweeper\minesweeper.py", line 206, in add_knowledge
    check_knowledge()
  File "T:\minesweeper\minesweeper.py", line 200, in check_knowledge
    for safe in sentence.known_safes():
RuntimeError: Set changed size during iteration
"""