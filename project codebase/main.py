from cmu_graphics import *
from game import Game
from buttonsAndScreens import *
from PIL import Image
import os, pathlib


def onAppStart(app):
    onGameStart(app)


def onGameStart(app):    
    app.width = 700
    app.height = 700
    app.gameOver = False
    app.winner = None
    app.gameStarted = False
    app.aiLevelSelection = False
    app.aiGame = False
    app.aiLevel = 1
    app.info = False
    app.themesSelection = False
    app.themeSelected = 1
    app.hint = False
    app.hintCell = None
    app.hintPieceCell = None
    app.volume = True

    # citation: refered to Images section under More CMU Graphics 
    # in the cmu_graphics documentation 
    # citation: image is from: 
    # https://www.rawpixel.com/image/9350501/home-icon-png-transparent-background
    homeButtonIMG = Image.open('images/homeButton.png')
    app.homeButtonIMG = CMUImage(homeButtonIMG)
    # citation: image was drawn with help of Johnatan Waller and LiLi Fishman
    logoIMG = Image.open('images/logo.jpg')
    app.logoIMG = CMUImage(logoIMG)
    # citation: image is from: 
    # https://keepcalms.com/p/keep-calm-you-win-player-1/
    player1winnerIMG = Image.open('images/player1champ.png')
    app.player1winnerIMG = CMUImage(player1winnerIMG)
    # citation: image is from: 
    # https://keepcalms.com/p/keep-calm-you-win-player-2/
    player2winnerIMG = Image.open('images/player2champ.png')
    app.player2winnerIMG = CMUImage(player2winnerIMG)
    # citation: image is from 
    # https://keepcalms.com/p/keep-calm-cause-you-ve-just-lost-the-game/
    aiWinnerIMG = Image.open('images/aichamp.png')
    app.aiWinnerIMG = CMUImage(aiWinnerIMG)
    # citation: image is from 
    # https://www.iconfinder.com/search/icons?family=line-278&q=volume
    volumeONIMG = Image.open('images/volumeON.png')
    app.volumeONIMG = CMUImage(volumeONIMG)
    # citation: image is from 
    # https://www.iconfinder.com/icons/6644765/mute_mute_button_mute_sound_mute_speaker_mute_volume_sound_off_speaker_off_icon
    volumeOFFIMG = Image.open('images/volumeOFF.png')
    app.volumeOFFIMG = CMUImage(volumeOFFIMG)
    

    # citation: sound is Vivaldi Four Seasons: Spring (La Primavera) from 
    # https://youtu.be/3LiztfE1X7E?si=19-ltuEf2ZwaQaEU
    app.classicThemeSong = loadSound("sounds/classicThemeSong.mp3")
    # citation: sound is The Gummy Bear Song (CHRISTMAS SPECIAL) from 
    # https://youtu.be/jEDSai-HKgw?feature=shared
    app.candyThemeSong = loadSound("sounds/candyThemeSong.mp3")
    # citation: sound is In The Jungle, The Mighty Jungle from 
    # https://youtu.be/KZ8beg31zyQ?feature=shared
    app.forestThemeSong = loadSound("sounds/forestThemeSong.mp3")
    # citation: sound is Baby Shark from 
    # https://youtu.be/IogPHjiS_HU?feature=shared
    app.oceanThemeSong = loadSound("sounds/oceanThemeSong.mp3")
    app.song = app.classicThemeSong
    app.song.play(loop=True)
    
    # start game
    app.checkersGame = Game(app)
    

def redrawAll(app):
    # draw home and volume buttons
    homeButton(app)
    volumeButton(app)


    if not app.gameStarted:
        if app.aiLevelSelection:
            aiLevelSelectionScreen()
        elif app.themesSelection:
            themesScreen()
        elif app.info:
            rulesScreen()
        else:
            startScreen(app)
    else:
        # draw win screens if game is over
        if app.gameOver:
            imageWidth, imageHeight = getImageSize(app.player1winnerIMG)
            if app.winner == 1:
                drawImage(app.player1winnerIMG, 350, 350, 
                          width=imageWidth/1.5, height=imageHeight/1.5, 
                          align='center')
            elif app.winner == 2:
                if not app.aiGame:
                    drawImage(app.player2winnerIMG, 350, 350, 
                              width=imageWidth/1.5, height=imageHeight/1.5, 
                              align='center')
                else:
                    drawImage(app.aiWinnerIMG, 350, 350, 
                              width=imageWidth/1.5, height=imageHeight/1.5, 
                              align='center')
        else:    
            # update the display after a click, move, hint, etc.
            app.checkersGame.updateGame()  
            for key in app.checkersGame.checkersBoard.pieces:
                app.checkersGame.checkersBoard.pieces[key].drawPiece()
            # draw the undo button, if an undo move is possible
            if app.checkersGame.checkersBoard.prevBoard != None:
                undoButton()
            # if a hint is asked, highlight the cell
            if app.hint:
                app.checkersGame.drawHint()


def onMousePress(app, mouseX, mouseY):
    # if home button is pressed
    if 15<=mouseX<=85 and 15<=mouseY<=85:
        app.gameOver = False
        app.winner = None
        app.gameStarted = False
        app.aiLevelSelection = False
        app.aiGame = False
        app.aiLevel = 1
        app.info = False
        app.themesSelection = False
        app.hint = False
        app.hintCell = None
        app.hintPieceCell = None
        app.checkersGame = Game(app)
        changeTheme(app)

    # if volume button is pressed
    if 620<=mouseX<=680 and 20<=mouseY<=80:
        app.volume = not app.volume
        if app.volume:
            app.song.play(loop=True)
        else:
            app.song.pause()
        
    if not app.gameStarted:
        if not app.aiLevelSelection:
            # clicking on the multiplayer button
            if 375<=mouseX<=625 and 450<=mouseY<=550:
                app.gameStarted = True
            # clicking on the single player button
            elif 75<=mouseX<=325 and 450<=mouseY<=550:
                app.aiLevelSelection = True
            # clicking on the themes button
            elif 425<=mouseX<=575 and 575<=mouseY<=625:
                app.themesSelection = True
            # clicking on the rules button
            elif 125<=mouseX<=275 and 575<=mouseY<=625:
                app.info = True

        # select an AI level
        if app.aiLevelSelection:
            # easy level
            if 25<=mouseX<=174 and 300<=mouseY<=400:
                app.aiLevel = 1
                app.aiGame = True
                app.aiLevelSelection = False
                app.gameStarted = True
            # medium level
            elif 192<=mouseX<=341 and 300<=mouseY<=400:
                app.aiLevel = 2
                app.aiGame = True
                app.aiLevelSelection = False
                app.gameStarted = True
            # hard level
            elif 359<=mouseX<=508 and 300<=mouseY<=400:
                app.aiLevel = 3
                app.aiGame = True
                app.aiLevelSelection = False
                app.gameStarted = True
            # expert level
            elif 526<=mouseX<=675 and 300<=mouseY<=400:
                app.aiLevel = 4
                app.aiGame = True
                app.aiLevelSelection = False
                app.gameStarted = True
    
        # select a theme
        elif app.themesSelection:
            if 88.5<=mouseX<=338.5 and 200<=mouseY<=300:
                app.themeSelected = 1
                changeTheme(app)
                app.themesSelection = False
            elif 362.5<=mouseX<=612.5 and 200<=mouseY<=300:
                app.themeSelected = 2
                changeTheme(app)
                app.themesSelection = False
            elif 88.5<=mouseX<=338.5 and 325<=mouseY<=425:
                app.themeSelected = 3
                changeTheme(app)
                app.themesSelection = False
            elif 362.5<=mouseX<=612.5 and 325<=mouseY<=425:
                app.themeSelected = 4
                changeTheme(app)
                app.themesSelection = False
            
    else:    
        # if no one has won yet
        if not app.gameOver:
            # if undo is possible and undo is clicked
            if app.checkersGame.checkersBoard.prevBoard != None:
                if 500<=mouseX<=600 and 605<=mouseY<=655:
                    app.checkersGame.undoMove()
            # get cell that was clicked
            cellRow, cellCol = getCellFromMousePress(app, mouseX, mouseY)
            if cellRow != None and cellCol != None:
                # if nothing is selcted
                if app.checkersGame.selectedPiece == None:
                    app.checkersGame.selectPieceOnCell(cellRow, cellCol)
                # else if a piece is selected
                else:
                    app.checkersGame.selectMoveforSelectedPiece(cellRow, cellCol)

                # Check for a winner after the move
                app.winner = app.checkersGame.checkersBoard.gameWon()
                if app.winner != None:
                    app.gameOver = True
                elif app.checkersGame.noLegalMoves() != None:
                    app.winner = app.checkersGame.noLegalMoves()
                    app.gameOver = True


def onKeyPress(app, key):
    # toggling hints on and off
    if app.gameStarted and key == 'h':
        app.hint = not app.hint
        if app.hint:
            app.hintCell, app.hintPieceCell = app.checkersGame.generateHint()
        else:
            app.hintCell = None
            app.hintPieceCell = None


def getCellFromMousePress(app, x, y):
    # calculate col and row number
    col = int((x - app.checkersGame.checkersBoard.boardLeft) // 
              app.checkersGame.checkersBoard.cellWidth)
    row = int((y - app.checkersGame.checkersBoard.boardTop) // 
              app.checkersGame.checkersBoard.cellHeight)
    # check if cell is within bounds
    if 0<=row<=7 and 0<=col<=7:
        return row, col
    else:
        return None, None
    

# citation: referred to sound demo on piazza
def loadSound(relativePath):
    # Convert to absolute path (because pathlib.Path only takes absolute paths)
    absolutePath = os.path.abspath(relativePath)
    # Get local file URL
    url = pathlib.Path(absolutePath).as_uri()
    # Load Sound file from local URL
    return Sound(url)


def main():
    runApp()


main()

# citation: overall game structure was inspired by Python/Pygame Checkers Tutorial
# (Part 2) - Pieces and Movement: https://youtu.be/LSYj8GZMjWY?si=vnmlBQ62pe5NdFV