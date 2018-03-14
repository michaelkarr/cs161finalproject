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

# potentially backtrace twice for upper and lower bounds
def backtracePath(A, B, i, j, dis, arr):  # dis = displacement to calculate
	# TODO: currently nonbounded, need to add 
	path = np.zeroes((i,), dtype=int)
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


def singleShortestPath(A, B, m, pl, pu, arr, pValDict):
	# computes pm by running the DP on the table bounded by pl and pu
	# step 1: compute dp
	val = disLCS(A, B, m, arr)
	pValDict[m] = val
	# step 2: backtracePath(A, B, i, j, dis, arr) and return the path
	# lets us compare the values in the strings in the grid
	A = A + A
	# backtraces starting at bottom right corner of DP array at row len(A) + m
	path = backtracePath(A, B, len(A) + m, len(B), m, arr)
	return path

def findShortestPaths(A, B, p, l, u, arr, pValDict):
	if u - l <= 1:
		return
	mid = int((l + u) / 2)
	p[mid] = singleShortestPath(A, B, mid, p[l], p[u], arr, pValDict)
	findShortestPaths(A, B, p, l, mid)
	findShortestPaths(A, B, p, mid, u)

def cut(s, i):
    return s[i:] + s[0:i]

# set up the dp arr
def setArr(m, n):
	return np.zeros((2 * m + 1, (n + 1)), dtype=int)

# dim: m (for each possible path p0-pm) x 2m (2m total rows)
def setP(m):
	return np.zeros((m + 1, (2 * m + 1)), dtype=int)

def main():
	if len(sys.argv) != 1:
		sys.exit('Usage: `python CLCSFast.py < input`')
	
	for l in sys.stdin:
		A,B = l.split()
		if len(A) > len(B):
			A, B = B, A
		arr = setArr(len(A), len(B))

		# THIS PIECE OF CODE IS TEMPORARY, JUST SO IT COMPILES RIGHT NOW
		maxLength = max([disLCS(cut(A, j), B, 0, arr) for j in range(len(A))])

		# TODO: this code should run, not above line
		p = setP(len(A))
		pValDict = dict()
		# p[0] is the backtrace of standard LCS
		# p[-1] is the same as p[0] but rows shifted down m
		# call findShortestPaths(A, B, p, 0, len(A), pValDict) to fill p array
		# return max([value for key, value in pValDict.iteritems()])
		print maxLength
	return

if __name__ == '__main__':
	main()
