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
from frame import Frame
import os.path

class Data():
	def getstartsemlex(self, devdir):
		semlexpath = "./"+devdir+"semlex_seed.in"
		if not os.path.isfile(semlexpath):
			print "WARNING: Seed words for the semantic lexicon have not been defined. Please create file 'semlex_seed.in' in the correct folder."
			return ""
		semlex = {} # Stores the semantic lexicon. Key is name of semantic category, value is the list of seed words (later list of all words in that semantic category)
		semroles = {} # Stores the semantic role for each category. Key is semantic category, value is the semantic role.
		with open(semlexpath, 'r') as seed_semlex:
			for line in seed_semlex:
				both = line.split("\t") #[0] is the name of the semantic category and semantic role, [1] is a list of seed words
				catandrole = both[0].strip().split("|") #[0] is name of semantic category, [1] is semantic role
				seeds = both[1].strip().split("|")
				updated = []
				for each in seeds:
					each = each.strip()
					eachUpdated = each+"|"+each
					updated.append(eachUpdated)
				semlex[catandrole[0]] = updated
				semroles[catandrole[0]] = catandrole[1]
		return semlex, semroles
	def readsemlextranslationsfromfile(self, mymap):
		#In: A file containing lemmas for Icelandic terms and the translation, separated by "\t"
		#Out: A list of dictionaries containing semantic lexicon words along with tags as key and translations as value
		#Note: These dictionaries are kept each in their own file, that makes reading them easier.
		all_semlex = []
		semlex_english = {}
		with open("./"+mymap+"English_semlex.out", 'r') as englishfile:
			for line in englishfile:
				both = line.split("\t") #[0] is Icelandic word, [1] is translation
				semlex_english[both[0].strip()] = both[1].strip()
		all_semlex.append(semlex_english)		
		semlex_polish = {}
		with open("./"+mymap+"Polish_semlex.out", 'r') as polishfile:
			for line in polishfile:
				both = line.split("\t") #[0] is Icelandic word, [1] is translation
				semlex_polish[both[0].strip()] = both[1].strip()
		all_semlex.append(semlex_polish)
		semlex_icelandic = {}
		with open("./"+mymap+"Icelandic_semlex.out", 'r') as icelandicfile:
			for line in icelandicfile:
				both = line.split("\t") #[0] is Icelandic word, [1] is translation
				semlex_icelandic[both[0].strip()] = both[1].strip()
		all_semlex.append(semlex_icelandic)
		return all_semlex
	def readpatterntranslationsfromfile(self, mymap):
		# Reads translations of patterns from files.
		all_frames = []
		frames_english = {}
		with open("./"+mymap+"English_patterns.out", 'r') as englishfile:
			for line in englishfile:
				both = line.split("\t") #[0] is Icelandic trigger, [1] is translation of trigger
				frames_english[both[0].strip()] = both[1].strip()
		all_frames.append(frames_english)
		frames_polish = {}
		with open("./"+mymap+"Polish_patterns.out", 'r') as polishfile:
			for line in polishfile:
				both = line.split("\t") #[0] is Icelandic trigger, [1] is translation of trigger
				frames_polish[both[0].strip()] = both[1].strip()
		all_frames.append(frames_polish)	
		frames_icelandic = {}
		with open("./"+mymap+"Icelandic_patterns.out", 'r') as icelandicfile:
			for line in icelandicfile:
				both = line.split("\t") #[0] is Icelandic trigger, [1] is translation of trigger
				frames_icelandic[both[0].strip()] = both[1].strip()
		all_frames.append(frames_icelandic)	
		return all_frames
	def readpreptranslationsfromfile(self, mymap):
		# Reads translations of prepositions from files.
		all_prep = []
		prep_english = {}
		with open("./"+mymap+"English_prep.out", 'r') as englishfile:
			for line in englishfile:
				both = line.split("\t") #[0] is Icelandic preposition, [1] is translation of trigger
				prep_english[both[0].strip()] = both[1].strip()
		all_prep.append(prep_english)
		prep_polish = {}
		with open("./"+mymap+"Polish_prep.out", 'r') as polishfile:
			for line in polishfile:
				both = line.split("\t") #[0] is Icelandic preposition, [1] is translation of trigger
				prep_polish[both[0].strip()] = both[1].strip()
		all_prep.append(prep_polish)
		prep_icelandic = {}
		with open("./"+mymap+"Icelandic_prep.out", 'r') as icelandicfile:
			for line in icelandicfile:
				both = line.split("\t") #[0] is Icelandic preposition, [1] is translation of trigger
				prep_icelandic[both[0].strip()] = both[1].strip()
		all_prep.append(prep_icelandic)
		return all_prep
	def readframesfromfile(self, mymap):
		framedict = {} #Key is trigger ("trigger, active"), value is frame object
		triggerdict = {} #Key is trigger ("trigger"), value is ["POS", frame object]
		pattern = ""
		semprefs = []
		frame = ""
		with open("./"+mymap+"myframes.out", 'r') as framefile:
			for line in framefile:
				if "\t\t" in line: #Found sempref
					semprefs.append(line.strip())
					continue
				elif "\t" in line: #Found pattern
					if pattern:
						frame.addpattern(pattern, semprefs)
						pattern = ""
						semprefs = []
					pattern = line.strip()
					continue
				elif "Trigger:" in line:
					if pattern:
						frame.addpattern(pattern, semprefs)
						pattern = ""
						semprefs = []
					#add former pattern and sempref to list
					triggerandtype = line.strip()[9:]
					both = triggerandtype.split(", ") #both[0] is trigger, both[1] is type
					frame = Frame(both[0], both[1])
					framedict[triggerandtype] = frame
					triggerdict[both[0].strip()] = [both[1].strip(), frame]
				else:
					continue
			frame.addpattern(pattern, semprefs)
			framedict[triggerandtype] = frame 
			both = triggerandtype.split(", ")
			triggerdict[both[0].strip()] = [both[1].strip(), frame]
			# Making the triggerdict for the translation part
			triggerlist = []
			for key in framedict.keys():
				trigger = key.split(", ")[0]
				triggerlist.append(trigger.strip())
		return framedict, triggerdict
