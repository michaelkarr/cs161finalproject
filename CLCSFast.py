import sys
import numpy as np

"""
Currently runs CLCSFast
"""

# used for calculating each DP
def disLCS(A, B, dis, arr):
	m = len(A)
	n = len(B)

	A = A + A

	# 0 out row before for calculation
	# do not need to 0 out first col bc always 0
	arr[dis] = 0

	for i in range(1,m+1):
		for j in range(1,n+1):
			if A[dis + i-1] == B[j-1]:
				arr[dis + i][j] = arr[dis + i-1][j-1]+1
			else:
				arr[dis + i][j] = max(arr[dis + i-1][j], arr[dis + i][j-1])
	#print arr
	return arr[m + dis][n]

def disLCSBounds(A, B, pl, pu, dis, arr):
	m = len(A)
	n = len(B)
	
	newA = A + A

	for i in range(1, m+2):
		arr[i + dis - 1] = 0


	"""
	W A R N I N G
	BELOW IS SOME OF THE MOST WASTEMAN CODE EVER WRITTEN
	APPROACH WITH CAUTION
	WE ARE ALL JUST AN OFF ONE ERROR
	"""
	# essentially computes the DP with bounds
	for i in range(1, m + 1):
		j = 1
		topBound = pu[dis + i] if pu[dis + i] != 0 else n + 1
		while True:
			if j < pl[dis + i]:
				j = pl[dis + i]
			if j > pu[dis + i + 1] and pu[dis + i + 1] > 0:
				break
			if j > n:
				break
			if newA[dis + i-1] == B[j-1] and topBound >= j-1 and pl[dis+i-1] <= j-1:
				arr[dis + i][j] = arr[dis + i-1][j-1]+1
			else:
				left = arr[dis + i][j-1] if pl[dis+i-1] <= j else -1
				up = arr[dis + i-1][j] if  topBound >= j else -1
				arr[dis + i][j] = max(up, left)
			j += 1

	return arr[m + dis][n]


# run this backtrace for the initialization of p0 and pm
def initBacktrace(A, B, i, j, pl, pu, dis, arr):  # dis = displacement to calculate
	path = np.zeros((len(A) + 1,), dtype=int)
	while i > 0 + dis and j > 0:
		if A[i-1] == B[j-1]:
			path[i - 1] = j - 1
			i -= 1
			j -= 1 
		elif arr[i-1][j] > arr[i][j-1]:
			path[i - 1] = j
			i -= 1
		else:
			path[i] = j - 1
			j -= 1
	return path


def backtracePathUp(A, B, i, j, pl, pu, dis, arr):  # dis = displacement to calculate
	path = np.zeros((len(A) + 1,), dtype=int)
	while i > 0 + dis and j > 0:
		# go left
		topBound = pu[i] if pu[i] != 0 else len(B) + 1
		if topBound >= j and arr[i-1][j] == arr[i][j] and i - 1 > dis:
			#print "UP"
		 	path[i-1] = j
			i -= 1
		# go diag
		elif topBound >= j - 1 and pl[i - 1] <= j - 1 and A[i-1] == B[j-1] and i-1 > dis:
			path[i - 1] = j - 1
			i -= 1
			j -= 1
			#print "DIAG"
		# go up
		else:
			path[i] = j -1
		 	j -= 1
		 	#print "LEFT"

	return path

def backtracePathLeft(A, B, i, j, pl, pu, dis, arr):  # dis = displacement to calculate
	path = np.zeros((len(A) + 1,), dtype=int)
	while i > 0 + dis and j > 0:
		# go left
		topBound = pu[i] if pu[i] != 0 else len(B) + 1
		if pl[i] <= j - 1 and arr[i][j-1] == arr[i][j]:
			#print "LEFT"
		 	path[i] = j - 1
			j -= 1
		# go diag
		elif topBound >= j - 1 and pl[i - 1] <= j - 1 and A[i-1] == B[j-1] and i-1 > dis:
			path[i - 1] = j - 1
			i -= 1
			j -= 1
			#print "DIAG"
		# go up
		else:
			path[i - 1] = j
		 	i -= 1
		 	#print "UP"

	return path


def singleShortestPath(A, B, m, pl, pu, arr, pValDict):
	# computes pm by running the DP on the table bounded by pl and pu
	# step 1: compute dp
	if m == 0 or m == len(A):
		val = disLCS(A, B, m, arr)
	else:
		val = disLCSBounds(A, B, pl, pu, m, arr)
	pValDict[m] = val
	# step 2: backtracePath(A, B, i, j, dis, arr) and return the path
	# lets us compare the values in the strings in the grid
	A = A + A
	# init is for first runs
	if m == 0 or m == len(A)/2:
		path = initBacktrace(A, B, len(A)/2 + m, len(B), pl, pu, m, arr)
		return path
	else:
		# backtraces starting at bottom right corner of DP array at row len(A) + m
		lowerBound = backtracePathUp(A, B, len(A)/2 + m, len(B), pl, pu, m, arr)
		upperBound = backtracePathLeft(A, B, len(A)/2 + m, len(B), pl, pu, m, arr)
	return lowerBound, upperBound

def findShortestPaths(A, B, pLower, pUpper, l, u, arr, pValDict):
	if l - u <= 1:
		return
	mid = int((l + u) / 2)
	low, up = singleShortestPath(A, B, mid, pLower[l], pUpper[u], arr, pValDict)
	pLower[mid] = low
	pUpper[mid] = up
	findShortestPaths(A, B, pLower, pUpper, l, mid, arr, pValDict)
	findShortestPaths(A, B, pLower, pUpper, mid, u, arr, pValDict)

def cut(s, i):
    return s[i:] + s[0:i]

# set up the dp arr
def setArr(m, n):
	return np.zeros((2 * m + 1, (n + 1)), dtype=int)

# dim: m (for each possible path p0-pm) x 2m (2m total rows)
def setP(m):
	return np.zeros((m + 1, 2 * m + 1), dtype=int), np.zeros((m + 1, 2 * m + 1), dtype=int)

def main():
	if len(sys.argv) != 1:
		sys.exit('Usage: `python CLCSFast.py < input`')
	
	for l in sys.stdin:
		A,B = l.split()
		if len(A) > len(B):
			A, B = B, A
		arr = setArr(len(A), len(B))

		pLower, pUpper = setP(len(A))
		pValDict = dict()
		# p[0] is the backtrace of standard LCS
		pUpper[0] = singleShortestPath(A, B, 0, pLower, pUpper, arr, pValDict)
		pLower[0] = pUpper[0]
		pUpper[-1] = singleShortestPath(A, B, len(A), pLower, pUpper, arr, pValDict)
		pLower[-1] = pUpper[-1]

		findShortestPaths(A, B, pLower, pUpper, len(A), 0, arr, pValDict)

		print max([value for key, value in pValDict.iteritems()])
	return

if __name__ == '__main__':
	main()
