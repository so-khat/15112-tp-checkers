from cmu_graphics import *
from board import Board
from minimax import minimaxAlgorithmWithAlphaBeta
from minimax import minimaxAlgorithmForHints

class Game:
    def __init__(self, app):
        self.app = app
        self.selectedPiece = None
        self.checkersBoard = Board(self.app)
        self.playerTurn = 1
        self.legalMoves = {}


    def updateGame(self):
        self.checkersBoard.updateBoard()
        self.checkersBoard.drawBoard()
        self.checkersBoard.drawBoardBorder()
        self.drawLegalMoves(self.legalMoves)


    def selectPieceOnCell(self, row, col):
        # if there is no piece selected
        if self.selectedPiece == None:
            # if there is a piece on the cell being clicked and 
            # it belongs to player whose turn it is, select the piece
            piece = self.checkersBoard.getPiece(row, col)
            if piece != None and piece.ownership == self.playerTurn:
                self.selectedPiece = piece
                self.legalMoves = self.checkersBoard.getLegalMoves(piece)
    

    def selectMoveforSelectedPiece(self, row, col):
        # if a piece is currently selected try to move it to the selected cell
        if self.selectedPiece != None:
            possibleMove = self.move(row, col)
            # if this move is valid, make the move
            if possibleMove and (row,col) in self.legalMoves:
                possibleMove
                self.legalMoves = {}
                self.selectedPiece = None
                self.checkersBoard.updateBoard()
            # deselct the piece
            self.selectedPiece = None
            self.legalMoves = {}
       

    def move(self, row, col):
        # while the game is still ongoing
        while not app.gameOver:
            app.hint = False
            app.hintCell = None
            self.checkersBoard.prevBoard = self.checkersBoard.copyBoard()
            # if a piece is selected, it's the players turn, 
            # the selected cell is empty and it is a legal move
            cellToMoveTo = self.checkersBoard.boardCells[row][col]
            if (self.selectedPiece != None and 
                self.selectedPiece.ownership == self.playerTurn and 
                cellToMoveTo == None and 
                self.legalMoves != None and 
                (row, col) in self.legalMoves):
                # make the move
                self.checkersBoard.move(self.selectedPiece, row, col)
                # remove the pieces that were captured if any
                jumpedOver = self.legalMoves[(row, col)]
                if jumpedOver != []:
                    self.checkersBoard.removePiece(jumpedOver)
                self.switchTurns()

                # for an ai game, immediately after the human's turn, 
                # let the ai move
                if app.aiGame:
                    if self.playerTurn == 2:
                        newBoard = (minimaxAlgorithmWithAlphaBeta(app, 
                        app.checkersGame.checkersBoard, app.aiLevel, -10000, 
                        10000, True)[1])
                        self.minimaxMove(newBoard)

                return True
            
            # invalid move
            else:
                return False


    def drawLegalMoves(self, moves):
        if moves != None:
            for move in moves:
                row, col = move
                coords = self.checkersBoard.getCellCenter(row, col)
                drawCircle(coords[0], coords[1], 5, fill='red' 
                           if self.playerTurn == 1 else 'maroon')


    def switchTurns(self):
        if self.playerTurn == 1:
            self.playerTurn = 2
        elif self.playerTurn == 2:
            self.playerTurn = 1


    # this is a part of the win condition 
    def noLegalMoves(self):
        # if player is not able to move any pieces on their turn, they lose
        if self.playerTurn == 1:
            for pieceName in self.checkersBoard.pieces:
                piece = self.checkersBoard.pieces[pieceName]
                if piece.ownership == self.playerTurn:
                    if self.checkersBoard.getLegalMoves(piece) != {}:
                        return None
            return 2
        elif self.playerTurn == 2:
            for pieceName in self.checkersBoard.pieces:
                piece = self.checkersBoard.pieces[pieceName]
                if piece.ownership == self.playerTurn:
                    if self.checkersBoard.getLegalMoves(piece) != {}:
                        return None
            return 1
        
    # handles the ai move
    def minimaxMove(self, board):
        # no legal moves left for the ai so it has lost the game
        if self.checkersBoard == board:
            app.winner = 1
            app.gameOver = True
        else:
            # replaces current board with new board after the ai has moved
            self.checkersBoard = board
            self.switchTurns()
                                                                                

    def undoMove(self):
        self.checkersBoard = self.checkersBoard.prevBoard
        # switch turns for multiplayer mode
        if not app.aiGame:
            self.switchTurns()
    

    def generateHint(self):
        # return the cell that is to be moved to
        hintCell = minimaxAlgorithmForHints(app, app.checkersGame.checkersBoard, 
                                            2, True)[2]
        pieceName = minimaxAlgorithmForHints(app, app.checkersGame.checkersBoard, 
                                             2, True)[3]
        piece = app.checkersGame.checkersBoard.pieces[pieceName]
        pieceCell = piece.position
        return hintCell, pieceCell


    def drawHint(self):
        # if a hint has been generated, draw it
        if app.hintCell != None:
            app.checkersGame.checkersBoard.drawCell(app.hintCell[0], 
                                                    app.hintCell[1], None, True)
        if app.hintPieceCell != None:
            app.checkersGame.checkersBoard.drawCell(app.hintPieceCell[0], 
                                                    app.hintPieceCell[1], 
                                                    None, True)