
#############################################################################
# I/O functions for Lab 1
# Alex Bartlett
# 
# includes functions for reading input file, passing each pair of matrices
# to be multiplied, and printing the results in human readable format
#
#############################################################################

# import functions for multiplying a pair of matrices
from Lab1_matrix_mult import *

# import library for easy indexing in matrices
import numpy as np

# libraries for error checking
import re
import math

# given a single input and the order of the matrices within, parse the text 
# into two matrices compatible with my multiplication functions
def extract_mats(file_chunk, order):
	
	# create storage for matrices
	A = []
	B = []

	# check to ensure matrices are proper
	nlines = len(file_chunk)
	assert(math.log(order, 2).is_integer()), "The order of a matrix in the input is not a power of 2"
	assert(nlines - 1 == 2 * order), "A matrix in the input has the wrong number of rows"
	
	# go through the piece of the input file line by line
	for line in range(1, nlines):

		# format line as matrix row and ensure it is proper
		current_line = file_chunk[line].strip()
		try:
			format_line = list(map(int, current_line.split()))
		except:
			format_line = list(map(float, current_line.split()))
		assert(len(format_line) == order), "At least one row of a matrix in the input has the wrong number of items"

		# this means current line is part of first matrix
		if line <= order:
			A.append(format_line)
		# this means current line is part of second matrix
		else:
			B.append(format_line)

	# convert lists of lists into NumPy arrays
	A = np.array(A)
	B = np.array(B)

	# return pair of matrices as workable NumPy arrays
	return A, B

# parse an input file into single inputs and then call matrix multiplication and 
# output generation functions for each input
def compute_products(contents, output = ''):
	
	# ensure input file contains only numeric characters and white space
	contents = contents.strip()
	assert(re.search(r"[^\d\s\.-]", contents) == None), "Your input file contains a character that cannot be multiplied"

	# ensure that the file has a blank line between inputs 
	# (or after the one and only input)
	inputs = contents.split('\n\n')
	assert(len(inputs) > 1), 'Your input file is formatted incorrectly'

	#consider each input in file separately
	for single_input in inputs:
		single_input_lines = single_input.split('\n')
		order = int(single_input_lines[0])

		# extract and multiply matrices from this input
		A, B = extract_mats(single_input_lines, order)
		C_orig, orig_count = mat_multiply(A, B)
		C_stras, stras_count = strassen_multiply(A, B)

		# store results from this input
		output = add_output(single_input, C_orig, C_stras, orig_count, stras_count, output)

	# return multiplication results from all inputs
	return output
	
# format a product NumPy array into a string that uses the same convention used in
# the input file	
def pretty_print(C):
	pretty_C = ''
	for i in range(len(C[0])):
		for j in range(len(C)):
			pretty_C += str(C[i,j]) + ' '
		pretty_C += '\n'
	return(pretty_C)

# given an input, its product, and its efficiency metrics, store this info in 
# human readable format
def add_output(input, C_orig, C_stras, orig_count, stras_count, output):


	output += 'Input:\n' + input + '\n\n'
	output += 'Original Method Product:\n' + pretty_print(C_orig) + '\n'
	output += 'Strassen Method Product:\n' + pretty_print(C_stras) + '\n'
	output += 'Multiplications in ordinary multiplication: ' + str(orig_count) + '\n'
	output += "Multiplications in Strassen's multiplication: " + str(stras_count) + '\n\n\n'

	# return human-readable results
	return output