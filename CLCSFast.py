import sys
import numpy as np

"""
Currently just runs LCS
TODO: implement CLCSFast algorithm
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

	return arr[m + dis][n]

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

# potentially backtrace for lower, priority up for tightness
def backtracePathUp(A, B, i, j, pl, pu, dis, arr):  # dis = displacement to calculate
	# TODO: currently nonbounded, need to add 
	path = np.zeros((len(A) + 1,), dtype=int)
	while i > 0 + dis and j > 0:
		# if A[i-1] == B[j-1]:
		# 	path[i - 1] = j - 1
		# 	i -= 1
		# 	j -= 1 
		# elif arr[i-1][j] > arr[i][j-1]:
		# 	path[i - 1] = j
		# 	i -= 1
		# else:
		# 	path[i] = j - 1
		# 	j -= 1
		if pu[i - 1] >= j and arr[i - 1][j] == arr[i][j]:
		 	path[i - 1] = j
		 	i -= 1
		elif pu[i - 1] >= j - 1 and pl[i - 1] <= j - 1 and A[i-1] == B[j-1]:
			path[i - 1] = j - 1
			i -= 1
			j -= 1
		else:
			path[i] = j - 1
			j -= 1
	return path

def backtracePathLeft(A, B, i, j, pl, pu, dis, arr):  # dis = displacement to calculate
	# TODO: currently nonbounded, need to add 
	path = np.zeros((len(A) + 1,), dtype=int)
	while i > 0 + dis and j > 0:
		# if A[i-1] == B[j-1]:
		# 	path[i - 1] = j - 1
		# 	i -= 1
		# 	j -= 1 
		# elif arr[i-1][j] > arr[i][j-1]:
		# 	path[i - 1] = j
		# 	i -= 1
		# else:
		# 	path[i] = j - 1
		# 	j -= 1
		if pu[i] >= j - 1 and arr[i][j-1] == arr[i][j]:
		 	path[i] = j - 1
			j -= 1
		elif pu[i - 1] >= j - 1 and pl[i - 1] <= j - 1 and A[i-1] == B[j-1]:
			path[i - 1] = j - 1
			i -= 1
			j -= 1
		else:
			path[i - 1] = j
		 	i -= 1
	return path


def singleShortestPath(A, B, m, pl, pu, arr, pValDict):
	# computes pm by running the DP on the table bounded by pl and pu
	# step 1: compute dp
	val = disLCS(A, B, m, arr)
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
		lowerPath = backtracePathUp(A, B, len(A)/2 + m, len(B), pl, pu, m, arr)
		upperPath = backtracePathLeft(A, B, len(A)/2 + m, len(B), pl, pu, m, arr)
	# print arr
	# print path
	# print lowerPath, upperPath
	return lowerPath, upperPath

def findShortestPaths(A, B, pLower, pUpper, l, u, arr, pValDict):
	# print u, l
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

		# TODO: this code should run, not above line
		pLower, pUpper = setP(len(A))
		pValDict = dict()
		# p[0] is the backtrace of standard LCS
		pUpper[0] = singleShortestPath(A, B, 0, pLower, pUpper, arr, pValDict)
		pLower[0] = pUpper[0]
		pUpper[-1] = singleShortestPath(A, B, len(A), pLower, pUpper, arr, pValDict)
		pLower[-1] = pUpper[-1]
		# p[m] is the same path as p[0] but shifted down m
		# p[-1] = np.concatenate(([0], p[0][int((len(p[0]) + 1)/2):], p[0][1:int((len(p[0]) + 1)/2)]))
		# print p[0]
		# print p[-1]
		# p[-1] is the same as p[0] but rows shifted down m
		findShortestPaths(A, B, pLower, pUpper, len(A), 0, arr, pValDict)
		# return max([value for key, value in pValDict.iteritems()])
		print max([value for key, value in pValDict.iteritems()])
	return

if __name__ == '__main__':
	main()
