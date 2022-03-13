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