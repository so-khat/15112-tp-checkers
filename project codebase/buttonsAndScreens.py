from cmu_graphics import *
from PIL import Image


def startScreen(app):
    # draw logo
    imageWidth, imageHeight = getImageSize(app.logoIMG)
    drawImage(app.logoIMG, 340, 260, 
              width=imageWidth/3, height=imageHeight/3, align='center')

    # draw Single Player Mode box
    singlePlayerColor = gradient('lightSeaGreen', 'mediumSpringGreen', 
                                 'lightSeaGreen', start='left')
    singlePlayerFactor = 1 if not app.singlePlayerButtonHovered else 1.2
    drawRect(200, 500, 250*singlePlayerFactor, 100*singlePlayerFactor, 
             fill=singlePlayerColor, 
             border='black', 
             borderWidth = 2 if not app.singlePlayerButtonHovered else 3,
             align='center')
    drawLabel('Single Player Mode', 200, 490, 
              size = 25 if not app.singlePlayerButtonHovered else 30, 
              bold = False if not app.singlePlayerButtonHovered else True)
    drawLabel('play against an AI bot', 200, 520, 
              size = 15 if not app.singlePlayerButtonHovered else 18)

    # draw Multiplayer Mode box
    multiplayerColor = gradient('dodgerBlue', 'deepSkyBlue', 
                                 'dodgerBlue', start='left')
    multiplayerFactor = 1 if not app.multiplayerButtonHovered else 1.2
    drawRect(500, 500, 250*multiplayerFactor, 100*multiplayerFactor, 
             fill=multiplayerColor, 
             border='black', 
             borderWidth = 2 if not app.multiplayerButtonHovered else 3,
             align='center')
    drawLabel('Multiplayer Mode', 500, 490, 
              size = 25 if not app.multiplayerButtonHovered else 30, 
              bold = False if not app.multiplayerButtonHovered else True)
    drawLabel('play against your friends', 500, 520, 
              size = 15 if not app.multiplayerButtonHovered else 18)

    # draw Rules box
    rulesColor = gradient('brown', 'chocolate', 
                          'brown', start='left')
    rulesFactor = 1 if not app.rulesButtonHovered else 1.2
    drawRect(200, 600, 150*rulesFactor, 50*rulesFactor, 
             fill=rulesColor, 
             border='black', 
             borderWidth = 2 if not app.rulesButtonHovered else 3, 
             align='center')
    drawLabel('Rules & Info', 200, 600, 
              size = 17 if not app.rulesButtonHovered else 20, 
              bold = False if not app.rulesButtonHovered else True)
    
    # draw Themes box
    themesColor = gradient('blueViolet', 'mediumSlateBlue', 
                           'blueViolet', start='left')
    themesFactor = 1 if not app.themesButtonHovered else 1.2
    drawRect(500, 600, 150*themesFactor, 50*themesFactor, 
             fill=themesColor, 
             border='black', 
             borderWidth = 2 if not app.themesButtonHovered else 3,
             align='center')
    drawLabel('Themes', 500, 600, 
              size = 17 if not app.themesButtonHovered else 20, 
              bold = False if not app.themesButtonHovered else True)


def aiLevelSelectionScreen():
    drawLabel('Choose a difficulty level for your AI opponent:', 350, 200, size = 32)
    
    # draw Easy level box
    drawRect(99.5, 350, 149, 100, fill='green', border='black', align='center')
    drawLabel('Easy', 99.5, 350, size=20)

    # draw Medium level box
    drawRect(266.5, 350, 149, 100, fill='yellow', border='black', align='center')
    drawLabel('Medium', 266.5, 350, size=20)

    # draw Hard level box
    drawRect(433.5, 350, 149, 100, fill='orange', border='black', align='center')
    drawLabel('Hard', 433.5, 350, size=20)

    # draw Expert level box
    drawRect(600.5, 350, 149, 100, fill='red', border='black', align='center')
    drawLabel('Expert', 600.5, 350, size=20)


def undoButton():
    # draw undo button
    factor = 1 if not app.undoButtonHovered else 1.2
    unhoveredColor = gradient('silver', 'slateGray', 'lightSlateGray', 
                               'slateGray', 'silver', start='top')
    hoveredColor = gradient('gold', 'orange', 'yellow', 
                            'orange', 'gold', start='top')
    drawRect(562.5, 635, 75*factor, 50*factor, 
             fill=unhoveredColor if not app.undoButtonHovered else hoveredColor, 
             border='black', 
             borderWidth = 2 if not app.undoButtonHovered else 3, align='center')
    drawLabel('UNDO', 562.5, 635, size=18*factor, 
              bold = False if not app.undoButtonHovered else True)
 

def rulesScreen():
    # Title
    drawLabel("Rules & Info", 350, 50, size = 30)

    # Gameplay Section
    drawLabel("Gameplay:", 30, 110, size=25, align='left')

    drawLabel("- Movement", 30, 140, size=20, align='left')
    drawLabel("  • Pieces can move diagonally forward into an adjacent empty cell", 
              30, 165, align='left')
    
    drawLabel("- Captures", 30, 195, size=20, align='left')
    drawLabel("  • Pieces can capture opponent pieces diagonally by 'jumping' over them diagonally", 
              30, 220, align='left')
    drawLabel("  • Multiple captures can be made in a single turn if the piece jumps to a cell where another capture is possible", 
              30, 240, align='left')
    drawLabel("  • Capturing a piece is not mandatory", 30, 260, align='left')

    drawLabel("- Kings", 30, 290, size=20, align='left')
    drawLabel("  • When a piece reaches the opponent's back row, it is crowned a king", 
              30, 315, align='left')
    drawLabel("  • Regular pieces can only move and capture forward, but King pieces can move and capture both forwards and backwards", 
              30, 335, align='left')

    # Extra Features Section
    drawLabel("Extra Features:", 30, 380, size=25, align='left')

    drawLabel("- Hints", 30, 410, size=20, align='left', font='symbols')
    drawLabel("  • Hints can be toggled on and off by pressing 'h'", 
              30, 435, align='left')
    
    drawLabel("- Undo Move", 30, 465, size=20, align='left')
    drawLabel("  • Moves can be undone by pressing the 'UNDO' button", 
              30, 490, align='left')
    
    drawLabel("- Themes & Background Music", 30, 520, size=20, align='left')
    drawLabel("  • The board's theme can be changed from the home screen", 
              30, 545, align='left')
    drawLabel("  • Each theme has a background song that goes along with it", 
              30, 565, align='left')
    drawLabel("  • You can start and stop the music with the volume button at the top right part of the screen", 
              30, 585, align='left')
    
    drawLabel("- Home Button", 30, 615, size=20, align='left')
    drawLabel("  • You can return to the start screen anytime by pressing the home button at the top left part of the screen", 
              30, 640, align='left')


def themesScreen():
    # draw the title and boxes for different themes
    drawLabel('Choose a Theme:', 350, 100, size = 30)

    drawRect(212.5, 250, 250, 100, 
             fill=gradient('red','maroon',start='left-top'), 
             border='black', 
             align='center')
    drawLabel('Classic Theme', 212.5, 250, size = 20)

    drawRect(487.5, 250, 250, 100, 
             fill=gradient('darkGreen','lime',start='left-top'), 
             border='black', 
             align='center')
    drawLabel('Forest Theme', 487.5, 250, size=20)

    drawRect(212.5, 375, 250, 100, 
             fill=gradient('magenta','indigo',start='left-top'), 
             border='black', 
             align='center')
    drawLabel('Candy Theme', 212.5, 375, size=20)

    drawRect(487.5, 375, 250, 100, 
             fill=gradient('blue','lightBlue',start='left-top'), 
             border='black', 
             align='center')
    drawLabel('Ocean Theme', 487.5, 375, size=20)


def changeTheme(app):
    # update the theme and song
    if app.themeSelected == 1:
        app.checkersGame.checkersBoard.color1 = 'cornSilk'
        app.checkersGame.checkersBoard.color2 = 'burlyWood'
        app.checkersGame.checkersBoard.color3 = 'saddleBrown'
        app.checkersGame.checkersBoard.color4 = 'sienna'
        app.song.pause()
        app.song = app.classicThemeSong
        if app.volume:
            app.song.play(restart=True, loop=True)
    elif app.themeSelected == 2:
        app.checkersGame.checkersBoard.color1 = 'lime'
        app.checkersGame.checkersBoard.color2 = 'lawnGreen'
        app.checkersGame.checkersBoard.color3 = 'teal'
        app.checkersGame.checkersBoard.color4 = 'forestGreen'
        app.song.pause()
        if app.volume:
            app.song = app.forestThemeSong
        app.song.play(restart=True, loop=True)
    elif app.themeSelected == 3:
        app.checkersGame.checkersBoard.color1 = 'violet'
        app.checkersGame.checkersBoard.color2 = 'orchid'
        app.checkersGame.checkersBoard.color3 = 'darkViolet'
        app.checkersGame.checkersBoard.color4 = 'blueViolet' 
        app.song.pause()
        app.song = app.candyThemeSong 
        if app.volume:
            app.song.play(restart=True, loop=True) 
    elif app.themeSelected == 4:
        app.checkersGame.checkersBoard.color1 = 'dodgerBlue'
        app.checkersGame.checkersBoard.color2 = 'cornflowerBlue'
        app.checkersGame.checkersBoard.color3 = 'mediumBlue'
        app.checkersGame.checkersBoard.color4 = 'navy'
        app.song.pause()
        app.song = app.oceanThemeSong
        if app.volume:
            app.song.play(restart=True, loop=True)
    app.checkersGame.checkersBoard.oddSquareColor = gradient(app.checkersGame.checkersBoard.color1,
                                                            app.checkersGame.checkersBoard.color2, 
                                                            app.checkersGame.checkersBoard.color1, 
                                                            app.checkersGame.checkersBoard.color2, 
                                                            app.checkersGame.checkersBoard.color1, 
                                                            app.checkersGame.checkersBoard.color2, 
                                                            app.checkersGame.checkersBoard.color1, 
                                                            app.checkersGame.checkersBoard.color2, 
                                                            start='left')
    app.checkersGame.checkersBoard.evenSquareColor = gradient(app.checkersGame.checkersBoard.color3, 
                                                              app.checkersGame.checkersBoard.color4, 
                                                              app.checkersGame.checkersBoard.color3, 
                                                              app.checkersGame.checkersBoard.color4, 
                                                              app.checkersGame.checkersBoard.color3, 
                                                              app.checkersGame.checkersBoard.color4, 
                                                              app.checkersGame.checkersBoard.color3, 
                                                              app.checkersGame.checkersBoard.color4, 
                                                              start='top')


def homeButton(app):
    imageWidth, imageHeight = getImageSize(app.homeButtonIMG)
    factor = 50 if not app.homeButtonHovered else 40
    drawImage(app.homeButtonIMG, 50, 50, width=imageWidth/factor, 
              height=imageHeight/factor, align='center')
            

def volumeButton(app):
    # draw respective buttons for volume on and off
    imageWidth, imageHeight = getImageSize(app.volumeONIMG)
    factor = 7 if not app.volumeButtonHovered else 5.7
    if app.volume:
        drawImage(app.volumeONIMG, 650, 50, width=imageWidth/factor, 
                height=imageHeight/factor, align='center')
    else:
        drawImage(app.volumeOFFIMG, 650, 50, width=imageWidth/factor, 
                height=imageHeight/factor, align='center')