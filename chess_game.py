
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
import json
from typing import List

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
    rank: str # row number as string (on chess board)

    # also store coords in numpy array
    file_idx: int
    rank_idx: int

    # capture
    is_capture: bool

    # if pawn/ambiguous capture, include the starting file letter (or potentially rank)
    is_pawn_capture: bool
    is_ambiguous: bool
    starting_file: str | None
    starting_file_idx: int | None
    starting_rank: str | None
    starting_rank_idx: int | None

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
            "rank": '1',
            "file_idx": 0,
            "rank_idx": 0,
            "is_capture": False,
            "is_pawn_capture": False,
            "is_ambiguous": False,
            "starting_file": None,
            "starting_rank": None,
            "starting_file_idx": None,
            "starting_rank_idx": None,
            "is_castle": False,
            "is_king_side": None,
            "is_check": False,
            "is_mate": False
        })


        # Get move number
        move = data.get("move")
        split_move = move.split(".")
        number = split_move[0]
        data.update({"number":number})

        # get the actual move text
        move_text = split_move[1]
        


        

        # castle validation (note that castle can still lead to check & mate)
        # handle this first since the notation is so different we can just check directly
        if move_text == "0-0":
            data.update({"is_castle": True})
            data.update({"is_king_side": True})
            if move_text.endswith("+"):
                data.update({"is_check": True})
            if move_text.endswith("#"):
                data.update({"is_mate": True})
            return
        
        if move_text == "0-0-0" :
            data.update({"is_castle": True})
            data.update({"is_king_side": False})
            if move_text.endswith("+"):
                data.update({"is_check": True})
            if move_text.endswith("#"):
                data.update({"is_mate": True})
            return

                
        

        # look for piece info
        c = move_text[0]
        if c.isupper():
            data.update({"piece": c})
        else:
            data.update({"piece": ""})

        # basically create a mini graph to sort through the rest
        # start by checking if the move is a capture
        if "x" in move_text:
            data.update({"is_capture": True})
            t = move_text.split("x")

            # handle pawn capture notation
            if data.get("piece") == "":
                data.update({
                    "is_pawn_capture": True,
                    "starting_file": t[0],
                    "starting_file_idx": ord(t[0]) - 97
                })
            
            # handle ambiguous capture (file or rank before x)
            elif len(t[0]) == 2:
                data.update({"is_ambiguous": True})
                # it's a number -> rank
                if ord((t[0])[1]) < 65:
                    data.update({"starting_rank": (t[0])[1], "starting_rank_idx": int((t[0])[1])-1})
                else:
                    data.update({"starting_file": (t[0])[1], "starting_file_idx": ord((t[0])[1])-97})
            
            # now get square info from the second half
            # t[1] should just be the coords for the new square
            square = t[1]
            data.update({
                "file": square[0],
                "rank": square[1],
                "file_idx": ord(square[0]) - 97,
                "rank_idx": int(square[1]) - 1
            })

            if square.endswith("#"):
                data.update({"is_mate": True})
            if square.endswith("+"):
                data.update({"is_check": True})
        
        # now handle the non-capture case
        else:
            
            # separate pawn move from other
            # allows us to check length
            if data.get("piece") == "":
                data.update({
                    "file": move_text[0],
                    "rank": move_text[1],
                    "file_idx": ord(move_text[0]) - 97,
                    "rank_idx": int(move_text[1]) - 1
                })
            
            # with piece, standard move is Bb4 (len = 3)
            # ambiguous move becomes Bcb4 or B3b4
            else:
                
                # use check_chars to handle length
                # if check or checkmate, len will be += 1
                check_chars = 0
                if move_text.endswith("#"):
                    data.update({"is_mate": True})
                    check_chars += 1
                if move_text.endswith("+"):
                    data.update({"is_check": True})
                    check_chars += 1

                # standard path
                if len(move_text) == 3 + check_chars:
                    data.update({
                        "file": move_text[1],
                        "rank": move_text[2],
                        "file_idx": ord(move_text[1]) - 97,
                        "rank_idx": int(move_text[2]) - 1
                    })
                else:
                    data.update({
                        "is_ambiguous": True,
                        "file": move_text[2],
                        "rank": move_text[3],
                        "file_idx": ord(move_text[2]) - 97,
                        "rank_idx": int(move_text[3]) - 1
                    })
                    if ord((move_text)[1]) < 65:
                        data.update({"starting_rank": (move_text)[1]})
                    else:
                        data.update({"starting_file": (move_text)[1]}) 

        super().__init__(**data)






class ChessGame:

    # defines a numpy board with pieces in initial positions (use a number for each piece)
    # initializes an array of chess notation moves for the game
    def __init__(self, board = None):

        # board
        # index by self.board[rank_idx, file_idx]
        self.board = np.array([
            [4, 2, 3, 5, 6, 3, 2, 4],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-4, -2, -3, -5, -6, -3, -2, -4]
        ]) if board is None else board

        # history of move objects
        self.moves = []

        # kingside and queenside castling rights
        self.white_can_castle_k = True
        self.white_can_castle_q = True
        self.black_can_castle_k = True
        self.black_can_castle_q = True
        pass

    # take in square coords and output value at that square
    def get_square(self, file_idx, rank_idx):
        return self.board[rank_idx, file_idx]
    
    # check if some square is on the board
    def on_board(self, file_idx, rank_idx):
        return (file_idx >= 0 and file_idx <= 7 and rank_idx >= 0 and rank_idx <= 7)
    
    # determine if a move puts user into check
    # accept a mutated board (different from self.board)
    # return a boolean (True means move is good -> NO CHECK)
    def validate_check(self, is_white, new_board) -> bool:

        pass


    # determine if the pawn move is valid  
    # return validity of the pawn move
    # NOTE -> does not yet consider en passant (we need previous move logic for this )
    def validate_pawn_move(self, move: ChessMove) -> bool:


        # ALGORITHM:
        # 0. Get the contents of the square that we are moving to 
        f = move.file_idx
        r = move.rank_idx
        square = self.get_square(f, r)
        # 1. If the move is NOT a pawn capture, just check if square empty and pawn can move there 
        if not move.is_pawn_capture:

            # check if square is empty
            is_empty = (square == 0)

            # white moves in increasing rank idx, black in decreasing
            # so white needs to start at smaller rank idx, black at larger
            pawn_exists = False
            if move.is_white:
                # a white pawn can move to the specified square if it's one rank behind
                # or if it's on the starting rank it can move two ranks given the intermediary rank is empty
                pawn_exists = (self.get_square(f, r-1) == 1 or (self.get_square(f, 1) == 1 and r == 3 and self.get_square(f, 2) == 0))
            else:
                # a black pawn can move to the specified square if it's one rank ahead
                # or if it's on the starting rank it can move two ranks given the intermediary rank is empty
                pawn_exists = (self.get_square(f, r+1) == -1 or (self.get_square(f, 6) == -1 and r == 4 and self.get_square(f, 5) == 0))

            # returns true if the square is empty and a paawn can go there
            return is_empty and pawn_exists

        # 2. If the move IS a pawn capture, the square should be occupied by a piece of the other color
        #       and there needs to be a pawn that can move diagonally there
        else:
            # make sure square is occupied
            is_occupied = False

            pawn_exists = False
            if move.is_white:
                is_occupied = (square < 0)
                # With pawn captures, the file of the pawn is provided
                #   and the rank is implied
                f_start = move.starting_file_idx
                pawn_exists = (self.get_square(f_start, r-1) == 1)

            else:
                is_occupied = (square > 0)
                f_start = move.starting_file_idx
                pawn_exists = (self.get_square(f_start, r+1) == 1)

            return is_occupied and pawn_exists
        
    # determine if a king move is valid
    # does NOT worry about check status
    def validate_king_move(self, move: ChessMove) -> bool:

        # get contents of square we are moving to
        f = move.file_idx
        r = move.rank_idx

        square = self.get_square(f, r)

        # use color to determine sign (white is pos, black is neg)
        sign = 1 if move.is_white else -1 
            
        # check if square is empty
        is_empty = (square == 0)

        # check that king can move theres
        # iterate over adjacent squares

        king_exists = False

        # iterate over ranks
        for i in range(3):

            # iterate over files
            for j in range(3):

                # get coords of square to check
                # i -> rank
                # j -> file

                check_rank = r + i - 2
                check_file = f + j - 2

                # make sure square is on board
                if self.on_board(check_file, check_rank):
                    if self.get_square(check_file, check_rank) == 6 * sign:
                        king_exists = True
        
        # if capturing, the square shouldn't be empty
        # otherwise, it should be
        if move.is_capture:
            return king_exists and (not is_empty)
        else:
            return is_empty and king_exists
        

    # determine if a knight move is valid
    def validate_knight_move(self, move: ChessMove) -> bool:

        # get contents of square we are moving to
        f = move.file_idx
        r = move.rank_idx

        square = self.get_square(f, r)

        # use color to determine sign (white is pos, black is neg)
        sign = 1 if move.is_white else -1 
            
        # check if square is empty
        is_empty = (square == 0)
        is_opponent = (square < 0) if move.is_white else (square > 0)

        # check that knight can move there
        # we have to check 8 squares 
        
        # (file, rank)
        movable_squares = [
            (f+2, r+1), (f+1, r+2),
            (f-2, r+1), (f-1, r+2),
            (f+2, r-1), (f+1, r-2),
            (f-2, r-1), (f-1, r-2),
        ]

        knight_exists = False
        for s in movable_squares:

            if not self.on_board(s[0], s[1]):
                continue

            if self.get_square(s[0], s[1]) == 2*sign:
                knight_exists = True

        return (knight_exists and (is_opponent)) if move.is_capture else (knight_exists and is_empty)
    

    def validate_bishop_move(self, move: ChessMove) -> bool:

        # get contents of square we are moving to
        f = move.file_idx
        r = move.rank_idx

        square = self.get_square(f, r)

        # use color to determine sign (white is pos, black is neg)
        sign = 1 if move.is_white else -1 
            
        # check if square is empty
        is_empty = (square == 0)
  

        # diagonals have slope of 1 and -1
        # r = f + b and r = -f + c

        # find items on positive diagonal
        b = r-f
        positive = []
        
        x = 0 if b > 0 else -1*b
        y = b if b > 0 else 0
        while y < 8 and x < 8:
            positive.append((x,y))
            x+=1
            y+=1

        # now check if move is valid on pos diagonal
        bishop_exists_pos = False
        bishop_square = (0,0) #(f,r)
        for s in positive:
            if self.get_square(s[0], s[1]) == sign*3:
                bishop_exists_pos = True
                bishop_square = s

        # then check for blockers
        blocked_pos = False
        capture_valid_pos = False
        if bishop_exists_pos:

            # see if we are moving down diagonal
            if bishop_square[0] < f:

                while bishop_square != (f,r):
                    bishop_square = (bishop_square[0]+1, bishop_square[1]+1)

                    # if (f,r) == bishop square and (f,r) is not empty, then should be a capture
                    if bishop_square == (f,r):
                        capture_valid_pos = True if (move.is_capture != is_empty) else False
                    
                    # otherwise, make sure no blockers
                    else:
                        p = self.get_square(*bishop_square)
                        if p != 0:
                            blocked_pos = True
            
            # moving up diagonal
            else:

                while bishop_square != (f,r):
                    bishop_square = (bishop_square[0]-1, bishop_square[1]-1)

                    # if (f,r) == bishop square and (f,r) is not empty, then should be a capture
                    if bishop_square == (f,r):
                        capture_valid_pos = True if (move.is_capture != is_empty) else False
                    
                    # otherwise, make sure no blockers
                    else:
                        p = self.get_square(*bishop_square)
                        if p != 0:
                            blocked_pos = True




        # find items on negative diagonal
        c = f+r
        negative = []
        x = 0 if c<8 else c-8
        y = c if c<8 else 7
        while y >= 0 and x < 8:
            negative.append((x,y))
            x+=1
            y-=1
        
        # now check if move is valid on pos diagonal
        bishop_exists_neg = False
        bishop_square = (0,0) #(f,r)
        for s in negative:
            if self.get_square(s[0], s[1]) == sign*3:
                bishop_exists_neg = True
                bishop_square = s

        # then check for blockers
        blocked_neg = False
        capture_valid_neg = False
        if bishop_exists_neg:

            # see if we are moving down diagonal
            if bishop_square[0] < f:

                while bishop_square != (f,r):
                    bishop_square = (bishop_square[0]+1, bishop_square[1]-1)

                    # if (f,r) == bishop square and (f,r) is not empty, then should be a capture
                    if bishop_square == (f,r):
                        capture_valid_neg = True if (move.is_capture != is_empty) else False
                    
                    # otherwise, make sure no blockers
                    else:
                        p = self.get_square(*bishop_square)
                        if p != 0:
                            blocked_neg = True

            # moving up
            else:

                while bishop_square != (f,r):
                    bishop_square = (bishop_square[0]-1, bishop_square[1]+1)

                    # if (f,r) == bishop square and (f,r) is not empty, then should be a capture
                    if bishop_square == (f,r):
                        capture_valid_neg = True if (move.is_capture != is_empty) else False
                    
                    # otherwise, make sure no blockers
                    else:
                        p = self.get_square(*bishop_square)
                        if p != 0:
                            blocked_neg = True

        # if either neg or pos works return True
        return ((not blocked_pos) and capture_valid_pos and bishop_exists_pos) or ((not blocked_neg) and capture_valid_neg and bishop_exists_neg)









    # checks if a move is valid
    # if returning true, the move has been made
    def validate_move(self, move: ChessMove) -> bool:

        # 1. Make sure the move is valid for the given piece/move type
        piece = move.piece

        valid_move = False
        if piece == "":
            valid_move = self.validate_pawn_move(move)
        elif piece == "N":
            valid_move = self.validate_knight_move(move)
        elif piece == "B":
            valid_move = self.validate_bishop_move(move)
        elif piece == "R":
            pass
        elif piece == "Q":
            pass
        elif piece == "K":
            valid_move = self.validate_king_move(move)
        else:
            # handle castling, edge cases, etc here.
            pass

        # 2. Create a new board with the move made to test for check

        # 3. Make sure the move doesn't place the user into check 

        # 4. Make the move (overwrite self.board with new board)

        return valid_move


