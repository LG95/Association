#! /usr/bin/python

from build import associate, support

def parse(original):
	"""
	Separates words by blanks (space, tab or newline).

	Returns a list containing each word.

	Input:
		original - string containing the separated words.
	"""

	original += '\n' # ensuring a final word is not forgotten
	word = ''	# currently found word

	for char in original:	# checking each character in original
		if char not in [' ', '\t', '\n']:	# char is not a blank
			word += char	# add char to word

		elif word != '':	# word has characters in it
			yield word 
			word = ''	# reset word

def main(filenames):
	"""
	Read attribute description and training set from files. Use them to build
	and display association rules.

	Input:
		filenames - list with the names of files containing the attribute
	description and the training set.
	"""

	attributes = []	# set of attributes
	training = []	# training set

	# extracting the name of each file from filenames
	attribute_filename, train_filename  = filenames

	try:
		with open(attribute_filename) as file:	# on attribute file
			for line in file:	# each line in the file
				words = tuple( parse(line) )	# separate the words on that line
				# add the attribute (name, continuous?, values) to attributes
				attributes.append( (words[0], words[1] == 'continuous', words[1:]) )

	except IOError:	# treat error opening attribute file
		print('Cannot read records without knowing their attributes. ' + attribute_filename + ' could not be opened.')

	try:
		with open(train_filename) as file:	# on training file
			for line in file:	# each line in the file
				record = {}	# record on this line

				# match each word in this line to its respective 
				# attribute (based on position), treating word as the
				# value for this attribute in this record
				for attribute, value in zip(attributes, parse(line)):
					# decompose the attribute
					name, continuous, values = attribute

					if continuous:	# continuous attribute
						record[name] = float(value)	# store as float

					else:
						# record[name] = value	# store as string
						record[name] = value != '0'

				training.append(record)	# add record to training

	except IOError:	# treat error opening file
		print('Cannot build association rules without training records. ' + training_filename + ' could not be opened.')

	if attributes != [] and training != []:	# attributes and training set were read
		print 'Minimum support:',
		mins = float( raw_input() )

		print 'Minimum confidence:',
		minc = float( raw_input() )

		# find the frequent itemsets and association rules for the training set
		frequent, rules = associate(training, attributes, mins, minc)

		print('\nAssociation rules')
		for rule in rules:
			print(str(rule[0]) + '\t--->\t' + str(rule[1]))

if __name__ == '__main__':
	from sys import argv

	if len(argv) == 2:	# a single word was passed as an argument
		# add the necessary suffixes to the word
		main( [ argv[1] + end for end in ['-attr.txt', '.txt',] ] )

	elif len(argv) == 3:	# each filename was passed individually
		main( argv[1:] )

	else:	# show help message
		print('Usage: ' + argv[0] + ' name')
		print('       ' + argv[0] + ' attribute_file training_file\n')
		print('       name: attribute file and training file are, respectively, name-attr.txt and name.txt')