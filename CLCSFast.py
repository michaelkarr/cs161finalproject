import sys
import numpy as np

"""
Currently just runs LCS
TODO: implement CLCSFast algorithm
"""

def LCSBig(A,B,arr):
	m = len(A)
	n = len(B)

	A = A + A

	for i in range(1,2 * m+1):
		for j in range(1,n+1):
			if A[i-1] == B[j-1]:
				arr[i][j] = arr[i-1][j-1]+1
			else:
				arr[i][j] = max(arr[i-1][j], arr[i][j-1])

	# return max(arr[i + m][n] for i in range(m))
	return arr[m][n]

def singleShortestPath(A, B, m, pl, pu):
	# computes pm by running the DP on the table bounded by pl and pu
	return

def findShortestPaths(A, B, p, l, u):
	if u - l <= 1:
		return
	mid = int((l + u) / 2)
	p[mid] = singleShortestPath(A, B, mid, p[l], p[u])
	findShortestPaths(A, B, p, l, mid)
	findShortestPaths(A, B, p, mid, u)

def cut(s, i):
    return s[i:] + s[0:i]

def setArr(m, n):
	# TODO: check dimensions
	return np.zeros((2 * m + 1, (n + 1)), dtype=int)

def main():
	if len(sys.argv) != 1:
		sys.exit('Usage: `python CLCSFast.py < input`')
	
	for l in sys.stdin:
		A,B = l.split()
		if len(A) > len(B):
			A, B = B, A
		arr = setArr(len(A), len(B))
		# cut A at all possible locations, B constant
		# take the maximum path length of those computed
		# TODO: should we be checking which is longer
		maxLength = max([LCSBig(cut(A, j), B, arr) for j in range(len(A))])
		# TODO: this code should run
		# findShortestPaths(A, B, p, 0, len(A))
		# return the shortest pi
		print maxLength
	return

if __name__ == '__main__':
	main()
