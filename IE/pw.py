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
import os
from math import log
from lxml import etree
from frame import Frame
from data import Data
from shell import Shell
import triggerops
import extractops
import treeops
import helpers

class FrameMaker():
	def __init__(self, devdir, startsemlex, catroles):
		self.devdir = devdir
		self.allpatterns = {} #extract|case|trigger|triggertype as key, value is [freq of pattern, [extracts, heads]]
		self.bestpatterns = [] #A simple list containing the idkeys of best patterns for lookup in self.allpatterns.
		self.semlex = startsemlex #names of semantic categories are keys, lists of pairs words in each category and their heads are values
		self.catroles = catroles #names of semantic categories are keys, the semantic role of each category is the value
		self.shell = Shell()
		self.data = Data()
	def generateframes(self): 
		if os.path.isfile(os.path.join('./', self.devdir, 'myframes.out')):
			print "Frames have already been generated. Delete myframes.out, lemmas.in, parse.in and parse.out if you want to update them for new texts and run program again."
		else:
			print "Generating all patterns..."
			self.generateallpatterns() #Fills self.allpatterns with all patterns found in devdir.
			print "Getting the best patterns..."
			self.weedpatterns() #Gives me the best patterns. Note self.reviewall() is called within this method.
			print "Expanding best patterns..."
			pattswithsempref = self.expandpatterns() #Expands the best patterns with roles and semantic preferences.
			print "Merging patterns into frames..."
			frames = self.mergepatterns(pattswithsempref) #make frames out of patterns sharing a trigger and trigger type  
			print "Printing frames to file..."
			with open(self.devdir+'myframes.out', 'a') as framesfile:
				for frame in frames:
					framesfile.write("Trigger: {}, {}\n".format(frame.trigger, frame.triggertype))
					for pattern in frame.patterns.keys():
						framesfile.write("\t{}\n".format(pattern))
						for item in frame.patterns[pattern]:
							framesfile.write("\t\t{}\n".format(item))
	def generateallpatterns(self):
		self.shell.make_datafiles(self.devdir) # Creates lemmas.in, parse.in, and parse.out
		all_lemmas = list()
		with open(self.devdir+'lemmas.in', 'r+') as lemmafile:
			for line in lemmafile:
				all_lemmas.append(line)
		parsed_sentence = list()
		with open(self.devdir+'parse.out', 'r+') as parse:
			for line in parse:
				parsed_sentence.append(line)
				if "</SENTENCE>" in line:
					sentence_string = " ".join(parsed_sentence)
					parsed_sentence = list() # Resetting the search
					lemma_string = all_lemmas.pop(0)
					lemmas_for_sentence = lemma_string.split(" ")
					self.patternfinder(sentence_string, lemmas_for_sentence)					
				else:
					continue
		print "All patterns have been generated."
	def patternfinder(self, sentence, lemmas):
		root = treeops.getroot(sentence)
		trigger, triggertype = "", ""
		root = treeops.addlemmas(root, lemmas)
		for node in root.iter(): #Looking for NPs
			text = treeops.text(node)
			yesterfound = False
			if "done" in helpers.cleantag(node.tag) or "sentence" in helpers.cleantag(node.tag):
				continue
			elif "np" in text or "ap-obj" in text or "ap-comp" in text or treeops.yester(node): #to account for ap-obj and ap-comp
				if treeops.yester(node):
					trigger, triggertype = triggerops.getyestertrigger(node, root)
					yesterfound = True
				myphrase, myhead, case = treeops.getnounphrase(node, root)
				if not case:
					if yesterfound:
						pass
					else:
						continue #Don't want a pattern with no case, unless timex
				elif "qual" in text or "timex" in text:
					continue
				elif "subj" in text:
					trigger, triggertype = triggerops.getsubjtrigger(node, root)
					extract = "subj"
				elif "comp" in text:
					trigger, triggertype = triggerops.getcomptrigger(node, root)
					extract = "comp"
				elif "iobj" in text:
					trigger, triggertype = triggerops.getiobjtrigger(node, root)
					extract = "iobj"
				elif "obj" in text: #objnom is included in "obj". AP-OBJ is covered here
					trigger, triggertype = triggerops.getobjtrigger(node, root)
					extract = "obj"	
				elif not case:
					continue #nothing to collect
				else: #NPs inside PPs
					trigger, triggertype = triggerops.getpreptrigger(node, root)
					extract = "noun"
				if yesterfound:
					extract = "noun"
					case = "nom"
					myphrase = "gær"
					myhead = "gær"
				if not trigger or not triggertype or not case:
					continue
				idkey = extract+"|"+case+"|"+trigger+"|"+triggertype
				if idkey not in self.allpatterns:
					self.allpatterns[idkey] = [0, []] # NOTE that the freq and extract list will be filled out in extractfinder()
		return
	def weedpatterns(self):
		if os.path.isfile(os.path.join('./', self.devdir, 'bestpatterns.out')): # If this file exists I can assume other files do
			print "Files containing the best patterns and words in the semantic lexicon have been created."
			self.reviewall()
		else:
			print "\t Getting all the extracts..."
			# Getting each sentence and the lemma string:
			self.shell.make_datafiles(self.devdir) # Creates both lemmas.in, parse.in, and parse.out if not already present
			all_lemmas = list()
			with open(self.devdir+'lemmas.in', 'r+') as lemmafile:
				for line in lemmafile:
					all_lemmas.append(line)
			parsed_sentence = list()
			triggerdict = {}
			for key in self.allpatterns.keys(): #Making triggerdict, triggers as keys and patterns as values
				triggs = key.split('|')[2]
				if triggs not in triggerdict.keys():
					triggerdict[triggs] = []
				triggerdict[triggs].append(key)
			with open(self.devdir+'parse.out', 'r+') as parse:
				for line in parse:
					parsed_sentence.append(line)
					if "</SENTENCE>" in line:
						found = False
						sentence_string = " ".join(parsed_sentence)
						parsed_sentence = list() # Resetting the search
						lemma_string = all_lemmas.pop(0)
						lemmas_for_sentence = lemma_string.split(" ")
						for word in lemmas_for_sentence:
							if word in triggerdict.keys():
								found = True
						if not found:
							continue
						else:
							self.extractfinder(sentence_string, lemmas_for_sentence, triggerdict) #fills self.allpatterns with freq and extracts
			# Weeding patterns, keeping the best ones in a special dict.
			bestscoredict = {} #keeps all the patterns, only updates patterns if I find better scores in scoredict. Key: The pattern, Value: The score
			print "\t Getting best patterns and words for each semantic category"
			for category in self.semlex.keys(): # Go through each semantic category to find patterns for it.
				#print "next category:", category
				for i in range(50):
					scoredict, fivebest = self.innerbootstrap(category)
					for each in fivebest:
						self.semlex[category].append(each)
				if not bestscoredict:
					bestscoredict = scoredict #Initiating, no point in copying one for one.
				else:
					for item in scoredict.keys(): #Iterating over, adding pattern if not there and updating if find better score.
						if item not in bestscoredict.keys():
							bestscoredict[item] = scoredict[item]
							continue
						if scoredict[item] > bestscoredict[item]:
							bestscoredict[item] = scoredict[item] #Updating the value
			with open(self.devdir+"patternsandsemlex.out", 'a') as pattsem:
				pattsem.write("PATTERNS AND EXTRACTS\n")
				for every in bestscoredict.keys():
					pattsem.write(every+","+str(bestscoredict[every])+"\n")
					extrs = set(self.allpatterns[every][1])
					for each in extrs:
						both = each.split("|")
						pattsem.write("||"+both[1]+"\n")
				pattsem.write("SEMLEX\n")
				for catg in self.semlex.keys():
					pattsem.write(catg+":\n")
					for sem in self.semlex[catg]:
						pattsem.write("\t"+sem+"\n")
			self.reviewall()
			print "Done!"
	def extractfinder(self, sentence_string, lemmas_for_sentence, triggerdict):
		root = treeops.getroot(sentence_string)
		root = treeops.addlemmas(root, lemmas_for_sentence)
		for node in root.findall(".//WORD"): 
			thislemma = treeops.lemma(node)
			if thislemma in triggerdict.keys(): #Trigger is always just one word; the head of the phrase 
				patternlist = triggerdict[thislemma]
				for patt in patternlist:
					if not treeops.triggermatch(patt, node): #PoS of trigger doesn't match pattern
						continue 
					if not treeops.mainverb(node, root):
						continue
					whole, head = "", ""
					extype = helpers.getextracttype(patt)
					if "subj" in extype:
						whole, head = extractops.findsubjextract(patt, node, root)
					elif "iobj" in extype:
						whole, head = extractops.findiobjextract(patt, node, root)
					elif "obj" in extype:
						whole, head = extractops.findobjextract(patt, node, root)
					elif "comp" in extype:
						whole, head = extractops.findcompextract(patt, node, root)
					elif "noun" in extype:
						whole, head = extractops.findppextract(patt, node, root)
					else:
						continue
					if not whole: #nothing found
						continue
					self.allpatterns[patt][0] += 1
					self.allpatterns[patt][1].append(whole+"|"+head)
	def innerbootstrap(self, category):
		mypatterns = {} #dict of idkeys and their score.
		newone = False
		templex = self.semlex[category]
		templexheads = [] #list of all the heads
		for each in templex:
			which = each.split("|")
			templexheads.append(which[1])
		tempbest = {} # tempbest[idkey] = score; idkey is the pattern from self.allpatterns
		while True:
			bestscore = 0.0
			bestextrpairs = [] #resetting
			bestpattern = ""
			for idkey in self.allpatterns.keys():
				if self.allpatterns[idkey][0] <= 1:
					continue #the frequency is too low to matter, either 0 or 1.
				extractsandheads = self.allpatterns[idkey][1] #list of extracts and heads
				fi, score = 0.0, 0.0
				ni = float(len(extractsandheads))
				for pair in extractsandheads: #If the head is in templexheads the frequency of the pattern goes up
					both = pair.split("|")
					if both[1] in templexheads:
						fi += 1
				if fi == 0.0:
					continue #no use in looking at more
				ri = fi / ni
				score = ri * log(fi, 2)
				if score >= bestscore:
					if idkey in mypatterns.keys():
						mypatterns[idkey] = score #updating score but not collecting again
						continue
					bestpattern = idkey
					bestscore = score
					bestextrpairs = extractsandheads #Remember, list of extracts and heads separated by |
			if bestscore <= 1.5: # Original value: 0.7
				break    
			mypatterns[bestpattern] = bestscore
			for item in bestextrpairs:
				if item not in templex: #I haven't already collected this phrase|lemma pair
					newone = True
					templex.append(item)
					templexheads.append(item.split("|")[1])
			if len(mypatterns.keys()) >= 10 and newone:
				if bestscore >= 2.5: #Original value: 1.8
					continue
				else:
					break
		fivebest = self.getfivebest(mypatterns, templex, category)
		return mypatterns, fivebest
	def getfivebest(self, mypatterns, templex, category):
		tractscore = {}
		fivebest = []
		for pair in templex: # phrase|lemma pair
			exfreq = 0.0
			for pattern in mypatterns.keys():
				if pair in self.allpatterns[pattern]:
					exfreq = exfreq + mypatterns[pattern] #the score matters for ties
			tractscore[pair] = exfreq
		best = []
		for i in range(5):
			bestex = ""	
			bestscore = 0.0
			for item in tractscore.keys(): #item is phrase|lemma
				if tractscore[item] >= bestscore and item not in best and item not in self.semlex[category]:
					bestscore = tractscore[item]
					bestex = item
				else:
					continue
			if not bestex: #just for sparse test data
				continue
			best.append(bestex)
		return best
	def expandpatterns(self): 
		#Getting frequency values for patterns:
		pattswithsempref = {} # Contains all the best patterns along with their semantic preferences and their roles. Pattern is key, value is ["sempref*role"]
		currpatt = ""
		pattfreq = 0
		semfreq = {} # Contains the frequency of each semantic category. The categories are keys, values are their frequency.
		for mysemcat in self.semlex.keys():
			semfreq[mysemcat] = 0
		with open(self.devdir+"patternsandsemlex.out", 'r+') as allpatts:
			for line in allpatts:
				myline = line.strip()
				if "SEMLEX" in myline:
					if currpatt:
						prefpatt = self.findsempref(pattfreq, semfreq)
						if currpatt not in pattswithsempref.keys():
							pattswithsempref[currpatt] = []
						for item in prefpatt:
							pattswithsempref[currpatt].append(item)
					break
				if "PATTERNS" in myline:
					continue
				elif "||" in myline and currpatt:
					#Here I want to count all freqs to get pattern frequence, sfreq for each semcat.
					extract = myline.replace("|", "")
					pattfreq += 1
					for item in self.semlex.keys():
						if extract in self.semlex[item]:
							semfreq[item] +=1
						else:
							continue
				elif "||" in myline and not currpatt:
					continue
				else:
					if myline in self.bestpatterns:
						prefpatt = self.findsempref(pattfreq, semfreq)
						if currpatt not in pattswithsempref.keys():
							pattswithsempref[currpatt] = []
						for item in prefpatt:
							pattswithsempref[currpatt].append(item)
						#Resetting:
						for freqkey in semfreq.keys():
							semfreq[freqkey] = 0
						pattfreq = 0
						currpatt = myline
						continue
					else:
						# Finish finding sempref for the pattern I was looking at, write somewhere, reset all freq stats
						prefpatt = self.findsempref(pattfreq, semfreq)
						if currpatt not in pattswithsempref.keys():
							pattswithsempref[currpatt] = []
						for item in prefpatt:
							pattswithsempref[currpatt].append(item)
						#Resetting:
						currpatt = ""
						pattfreq = 0
						for freqkey in semfreq.keys():
							semfreq[freqkey] = 0
						continue
		return pattswithsempref 
	def findsempref(self, pattfreq, semfreq):
		#Finding the semantic preference of each pattern.
		semprefs = []
		for each in self.semlex.keys():
			if self.semcatstrong(pattfreq, semfreq[each]):
				role = self.catroles[each]
				mystring = "{}*{}".format(each, role)
				semprefs.append(mystring)
		return semprefs
	def semcatstrong(self, pfreq, sfreq):
		F1 = 3
		F2 = 2
		P = 0.1
		if pfreq == 0:
			return False
		prob = float(sfreq)/float(pfreq)
		if sfreq >= F1 or (sfreq >= F2 and prob <= P):
			return True
		else:
			return False
	def mergepatterns(self, pattswithsempref):
		#Make triggerdict from bestpatterns
		triggerdict = {}
		frames = []
		print len(pattswithsempref), len(self.bestpatterns)
		for pattern in self.bestpatterns:
			thistrigger = helpers.getpatterntrigger(pattern)
			if thistrigger not in triggerdict:
				triggerdict[thistrigger] = []
			if pattern not in triggerdict[thistrigger]:
				triggerdict[thistrigger].append(pattern)
		#Merging patterns into frames, filling frames[]
		for trigger in triggerdict:
			activeframe = Frame(trigger, "active") 
			passiveframe = Frame(trigger, "passive")
			nounframe = Frame(trigger, "noun")
			patternlist = triggerdict[trigger]
			for patt in patternlist:
				mytype = helpers.gettriggertype(patt)
				semprefs = pattswithsempref[patt]
				if mytype == "active":
					activeframe.addpattern(patt, semprefs)
				elif mytype == "passive":
					passiveframe.addpattern(patt, semprefs)
				elif mytype == "noun":
					nounframe.addpattern(patt, semprefs)
				else:
					print "Couldn't find triggertype, can't add pattern! Type: {}".format(mytype)
			if activeframe.isnotempty():
				frames.append(activeframe)
			if passiveframe.isnotempty():
				frames.append(passiveframe)
			if nounframe.isnotempty():
				frames.append(nounframe)
			continue
		return frames
	def reviewall(self):
		#This requires manually reviewing patterns and words for the semantic lexicon the program has churned out into patternsandsemlex.out. Manually chosen patterns need to be added to the file bestpatterns.out and words for each semantic category to semlex_X.out, where X is the name of each semantic category.
        		# When this has been done the program can continue.
		while True:
			response = raw_input("Have semlex_X.out files been reviewed and bestpatterns.out created with reviewed patterns from m? y/n\n")
			if response is "n":
				print "Then do it now."
				continue
			elif response is "y":
				print "\tUpdating semantic lexicon and patterns..."
				with open(self.devdir+'bestpatterns.out', 'r+') as pattfile:
					for line in pattfile:
						self.bestpatterns.append(line.strip())
				for category in self.semlex: #Emptying self.semlex and writing updated semlex to files
					self.semlex[category] = []
					myfilename = "{}semlex_{}.out".format(self.devdir, category)
					#print myfilename
					if not os.path.isfile(myfilename):
						print "The file {} does not exist.".format(myfilename)
					with open (myfilename) as X:
						for line in X:
							self.semlex[category].append(line.strip())
					X.close()
				return
			else:
				print "Invalid response. Try again."
				continue
		return
if __name__ == "__main__":
	print "to be implemented"