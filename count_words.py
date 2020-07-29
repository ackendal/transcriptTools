#!/usr/bin/env python3

""" Alex Kendal												*
  * A program that reads a transcript and outputs a count	*
  * of how many words each person mentioned within the  	*
  * script says.											*
															"""

import argparse
import sys

"""
	clear_special_characters: Function takes in a string
	and strips text of all characters that are not letters, 	
	including the enter key.
															"""
def clear_special_characters(input):
	output = ""
	for c in input:
		if((c == '(') or (c == ')') or (c == '.') or (c == ',') or (c == '-') or (c == '!')
				or (c == ';') or (c == '?') or (c == '\n') or (c == '\r')):
			c = ' '
		output += c
	return output

"""
	print_nicely: Function formats the output into a
	readable print statement.
															"""
	
def print_nicely(input):
	input.sort(key = lambda tup: tup[1])
	output = ""
	count = 0
	for tuple in input:
		output += (str(tuple[0]) + ": " + str(tuple[1]) + "\n")
		count += int(tuple[1])
	print(output)
	return count
	
"""
	speakers: Function takes in a list of words input and
	sorts out the (fully capslocked) names into a new list
	which the function returns.
															"""
		
def speakers(input):
	namelist = []
	for word in input:
		if(word.isupper()):
			if(((word, 0) not in namelist) and (len(word) > 1) and (word != "AM")):
				namelist.append((word, 0))
	return namelist
	
"""
	analyse: Function takes in the list of people who speak 
	alongside the list of words input and counts words per
	speaker, returning a list of tuples where the first
	value is the speaker and the second value is the word
	count.
															"""
	
def analyse(input, namelist):
	wordlist = namelist
	speaker = ""
	speakcount = 0
	ind = 0
	for word in input:
		if(word.isupper() and (len(word) > 1) and (word != "AM")):
			wordlist[ind] = (speaker, speakcount)
			speaker = word
			speakcount = 0
			for tuple in wordlist:
				if tuple[0] == word:
					ind = wordlist.index((word, tuple[1]))
					speakcount = tuple[1]
		else:
			speakcount = speakcount + 1
	wordlist[ind] = (speaker, speakcount)
	return wordlist
	
"""
	main: Function reads in an input file, opens it, 
	stores the words in a list, and runs the analysis.
														"""
	
def main():

	file = None

	"""
		Examining arguments from the command line. "--infile"		
		opens a file (specified in the following argument)
		Any other argument doesn't do anything.
																"""
	parser = argparse.ArgumentParser()
	parser.add_argument("--infile", action="store")
	parser.add_argument("--count", action="store")
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
	
	"""
		Running the filters and sorting.
														"""
	
	input = clear_special_characters(input)
	words = input.split()
	namelist = speakers(words)
	wordlist = analyse(words, namelist)
	totalc = print_nicely(wordlist)
	
	if args.count:
		print("The total words in this episode was " + str(totalc))

if __name__ == "__main__":
	main()