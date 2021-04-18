
#############################################################################
# Implementations of Strassen's algorithm and ordinary matrix multiplcation
# for Lab 1
# Alex Bartlett
#
# includes functionality for comparing efficiency between the two methods
#
#############################################################################

# library for easily indexing into matrices
import numpy as np

# multiply matrices A and B using SQUARE_MATRIX_MULTIPLY algorithm
def mat_multiply(A, B):
	count = 0
	n = len(A)

	# formt the product array to display decimals or not based on 
	# contents of A and B
	if (A.dtype == 'float64' or B.dtype == 'float64'):
		C = np.array([[0.0 for i in range(n)] for j in range(n)])
	else:
		C = np.array([[0 for i in range(n)] for j in range(n)])

	# perform multiplication
	for i in range(len(A)):
		for j in range(len(B[0])):
			for k in range(len(B)):
				C[i, j] += A[i, k] * B[k, j]
				count += 1

	# return product matrix as well as count of multiplications performed
	return C, count

# partition matrix A into 4 quadrants, each a matrix with dimensions n/2 x n/2
def make_submatrices(A):
	n = len(A)
	new_n = int(n/2)

	# return quadrants
	return A[:new_n, :new_n], A[:new_n, new_n:], A[new_n:, :new_n], A[new_n:, new_n:]

# multiply matrices using Strassen's algorithm
def strassen_multiply(A, B):

	# base case = matrices are actually single numbers, can multiply normally
	# 1 multiplication has been performed (for later combination and comparison)
	if len(A) == 1:
		return A * B, 1

	# split A and B into quadrants for recursion
	a11, a12, a21, a22 = make_submatrices(A)
	b11, b12, b21, b22 = make_submatrices(B)

	# calculate the 10 sums and differences of submatrices as in book
	s1 = b12 - b22
	s2 = a11 + a12
	s3 = a21 + a22
	s4 = b21 - b11
	s5 = a11 + a22
	s6 = b11 + b22
	s7 = a12 - a22
	s8 = b21 + b22
	s9 = a11 - a21
	s10 = b11 + b12

	# recursively calculate the 7 products of the submatrices, as in book
	p1, count1 = strassen_multiply(a11, s1)
	p2, count2 = strassen_multiply(s2, b22)
	p3, count3 = strassen_multiply(s3, b11)
	p4, count4 = strassen_multiply(a22, s4)
	p5, count5 = strassen_multiply(s5, s6)
	p6, count6 = strassen_multiply(s7, s8)
	p7, count7 = strassen_multiply(s9, s10)

	# add the multiplication counts from previous recursions
	# to be returned as the count as of this recursion
	count = count1 + count2 + count3 + count4 + count5 + count6 + count7

	# calculate the quadrants of the product matrix C using the 7 products, 
	# as in book
	c11 = p5 + p4 - p2 + p6
	c12 = p1 + p2
	c21 = p3 + p4
	c22 = p5 + p1 - p3 - p7

	# assemble the product matrix C from its quadrants
	C = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))  

	# return product matrix as well as count of multiplications performed
	return C, count