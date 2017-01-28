#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of IE.

IE is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

IE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with IE.  If not, see <http://www.gnu.org/licenses/>.
"""

import subprocess
import sys
import os

class Shell(object):
	def __init__(self):
		self.segmentizer = './srxsegmentizer.sh'
		self.tagger = './icetagger.sh'
		self.empty = "sed '/^$/d'" #Command to rid file of empty lines
		self.clean = "sed 's/[\"„“]//g'" # Command to clean file of quotation marks, as they complicate reading lemmas
		self.tagger = './icetagger.sh'
		self.parser = './iceparser.sh'
	def make_translatefiles(self, mystring):
		# Clean, parse and lemmatize request from GUI
		# In: String to clean, parse and lemmatize
		# Out: String with parse, don't want to write to file so don't have to read in again.
		origpath = os.getcwd()
		mystring = mystring.replace("\'", "")
		mystring = mystring.replace("\"", "")
		lemmas = []
		cleancommand = "echo \"{}\" | {} | {}".format(mystring, self.empty, self.clean)
		cleanstring = subprocess.Popen([cleancommand], shell=True, stdout=subprocess.PIPE).communicate()[0]
		# Have clean string, need to call everything in IceNLP.
		newpath = origpath+'/IceNLPCore/bat/srxsegmentizer' 
		os.chdir(newpath)
		srxcommand = "echo '{}' | ./srxsegmentizer.sh".format(cleanstring)
		segmented_string = subprocess.Popen([srxcommand], shell=True, stdout=subprocess.PIPE).communicate()[0]
		tagpath = origpath+'/IceNLPCore/bat/icetagger'
		os.chdir(tagpath)
		tagcommand = "echo '{}' | ./icetagger.sh".format(segmented_string)
		tagged_string = subprocess.Popen([tagcommand], shell=True, stdout=subprocess.PIPE).communicate()[0]
		parpath = origpath + "/IceNLPCore/bat/iceparser"
		os.chdir(parpath)
		parcommand = "echo '{}' | ./iceparser.sh -f -a -m -xml".format(tagged_string)
		parsed_string = subprocess.Popen([parcommand], shell=True, stdout=subprocess.PIPE).communicate()[0]
		# Making the lemmalist
		for sentence in segmented_string.strip().split("\n"):
			lempath = origpath+"/IceNLPCore/bat/lemmald"
			os.chdir(lempath)
			lemcommand = "echo '{}' | ./lemmatize.sh".format(sentence)
			lemmas_sentence = subprocess.Popen([lemcommand], shell=True, stdout=subprocess.PIPE).communicate()[0]
			lemmalist = list()
			for line in lemmas_sentence.split("\n"):
				words = line.split(" ")
				if len(words) < 2:
					continue
				lemmalist.append(words[1])
			lemmastring = " ".join(lemmalist)
			lemmas.append(lemmastring)		
		os.chdir(origpath)
		return parsed_string, lemmas
	def make_datafiles(self, mymap):
		# Parse and lemmatize text files
		# In: Folder with text files to parse and lemmatize
		# Out: Parsed text files and lemmatized text files. Note that if parse.out already exists it will not be updated.
		if os.path.isfile(os.path.join('./', mymap, 'parse.out')):
			print "Parsed files have already been generated. Delete them if you want them to be updated."
			return 
		origpath = os.getcwd()
		origfiles = subprocess.Popen(['ls', mymap], shell=False, stdout=subprocess.PIPE).communicate()[0].strip().split('\n')
		with open(mymap+'parse.in', 'w+') as parsein, open(mymap+'lemmas.in', 'w') as lemmafile:
			for afile in list(one for one in origfiles if one.endswith('.txt')):
				print "Start of loop: Looking at {}".format(afile)
				longpath = mymap+afile
				infile = open(longpath)
				cleancommand = 'cat {} | {} | {}'.format(longpath, self.empty, self.clean)
				cleanfile = subprocess.Popen([cleancommand], shell=True, stdout=subprocess.PIPE).communicate()[0]
				# Files have been rid of empty lines and apostrophes, now they are divided into sentences.
				newpath = origpath+'/IceNLPCore/bat/srxsegmentizer' 
				os.chdir(newpath)
				srxcommand = "echo '{}' | ./srxsegmentizer.sh".format(cleanfile)
				segmentedfile = subprocess.Popen([srxcommand], shell=True, stdout=subprocess.PIPE).communicate()[0]
				# Files are tagged and lemmatized in the same loop.
				for sentence in segmentedfile.strip().split("\n"):
					if not sentence:
						continue
					tagpath = origpath+'/IceNLPCore/bat/icetagger'
					os.chdir(tagpath)
					tagcommand = "echo '{}' | ./icetagger.sh".format(sentence)
					tagged_sentence = subprocess.Popen([tagcommand], shell=True, stdout=subprocess.PIPE).communicate()[0]
					lempath = origpath+"/IceNLPCore/bat/lemmald"
					os.chdir(lempath)
					lemcommand = "echo '{}' | ./lemmatize.sh".format(sentence)
					lemmas_sentence = subprocess.Popen([lemcommand], shell=True, stdout=subprocess.PIPE).communicate()[0]
					lemmalist = list()
					for line in lemmas_sentence.split("\n"):
						words = line.split(" ")
						if len(words) < 2:
							continue
						lemmalist.append(words[1])
					lemmastring = " ".join(lemmalist)
					parsein.write(tagged_sentence)
					lemmafile.write(lemmastring+'\n')
					os.chdir(origpath)
				infile.close()
				os.chdir(origpath)
		parpath = origpath + "/IceNLPCore/bat/iceparser"
		os.chdir(parpath)
		infile = '../../../'+mymap+'parse.in'
		outfile = '../../../'+mymap+'parse.out'
		parcommand = '{} -i {} -o {} -f -a -m -xml'.format(self.parser, infile, outfile)
		open_infile = open(infile)
		open_outfile = open(outfile, 'w')
		p = subprocess.Popen([parcommand], shell=True) 
		p.wait()
		open_outfile.flush()
		open_infile.close()
		open_outfile.close()
		os.chdir(origpath)
		return
if __name__ == "__main__":
	map = 'testcorp/'
	myshell = Shell()
	myshell.make_files(map)
	print "All done!"
