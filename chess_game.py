
# The class for a chess game that stores the board and updates as we go

# CHESS NOTATION:
#   Move Number – First we need the move number (1.) Note both white and black have 1, then 2, ... 
#   Piece Names – Piece names are always upeprcase (King: K, Queen: Q, Knight: N, Rook: R, Bishop: B, Pawn: None)
#   Squares – Letter then Number (a5)
#   Capture – Add an 'x' between the piece being moved and the square coordinates
#   Pawn Capture – First use the file the pawn started on: (bxc6) means pawn from b captured on c6
#   Castle – kingside: (0-0), queenside (0-0-0)
#   Check – append a '+' to the end of the move (Bc6+)
#   Checkmate – append a '#' to the end of the move
#   Results – white wins: (1-0), black wins: (0-1), draw: (1/2-1/2)
#   Notes: If two of the same piece can move to the same square, differentiate with file 
#               i.e. (Nfd2) means knight on f moved to d2
#          If they are on the same file, use the rank instead
#               i.e. (N3d2) means knight at rank 3 moved to d2

# THE BOARD:
#   8*8 numpy array
#   stores integers for each square
#   white pieces positive, black negative
#   empty: 0
#   pawn: 1, -1
#   knight: 2, -2
#   bishop: 3, -3
#   rook: 4, -4
#   queen: 5, -5
#   king: 6, -6
#   rows are rank i+1
#   columns are file (0->a, 1->b, ..., 7->h)


import numpy as np
from pydantic import BaseModel

# use this for parsing moves into my board format
class ChessMove(BaseModel):

    # notation string
    move: str

    # basic data
    number: int
    is_white: bool # white is true
    piece: str # string char for piece, pawn is empty

    # parse square into file and rank
    file: str # file string
    rank: int # row number (on chess board)

    # also store coords in numpy array
    file_idx: int
    rank_idx: int

    # capture
    is_capture: bool

    # if pawn capture, include the starting file letter
    is_pawn_capture: bool
    starting_file: str | None

    # castle
    is_castle: bool
    is_king_side: bool | None

    # check/checkmate
    is_check: bool
    is_mate: bool

    # DO: Create some methods to automatically parse move data based on the chess notation
    # Shouldn't be based on board
    # We need to figure out color based on game context though (should be passed in)
    # NO SPACES
    # KINDS OF MOVES:
    #   pawn move ---------> 1.b4
    #   other piece move --> 1.Nb3
    #   ambiguous move ----> 7.Bdb2
    #   same file ---------> 9.B3b2
    #   pawn capture ------> 4.bxc6
    #   other capture -----> 6.Bxg7
    #   ambiguous capture -> 8.Kdxf5
    #   castle ------------> 5.0-0
    #   then check/checkmate just have +/# at the end

    def __init__(self, **data):

        # boilerplate data (default values)
        data.update({
            "piece": "",
            "file": "a",
            "rank": 1,
            "file_idx": 0,
            "rank_idx": 0,
            "is_capture": False,
            "is_pawn_capture": False,
            "starting_file": None,
            "is_castle": False,
            "is_king_side": None,
            "is_check": False,
            "is_mate": False
        })

        # Get move number
        split_move = move.split(".")
        number = split_move[0]
        print(number)
        data.update({"number":number})

        print("DATA: ", data)
        move = data.get("move")

        # castle validation (note that castle can still lead to check & mate)
        if split_move[0:3] is "0-0":
            data.update({"is_castle": True})
            data.update({"is_king_side": True})
            if split_move.endswith("+"):
                data.update({"is_check": True})
            if split_move.endswith("#"):
                data.update({"is_mate": True})
            return
        
        if split_move[0:5] is "0-0-0" :
            data.update({"is_castle": True})
            data.update({"is_king_side": False})
            if split_move.endswith("+"):
                data.update({"is_check": True})
            if split_move.endswith("#"):
                data.update({"is_mate": True})
            return

                
        

        # now we can iterate through the actual move text 
        move_text = split_move[1]
        length = len(move_text)

        for i in range(length):
            c = move_text[i]

            # look for piece info
            if i == 0:
                if c.isupper():
                    data.update({"piece": c})
                else:
                    data.update({"piece": ""})



        print("NEW DATA:", data)

        super().__init__(**data)






class ChessGame:

    # defines a numpy board with pieces in initial positions (use a number for each piece)
    # initializes an array of chess notation moves for the game
    def __init__(self):

        # board
        self.board = np.array([
            [4, 2, 3, 5, 6, 3, 2, 4],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-4, -2, -3, -5, -6, -3, -2, -4]
        ])

        # history of move objects
        self.moves = []

        # kingside and queenside castling rights
        self.white_can_castle_k = True
        self.white_can_castle_q = True
        self.black_can_castle_k = True
        self.black_can_castle_q = True
        pass

    # checks if a move for white is valid
    def validate_white_move(self, move) -> bool:
        pass

    def validate_black_move(self, move) -> bool:
        pass


def main():

    move = ChessMove(move= "1.b4+", is_white=True)

    print(move)

main()