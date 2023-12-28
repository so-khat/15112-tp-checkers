from cmu_graphics import *
from PIL import Image

class Piece:
    def __init__(self, app, ownership, row, col):
        self.app = app
        self.ownership = ownership
        self.position = (row, col)
        #self.coords = app.checkersGame.checkersBoard.getCellCenter(row, col)
        self.coords = None
        self.king = False
        # citation: refered to Images section under More CMU Graphics in the 
        # cmu_graphics documentation 
        # citation image is from: 
        # https://www.cleanpng.com/png-crown-desktop-wallpaper-computer-icons-clip-art-no-1577439/
        crownIMG = Image.open('images/crown.png')
        self.crownIMG = CMUImage(crownIMG)


    def drawPiece(self):
        self.coords = app.checkersGame.checkersBoard.getCellCenter(self.position[0], 
                                                                   self.position[1])
        pieceX = self.coords[0]
        pieceY = self.coords[1]
        drawCircle(pieceX, pieceY, 20, fill = 'red' if self.ownership == 1 
                   else 'black')
        drawCircle(pieceX, pieceY, 14, fill = None, border='maroon')
        drawCircle(pieceX, pieceY, 8, fill = None, border='maroon')
        drawCircle(pieceX, pieceY, 3, fill = None, border='maroon')
        # draw a crown if the piece is a king
        if self.king == True:
            imageWidth, imageHeight = getImageSize(self.crownIMG)
            drawImage(self.crownIMG, pieceX, pieceY, width=imageWidth/22, 
                      height=imageHeight/22, align='center')


    def makeKing(self):
        self.king = True


    def move(self, row, col):
        self.position = (row, col)
        self.coords = app.checkersGame.checkersBoard.getCellCenter(row, col)


    def copyPiece(self):
        # copy attributes of piece into a new piece
        duplicatePiece = Piece(self.app, self.ownership, self.position[0], 
                               self.position[1])
        duplicatePiece.king = self.king
        duplicatePiece.crownIMG = self.crownIMG
        return duplicatePiece