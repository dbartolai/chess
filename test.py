from chess_game import ChessMove, ChessGame
import numpy as np

# ================== PAWN TESTS ====================

def test_pawn_valid_move():

    board = np.array([
            [4, 2, 3, 5, 6, 3, 2, 4],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-4, -2, -3, -5, -6, -3, -2, -4]
        ])
    
    game = ChessGame(board)

    move = "1." + "b4"
    m = ChessMove(move=move, is_white = True)

    if not game.validate_move(m):
        print("TEST PAWN VALID MOVE FAILED")
        return False
    return True


def test_pawn_invalid_move():

    board = np.array([
            [4, 2, 3, 5, 6, 3, 2, 4],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-4, -2, -3, -5, -6, -3, -2, -4]
        ])
    
    game = ChessGame(board)

    move = "1." + "b6"
    m = ChessMove(move=move, is_white = True)

    if game.validate_move(m):
        print("TEST PAWN INVALID MOVE FAILED")
        return False
    return True


def test_pawn_capture():
    
    board = np.array([
            [4, 2, 3, 5, 6, 3, 2, 4],
            [1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, -3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-4, -2, -3, -5, -6, -3, -2, -4]
        ])
    
    game = ChessGame(board)

    move = "1." + "dxe5"
    m = ChessMove(move=move, is_white = True)
    if not game.validate_move(m):
        print("TEST PAWN CPATURE FAILED")
        return False
    return True


def test_pawn_bad_capture():
    
    board = np.array([
            [4, 2, 3, 5, 6, 3, 2, 4],
            [1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-4, -2, -3, -5, -6, -3, -2, -4]
        ])
    
    game = ChessGame(board)

    move = "1." + "dxe5"
    m = ChessMove(move=move, is_white = True)
    
    if game.validate_move(m):
        print("TEST PAWN BAD CAPTURE FAILED")
        return False
    return True

# ================== KNIGHT TESTS ====================

def test_knight_move():
    
    board = np.array([
            [4, 2, 3, 5, 6, 3, 2, 4],
            [1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-4, -2, -3, -5, -6, -3, -2, -4]
        ])
    
    game = ChessGame(board)

    move = "1." + "Nc3"
    m = ChessMove(move=move, is_white = True)
    
    if not game.validate_move(m):
        print("TEST KNIGHT MOVE FAILED")
        return False
    return True

def test_knight_bad_move():
    
    board = np.array([
            [4, 2, 3, 5, 6, 3, 2, 4],
            [1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-4, -2, -3, -5, -6, -3, -2, -4]
        ])
    
    game = ChessGame(board)

    move = "1." + "Nc5"
    m = ChessMove(move=move, is_white = True)
    
    if game.validate_move(m):
        print("TEST KNIGHT BAD MOVE FAILED")
        return False
    return True

def test_knight_capture():
    
    board = np.array([
            [4, 2, 3, 5, 6, 3, 2, 4],
            [1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, -4, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-4, -2, -3, -5, -6, -3, -2, -4]
        ])
    
    game = ChessGame(board)

    move = "1." + "Nxc3"
    m = ChessMove(move=move, is_white = True)
    
    if not game.validate_move(m):
        print("TEST KNIGHT CAPTURE FAILED")
        return False
    return True

def test_knight_bad_capture():
    
    board = np.array([
            [4, 2, 3, 5, 6, 3, 2, 4],
            [1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 4, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-4, -2, -3, -5, -6, -3, -2, -4]
        ])
    
    game = ChessGame(board)

    move = "1." + "Nxc3"
    m = ChessMove(move=move, is_white = True)
    
    if game.validate_move(m):
        print("TEST KNIGHT BAD CAPTURE FAILED")
        return False
    return True

# ================== BISHOP TESTS ====================

def test_bishop_move():
    
    board = np.array([
            [4, 2, 3, 5, 6, 3, 2, 4],
            [1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-4, -2, -3, -5, -6, -3, -2, -4]
        ])
    
    game = ChessGame(board)

    move = "1." + "Be3"
    m = ChessMove(move=move, is_white = True)
    
    if not game.validate_move(m):
        print("TEST BISHOP MOVE FAILED")
        return False
    return True

def test_bishop_bad_move():
    
    board = np.array([
            [4, 2, 3, 5, 6, 3, 2, 4],
            [1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-4, -2, -3, -5, -6, -3, -2, -4]
        ])
    
    game = ChessGame(board)

    move = "1." + "Bb8"
    m = ChessMove(move=move, is_white = True)
    
    if game.validate_move(m):
        print("TEST BISHOP BAD MOVE FAILED")
        return False
    return True

def test_bishop_blocked_move():
    
    board = np.array([
            [4, 2, 3, 5, 6, 3, 2, 4],
            [1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-4, -2, -3, -5, -6, -3, -2, -4]
        ])
    
    game = ChessGame(board)

    move = "1." + "Ba3"
    m = ChessMove(move=move, is_white = True)
    
    if game.validate_move(m):
        print("TEST BISHOP BLOCKED MOVE FAILED")
        return False
    return True


def test_bishop_capture():
    
    board = np.array([
            [4, 2, 3, 5, 6, 3, 2, 4],
            [1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, -4, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-4, -2, -3, -5, -6, -3, -2, -4]
        ])
    
    game = ChessGame(board)

    move = "1." + "Bxe3"
    m = ChessMove(move=move, is_white = True)
    
    if not game.validate_move(m):
        print("TEST BISHOP CAPTURE FAILED")
        return False
    return True

def test_bishop_bad_capture():
    
    board = np.array([
            [4, 2, 3, 5, 6, 3, 2, 4],
            [1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 4, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-4, -2, -3, -5, -6, -3, -2, -4]
        ])
    
    game = ChessGame(board)

    move = "1." + "Bxd2"
    m = ChessMove(move=move, is_white = True)
    
    if game.validate_move(m):
        print("TEST KNIGHT BAD CAPTURE FAILED")
        return False
    return True


def test_bishop_blocked_capture():
    
    board = np.array([
            [4, 2, 3, 5, 6, 3, 2, 4],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 4, 0, -2, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-4, -2, -3, -5, -6, -3, -2, -4]
        ])
    
    game = ChessGame(board)

    move = "1." + "Bxe3"
    m = ChessMove(move=move, is_white = True)
    
    if game.validate_move(m):
        print("TEST BISHOP BLOCKED CAPTURE FAILED")
        return False
    return True





def tests():

    all_passed = True

    # PAWN TESTS
    if not test_pawn_valid_move(): all_passed = False
    if not test_pawn_invalid_move(): all_passed = False
    if not test_pawn_bad_capture(): all_passed = False
    if not test_pawn_capture(): all_passed = False


    # KNIGHT TESTS
    if not test_knight_move(): all_passed = False
    if not test_knight_bad_move(): all_passed = False
    if not test_knight_capture(): all_passed = False
    if not test_knight_bad_capture(): all_passed = False

    # BISHOP TESTS
    if not test_bishop_move(): all_passed = False
    if not test_bishop_bad_move(): all_passed = False
    if not test_bishop_blocked_move(): all_passed = False
    if not test_bishop_capture(): all_passed = False
    if not test_bishop_bad_capture(): all_passed = False
    if not test_bishop_blocked_capture(): all_passed = False

    # KING TESTS
    


    # all passed
    if all_passed: print("ALL TESTS PASSED!!")

tests()