from cmu_graphics import *


def minimaxAlgorithmWithAlphaBeta(app, boardPosition, depth, alpha, beta, maxPlayer):
    # base case
    # if you have reached the maximum depth or if someone has won the game,
    # return the score of the position and the position of the board
    if depth == 0 or boardPosition.gameWon() != None:
        return boardPosition.evaluatePosition(), boardPosition

    # recursive case
    else:
        # player that is trying to maximize their score
        if maxPlayer:
            # since no score has been encountered at the start, 
            # the max score is a large negative number
            maxScore = -10000
            bestMove = None
            # loop through all possible moves to find out the best score 
            # which is the score assigned to the parent node
            #  and also to find out the best move
            allPossibleMoves = getAllMoves(boardPosition, 2)
            if not allPossibleMoves:
                boardPosition.gameWon(True)
                return maxScore, boardPosition
            for move in allPossibleMoves:
                currScore = minimaxAlgorithmWithAlphaBeta(app, move, depth-1, 
                                                          alpha, beta, False)[0]
                # if current score is equal to max score that means 
                # this is the move with the best score until 
                # now so it is the best move
                if currScore > maxScore:
                    bestMove = move
                    maxScore = currScore
                
                alpha = max(alpha, maxScore)
                if alpha >= beta:
                    break  # beta cutoff

            return maxScore, bestMove

        # player that is trying to minimize their score
        else:
            minScore = 10000
            bestMove = None
            allPossibleMoves = getAllMoves(boardPosition, 1)
            if not allPossibleMoves:
                boardPosition.gameWon(True)
                return minScore, boardPosition

            for move in allPossibleMoves:
                currScore = minimaxAlgorithmWithAlphaBeta(app, move, depth-1, 
                                                          alpha, beta, True)[0]
                if currScore < minScore:
                    bestMove = move
                    minScore = currScore

                beta = min(beta, minScore)
                if alpha >= beta:
                    break  # alpha cutoff

            return minScore, bestMove


def getAllMoves(boardPosition, playerNum):
    positions = []
    # loop through all the pieces on the board
    for pieceName in boardPosition.pieces:
        piece = boardPosition.pieces[pieceName]
        # if the piece belongs to the relevant player
        if piece.ownership == playerNum:
            legalMoves = boardPosition.getLegalMoves(piece)
            # get the cell to land on and pieces jumped over from the 
            # key-value pair in the moves dictionary
            for cell, piecesJumpedOver in legalMoves.items():
                # create a copy of the board and pieces and
                # simulate the move on the copied board
                tempBoard = boardPosition.copyBoard()
                tempPiece = tempBoard.pieces[pieceName]
                tempPiecesJumpedOver = []
                for p in piecesJumpedOver:
                    pName = next(key for key, value in boardPosition.pieces.items() if value == p)
                    tempPiecesJumpedOver.append(tempBoard.pieces[pName])
                newBoard = simulateMove(tempPiece, cell, tempBoard, piecesJumpedOver)
                # append the board after simulating move to the positions list
                positions.append(newBoard)
    return positions


# similar to minimaxAlgorithm function above but 
# returns the cells for hints as well
def minimaxAlgorithmForHints(app, boardPosition, depth, maxPlayer, alpha=-10000,
                            beta=10000, bestMove=None):
    playerNum = app.checkersGame.playerTurn
    oppPlayerNum = 1 if app.checkersGame.playerTurn == 2 else 2

    # base case
    # if you have reached the maximum depth or if someone has won the game,
    # return the score of the position and the position of the board
    if depth == 0 or boardPosition.gameWon() is not None:
        return boardPosition.evaluatePositionForHints(playerNum), boardPosition, bestMove, None
    
    # recursive case
    else:
        # player that is trying to maximise their score
        if maxPlayer:
            maxScore = -10000
            bestPosition = None
            bestMove = None
            bestPiece = None
            allPossiblePositions, allPossibleMoves, allPossiblePieces = getAllMovesforHints(boardPosition, playerNum)
            if allPossiblePositions == []:
                boardPosition.gameWon(True)
                return maxScore, boardPosition, None, None
            for i in range(len(allPossiblePositions)):
                position = allPossiblePositions[i]
                move = allPossibleMoves[i]
                piece = allPossiblePieces[i]
                currScore = minimaxAlgorithmForHints(app, position, depth-1, 
                                                     False, alpha, beta, move)[0]
                if currScore > maxScore:
                    bestPosition = position
                    maxScore = currScore
                    bestMove = move
                    bestPiece = piece
                # alpha-beta pruning
                alpha = max(alpha, currScore)
                if alpha >= beta:
                    break
            return maxScore, bestPosition, bestMove, bestPiece
                
        # player that is trying to minimise their score
        else:
            minScore = 10000
            bestPosition = None
            bestMove = None
            bestPiece = None
            allPossiblePositions, allPossibleMoves, allPossiblePieces = getAllMovesforHints(boardPosition, oppPlayerNum)
            if allPossiblePositions == []:
                boardPosition.gameWon(True)
                return minScore, boardPosition, None, None
            for i in range(len(allPossiblePositions)):
                position = allPossiblePositions[i]
                move = allPossibleMoves[i]
                piece = allPossiblePieces[i]
                currScore = minimaxAlgorithmForHints(app, position, depth-1, 
                                                     True, alpha, beta, move)[0]
                if currScore < minScore:
                    bestPosition = position
                    bestMove = move
                    bestPiece = piece
                    minScore = currScore
                # alpha-beta pruning
                beta = min(beta, currScore)
                if alpha >= beta:
                    break
            return minScore, bestPosition, bestMove, bestPiece


# similar to getAllMoves function but returns cell landed on as well
def getAllMovesforHints(boardPosition, playerNum):
    positions = []
    moves = []
    pieces = []
    for pieceName in boardPosition.pieces:
        piece = boardPosition.pieces[pieceName]
        if piece.ownership == playerNum:
            legalMoves = boardPosition.getLegalMoves(piece)
            for cell, piecesJumpedOver in legalMoves.items():
                tempBoard = boardPosition.copyBoard()
                tempPiece = tempBoard.pieces[pieceName]
                tempPiecesJumpedOver = []
                for p in piecesJumpedOver:
                    pName = next(key for key, value in 
                                 boardPosition.pieces.items() if value == p)
                    tempPiecesJumpedOver.append(tempBoard.pieces[pName])
                newBoard = simulateMove(tempPiece, cell, tempBoard, 
                                        piecesJumpedOver)
                positions.append(newBoard)
                moves.append(cell)
                pieces.append(pieceName)
    return positions, moves, pieces


# simulates a move on a board that is passed in
def simulateMove(piece, cell, board, piecesJumpedOver):
    board.move(piece, cell[0], cell[1])
    if piecesJumpedOver != []:
        for pieceToRemove in piecesJumpedOver:
            board.removePiece([pieceToRemove])
    return board


# citation: minimax structure was inspired by: Python Checkers AI Tutorial Part 2
# - Implementation & Visualization (Minimax) https://youtu.be/mYbrH1Cl3nw?feature=shared