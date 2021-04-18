
#############################################################################
# Main driver for Lab 1
# Alex Bartlett
#
# Parses input file, performs ordinary matrix multiplication and Strassen's
# algorithm, and writes output to file along with efficiency metrics
#
##############################################################################

# imports module for reading and writing matrices from input file
from Lab1_utils import *

# main driver
if __name__ == "__main__":

	# read input file
	##### THIS PATH MUST BE CHANGED TO CHANGE INPUT FILES #####
	with open('inputs/extreme_input.txt') as file:
		contents = file.read()

	# parse input, perform calculations, and create output
	output = compute_products(contents)

	# write output to file
	##### THIS PATH MUST BE CHANGED TO CHANGE OUTPUT FILES #####
	outfile = open('outputs/extreme_output.txt', 'w')
	outfile.writelines(output)
	outfile.close()

