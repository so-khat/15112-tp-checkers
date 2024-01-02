from cmu_graphics import *
import copy
from piece import Piece
    
class Board():
    def __init__(self, app):
        self.app = app
        self.rows = 8
        self.cols = 8
        self.boardLeft = 100
        self.boardTop = 100
        self.boardWidth = 500
        self.boardHeight = 500
        self.cellBorderWidth = 1
        self.borderColor = 'black'
        self.boardCells = [([None] * self.cols) for row in range(self.rows)]
        self.P1pieces = 12
        self.P2pieces = 12
        self.P1kings = 0
        self.P2kings = 0
        self.cellWidth = self.boardHeight / 8
        self.cellHeight = self.boardWidth / 8

        # citation: referred to cmu_graphics documentation 
        # gradients section under colors
        self.color1 = 'cornSilk'
        self.color2 = 'burlyWood'
        self.color3 = 'saddleBrown'
        self.color4 = 'sienna'
        self.oddSquareColor = gradient(self.color1, self.color2, self.color1, 
                                       self.color2, self.color1, self.color2, 
                                       self.color1, self.color2, start='left')
        self.evenSquareColor = gradient(self.color3, self.color4, self.color3, 
                                        self.color4, self.color3, self.color4, 
                                        self.color3, self.color4, start='top')
        
        # make pieces
        self.pieces = {}
        for player in [1, 2]:
            if player == 1:
                pieceNum = 0
                for row in range(5, 8):
                    for col in range(self.cols):
                        if (row%2 == 0 and col%2 == 0) or (row%2 == 1 and col%2 == 1):
                            self.pieces[f'P{player}p{pieceNum}'] = Piece(app, player, row, col)
                            pieceNum += 1
            elif player == 2:
                pieceNum = 0
                for row in range(3):
                    for col in range(self.cols):
                        if (row%2 == 0 and col%2 == 0) or (row%2 == 1 and col%2 == 1):
                            self.pieces[f'P{player}p{pieceNum}'] = Piece(app, player, row, col)
                            pieceNum += 1

        self.prevBoard = None


    # citation: referred to Tetris Case Study in 
    # section 5.3.6 of the cmu cs academy notes
    def drawCell(self, row, col, color, hint=False):
        cellLeft, cellTop = self.getCellLeftTop(row, col)
        drawRect(cellLeft, cellTop, self.cellWidth, self.cellHeight,
                fill=color, border=self.borderColor if not hint else 'yellow',
                borderWidth=self.cellBorderWidth if not hint else 6)
    

    # citation: referred to Tetris Case Study in 
    # section 5.3.6 of the cmu cs academy notes
    def drawBoard(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.drawCell(row, col, self.oddSquareColor if (col%2 == row%2) 
                              else self.evenSquareColor)
        drawLabel('Player 1', 
                  100, 620, 
                  fill = 'black' if self.app.checkersGame.playerTurn==1 else 'dimGrey', 
                  align='left', 
                  size = 25 if self.app.checkersGame.playerTurn == 1 else 20, 
                  bold = True if self.app.checkersGame.playerTurn == 1 else False)
        drawLabel('Player 2' if app.aiGame==False else f'AI Bot Level {app.aiLevel}',
                   100, 80, 
                   fill = 'black' if self.app.checkersGame.playerTurn == 2 else 'dimGrey', 
                   align='left', 
                   size = 25 if self.app.checkersGame.playerTurn == 2 else 20, 
                   bold = True if self.app.checkersGame.playerTurn == 2 else False)
        drawLabel("press 'h' to toggle the hint on and off", 350, 620, size=13)


    # citation: referred to Tetris Case Study in 
    # section 5.3.6 of the cmu cs academy notes
    def drawBoardBorder(self):
    # draw the board outline (with double-thickness):
        drawRect(self.boardLeft, self.boardTop, self.boardWidth, self.boardHeight,
                fill=None, border=self.borderColor,
                borderWidth=2*self.cellBorderWidth)


    # citation: referred to Tetris Case Study in
    # section 5.3.6 of the cmu cs academy notes
    def getCellLeftTop(self, row, col):
        cellLeft = self.boardLeft + col * self.cellWidth
        cellTop = self.boardTop + row * self.cellHeight
        return (cellLeft, cellTop)


    def getCellCenter(self, row, col):
        (cellLeft, cellTop) = self.getCellLeftTop(row, col)
        cellCenter = (cellLeft + self.cellWidth/2, cellTop + self.cellHeight/2)
        return cellCenter


    def move(self, piece, row, col):
        # switch the value of the cell the piece is in currently with
        # the value of the cell the piece is moving to
        self.boardCells[piece.position[0]][piece.position[1]], self.boardCells[row][col] = self.boardCells[row][col], self.boardCells[piece.position[0]][piece.position[1]]
        piece.move(row, col)
        # check if a piece reaches the end of the board and becomes a king
        if piece.ownership == 1:
            if row == 0:
                piece.makeKing()
                self.P1kings += 1
        else:
            if row == 7:
                piece.makeKing()
                self.P2kings += 1
                

    def getPiece(self, row, col):
        pieceName = self.boardCells[row][col]
        return self.pieces.get(pieceName, None)


    def updateBoard(self):
        self.boardCells = [([None] * self.cols) for row in range(self.rows)]
        for piece in self.pieces:
            pieceRow, pieceCol = self.pieces[piece].position[0], self.pieces[piece].position[1]
            self.boardCells[pieceRow][pieceCol] = piece


    def removePiece(self, piecesToRemove):
        # remove piece when it is jumped over 
        # and account for new number and type of pieces
        if piecesToRemove != []:
            for piece in piecesToRemove:
                pieceName = self.boardCells[piece.position[0]][piece.position[1]]
                try:
                    piece = self.pieces[pieceName]
                except KeyError:
                    continue
                ownedBy = piece.ownership
                if ownedBy == 1:
                    self.P1pieces -= 1
                    if piece.king:
                        self.P1kings -= 1
                elif ownedBy != 1:
                    self.P2pieces -= 1
                    if piece.king:
                        self.P2kings -= 1
                self.pieces.pop(pieceName)
                self.boardCells[piece.position[0]][piece.position[1]] = None


    def getLegalMoves(self, piece):
        # helper functions for chain captures

        def additionalDownwardCaptures(result, playerNum):
            # if a jumpMove is possible
            if result != {}:
                # for every jump that is possible, we are tyring to find successive jumps
                # obtain key from initial dict which represents the cell landed on
                for (x, y) in result:
                    # try to capture in downwardRight direction
                    result2 = self.downwardRightCapture(x, y, playerNum)
                    # if a chain capture exists, update new dict such that this chain capture
                    # has a key which is the cell you land on and a respective 
                    # value which is all the pieces that have been jumped over
                    if result2 != {}:
                        for p, q in result2:
                            result2[(p,q)]+=(result[(x,y)])
                    # try to capture in downwardLeft direction        
                    result3 = self.downwardLeftCapture(x, y, playerNum)
                    if result3 != {}:
                        for p, q in result3:
                            result3[(p,q)]+=(result[(x,y)])
                # update inital dict with all the moves that can be made
                result.update(result2)
                result.update(result3)

        def additionalUpwardCaptures(result, playerNum):
            # if a jumpMove is possible
            if result != {}:
                # while True, for every jump that is possible, we are tyring 
                # to find successive jumps
                for (x, y) in result:
                    result2 = self.upwardRightCapture(x, y, playerNum)
                    if result2 != {}:
                        for p, q in result2:
                            result2[(p,q)]+=(result[(x,y)])
                    result3 = self.upwardLeftCapture(x, y, playerNum)
                    if result3 != {}:
                        for p, q in result3:
                            result3[(p,q)]+=(result[(x,y)])
                result.update(result2)
                result.update(result3)

        def additionalKingCaptures(result, playerNum):
            # if a jumpMove is possible
            if result != {}:
                # while True, for every jump that is possible, we are tyring to
                # find successive jumps
                for (x, y) in result:
                    result2 = self.downwardRightCapture(x, y, playerNum)
                    if result2 != {}:
                        for p, q in result2:
                            result2[(p,q)]+=(result[(x,y)])
                    result3 = self.downwardLeftCapture(x, y, playerNum)
                    if result3 != {}:
                        for p, q in result3:
                            result3[(p,q)]+=(result[(x,y)])
                    result4 = self.upwardRightCapture(x, y, playerNum)
                    if result4 != {}:
                        for p, q in result4:
                            result4[(p,q)]+=(result[(x,y)])
                    result5 = self.upwardLeftCapture(x, y, playerNum)
                    if result5 != {}:
                        for p, q in result5:
                            result5[(p,q)]+=(result[(x,y)])
                result.update(result2)
                result.update(result3)
                result.update(result4)
                result.update(result5)

        # dictionary of keys as cells where you land after a move
        # whose respective values are all the pieces that were 'jumped' over
        # (value will be empty if its a regular move n not a capture)
        moves = {}
        row = piece.position[0]
        col = piece.position[1]
        playerNum = piece.ownership
        # if piece is player 1's
        if playerNum == 1:
            # if piece is not a king
            if not piece.king:
                # check if upwardRightMove is valid
                moves.update(self.upwardRightMove(row, col))

                # check if upwardRightCapture is valid
                futureMoves = self.upwardRightCapture(row, col, playerNum)
                length = 0
                # if the capture is valid, chain cpature until you cant anymore
                while len(futureMoves) > length:
                    length = len(futureMoves)
                    additionalUpwardCaptures(futureMoves, playerNum)
                moves.update(futureMoves)   

                # check if upwardLeftMove is valid
                moves.update(self.upwardLeftMove(row, col))

                futureMoves = self.upwardLeftCapture(row, col, playerNum)
                length = 0
                while len(futureMoves) > length:
                    length = len(futureMoves)
                    additionalUpwardCaptures(futureMoves, playerNum)
                moves.update(futureMoves)

            # if piece is a king
            else:
                # check if downwardRightMove is valid
                moves.update(self.downwardRightMove(row, col))

                # check if downwardRightCapture is valid
                futureMoves = self.downwardRightCapture(row, col, playerNum)
                length = 0
                while len(futureMoves) > length:
                    length = len(futureMoves)
                    additionalKingCaptures(futureMoves, playerNum)
                moves.update(futureMoves)

                # check if downwardLeftMove is valid
                moves.update(self.downwardLeftMove(row, col))

                # check if downwardLeftCapture is valid
                futureMoves = self.downwardLeftCapture(row, col, playerNum)
                length = 0
                while len(futureMoves) > length:
                    length = len(futureMoves)
                    additionalKingCaptures(futureMoves, playerNum)
                moves.update(futureMoves)

                # check if upwardRightMove is valid
                moves.update(self.upwardRightMove(row, col))

                # check if upwardRightCaptureMove is valid
                futureMoves = self.upwardRightCapture(row, col, playerNum)
                length = 0
                while len(futureMoves) > length:
                    length = len(futureMoves)
                    additionalKingCaptures(futureMoves, playerNum)
                moves.update(futureMoves)

                # check if upwardLeftMove is valid
                moves.update(self.upwardLeftMove(row, col))

                # check if upwardLeftCapture is valid
                futureMoves = self.upwardLeftCapture(row, col, playerNum)
                length = 0
                while len(futureMoves) > length:
                    length = len(futureMoves)
                    additionalKingCaptures(futureMoves, playerNum)
                moves.update(futureMoves)

        # else if piece is player 2's
        else:
            # if piece is not a king
            if not piece.king:
                # check if downwardRightMove is valid
                moves.update(self.downwardRightMove(row, col))

                # check if downwardRightCapture is valid
                futureMoves = self.downwardRightCapture(row, col, playerNum)
                length = 0
                while len(futureMoves) > length:
                    length = len(futureMoves)
                    additionalDownwardCaptures(futureMoves, playerNum)
                moves.update(futureMoves)

                # check if downwardLeftMove is valid
                moves.update(self.downwardLeftMove(row, col))

                # check if downwardLeftCapture is valid
                futureMoves = self.downwardLeftCapture(row, col, playerNum)
                length = 0
                while len(futureMoves) > length:
                    length = len(futureMoves)
                    additionalDownwardCaptures(futureMoves, playerNum)
                moves.update(futureMoves)

            # if piece is a king
            else:
                # check if downwardRightMove is valid
                moves.update(self.downwardRightMove(row, col))

                # check if downwardRightCapture is valid
                futureMoves = self.downwardRightCapture(row, col, playerNum)
                length = 0
                while len(futureMoves) > length:
                    length = len(futureMoves)
                    additionalKingCaptures(futureMoves, playerNum)
                moves.update(futureMoves)

                # check if downwardLeftMove is valid
                moves.update(self.downwardLeftMove(row, col))

                # check if downwardLeftCapture is valid
                futureMoves = self.downwardLeftCapture(row, col, playerNum)
                length = 0
                while len(futureMoves) > length:
                    length = len(futureMoves)
                    additionalKingCaptures(futureMoves, playerNum)
                moves.update(futureMoves)

                # check if upwardRightMove is valid
                moves.update(self.upwardRightMove(row, col))

                # check if upwardRightCaptureMove is valid
                futureMoves = self.upwardRightCapture(row, col, playerNum)
                length = 0
                while len(futureMoves) > length:
                    length = len(futureMoves)
                    additionalKingCaptures(futureMoves, playerNum)
                moves.update(futureMoves)

                # check if upwardLeftMove is valid
                moves.update(self.upwardLeftMove(row, col))

                # check if upwardLeftCapture is valid
                futureMoves = self.upwardLeftCapture(row, col, playerNum)
                length = 0
                while len(futureMoves) > length:
                    length = len(futureMoves)
                    additionalKingCaptures(futureMoves, playerNum)
                moves.update(futureMoves)

        # # if standard mode is being played, 
        # # update moves to show only captures if captures are possible
        # capturePossible = False
        # if not app.newbieMode:
        #     for jumpedOver in moves.values():
        #         if jumpedOver != []:
        #             print('capture moves available') #debugger
        #             capturePossible = True
        #             break
        #     if capturePossible:
        #         captureMoves = {}
        #         for move in moves:
        #             if moves[move] != []:
        #                 captureMoves[move] = moves[move]
        #         moves = captureMoves
        # print(moves) #debugger
        # return moves


    def gameWon(self, noAIMovesLeft=False):
        # one of the win conditions, other is implemented in 
        # noLegalMoves in Game class
        if self.P1pieces <= 0:
            return 2
        elif self.P2pieces <= 0:
            return 1
        elif noAIMovesLeft:
            return 1


    def downwardLeftMove(self, row, col):
        # if move is within board
        if 0<=row+1<self.rows and 0<=col-1<self.cols:
            cellToMove = self.getPiece(row+1, col-1)
            # if cell is empty
            if cellToMove == None:
                return {(row+1, col-1):[]}
        return {}
        

    def downwardLeftCapture(self, row, col, ownedBy):
        # if cell is within board and cell is occupied by opposition piece
        if 0<=row+1<self.rows and 0<=col-1<self.cols:
            cellToJump = self.getPiece(row+1, col-1)
            if cellToJump != None and cellToJump.ownership != ownedBy:
                # if cell you land on after jumping is within cell and empty
                if 0<=row+2<self.rows and 0<=col-2<self.cols:
                    cellToLand = self.getPiece(row+2, col-2)
                    if cellToLand == None:
                        return {(row+2, col-2):[self.getPiece(row+1, col-1)]}
        return {}


    def upwardLeftMove(self, row, col):
        # if move is within board
        if 0<=row-1<self.rows and 0<=col-1<self.cols:
            cellToMove = self.getPiece(row-1, col-1)
            # if cell is empty
            if cellToMove == None:
                return {(row-1, col-1):[]}
        return {}
        

    def upwardLeftCapture(self, row, col, ownedBy):
        # if cell is within board and cell is occupied by opposition piece
        if 0<=row-1<self.rows and 0<=col-1<self.cols:
            cellToJump = self.getPiece(row-1, col-1)
            if cellToJump != None and cellToJump.ownership != ownedBy:
                # if cell you land on after jumping in within cell and empty
                if 0<=row-2<self.rows and 0<=col-2<self.cols:
                    cellToLand = self.getPiece(row-2, col-2)
                    if cellToLand == None:
                        return {(row-2, col-2):[self.getPiece(row-1, col-1)]}
        return {}
    

    def downwardRightMove(self, row, col):
        # if move is within board
        if 0<=row+1<self.rows and 0<=col+1<self.cols:
            cellToMove = self.getPiece(row+1, col+1)
            # if cell is empty
            if cellToMove == None:
                return {(row+1, col+1):[]}
        return {}
        

    def downwardRightCapture(self, row, col, ownedBy):
        # if cell is within board and cell is occupied by opposition piece
        if 0<=row+1<self.rows and 0<=col+1<self.cols:
            cellToJump = self.getPiece(row+1, col+1)
            if cellToJump != None and cellToJump.ownership != ownedBy:
                # if cell you land on after jumping in within cell and empty
                if 0<=row+2<self.rows and 0<=col+2<self.cols:
                    cellToLand = self.getPiece(row+2, col+2)
                    if cellToLand == None:
                        return {(row+2, col+2):[self.getPiece(row+1, col+1)]}
        return {}
    

    def upwardRightMove(self, row, col):
        # if move is within board
        if 0<=row-1<self.rows and 0<=col+1<self.cols:
            cellToMove = self.getPiece(row-1, col+1)
            # if cell is empty
            if cellToMove == None:
                return {(row-1, col+1):[]}
        return {}
        

    def upwardRightCapture(self, row, col, ownedBy):
        # if cell is within board and cell is occupied by opposition piece
        if 0<=row-1<self.rows and 0<=col+1<self.cols:
            cellToJump = self.getPiece(row-1, col+1)
            if cellToJump != None and cellToJump.ownership != ownedBy:
                # if cell you land on after jumping in within cell and empty
                if 0<=row-2<self.rows and 0<=col+2<self.cols:
                    cellToLand = self.getPiece(row-2, col+2)
                    if cellToLand == None:
                        return {(row-2, col+2):[self.getPiece(row-1, col+1)]}
        return {}


    def copyBoard(self):
        # copy the attributes of the board into a new board
        duplicateBoard = Board(self.app)
        duplicateBoard.rows = self.rows
        duplicateBoard.cols = self.cols
        duplicateBoard.boardLeft = self.boardLeft
        duplicateBoard.boardTop = self.boardTop
        duplicateBoard.boardWidth = self.boardWidth
        duplicateBoard.boardHeight = self.boardHeight
        duplicateBoard.cellBorderWidth = self.cellBorderWidth
        duplicateBoard.borderColor = self.borderColor
        duplicateBoard.boardCells = copy.deepcopy(self.boardCells)
        duplicateBoard.P1pieces = self.P1pieces
        duplicateBoard.P2pieces = self.P2pieces
        duplicateBoard.P1kings = self.P1kings
        duplicateBoard.P2kings = self.P2kings
        duplicateBoard.cellWidth = self.cellWidth
        duplicateBoard.cellHeight = self.cellHeight
        duplicateBoard.color1 = self.color1
        duplicateBoard.color2 = self.color2
        duplicateBoard.color3 = self.color3
        duplicateBoard.color4 = self.color4
        duplicateBoard.oddSquareColor = self.oddSquareColor
        duplicateBoard.evenSquareColor = self.evenSquareColor
        # copy piece list
        duplicateBoard.pieces = {}
        for pieceName, piece in self.pieces.items():
            duplicateBoard.pieces[pieceName] = piece.copyPiece()
        duplicateBoard.prevBoard = self.prevBoard
        return duplicateBoard


    # this method evalautes the position of the board and assigns a score to it
    # each regular piece is worth 1 point while kings are worth 3 points
    # a win is worth a 100 points
    def evaluatePosition(self):
        if self.gameWon == 1:
            return -100
        elif self.gameWon == 2:
            return 100
        else:
            return (self.P2pieces + (self.P2kings * 2) 
                    - self.P1pieces - (self.P1kings * 2))
        

    # this method is similar to evaluatePosition() written above
    def evaluatePositionForHints(self, playerNum):
        oppPlayerNum = 2 if playerNum == 1 else 1
        if self.gameWon == playerNum:
            return -100
        elif self.gameWon == oppPlayerNum:
            return 100
        else:
            if playerNum == 1:
                return (self.P1pieces + (self.P1kings * 2) 
                        - self.P2pieces - (self.P2kings * 2))
            else:
                return (self.P2pieces + (self.P2kings * 2) 
                        - self.P1pieces - (self.P1kings * 2))