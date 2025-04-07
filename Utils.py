class Utils:
  @staticmethod
  def getCoordinates(board, rows, cols, value):
    for x in range (rows):
      for y in range (cols):
        if board[x][y] == value:
          return x, y
    return None
  
  @staticmethod
  def printEntitiesCoordinates(board, rows, cols, Pacman, blueGhost, pinkGhost, redGhost, orangeGhost):
    print("Pacman:", Utils.getCoordinates(board, rows, cols, Pacman))
    print("blueGhost:", Utils.getCoordinates(board, rows, cols, blueGhost))
    print("pinkGhost:", Utils.getCoordinates(board, rows, cols, pinkGhost))
    print("redGhost:", Utils.getCoordinates(board, rows, cols, redGhost))
    print("orangeGhost:", Utils.getCoordinates(board, rows, cols, orangeGhost))