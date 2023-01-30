import move_storage
import pdb

ms = move_storage.MoveStore()
class Board:
	rowNames = ["1","2","3","4","5","6","7","8"]
	columnNames = ["a","b","c","d","e","f","g","h"]
	def __init__(self):
		#Initiate 8x8 cells
		self.rows = []
		self.columns = [Column(colname) for colname in self.columnNames]
		#Might optimise this later

		for col in self.columns:
			for row in self.rowNames:
				col.push(Cell(col.columnId + row))
		for i in range(8):
			r = Row(self.rowNames[i])
			for x in self.columns:
				r.cells.append(x.cells[i])
			self.rows.append(r)

	def getCell(self, cellid):
		for col in self.columns:
			if cellid[0]==col.columnId:
				for cell in col.cells:
					if cell.name[1]==cellid[1]:
						return cell
	def getColumn(self, cellid):
		for col in self.columns:
			if cellid[0]==col.columnId:
				return col
	def getRow(self, cellid):
		for row in self.rows:
			if cellid[1]==row.rowId:
				return row
	def remove(self, pieceToBeRemoved):
		#This i made just for en passant
		#could have better use later on
		pieceToBeRemoved.currentcell.update(None)
	def boardState(self):
		allCells = []
		for col in self.columns:
			for c in col.cells:
				allCells.append(c)
		return allCells
class Row:
	def __init__(self, rowId):
		self.rowId = rowId
		self.cells = []
	def moveRight(self, cell):
		for i, c in enumerate(self.cells):
			if cell==c and i!=len(self.cells)-1:
				return self.cells[i+1]
		return None
	def moveLeft(self, cell):
		for i, c in enumerate(self.cells):
			if cell==c and i!=0:
				return self.cells[i-1]
		return None
class Column:
	def __init__(self, columnId):
		self.columnId = columnId
		self.cells = []
	def push(self, cell):
		self.cells.append(cell)
	def moveUp(self, cell):
		for i, c in enumerate(self.cells):
			if cell==c and i!=len(self.cells)-1:
				return self.cells[i+1]
		return None
	def moveDown(self, cell):
		for i, c in enumerate(self.cells):
			if cell==c and i!=0:
				return self.cells[i-1]
		return None
	#used for debugging
	def __str__(self):
		return " ".join([x.name for x in self.cells])
		
class Cell:
	def __init__(self, name):
		self.name = name
		self.piece = None
		self.occupied = False
	def update(self, piece):
		self.piece = piece
		if self.piece != None:
			self.occupied = True
		else:
			self.occupied = False

#Check whether the king is in check
def isKingInCheck(board, color):
	opponentPieces = []
	kingsCell = None
	boardState = board.boardState()
	for cell in boardState:
		if cell.piece!=None:
			if cell.piece.colour!=color:
				opponentPieces.append(cell.piece)
			else:
				if cell.piece.identityClass=="king":
					kingsCell = cell.piece.currentcell
	for opponent in opponentPieces:
		oppInitSquare = opponent.currentcell
		if opponent.kill(kingsCell.name):
			opponent.updateDetails(oppInitSquare)
			kingsCell.update(ms.killedPieces.pop())
			return True
	return False

class Piece:
	def __init__(self, board, identityClass, square, colour, image):
		self.square = square
		self.board = board
		self.colour = colour
		#we are creating identityClass to avoid the use of isinstance function
		self.identityClass = identityClass

		#Get the cell for updating purposes
		self.currentcell = board.getCell(square)

		#The square will be provided from outside
		#and that will be the current square
		#Fill the cell first by updating it.
		self.currentcell.update(self)

		#getting the row and column of current square
		for col in board.columns:
			if col.columnId==square[0]:
				self.currentColumn = col
				break
		for row in board.rows:
			if row.rowId==square[1]:
				self.currentRow = row
				break
		self.image = image
	def updateDetails(self, newcell):
		if newcell.piece!=None:
			ms.killedPieces.append(newcell.piece)
		newcell.update(self)
		#This will only update the occupied and piece
		self.currentcell.update(None)
		#I also have to update myself
		#other cells has been updated.
		self.square = newcell.name
		self.currentcell = newcell
		self.currentColumn = self.board.getColumn(newcell.name)
		self.currentRow = self.board.getRow(newcell.name)

class Pawn(Piece):
	def __init__(self, board, identityClass, square, colour, image):
		self.firstMove = True
		self.isFirstMoveDouble = False
		Piece.__init__(self, board, identityClass, square, colour, image)
		
	def move(self, square):
		possible=False
		initialcell = self.square

		if (self.currentColumn.columnId==square[0]):
			#normal move
			if not(self.firstMove):
				if self.colour=="white":
					if ((int(self.currentRow.rowId)+1) == int(square[1])):
						cell = self.currentColumn.moveUp(self.currentcell)
						if square == cell.name and cell.occupied==False:
							#Get the cell for updating purposes
							newcell = self.board.getCell(square)
							self.updateDetails(newcell)
							possible = True
				else:
					if ((int(self.currentRow.rowId)-1) == int(square[1])):
						cell = self.currentColumn.moveDown(self.currentcell)
						if square == cell.name and cell.occupied==False:
							#Get the cell for updating purposes
							newcell = self.board.getCell(square)
							self.updateDetails(newcell)
							possible = True
			#first move
			else:
				if self.colour=="white":
					if (int(self.currentRow.rowId) < int(square[1]) <=int(self.currentRow.rowId) + 2):
						firstcell = self.currentColumn.moveUp(self.currentcell)
						if firstcell.occupied==False:
							if firstcell.name==square:
								self.updateDetails(firstcell)
								#first move is over
								self.firstMove = False
								possible = True
						#if it reaches here that means first cell was not the square
						secondcell = self.currentColumn.moveUp(firstcell)
						if secondcell.occupied==False:
							if secondcell.name==square:
								self.updateDetails(secondcell)
								#first move is over
								self.firstMove = False
								self.isFirstMoveDouble = True
								possible = True
				else:
					if ((int(self.currentRow.rowId)-2) <= int(square[1]) <int(self.currentRow.rowId)):
						firstcell = self.currentColumn.moveDown(self.currentcell)
						if firstcell.occupied==False:
							if firstcell.name==square:
								self.updateDetails(firstcell)
								#first move is over
								self.firstMove = False
								possible = True
						#if it reaches here that means first cell was not the square
						secondcell = self.currentColumn.moveDown(firstcell)
						if secondcell.occupied==False:
							if secondcell.name==square:
								self.updateDetails(secondcell)
								#first move is over
								self.firstMove = False
								self.isFirstMoveDouble = True
								possible = True
		if possible:
			#if isKingInCheck(self.board, self.colour):
			#	self.updateDetails(self.board.getCell(initialcell))
			#	possible=False
			#else:
			#	ms.storeMove(self, "", square)
			ms.storeMove(self, "", square)
		return possible
	def isPromotionPossible(self):
		promotionPossible = False
		if self.colour=="white" and self.currentRow.rowId=="8":
			promotionPossible = True
		elif self.colour=="black" and self.currentRow.rowId=="1":
			promotionPossible = True
		return promotionPossible
	def promote(self, PieceClass, board, identityClass, square, colour, image):
		self = PieceClass()
	def kill(self, square):
		possible=False
		curCellName = self.square
		otherCell = self.board.getCell(square)
		if otherCell==None:
			return
		if otherCell.piece!=None:
			if otherCell.piece.colour!=self.colour:
				#we can first move up for white
				#move down for black
				#and then we can check right and left
				if self.colour == "white":
					interCell = self.currentColumn.moveUp(self.currentcell)
				else:
					interCell = self.currentColumn.moveDown(self.currentcell)
				interRow = self.board.rows[int(interCell.name[1])-1]
				if interRow.moveLeft(interCell)!=None:
					if interRow.moveLeft(interCell).name==square:
						newcell = interRow.moveLeft(interCell)
						self.updateDetails(newcell)
						#first move is over
						self.firstMove = False
						possible = True
						

				if interRow.moveRight(interCell)!=None:
					if interRow.moveRight(interCell).name==square:
						newcell = interRow.moveRight(interCell)
						self.updateDetails(newcell)
						#first move is over
						self.firstMove = False
						possible = True

		if possible:
			#This is how killing move is represented.
			ms.storeMove(self, curCellName[0]+"x", square)
		return possible
	def enPassant(self, square):
		#there is possibilty of en passant
		curCellName = self.square
		removingSquare = None
		possible = False
		prevMove = ms.getPreviousMove()
		prevMovePiece = None
		if prevMove!=None:
			prevMovePiece = prevMove[0]
		else:
			return False, None
		if prevMovePiece.identityClass=="pawn":
			if prevMovePiece.isFirstMoveDouble==True:
				if self.colour == "white":
					interCell = self.currentColumn.moveUp(self.currentcell)
				else:
					interCell = self.currentColumn.moveDown(self.currentcell)
				interRow = self.board.getRow(interCell.name)
				if interRow.moveLeft(interCell)!=None:
					if interRow.moveLeft(interCell).name==square:
						newcell = interRow.moveLeft(interCell)
						pieceToRemove = self.currentRow.moveLeft(self.currentcell).piece
						
						if pieceToRemove==prevMovePiece:
							removingSquare = pieceToRemove.square
							self.board.remove(pieceToRemove)
							self.updateDetails(newcell)
							ms.storeMove(self, curCellName[0]+"x", square)
							possible = True

				if not(possible) and interRow.moveRight(interCell)!=None:
					if interRow.moveRight(interCell).name==square:
						newcell = interRow.moveRight(interCell)
						pieceToRemove = self.currentRow.moveRight(self.currentcell).piece
						if pieceToRemove==prevMovePiece:
							removingSquare = pieceToRemove.square
							self.board.remove(pieceToRemove)
							self.updateDetails(newcell)
							ms.storeMove(self, curCellName[0]+"x", square)
							possible = True
		return possible, removingSquare
class Bishop(Piece):
	def __init__(self, board, identityClass, square, colour, image):
		Piece.__init__(self, board, identityClass, square, colour, image)
	def move(self, square):
		possible=False
		possibleSquares = self.getPossibleSqaures()[0]

		#after getting possible squares, now we can check move
		for diag in possibleSquares:
			for c in diag:
				if c.name==square:
					newcell = self.board.getCell(square)
					self.updateDetails(newcell)
					possible = True
		if possible:
			ms.storeMove(self, "B", square)
		return possible
	def kill(self, square):
		possible = False
		killingSquares = self.getPossibleSqaures()[1]

		for c in killingSquares:
			if c.name==square:
				if c.occupied==True and c.piece.colour!=self.colour:
					newcell = self.board.getCell(square)
					self.updateDetails(newcell)
					possible = True
		if possible:
			ms.storeMove(self, "Bx", square)
		return possible
	def getPossibleSqaures(self):
		#Might optimise the algorithm in future
		possibleMoveSquares = []

		#checking for TOP RIGHT DIAGONAL
		possCell = self.currentcell.name
		rightTop = []
		#by up and then right movement
		while  True:
			icol = self.board.getColumn(possCell)
			inter_up_cell = icol.moveUp(self.board.getCell(possCell))
			if inter_up_cell!=None:
				irow = self.board.getRow(inter_up_cell.name)
				inter_row_cell = irow.moveRight(inter_up_cell)
				if inter_row_cell!=None:
					rightTop.append(inter_row_cell)
					possCell = inter_row_cell.name
				else:
					break
			else:
				break

		#checking for TOP LEFT DIAGONAL
		possCell = self.currentcell.name
		leftTop = []
		#by up and then left movement
		while  True:
			icol = self.board.getColumn(possCell)
			inter_up_cell = icol.moveUp(self.board.getCell(possCell))
			if inter_up_cell!=None:
				irow = self.board.getRow(inter_up_cell.name)
				inter_row_cell = irow.moveLeft(inter_up_cell)
				if inter_row_cell!=None:
					leftTop.append(inter_row_cell)
					possCell = inter_row_cell.name
				else:
					break
			else:
				break
		#checking for BOTTOM LEFT DIAGONAL
		possCell = self.currentcell.name
		leftBottom = []
		#by down and then left movement
		while  True:
			icol = self.board.getColumn(possCell)
			inter_up_cell = icol.moveDown(self.board.getCell(possCell))
			if inter_up_cell!=None:
				irow = self.board.getRow(inter_up_cell.name)
				inter_row_cell = irow.moveLeft(inter_up_cell)
				if inter_row_cell!=None:
					leftBottom.append(inter_row_cell)
					possCell = inter_row_cell.name
				else:
					break
			else:
				break
		#checking for BOTTOM RIGHT DIAGONAL
		possCell = self.currentcell.name
		rightBottom = []
		#by down and then right movement
		while  True:
			icol = self.board.getColumn(possCell)
			inter_up_cell = icol.moveDown(self.board.getCell(possCell))
			if inter_up_cell!=None:
				irow = self.board.getRow(inter_up_cell.name)
				inter_row_cell = irow.moveRight(inter_up_cell)
				if inter_row_cell!=None:
					rightBottom.append(inter_row_cell)
					possCell = inter_row_cell.name
				else:
					break
			else:
				break
		possibleMoveSquares.extend([rightTop, leftTop, leftBottom, rightBottom])
		
		possibleKillingSquares = []
		#eliminate blockade squares
		for indMain, diag in enumerate(possibleMoveSquares):
			for ind, cell in enumerate(diag):
				if cell.occupied:
					diag = diag[:ind]
					possibleMoveSquares[indMain] = diag
					possibleKillingSquares.append(cell)
					break
		return possibleMoveSquares, possibleKillingSquares

class Rook(Piece):
	def __init__(self, board, identityClass, square, colour, image):
		Piece.__init__(self, board, identityClass, square, colour, image)
		self.hasMoved = False
	def move(self, square):
		possible = False
		possibleSquares = self.getPossibleSqaures()[0]

		#after getting possible squares, now we can check move
		for lane in possibleSquares:
			for c in lane:
				if c.name==square:
					newcell = self.board.getCell(square)
					self.updateDetails(newcell)
					self.hasMoved = True
					possible = True
		if possible:
			ms.storeMove(self, "R", square)
		return possible
	def castleMove(self, castleSquare):
		newcell = self.board.getCell(castleSquare)
		self.updateDetails(newcell)
		self.hasMoved = True
	def kill(self, square):
		possible = False
		killingSquares = self.getPossibleSqaures()[1]

		for c in killingSquares:
			if c.name==square:
				if c.occupied==True and c.piece.colour!=self.colour:
					newcell = self.board.getCell(square)
					self.updateDetails(newcell)
					self.hasMoved = True
					possible = True
		if possible:
			ms.storeMove(self, "Rx", square)
		return possible
	def getPossibleSqaures(self):
		#Might optimise the algorithm in future
		possibleMoveSquares = []

		#checking for TOP
		possCell = self.currentcell.name
		top = []
		while  True:
			inter_up_cell = self.currentColumn.moveUp(self.board.getCell(possCell))
			if inter_up_cell!=None:
				top.append(inter_up_cell)
				possCell = inter_up_cell.name
			else:
				break
		#checking for BOTTOM
		possCell = self.currentcell.name
		bottom = []
		while  True:
			inter_down_cell = self.currentColumn.moveDown(self.board.getCell(possCell))
			if inter_down_cell!=None:
				bottom.append(inter_down_cell)
				possCell = inter_down_cell.name
			else:
				break
		#checking for RIGHT
		possCell = self.currentcell.name
		right = []
		while  True:
			inter_right_cell = self.currentRow.moveRight(self.board.getCell(possCell))
			if inter_right_cell!=None:
				right.append(inter_right_cell)
				possCell = inter_right_cell.name
			else:
				break
		#checking for LEFT
		possCell = self.currentcell.name
		left = []
		while  True:
			inter_left_cell = self.currentRow.moveLeft(self.board.getCell(possCell))
			if inter_left_cell!=None:
				left.append(inter_left_cell)
				possCell = inter_left_cell.name
			else:
				break
		possibleMoveSquares.extend([top, bottom, right, left])
		
		possibleKillingSquares = []
		#eliminate blockade squares
		for indMain, lane in enumerate(possibleMoveSquares):
			for ind, cell in enumerate(lane):
				if cell.occupied:
					lane = lane[:ind]
					possibleMoveSquares[indMain] = lane
					possibleKillingSquares.append(cell)
					break
		return possibleMoveSquares, possibleKillingSquares

class Queen(Rook, Bishop):
	def __init__(self, board, identityClass, square, colour, image):
		Piece.__init__(self, board, identityClass, square, colour, image)
	def move(self, square):
		possible = False
		straightPossible = super(Queen, self).getPossibleSqaures()[0]
		diagonalPossible = super(Rook, self).getPossibleSqaures()[0]
		possibleSquares= straightPossible + diagonalPossible

		#after getting possible squares, now we can check move
		for line in possibleSquares:
			for c in line:
				if c.name==square:
					newcell = self.board.getCell(square)
					self.updateDetails(newcell)
					possible = True
		if possible:
			ms.storeMove(self, "Q", square)
		return possible
	def kill(self, square):
		possible = False
		straightKills = super(Queen, self).getPossibleSqaures()[1]
		diagonalKills = super(Rook, self).getPossibleSqaures()[1]
		possibleKills= straightKills + diagonalKills

		for c in possibleKills:
			if c.name==square:
				if c.occupied==True and c.piece.colour!=self.colour:
					newcell = self.board.getCell(square)
					self.updateDetails(newcell)
					possible = True
		if possible:
			ms.storeMove(self, "Qx", square)
		return possible

class King(Piece):
	def __init__(self, board, identityClass, square, colour, image):
		Piece.__init__(self, board, identityClass, square, colour, image)
		self.hasMoved = False
	def move(self, square):
		possible = False
		moveSquares = self.getPossibleSquares()[0]
		for c in moveSquares:
			if c.name==square:
				newcell = self.board.getCell(square)
				self.updateDetails(newcell)

				self.hasMoved = True
				possible = True
		if possible:
			ms.storeMove(self, "K", square)
		return possible

	#CASTLING
	#I can definitely reduce the number of statements but for
	#now it should do
	def castle(self, square):
		rookToMove = None
		initialRookPos = None
		finalRookPos = None
		possible = False

		# i will hard code check for castling
		if self.hasMoved==False:
			#just double checking to be safe
			if self.colour=="white" and self.square=="e1":
				#king side castling
				if self.board.getCell("f1").occupied==False and self.board.getCell("g1").occupied==False:
					pieceToCastle = self.board.getCell("h1").piece
					if pieceToCastle.identityClass == "rook":
						if pieceToCastle.hasMoved==False:
							if square=="g1":
								rookToMove = pieceToCastle
								initialRookPos = rookToMove.square
								finalRookPos = "f1"
								rookToMove.castleMove(finalRookPos)
								ms.storeMove(self, "O-O", "")
								self.updateDetails(self.board.getCell(square))
								possible = True
				#queen side castling
				elif self.board.getCell("d1").occupied==False and self.board.getCell("c1").occupied==False and self.board.getCell("b1").occupied==False:
					pieceToCastle = self.board.getCell("a1").piece
					if pieceToCastle.identityClass == "rook":
						if pieceToCastle.hasMoved==False:
							if square=="c1":
								rookToMove = pieceToCastle
								initialRookPos = rookToMove.square
								finalRookPos = "d1"
								rookToMove.castleMove(finalRookPos)
								ms.storeMove(self, "O-O-O", "")
								self.updateDetails(self.board.getCell(square))
								possible = True
			elif self.colour=="black" and self.square=="e8":
				#king side castling
				if self.board.getCell("f8").occupied==False and self.board.getCell("g8").occupied==False:
					pieceToCastle = self.board.getCell("h8").piece
					if pieceToCastle.identityClass == "rook":
						if pieceToCastle.hasMoved==False:
							if square=="g8":
								rookToMove = pieceToCastle
								initialRookPos = rookToMove.square
								finalRookPos = "f8"
								rookToMove.castleMove(finalRookPos)
								ms.storeMove(self, "O-O", "")
								self.updateDetails(self.board.getCell(square))
								possible = True
				#queen side castling
				elif self.board.getCell("d8").occupied==False and self.board.getCell("c8").occupied==False and self.board.getCell("b8").occupied==False:
					pieceToCastle = self.board.getCell("a8").piece
					if pieceToCastle.identityClass == "rook":
						if pieceToCastle.hasMoved==False:
							if square=="c8":
								rookToMove = pieceToCastle
								initialRookPos = rookToMove.square
								finalRookPos = "d8"
								rookToMove.castleMove(finalRookPos)
								ms.storeMove(self, "O-O-O", "")
								self.updateDetails(self.board.getCell(square))
								possible = True
			else:
				possible = False
		return possible, rookToMove, initialRookPos, finalRookPos

	def kill(self, square):
		possible = False
		killSquares = self.getPossibleSquares()[1]

		for c in killSquares:
			if c.name==square:
				if c.piece.colour!=self.colour: #uneccesary check but still..
					newcell = self.board.getCell(square)
					self.updateDetails(newcell)
					self.hasMoved = True
					possible = True
		if possible:
			ms.storeMove(self, "Kx", square)
		return possible

	#TODO: OFCOURSE THE KING CANNOT MOVE IN THE CHECK SPOTS
	def getPossibleSquares(self):
		c_fw = self.currentColumn.moveUp(self.currentcell)
		if c_fw!=None:
			c_tr = self.board.getRow(c_fw.name).moveRight(c_fw)
			c_tl = self.board.getRow(c_fw.name).moveLeft(c_fw)
		else:
			c_tr = None
			c_tl = None
		c_dw = self.currentColumn.moveDown(self.currentcell)
		if c_dw!=None:
			c_br = self.board.getRow(c_dw.name).moveRight(c_dw)
			c_bl = self.board.getRow(c_dw.name).moveLeft(c_dw)
		else:
			c_br = None
			c_bl = None
		c_r = self.currentRow.moveRight(self.currentcell)
		c_l = self.currentRow.moveLeft(self.currentcell)
		movingSquares = [c_fw, c_tr, c_tl, c_dw, c_br, c_bl, c_r, c_l]
		possibleMovingSquares = []
		possibleKillingSquares = []
		for c in movingSquares:
			if c!=None:
				if c.occupied==False:
					possibleMovingSquares.append(c)
				else:
					if c.piece.colour!=self.colour:
						possibleKillingSquares.append(c)
		return possibleMovingSquares, possibleKillingSquares

#TODO: REDUCE THE NUMBER OF REDUNDANCIES
#BY MAKING MOVE AND KILL PARENT CLASS (PIECE)
class Knight(Piece):
	def __init__(self, board, identityClass, square, colour, image):
		Piece.__init__(self, board, identityClass, square, colour, image)
	def move(self, square):
		possible = False
		moveSquares = self.getPossibleSquares()[0]
		for c in moveSquares:
			if c.name==square:
				newcell = self.board.getCell(square)
				self.updateDetails(newcell)
				possible = True
		if possible:
			ms.storeMove(self, "N", square)
		return possible
	def kill(self, square):
		possible = False
		killSquares = self.getPossibleSquares()[1]

		for c in killSquares:
			if c.name==square:
				if c.piece.colour!=self.colour:
					newcell = self.board.getCell(square)
					self.updateDetails(newcell)
					possible = True
		if possible:
			ms.storeMove(self, "Nx", square)
		return possible
	def getPossibleSquares(self):
		possibleSquares = []

		#first move two cells up and then check right and left
		#similarly we can create others
		firstcellup = self.currentColumn.moveUp(self.currentcell)
		if firstcellup!=None:
			secondcellup = self.currentColumn.moveUp(firstcellup)
			if secondcellup!=None:
				possibleSquares.append(self.board.getRow(secondcellup.name).moveRight(secondcellup))
				possibleSquares.append(self.board.getRow(secondcellup.name).moveLeft(secondcellup))
		firstcelldown = self.currentColumn.moveDown(self.currentcell)
		if firstcelldown!=None:
			secondcelldown = self.currentColumn.moveDown(firstcelldown)
			if secondcelldown!=None:
				possibleSquares.append(self.board.getRow(secondcelldown.name).moveRight(secondcelldown))
				possibleSquares.append(self.board.getRow(secondcelldown.name).moveLeft(secondcelldown))
		firstcellleft = self.currentRow.moveLeft(self.currentcell)
		if firstcellleft!=None:
			secondcellleft = self.currentRow.moveLeft(firstcellleft)
			if secondcellleft!=None:
				possibleSquares.append(self.board.getColumn(secondcellleft.name).moveUp(secondcellleft))
				possibleSquares.append(self.board.getColumn(secondcellleft.name).moveDown(secondcellleft))
		firstcellright = self.currentRow.moveRight(self.currentcell)
		if firstcellright!=None:
			secondcellright = self.currentRow.moveRight(firstcellright)
			if secondcellright!=None:
				possibleSquares.append(self.board.getColumn(secondcellright.name).moveUp(secondcellright))
				possibleSquares.append(self.board.getColumn(secondcellright.name).moveDown(secondcellright))

		#distribute and eliminate the pieces
		possibleMovingSquares = []
		possibleKillingSquares = []
		for c in possibleSquares:
			if c!=None:
				if c.occupied==False:
					possibleMovingSquares.append(c)
				else:
					possibleKillingSquares.append(c)
		return possibleMovingSquares, possibleKillingSquares

#the one who is giving the check must be giving checkmate
#he must be giving the color of opponent's king
def checkmate(board, color):
	#artificial board for future movement
	ourPieces = []
	artificialBoard = board.boardState()
	if isKingInCheck(board, color):
		pass
	else:
		return False
	for c in artificialBoard:
		if c.piece!=None:
			if c.piece.colour!=color:
				ourPieces.append(c.piece)
			else:
				if c.piece.identityClass=="king":
					oppking = c.piece
	initSquare = oppking.square
	initCell = oppking.currentcell

	kingmoves, kingkills = board.getCell(initSquare).piece.getPossibleSquares()
	for our in ourPieces:
		
		for moveCell in kingmoves:
			oppking.updateDetails(moveCell)
			if our.kill(moveCell)==False:
				return False
			else:
				
				moveCell.piece.updateDetails(initCell)
		for killCell in kingkills:
			oppking.updateDetails(killCell)
			backToInitial = False
			if isKingInCheck(board, color):
				oppking.updateDetails(initCell)
				killCell.update(ms.killedPieces.pop())
				backToInitial = True

			if our.kill(oppking.square)==False:
				return False
			else:
				if not(backToInitial):
					oppking.updateDetails(initCell)
				#restoring piece back to cell
				killCell.update(ms.killedPieces.pop())

	return True

#debugging
#TODO: PROMOTING, CHECK SPOTS: FIX CASTLING AND MOVEMENT FOR KING

#We are not deleting the killed pieces
#Might want them later on