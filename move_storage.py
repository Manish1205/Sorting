# I will probably be using this class
# for machine learning purposes, so we can store the games
# in different files to store different games, probably single file
class MoveStore:
	def __init__(self):
		self.movesList = []
		self.whiteMoves = []
		self.blackMoves = []
		self.killedPieces = []
		self.numberOfMoves = 0
	def storeMove(self, pickedPiece, pieceSuffix, landingSquare):
		if pickedPiece.colour=="white":
			self.whiteMoves.append((pickedPiece, pieceSuffix+landingSquare))
		elif pickedPiece.colour=="black":
			self.blackMoves.append((pickedPiece, pieceSuffix+landingSquare))

			#black, that means turn is over
		else:
			print("Given wrong input colours")

		self.movesList.append((pickedPiece, pieceSuffix+landingSquare))
	def getPreviousMove(self):
		if self.movesList!=[]:
			return self.movesList[-1]
		return None
	def displayMoves(self):
		numberOfTotalMoves = len(self.movesList)
		if numberOfTotalMoves%2==0:
			print(self.movesList[-1][1])
		else:
			print((str(numberOfTotalMoves//2+1)+". "+self.movesList[-1][1]), end=" ")
