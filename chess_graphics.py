import os
import pygame
import chess_pieces
import chess_speech

pygame.init()

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Chess")
screenRect = screen.get_rect()
#background
background = pygame.Surface(screen.get_size())
background.fill((100, 100, 100))
background = background.convert()

#chess board
cellSize = 80
chessboardwidth = cellSize*8
chessboardheight = cellSize*8
chessboardsurface = pygame.Surface((chessboardwidth, chessboardheight))
chessboardsurface.fill((232,50,239))
chessboardsurface = chessboardsurface.convert()
chessboardsurfaceRect = chessboardsurface.get_rect()

#we want to define everything from the screen
#setting offset
promotionSurfaceX = 800
promotionSurfaceY = 45
boardOffsetX = (screenRect.width - chessboardsurfaceRect.width)//2 - 100
boardOffsetY = (screenRect.height - chessboardsurfaceRect.height)//2 - 40

#Defining some common things
numtoalpha = {1:"a", 2:"b", 3:"c", 4:"d", 5:"e", 6:"f", 7:"g", 8:"h"}
clock = pygame.time.Clock()
red = (200,0,0)
orange = (200, 140, 0)
green = (0,200,0)
moderate_opal = (76, 178, 161)
bright_red = (255,0,0)
bright_orange = (255, 165, 0)
bright_green = (0,255,0)
light_opal = (127, 229, 212)

class Matrix:
    def __init__(self):
        self.graphic_cells = []
    def getGraphicCell(self, cellid):
        for cell in self.graphic_cells:
            if cell.id==cellid:
                return cell
    def push(self, cell):
        self.graphic_cells.append(cell)

class GraphicCell:
    def __init__(self, id, colour, x, y):
        self.cellsurface = pygame.Surface((cellSize, cellSize), flags=pygame.SRCALPHA)
        self.cellsurface.fill(colour)

        #remove black color from background of pieces if any
        #self.cellsurface.set_colorkey((0,0,0))
        #This is just for shape
        #in future if we want circle then we can do it easily
        pygame.draw.rect(self.cellsurface, colour, (0, 0, cellSize, cellSize))
        self.cellsurface = self.cellsurface.convert()

        chessboardsurface.blit(self.cellsurface, (x, y))
        #Cell remember its positionm as well as colour
        self.x = x
        self.y = y
        self.colour = colour

        self.id = id
    def updateGraphics(self, image):
        self.cellsurface.fill(self.colour)
        self.cellsurface.blit(image, (0,0))
        chessboardsurface.blit(self.cellsurface, (self.x, self.y))
    def selectedHighlight(self, image):
        tmpcolor = self.colour
        tmpcolor = (tmpcolor[0]-50, tmpcolor[1]-50, tmpcolor[2]-50)
        self.cellsurface.fill(tmpcolor)
        self.cellsurface.blit(image, (0,0))
        chessboardsurface.blit(self.cellsurface, (self.x, self.y))

#One time setup

#initiate the matrix class to hold all the graphic cells
matrix = Matrix()

#initiate the graphic board
for i in range(8):
    c = numtoalpha[i+1]
    if i%2==0:
        for j in range(8):
            if j%2==0:
                matrix.push(GraphicCell(c+str(j+1), (125, 135, 150), i*cellSize, cellSize*8-(j+1)*cellSize))
            else:
                matrix.push(GraphicCell(c+str(j+1), (232, 235, 239), i*cellSize, cellSize*8-(j+1)*cellSize))
    else:
        for j in range(8):
            if j%2==0:
                matrix.push(GraphicCell(c+str(j+1), (232, 235, 239), i*cellSize, cellSize*8-(j+1)*cellSize))
            else:
                matrix.push(GraphicCell(c+str(j+1), (125, 135, 150), i*cellSize, cellSize*8-(j+1)*cellSize))

#get the images
#loading the graphics
whitepawn = pygame.image.load(os.path.join("images", "chess_whitepawn.png"))
whitebishop = pygame.image.load(os.path.join("images", "chess_whitebishop.png"))
whiterook = pygame.image.load(os.path.join("images", "chess_whiterook.png"))
whitequeen = pygame.image.load(os.path.join("images", "chess_whitequeen.png"))
whiteking = pygame.image.load(os.path.join("images", "chess_whiteking.png"))
whiteknight = pygame.image.load(os.path.join("images", "chess_whiteknight.png"))
blackpawn = pygame.image.load(os.path.join("images", "chess_blackpawn.png"))
blackbishop = pygame.image.load(os.path.join("images", "chess_blackbishop.png"))
blackrook = pygame.image.load(os.path.join("images", "chess_blackrook.png"))
blackqueen = pygame.image.load(os.path.join("images", "chess_blackqueen.png"))
blackking = pygame.image.load(os.path.join("images", "chess_blackking.png"))
blackknight = pygame.image.load(os.path.join("images", "chess_blackknight.png"))
#scale them and display it on the screen 
whitepawn = pygame.transform.scale(whitepawn, (cellSize, cellSize)).convert_alpha()
whitebishop = pygame.transform.scale(whitebishop, (cellSize, cellSize)).convert_alpha()
whiterook = pygame.transform.scale(whiterook, (cellSize, cellSize)).convert_alpha()
whitequeen = pygame.transform.scale(whitequeen, (cellSize, cellSize)).convert_alpha()
whiteking = pygame.transform.scale(whiteking, (cellSize, cellSize)).convert_alpha()
whiteknight = pygame.transform.scale(whiteknight, (cellSize, cellSize)).convert_alpha()
blackpawn = pygame.transform.scale(blackpawn, (cellSize, cellSize)).convert_alpha()
blackbishop = pygame.transform.scale(blackbishop, (cellSize, cellSize)).convert_alpha()
blackrook = pygame.transform.scale(blackrook, (cellSize, cellSize)).convert_alpha()
blackqueen = pygame.transform.scale(blackqueen, (cellSize, cellSize)).convert_alpha()
blackking = pygame.transform.scale(blackking, (cellSize, cellSize)).convert_alpha()
blackknight = pygame.transform.scale(blackknight, (cellSize, cellSize)).convert_alpha()
#first of all, load the transparent file and then scale it
#to empty the surface, this is required
#moveGraphics() needs this to update the position
emptyGraphics = pygame.image.load(os.path.join("images", "transparent_empty.png"))
emptyGraphics = pygame.transform.scale(emptyGraphics, (cellSize, cellSize)).convert_alpha()

#initiate the instances
chessboard = chess_pieces.Board()
speech = False

def createGraphics(graphic, pos):
	#update the graphics
	(matrix.getGraphicCell(pos)).updateGraphics(graphic)

def createStandardBoard():
    wp1 = chess_pieces.Pawn(chessboard, "pawn", "a2", "white", whitepawn)
    wp2 = chess_pieces.Pawn(chessboard, "pawn", "b2", "white", whitepawn)
    wp3 = chess_pieces.Pawn(chessboard, "pawn", "c2", "white", whitepawn)
    wp4 = chess_pieces.Pawn(chessboard, "pawn", "d2", "white", whitepawn)
    wp5 = chess_pieces.Pawn(chessboard, "pawn", "e2", "white", whitepawn)
    wp6 = chess_pieces.Pawn(chessboard, "pawn", "f2", "white", whitepawn)
    wp7 = chess_pieces.Pawn(chessboard, "pawn", "g2", "white", whitepawn)
    wp8 = chess_pieces.Pawn(chessboard, "pawn", "h2", "white", whitepawn)

    bp1 = chess_pieces.Pawn(chessboard, "pawn", "a7", "black", blackpawn)
    bp2 = chess_pieces.Pawn(chessboard, "pawn", "b7", "black", blackpawn)
    bp3 = chess_pieces.Pawn(chessboard, "pawn", "c7", "black", blackpawn)
    bp4 = chess_pieces.Pawn(chessboard, "pawn", "d7", "black", blackpawn)
    bp5 = chess_pieces.Pawn(chessboard, "pawn", "e7", "black", blackpawn)
    bp6 = chess_pieces.Pawn(chessboard, "pawn", "f7", "black", blackpawn)
    bp7 = chess_pieces.Pawn(chessboard, "pawn", "g7", "black", blackpawn)
    bp8 = chess_pieces.Pawn(chessboard, "pawn", "h7", "black", blackpawn)

    wb1 = chess_pieces.Bishop(chessboard, "bishop", "c1", "white", whitebishop)
    wb2 = chess_pieces.Bishop(chessboard, "bishop", "f1", "white", whitebishop)
    bb1 = chess_pieces.Bishop(chessboard, "bishop", "c8", "black", blackbishop)
    bb2 = chess_pieces.Bishop(chessboard, "bishop", "f8", "black", blackbishop)

    wr1 = chess_pieces.Rook(chessboard, "rook", "a1", "white", whiterook)
    wr2 = chess_pieces.Rook(chessboard, "rook", "h1", "white", whiterook)
    br1 = chess_pieces.Rook(chessboard, "rook", "a8", "black", blackrook)
    br2 = chess_pieces.Rook(chessboard, "rook", "h8", "black", blackrook)

    wn1 = chess_pieces.Knight(chessboard, "knight", "b1", "white", whiteknight)
    wn2 = chess_pieces.Knight(chessboard, "knight", "g1", "white", whiteknight)
    bn1 = chess_pieces.Knight(chessboard, "knight", "b8", "black", blackknight)
    bn2 = chess_pieces.Knight(chessboard, "knight", "g8", "black", blackknight)

    wq1 = chess_pieces.Queen(chessboard, "queen", "d1", "white", whitequeen)
    bq1 = chess_pieces.Queen(chessboard, "queen", "d8", "black", blackqueen)
    wk1 = chess_pieces.King(chessboard, "king", "e1", "white", whiteking)
    bk1 = chess_pieces.King(chessboard, "king", "e8", "black", blackking)

    createGraphics(wp1.image, wp1.square)
    createGraphics(wp2.image, wp2.square)
    createGraphics(wp3.image, wp3.square)
    createGraphics(wp4.image, wp4.square)
    createGraphics(wp5.image, wp5.square)
    createGraphics(wp6.image, wp6.square)
    createGraphics(wp7.image, wp7.square)
    createGraphics(wp8.image, wp8.square)

    createGraphics(bp1.image, bp1.square)
    createGraphics(bp2.image, bp2.square)
    createGraphics(bp3.image, bp3.square)
    createGraphics(bp4.image, bp4.square)
    createGraphics(bp5.image, bp5.square)
    createGraphics(bp6.image, bp6.square)
    createGraphics(bp7.image, bp7.square)
    createGraphics(bp8.image, bp8.square)

    createGraphics(wb1.image, wb1.square)
    createGraphics(wb2.image, wb2.square)
    createGraphics(bb1.image, bb1.square)
    createGraphics(bb2.image, bb2.square)

    createGraphics(wr1.image, wr1.square)
    createGraphics(wr2.image, wr2.square)
    createGraphics(br1.image, br1.square)
    createGraphics(br2.image, br2.square)

    createGraphics(wn1.image, wn1.square)
    createGraphics(wn2.image, wn2.square)
    createGraphics(bn1.image, bn1.square)
    createGraphics(bn2.image, bn2.square)

    createGraphics(wq1.image, wq1.square)
    createGraphics(bq1.image, bq1.square)
    createGraphics(wk1.image, wk1.square)
    createGraphics(bk1.image, bk1.square)

def moveGraphics(graphic, initial, final):
    
    (matrix.getGraphicCell(initial)).updateGraphics(emptyGraphics)
    (matrix.getGraphicCell(final)).updateGraphics(emptyGraphics)
    graphicsToShift = pygame.transform.scale(graphic, (cellSize, cellSize))
    (matrix.getGraphicCell(final)).updateGraphics(graphicsToShift)
def removeGraphics(curSquare):
    (matrix.getGraphicCell(curSquare)).updateGraphics(emptyGraphics)

def getCellName(coordinates):
    x = coordinates[0] - boardOffsetX
    y = coordinates[1] - boardOffsetY
    
    try:
        col = numtoalpha[x//cellSize + 1]
        row = 8 - y//cellSize
    except:
        return
    
    return col+str(row)

def highlightActive(square, image):
    gc = matrix.getGraphicCell(square)
    gc.selectedHighlight(image)
def dishighlightActive(square, image):
    gc = matrix.getGraphicCell(square)
    gc.updateGraphics(image)
def changeColor(curcolor):
    if curcolor=="white":
        return "black"
    elif curcolor=="black":
        return "white"
    else:
        return None

#creating the stamdard board to play
#in future fischer board or others are possible
createStandardBoard()

def quitgame():
    quit()
#for rendering text
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
#for toggling speech
def toggleSpeech():
    global speech
    speech = not(speech)
#for creating buttons
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText, (0,0,0))
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)
#menu
def menu():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.fill((255, 255, 255))
        largeText = pygame.font.SysFont("comicsansms",115)
        titleSurf, titleRect = text_objects("Smart Chess", largeText, (0,0,0))
        titleRect.center = ((screenRect.width/2),(screenRect.height/2) - 200)
        screen.blit(titleSurf, titleRect)

        button("PLAY",220,400,100,50,green,bright_green,play)
        button("TOGGLE SPEECH: ",420,400,175,50,orange,bright_orange,toggleSpeech)
        smallText = pygame.font.SysFont("comicsansms",32)
        if speech==True:
            txtState = "Speech: ON"
        else:
            txtState = "Speech: OFF"
        speechSurf, speechRect = text_objects(txtState, smallText, (0,0,0))
        speechRect.center = ((screenRect.width/2),(screenRect.height/2) +200)
        screen.blit(speechSurf, speechRect)

        button("QUIT",695,400,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(5)
def intro():

    i = 0
    #intro background for chess board
    bgIntro = pygame.Surface((640, 640))
    r = 0
    g = 0
    b = 0
    bgIntro.fill((r,g,b))
    bgIntro = bgIntro.convert()

    while i<50:
        r += 10
        g += 10
        b += 10
        bgIntro.fill((r,g,b))
        background.blit(bgIntro, (boardOffsetX, boardOffsetY))
        screen.blit(background, (0,0))
        pygame.display.flip()
        i += 2
        pygame.time.delay(50)
def createPromotionSurface(colour):
    promotionSurface = pygame.Surface((2*cellSize, 2*cellSize)).convert_alpha()
    promotionSurface.fill((50, 50, 50, 100))

    if colour=="white":
        imgs = [whitequeen, whiterook, whiteknight, whitebishop]
    else:
        imgs = [blackqueen, blackrook, blackknight, blackbishop]
    pygame.draw.rect(promotionSurface, (200, 200, 200), (0, 0, cellSize, cellSize), 1)
    promotionSurface.blit(imgs[0], (0, 0))
    pygame.draw.rect(promotionSurface, (200, 200, 200), (cellSize, 0, cellSize, cellSize), 1)
    promotionSurface.blit(imgs[1], (cellSize, 0))
    pygame.draw.rect(promotionSurface, (200, 200, 200), (0, cellSize, cellSize, cellSize), 1)
    promotionSurface.blit(imgs[2], (0, cellSize))
    pygame.draw.rect(promotionSurface, (200, 200, 200), (cellSize, cellSize, cellSize, cellSize), 1)
    promotionSurface.blit(imgs[3], (cellSize, cellSize))

    return promotionSurface

#MOST IMPORTANT FUNCTION
#CONTROLLING THE FLOW OF THE GAME
def play():
    #defining some variables
    activeSquare = False
    initialsquare = None
    movingsquare = None
    pieceToMove = None
    playPossible = False
    disableBoard = False
    colorTurn = "white" #because first to move will be white

    mainloop = True
    intro()

    while mainloop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False # pygame window closed by user
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
            #the below code multiple clicks if mouse moves
            #if pygame.mouse.get_pressed()[0]:
                #for DEBUGGING purposes
                #print("Active:",activeSquare,"initial:",initialsquare,"moving:",movingsquare,"piece:",pieceToMove,"playpossible:",playPossible)
                if activeSquare:
                    #we are getting the squares by mouse click
                    #ADD-ON: WE CAN DO SPEECH CONTROL
                    if speech:
                        movingsquare = chess_speech.promptSpeech()
                    else:
                        movingsquare = getCellName(pygame.mouse.get_pos())

                    dishighlightActive(initialsquare, pieceToMove.image)
                    playPossible = True
                    activeSquare = False
                else:
                    if speech:
                        clickedSquare = chess_speech.promptSpeech()
                    else:
                        clickedSquare = getCellName(pygame.mouse.get_pos())

                    if clickedSquare==None:
                        continue
                    clickedCell = chessboard.getCell(clickedSquare)
                    if clickedCell==None:
                        continue
                    if clickedCell.piece!=None and clickedCell.piece.colour==colorTurn:
                        pieceToMove = chessboard.getCell(clickedSquare).piece
                        initialsquare = clickedSquare
                        activeSquare = True
                        highlightActive(initialsquare, pieceToMove.image)
                #print("Active:",activeSquare,"initial:",initialsquare,"moving:",movingsquare,"piece:",pieceToMove,"playpossible:",playPossible)
                if playPossible:
                    if pieceToMove.move(movingsquare):
                        #if (chess_pieces.checkmate(chessboard, changeColor(colorTurn))):
                        #   print("Checkmate")

                        #Check for promotion here, there might be a better way
                        #but for now this will do
                        if pieceToMove.identityClass=="pawn":
                            if pieceToMove.isPromotionPossible():
                                #promotion screen
                                promotionSurface = createPromotionSurface(pieceToMove.colour)
                                isPromotionDone = False
                                #while not(isPromotionDone):
                                #   event = pygame.event.wait()
                                #  if event.type == pygame.MOUSEBUTTONDOWN:
                                #put check and conditions for promotion buttons clicked

                                disableBoard = True

                        moveGraphics(pieceToMove.image, initialsquare, movingsquare)
                        colorTurn = changeColor(colorTurn)
                    elif pieceToMove.kill(movingsquare):
                        #if (chess_pieces.checkmate(chessboard, changeColor(colorTurn))):
                        #   print("Checkmate")
                        moveGraphics(pieceToMove.image, initialsquare, movingsquare)
                        #the color has to change because either the piece has
                        #killed or moved somewhere
                        colorTurn = changeColor(colorTurn)
                    else:
                        #check for castling
                        if pieceToMove.identityClass=="king":
                            canCastle, castlingRook, rooksCurrentSquare, rooksMovingSquare = pieceToMove.castle(movingsquare)
                            if canCastle:
                                moveGraphics(pieceToMove.image, initialsquare, movingsquare)
                                moveGraphics(castlingRook.image, rooksCurrentSquare, rooksMovingSquare)
                                colorTurn = changeColor(colorTurn)
                        #check for en passant
                        elif pieceToMove.identityClass=="pawn":
                            canEnPassant, cellToBeRemoved = pieceToMove.enPassant(movingsquare)
                            if canEnPassant:
                                moveGraphics(pieceToMove.image, initialsquare, movingsquare)
                                removeGraphics(cellToBeRemoved)
                                colorTurn = changeColor(colorTurn)
                    initialsquare = None
                    movingsquare = None
                    pieceToMove = None
                    playPossible = False

        if disableBoard:
            background.blit(promotionSurface, (promotionSurfaceX,promotionSurfaceY))

        background.blit(chessboardsurface, (boardOffsetX, boardOffsetY))
        
        screen.blit(background, (0,0))
        button("BACK",815,75,100,50,moderate_opal,light_opal,menu)
        colorText = pygame.font.SysFont("timesnewroman",32)
        colorSurf, colorRect = text_objects("Current player:"+colorTurn, colorText, (240, 240, 240))
        colorRect.center = (860,200)
        screen.blit(colorSurf, colorRect)
        pygame.display.flip()

#just play the game
#in future we can toggle it on and off
#play()
menu()

#i could have make layer system to dispaly different menus
#but this also works, i will do that later