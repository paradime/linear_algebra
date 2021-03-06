from fractions import Fraction
from math import isclose
from sympy import radsimp, sqrt

def scale(scalar, row):
  return list(map(lambda x: x * scalar, row))

def addRow(row1, row2):
  return list(map(lambda i: 
    row1[i] + row2[i], range(0, len(row1))
  ))

def height(matrix):
  return len(matrix)

def width(matrix): 
  return len(matrix[0])

def pivotEntry(rowNum, matrix):
  return matrix[rowNum][rowNum]

def newEmptyMatrix(matrix):
  return list(map(lambda _: [], matrix))

def swapRow(i, j, matrix):
  tempRow = matrix[i]
  matrix[i] = matrix[j]
  matrix[j] = tempRow
  return matrix

def rref(matrix):
  newMatrix = matrix
  for i in range(0, height(matrix)):
    if(i>= width(matrix)):
      return newMatrix
    tempMatrix = newEmptyMatrix(matrix)
    pivotRowNum = i
    if(pivotEntry(i, newMatrix) == 0):
      swapped = False
      for j in range(i+1, height(newMatrix)):
        if newMatrix[j][i] != 0:
          newMatrix = swapRow(i, i+1, newMatrix)
          swapped = True
      if not swapped:
        continue
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
      try:
        v = str(radsimp(entry)) +"\t"
      except:
        v = str(int(entry) if entry % 1 == 0 else Fraction(entry)) +"\t"
      r+= v
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
  rrefForm = rref(augmentMatrix(matrix, identityMatrix(height(matrix))))
  newMatrix = []
  for row in rrefForm:
    newMatrix.append(row[width(matrix):])
  return newMatrix


def dotProdSimp(row, col):
  val = 0
  for i in range(0, len(row)):
    val += row[i]*col[i]
  return val

def dotProd(m1, m2):
  newMatrix = []
  for i in range(0, height(m1)):
    newMatrix.append([])
    for j in range(0, width(m2)):
      newMatrix[i].append(dotProdSimp(m1[i], columnAt(j, m2)))
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

def determinateOf3By3(matrix):
  return ruleOfSarrus(matrix)

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
    valsToSum.append(sign*matrix[i][0]*determinateOf3By3(matrix))
  return sum(valsToSum)

def transpose(matrix):
  newMatrix = []
  for i in range(0, width(matrix)):
    newRow = []
    for row in matrix:
      newRow.append(row[i])
    newMatrix.append(newRow)
  return newMatrix

def extractColumnMatrix(index, matrix):
  return transpose([columnAt(index, matrix)])
    
def addMatrix(m1, m2):
  newMatrix = []
  for i in range(0, height(m1)):
    newMatrix.append(addRow(m1[i], m2[i]))
  return newMatrix

def projectionMatrix(matrix):
  return dotProd(
    dotProd(
      matrix, 
      inverseOfMatrix(dotProd(transpose(matrix), matrix))
    ), 
    transpose(matrix)
  )

def projectWithOrthonormal(orthonormalMatrix, x):
  return dotProd(
    dotProd(orthonormalMatrix, transpose(orthonormalMatrix)),
     x
  )

def leastSquares(matrix, b):
  tOfM = transpose(matrix)
  ref = rref(
    augmentMatrix(
      dotProd(tOfM,matrix),
      dotProd(tOfM,b)
    )
  )
  newMatrix = []
  for row in ref:
    newMatrix.append([row[-1]])
  return newMatrix

# C^-1 . vector
def transformToNewBasis(basisMatrix, vectorMatrix):
  return dotProd(inverseOfMatrix(basisMatrix), vectorMatrix)

# in: A, C
# out: M
def transMatrixInBasis(transMatrix, basisMatrix):
  return dotProd(
    dotProd(
      inverseOfMatrix(basisMatrix),
      transMatrix
    ),
    basisMatrix
  )

# in: A, C, [v](in new basis)
# out: [T(x)] (in new basis)
def transformVectorInBasis(transMatrix, basisMatrix, vectorMatrix):
  return dotProd(
    transMatrixInBasis(transMatrix, basisMatrix),
    vectorMatrix
  )

def isOrthogonal(v1, v2):
  return dotProd([v1],transpose([v2]))[0][0] == 0

def isNormalized(vector):
  return isclose(dotProd([vector], transpose([vector]))[0][0], 1)

def isOrthonormal(v1, v2):
  return isNormalized(v1) and isNormalized(v2) and isOrthogonal(v1,v2)

def lengthOfVector(vectorMatrix):
  valsToSum = []
  for entryRow in vectorMatrix:
    valsToSum.append(entryRow[0]**2)
  return sqrt(sum(valsToSum))

def asUnitVector(vectorMatrix):
  return scaleMatrix(1/lengthOfVector(vectorMatrix), vectorMatrix)

def asOrthogonalVectorTo(vectorMatrix, orthonormalMatrix):
  valToSum =[]
  for i in range(0, width(orthonormalMatrix)):
    orthogonalVector = extractColumnMatrix(i, orthonormalMatrix)
    valToSum.append(scaleMatrix(dotProd(
      transpose(vectorMatrix), orthogonalVector)[0][0], 
      orthogonalVector
    ))
  summedMatrix = valToSum[0]
  for i in range(1, len(valToSum)):
    summedMatrix = addMatrix(summedMatrix, valToSum[i])
  return addMatrix(vectorMatrix, scaleMatrix(-1, summedMatrix)) 

def convertToOrthonormalBasis(matrix):
  matrixVOrtho = asUnitVector(extractColumnMatrix(0, matrix))
  for c in range(1, width(matrix)):
    columnVector = extractColumnMatrix(c, matrix)
    vectorAsOrthogonal = asOrthogonalVectorTo(columnVector, matrixVOrtho)
    u = asUnitVector(vectorAsOrthogonal)
    matrixVOrtho = augmentMatrix(matrixVOrtho, u)
  return matrixVOrtho
