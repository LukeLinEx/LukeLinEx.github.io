#from sys import argv
from aetna_register import *


if __name__ == '__main__':
	#_, input_file, output_file = argv
	input_file = raw_input('Enter the data source: \n')
	output_file= raw_input('Enter the fiel to save: \n')
	Aetna_register().auto_process(input_file).show_table().\
	to_csv(output_file, index=None)
