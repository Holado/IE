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

from shell import Shell
import treeops
import helpers
import extractops
from lxml import etree
import copy
import os

class Translator():
	def __init__(self, frames, semlexcollection, patterncollection, prepcollection, language):
		self.shell = Shell()
		self.frames = frames #Key is trigger ("trigger, active"), value is frame object
		self.filledframes = []
		self.semlex = {}
		self.patterns = {}
		self.prepositions = {}
		self.language = language
		self.semlexcollection = semlexcollection
		self.patterncollection = patterncollection
		self.prepcollection = prepcollection
	def tester(self, triggerdict, transdir):
		with open("testresults.out", "w+") as outfile:
			for X in [f for f in os.listdir(transdir) if f.endswith('.txt')]: 
				outfile.write(X+"\n")
				with open(transdir+X, 'r') as Xfile:
					for line in Xfile:
						totranslate = line.strip()
						outfile.write(totranslate+"\n")
						parsedstring, all_lemmas = self.shell.make_translatefiles(totranslate)
						parsed_sentence = list()
						for line in parsedstring.split("\n"):
							parsed_sentence.append(line)
							if "</SENTENCE>" in line:
								found = False
								sentence_string = " ".join(parsed_sentence) 
								parsed_sentence = list() #Resetting the collection
								if not all_lemmas:
									continue
								lemma_string = all_lemmas.pop(0)
								#print "LEMMA STRING: {}".format(lemma_string)
								lemmas_for_sentence = lemma_string.split(" ")
								for word in lemmas_for_sentence:
									if word in triggerdict:
										found = True
								if not found:
									continue #No possible trigger found in sentence, moving on.
								else: #Found possible trigger in sentence, need to process sentence.
									self.fillframes(sentence_string, lemmas_for_sentence, triggerdict) 
								for a in self.filledframes:
									outfile.write("Trigger: {}, {}\n".format(a.trigger, a.triggertype))
									for patt in a.patterns.keys():
										if a.patternhasextracts(patt):
											outfile.write("\t{}\n".format(patt))
											for ex in a.getextracts(patt):
												outfile.write("\t\t{}\n".format(ex))
								self.filledframes = [] #Emptying filledframes
					Xfile.close()
	def translate(self, totranslate, language, triggerdict):
		self.setlanguage(language)
		parsedstring, all_lemmas = self.shell.make_translatefiles(totranslate)
		parsed_sentence = list()
		for line in parsedstring.split("\n"):
			parsed_sentence.append(line)
			if "</SENTENCE>" in line:
				found = False
				sentence_string = " ".join(parsed_sentence) 
				parsed_sentence = list() #Resetting the collection
				if not all_lemmas:
					continue
				lemma_string = all_lemmas.pop(0)
				lemmas_for_sentence = lemma_string.split(" ")
				for word in lemmas_for_sentence:
					if word in triggerdict:
						found = True
				if not found:
					continue #No possible trigger found in sentence, moving on.
				else: #Found possible trigger in sentence, need to process sentence.
					self.fillframes(sentence_string, lemmas_for_sentence, triggerdict) 
		#Merging frames
		for eachframe in self.filledframes:
			compatible = True
			for another in self.filledframes:
				if eachframe.gettrigger() is another.gettrigger():
					for patt in set(eachframe.patterns) & set(eachframe.patterns):
						if eachframe.patternhasextracts(patt) and another.patternhasextracts(patt):
							compatible = False
							break
						else:
							continue
				else:
					continue
				if compatible:
					for mypatt in set(eachframe.patterns) & set(eachframe.patterns):
						if eachframe.patternhasextracts(mypatt):
							continue
						elif another.patternhasextracts(mypatt):
							myextract = another.getextracts(mypatt)[0]
							eachframe.addextract(mypatt, myextract)
						else: #Neither has extract
							continue
					self.filledframes.remove(another)				
		for eachframe in self.filledframes:
			self.translateframe(eachframe)
	def translateframe(self, frame):
		#In: Pattern along with extract, possibly choice of language 
		#Out: "translation" of pattern in context with extract
		#If can't find word in dictionary, send through untranslated.
		subj, iobj, obj, comp, pp = "", "", "", "", ""
		triggerandtype = self.gettriggerkey(frame)
		trigger = self.patterns[triggerandtype]
		pps = []
		extractfound = False
		for eachpatt in frame.getpatterns():
			if frame.patternhasextracts(eachpatt):
				extractfound = True
				mytype = helpers.getextracttype(eachpatt)
				extracts = frame.getextracts(eachpatt)
				if "subj" in mytype:
					phrase = []
					for eachword in extracts[0].split("*")[0].split(" "):
						if eachword not in self.semlex.keys():
							phrase.append(eachword)
						else:
							phrase.append(self.semlex[eachword])
					subj = " ".join(phrase)
				elif "iobj" in mytype:
					phrase = []
					for eachword in extracts[0].split("*")[0].split(" "):
						if eachword not in self.semlex.keys():
							phrase.append(eachword)
						else:
							phrase.append(self.semlex[eachword])
					iobj = " ".join(phrase)
				elif "obj" in mytype:
					phrase = []
					for eachword in extracts[0].split("*")[0].split(" "):
						if eachword not in self.semlex.keys():
							phrase.append(eachword)
						else:
							phrase.append(self.semlex[eachword])
					obj = " ".join(phrase)
				elif "comp" in mytype:
					phrase = []
					for eachword in extracts[0].split("*")[0].split(" "):
						if eachword not in self.semlex.keys():
							phrase.append(eachword)
						else:
							phrase.append(self.semlex[eachword])
					comp = " ".join(phrase)
				elif "noun" in mytype:
					phrase = []
					prep = helpers.getpatternprep(eachpatt)
					translated_prep = self.prepositions[prep]
					for thisphrase in extracts:
						phrase.append(translated_prep)
						for eachword in thisphrase.split("*")[0].split(" "):
							if eachword not in self.semlex.keys():
								phrase.append(eachword.strip())
							else:
								phrase.append(self.semlex[eachword])
						pps.append(" ".join(phrase))
					pp = " ".join(pps)
				else:
					continue
			else:
				continue
		if "english" in self.language:
			mysentence = [subj, trigger, iobj, obj, comp, pp]
			for item in mysentence:
				if not item:
					mysentence.remove(item)
			if not extractfound: #Don't want to print if only the trigger is available
				return
			mystring = " ".join(mysentence)
			print mystring
		elif "polish" in self.language:
			mysentence = [subj, trigger, iobj, obj, comp, pp]
			for item in mysentence:
				if not item:
					mysentence.remove(item)
			mystring = " ".join(mysentence)
			print mystring
		elif "icelandic" in self.language:
			mysentence = [subj, trigger, iobj, obj, comp, pp]
			for item in mysentence:
				if not item:
					mysentence.remove(item)
			mystring = " ".join(mysentence)
			print mystring

	def fillframes(self, sentence_string, lemmas_for_sentence, triggerdict):
		#Fills frames in self.filledframes with extracts.
		root = treeops.getroot(sentence_string)
		root = treeops.addlemmas(root, lemmas_for_sentence)
		for node in root.findall(".//WORD"):
			thislemma = treeops.lemma(node)
			if thislemma in triggerdict:
				trigtype = treeops.gettriggertype(node)
				if trigtype is "None":
					continue
				else: #Found a valid trigger, checking if have compatible frame.
					if trigtype in triggerdict[thislemma][0]:
						myframe = copy.deepcopy(triggerdict[thislemma][1]) #Deepcopy keeps changes to myframe from influencing the original frame in triggerdict. 
						for patt in myframe.getpatterns():
							extype = helpers.getextracttype(patt)
							if "subj" in extype:
								whole, head = extractops.findsubjextract(patt, node, root)
								if head:
									myextract = head+"*"+whole+"*"+treeops.tag(node)
									myframe.addextract(patt, myextract)
							elif "iobj" in extype:
								whole, head = extractops.findiobjextract(patt, node, root)
								if head:
									myextract = head+"*"+whole+"*"+treeops.tag(node)
									myframe.addextract(patt, myextract)
							elif "obj" in extype:
								whole, head = extractops.findobjextract(patt, node, root)
								if head:
									myextract = head+"*"+whole+"*"+treeops.tag(node)
									myframe.addextract(patt, myextract)
							elif "comp" in extype:
								whole, head = extractops.findcompextract(patt, node, root)
								if head:
									myextract = head+"*"+whole+"*"+treeops.tag(node)
									myframe.addextract(patt, myextract)
							elif "noun" in extype:
								whole, head = extractops.findppextract(patt, node, root)
								if head:
									myextract = head+"*"+whole+"*"+treeops.tag(node)
									myframe.addextract(patt, myextract)
							else:
								continue
						if myframe.hasextracts():
							self.filledframes.append(myframe)
			else:
				continue
		return 
	def gettriggerkey(self, frame):
		#In: Pattern containing information to form the trigger translation key
		#Out: A correctly formed trigger translation key
		trigger = frame.gettrigger()
		triggertype = frame.gettriggertype()
		triggerandtype = trigger+"|"+triggertype
		return triggerandtype
	def setlanguage(self, language):
		if "english" in language:
			self.semlex = self.semlexcollection[0]
			self.patterns = self.patterncollection[0]
			self.prepositions = self.prepcollection[0]
		elif "polish" in language:
			self.semlex = self.semlexcollection[1]
			self.patterns = self.patterncollection[1]
			self.prepositions = self.prepcollection[1]
		elif "icelandic" in language:
			self.semlex = self.semlexcollection[2]
			self.patterns = self.patterncollection[2]
			self.prepositions = self.prepcollection[2]
		else:
			print "WARNING: Language is not properly defined. Translation won't work."
if __name__ == "__main__":
	print "Implement if needed"
