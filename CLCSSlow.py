import sys
import numpy as np

arr = np.zeros((2048, 2048), dtype=int)

"""
Currently runs CLCSSlow
"""

def LCS(A,B):
	m = len(A)
	n = len(B)

	for i in range(1,m+1):
		for j in range(1,n+1):
			if A[i-1] == B[j-1]:
				arr[i][j] = arr[i-1][j-1]+1
			else:
				arr[i][j] = max(arr[i-1][j], arr[i][j-1])
	return arr[m][n]

def cut(s, i):
    return s[i:] + s[0:i]

def main():
	if len(sys.argv) != 1:
		sys.exit('Usage: `python CLCSSlow.py < input`')
	
	for l in sys.stdin:
		A,B = l.split()
		if len(A) > len(B):
			A, B = B, A
		# cut A at all possible locations, B constant
		# take the maximum path length of those computed
		maxLength = max([LCS(cut(A, j), B) for j in range(len(A))])
		print maxLength
	return

if __name__ == '__main__':
	main()
