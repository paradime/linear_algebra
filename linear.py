from fractions import Fraction

def scale(scalar, row):
  newRow = []
  for e in row:
    newRow.append(e * scalar)
  return newRow

def addRow(row1, row2):
  newRow = []
  for i in range(0, len(row1)):
    newRow.append(row1[i] + row2[i])
  return newRow

def height(matrix):
  return len(matrix)

def width(matrix): 
  return len(matrix[0])

def pivotEntry(rowNum, matrix):
  return matrix[rowNum][rowNum]

def newEmptyMatrix(matrix):
  newMatrix = []
  for _ in matrix:
    newMatrix.append([])
  return newMatrix

def rref(matrix):
  newMatrix = matrix
  for i in range(0, height(matrix)):
    tempMatrix = newEmptyMatrix(matrix)
    pivotRowNum = i
    pivotRow = scale(1/pivotEntry(i, newMatrix), newMatrix[pivotRowNum])
    tempMatrix[i] = pivotRow
    for j in range(0, height(matrix)):
      if i == j:
        continue
      otherRow = newMatrix[j]
      tempMatrix[j] = addRow(otherRow, scale((-1*otherRow[i]), pivotRow))
    newMatrix = tempMatrix
  return newMatrix

def printMatrix(matrix):
  for row in matrix:
    r = ""
    for entry in row:
      r+= str(Fraction(entry).limit_denominator()) + "\t"
    print(r)

def augmentMatrix(originalMatrix, augment):
  newMatrix = []
  for i in range(0, height(originalMatrix)):
    newMatrix.append(originalMatrix[i] + augment[i])
  return newMatrix

def identityMatrix(height):
  newMatrix = []
  for i in range(0, height):
    row = []
    for j in range(0, height):
      if i == j:
        row.append(1)
      else:
        row.append(0)
    newMatrix.append(row)
  return newMatrix

def inverseOfMatrix(matrix):
  return rref(augmentMatrix(matrix, identityMatrix(height(matrix))))

def dotProdSimp(row, col):
  val = 0
  for i in range(0, len(row)):
    val += row[i]*col[i]
  return val

def dotProd(m1, m2):
  newMatrix = []
  for row in m1:
    for i in range(0, width(m2)):
      newMatrix.append([dotProdSimp(row, columnAt(i, m2))])
  return newMatrix

def columnAt(index, matrix):
  column= []
  for row in matrix:
    column.append(row[index])
  return column

def scaleMatrix(scalar, matrix):
  newMatrix = []
  for row in matrix:
    newMatrix.append(scale(scalar, row))
  return newMatrix

def determinateOf2By2(matrix):
  return (matrix[0][0]*matrix[1][1]) - (matrix[1][0]*matrix[0][1])

def inverseOf2By2(matrix):
  return scaleMatrix((1/determinateOf2By2(matrix)), specialFlip2By2(matrix))

def specialFlip2By2(matrix):
  return [
    [matrix[1][1], -matrix[0][1]],
    [-matrix[1][0], matrix[0][0]],
  ]

def ruleOfSarrus(matrix):
  augMatrix = list(map(lambda row: row[0:2], matrix))
  newMatrix = augmentMatrix(matrix, augMatrix)
  valsToSum = []
  for i in range(0, 3):
    #diagonal down
    valsToSum.append(
      newMatrix[0][i] *
      newMatrix[1][i+1] *
      newMatrix[2][i+2]
    )
    #diagonal up
    valsToSum.append(-1 * 
      newMatrix[2][i] *
      newMatrix[1][i+1] *
      newMatrix[0][i+2]
    )
  return sum(valsToSum)
    
def determinateOf4By4(matrix):
  valsToSum = []
  for i in range(0,height(matrix)):
    sign = 1 if i % 2 == 0 else -1
    matrixToSarrus = []
    for j in range(0, height(matrix)):
      if(i == j):
        continue
      matrixToSarrus.append(matrix[j][1:])
    valsToSum.append(sign*matrix[i][0]*ruleOfSarrus(matrixToSarrus))
  return sum(valsToSum)

    

print("~~1~~")


print("~~2~~")
matrix = [
  [-3,1,2],
  [2,-2,0],
  [1,4,-4]
]
print(ruleOfSarrus(matrix))


print("~~3~~")

matrix = [
  [1,5,-1],
  [-1,1,3],
  [1,3,-2]
]
print(ruleOfSarrus(matrix))
matrix = [
  [1,5,-1],
  [3,-2,2],
  [-1,1,3]
]
print(-2*ruleOfSarrus(matrix))

matrix = [
  [1,5,0,-1],
  [3,-2,-1,2],
  [-1,1,0,3],
  [1,3,2,-2]
]
print(determinateOf4By4(matrix))