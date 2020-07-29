#!/usr/bin/env python3

""" Alex Kendal, V00872134									*
  * A program that reads a file and outputs a count of how	*
  * many words of all lengths it finds are in the file. 	*
  * This list of counts can be sorted or unsorted (default)	*
  * and printed with or without (default) a list of the 	*
  * words of each length. Only non letter characters are 	*
  * .,();.													*
															"""

import argparse
import sys


"""
	find_lowest_node: Function takes in a list and locates	
	the word that is alphabetically closest to a.			
															"""
def find_lowest_node(input):
	min = input[0]
	for word in input:
		if word < min:
			min = word
	return min


"""
	clear_special_characters: Function takes in a string
	and strips text of all characters that are not letters, 	
	including the enter key, and makes all letters
	lowercase.
															"""
def clear_special_characters(input):
	output = ""
	for c in input:
		c = c.lower()
		if((c == '(') or (c == ')') or (c == '.') or (c == ',') or (c == '-') or (c == '!')
				or (c == ';') or (c == '?') or (c == '\n') or (c == '\r')):
			c = ' '
		output += c
	return output

		
"""
	max_length: Function takes in a list and outputs the 	
	longest word length in the list.				
 															"""
def max_length(input):
	max = 0
	for word in input:
		if len(word) > max:
			max = len(word)
	return max
		
		
"""
	frequencies: Function takes in a list of words and the
	maximum length of a word and returns another list of
	lengths and their corrosponding frequencies.
															"""
def frequencies(input):
	wordlist = []
	added = 0;
	count = -1;
	backcount = 0;
	print(input)
	for x in range(0, len(input)):
		word = input[x]
		count = count+1
		for tuple in wordlist:
			if tuple[0] == word:
				temp = (tuple[0], tuple[1]+1)
				ind = wordlist.index((word, tuple[1]))
				wordlist[ind] = temp;
				added = 1;
				count = -1;
		if added == 0:
			temp = (word, 1)
			print(temp)
			wordlist.append(temp)
			count = -1;
		added = 0
	print(wordlist)
	wordlist.sort(key = lambda tup: tup[1])
	print(wordlist)
	return wordlist
	
def print_nicely(input):
	output = ""
	count = 0;
	for tuple in input:
		output += (str(tuple[0]) + ": " + str(tuple[1]) + "   ")
		count = count + 1
		if(count%5 == 0):
			output += "\n"
	print(output)
	
	
"""
	check_counts: precursor to print_words(). Runs through 
	a list of words and an expected value to be the length 
	of. It returns the number of words of that length.										*
															"""
def check_counts(input, count):
	num = 0
	for word in input:
		if(len(word) == count):
			num = num + 1
	return num
	
	
"""
	print_by_length: Function to print in order from shortest
	word length to longest. Takes in the list of frequencies
	and whether to print words.
															"""
def print_by_length(input, print_on, words):
	output = ""
	for x in range(len(input)):
		l = str(input[x]['length'])
		f = str(input[x]['frequency'])
		output = ("Count[" + l + "]=" + f + ";")
		if print_on:
			output += (" " + print_words(words, input[x]['length']))
		print(output)

	
"""
	print_by_frequency: Function to print in order from
	least to most common lengths. Takes in the list of 
	frequencies and whether to print words.
															"""
def print_by_frequency(input, print_on, words):
	output = ""
	list = [x['frequency'] for x in input]
	list.sort()
	list.reverse()
	for y in list:
		length = len(input)
		index = 0
		while(index < length):
			if(input[index]['frequency'] == y):
				l = str(input[index]['length'])
				f = str(y)
				output = ("Count[" + l + "]=" + f + ";")
				if print_on:
					output += (" " + print_words(words, input[index]['length']))
				print(output)
				del input[index]
				length = length - 1
				index = 0
			else:
				index = index + 1

				
"""
	print_words: Function to print words of a given length.
	Takes in the list of words and the length to print.
															"""
def print_words(input, count):
	output = "(words: "
	num = check_counts(input, count)
	index = 0
	if(num == 0):
		return;
	elif(num == 1):
		for word in input:
			if(len(word) == count):
				output += ("\"" + word + "\")")
	elif(num == 2):
		for word in input:
			if((len(word) == count) and (index < (num - 1))):
				output += ("\"" + word + "\" ")
				index = index + 1
			elif(len(word) == count):
				output += ("and \"" + word + "\")")
	else:
		for word in input:
			if((len(word) == count) and (index < (num - 2))):
				output += ("\"" + word + "\", ")
				index = index + 1
			elif((len(word) == count) and (index < (num - 1))):
				output += ("\"" + word + "\" ")
				index = index + 1
			elif(len(word) == count):
				output += ("and \"" + word + "\")")
	return output
	
	
def main():

	file = None

	"""
		Examining arguments from the command line. "--infile"		
		opens a file (specified in the following argument),
		"--sort" turns the sort_on on, and "--print-words" turns
		print_on on. Any other argument doesn't do anything.
																"""
	parser = argparse.ArgumentParser()
	parser.add_argument("--infile", action="store")
	parser.add_argument("--sort", action="store_true")
	parser.add_argument("--print-words", action="store_true")
	args = parser.parse_args()
	
	if args.infile:
		try:
			file = open(args.infile, "r")
		except FileNotFoundError:
			print("Cannot open input file.")
			sys.exit(1)
		
	"""
		Accessing the file and storing it to a string 
		so that it can be accessed by the program.		
														"""
	if(file is None):
		print("No file could be accessed.")
	
	input = file.read()
	file.close()
	
	input = clear_special_characters(input)
	words = input.split()
	max = max_length(words)
	freqlist = frequencies(words)
	print_nicely(freqlist)
		
	"""
		Series of checks and functions calls. Options 
		are between displaying counts sorted or 
		unsorted, with or without a list of unique 
		words used.					
														"""	
	
	# if args.sort:
		# print_by_frequency(freqlist, args.print_words, words)
	# else:
		# print_by_length(freqlist, args.print_words, words)

if __name__ == "__main__":
	main()