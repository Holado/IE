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
from lxml import etree
import helpers

def getroot(sentence_string):
	root = etree.fromstring(sentence_string)
	return root
def addlemmas(root, lemmalist):
	for node in (node for node in root.iter() if isleaf(node)):
		parent = node.getparent()
		lemmanode = etree.SubElement(parent, "LEMMA")
		lemmanode.text = lemmalist.pop(0).decode('utf-8')
	return root
def gettriggerverb(node):
	mylemma = ""
	for word in (word for word in node.findall(".//WORD") if not "a" in tag(word)[0] and not "cn" in tag(word)):
		mylemma = lemma(word)
	return mylemma
def gettriggernoun(node):
	trigger = ""
	for word in (word for word in node.findall(".//WORD") if not trigger and isnoun(word) and not "qual" in tag(word)):
		trigger = lemma(word)
	for word in (word for word in node.findall(".//WORD-done") if not trigger and isnoun(word) and not "qual" in tag(word)):
		trigger = lemma(word)
	return trigger 
def gettriggeradj(node): #Or numeral
	trigger = ""
	for word in (word for word in node.findall(".//WORD") if not trigger and (isadj(word) or isnum(word)) and not "qual" in tag(word)):
		trigger = lemma(word)
	for word in (word for word in node.findall(".//WORD-done") if not trigger and (isadj(word) or isnum(word)) and not "qual" in tag(word)):
		trigger = lemma(word)
	return trigger 
def getnounphrase(node, root):
	# In: node containing possible head, root
	# Out: String containing the lemma for the head, string containing lemmas for the whole phrase and a string containing the case of the head.
	# For purposes of pattern search, if head is not found, case from first node is used.
	phrase, head, mycase = "", "", ""
	extracase, extrahead = "", "" #In case I don't find a real head.
	parts = []
	phrasetype = helpers.cleanfunction(text(node)) #To check if more than one in a row
	posshead = ""
	words = node.findall(".//WORD")
	for word in words:
		wtext = lemma(word)
		if word is last(root):
			wtext = helpers.period(wtext)
		if isnoun(word):
			head = lemma(word)
			mycase = headcase(tag(word))	
		elif isadj(word):
			posshead = word
		parts.append(wtext)
	if not head: # Haven't found head, collect extrahead
		extrahead = helpers.period(lemma(words[0]))
		extracase = headcase(tag(words[0]))
	marksubtreedone(node)
	parent = getparentphrase(node, root)
	#Checking before
	current = parent
	before = []
	while current.getprevious() is not None:
		current = current.getprevious()
		ctext = helpers.cleanfunction(text(current))
		if not ctext:
			continue
		if "qual" in ctext or "timex" in ctext or ctext in "ap" or ctext in "aps" or ctext in "np" or ctext in "nps" or phrasetype in ctext:
			for item in current.findall(".//WORD"):
				itext = lemma(item)
				if item is last(root):
					itext = helpers.period(itext)
				if not head:
					if isnoun(item):
						head = lemma(item)
						mycase = headcase(tag(item))
					elif isadj(item) and not posshead:
						posshead = item
				before.append(itext)
			marksubtreedone(current)
		else:
			break
	if before:
		before_reversed = before[::-1]
		before_reversed.extend(parts)
		parts = before_reversed
	#Checking after
	current = parent
	after = []
	while current.getnext() is not None:
		current = current.getnext()
		ctext = helpers.cleanfunction(text(current))
		if not ctext:
			continue
		if "comp" in ctext or "qual" in ctext or "timex" in ctext or ctext in "np" or ctext in "nps" or ctext in "ap" or ctext in "aps" or phrasetype in ctext:
			for item in current.findall(".//WORD"):
				itext = lemma(item)
				if item is last(root):
					itext = helpers.period(itext)
				if not head:
					if isnoun(item):
						head = lemma(item)
						mycase = headcase(tag(item))
					elif isadj(item):
						posshead = item
				after.append(itext)
			marksubtreedone(current)
		else:
			break
	if after:
		parts.extend(after)
	phrase = " ".join(parts)
	if not head:
		if posshead:
			head = lemma(posshead)
			mycase = headcase(tag(posshead))
		else:
			return phrase, extrahead, extracase
	return phrase, head, mycase
def getextractphrase(node, root):
	# In: node containing possible head, root
	# Out: String containing the lemma for the head, string containing lemmas for the whole phrase and a string containing the case of the head.
	phrase, head, mycase = "", "", ""
	parts = []
	phrasetype = helpers.cleanfunction(text(node)) #To check if more than one in a row
	posshead = ""
	for word in node.findall(".//WORD"):
		wtext = lemma(word)
		if word is last(root):
			wtext = helpers.period(wtext)
		if isnoun(word):
			head = lemma(word)
			mycase = headcase(tag(word))
		elif isadj(word): # if alone in phrase, should be head
			posshead = word
		parts.append(wtext)
	marksubtreedone(node)
	parent = getparentphrase(node, root)
	#Checking before
	current = parent
	before = []
	while current.getprevious() is not None:
		current = current.getprevious()
		ctext = helpers.cleanfunction(text(current))
		if not ctext:
			continue
		if "qual" in ctext or "timex" in ctext or ctext in "ap" or ctext in "aps" or ctext in "np" or ctext in "nps" or phrasetype in ctext:
			for item in current.findall(".//WORD"):
				itext = lemma(item)
				if item is last(root):
					itext = helpers.period(itext)
				if not head:
					if isnoun(item):
						head = lemma(item)
						mycase = headcase(tag(item))
					elif isadj(item) and not posshead:
						posshead = item
				before.append(itext)
			marksubtreedone(current)
		else:
			break
	if before:
		before_reversed = before[::-1]
		before_reversed.extend(parts)
		parts = before_reversed
	#Checking after
	current = parent
	after = []
	while current.getnext() is not None:
		current = current.getnext()
		ctext = helpers.cleanfunction(text(current))
		if not ctext:
			continue
		if "comp" in ctext or "qual" in ctext or "timex" in ctext or ctext in "np" or ctext in "nps" or ctext in "ap" or ctext in "aps" or phrasetype in ctext:
			for item in current.findall(".//WORD"):
				itext = lemma(item)
				if item is last(root):
					itext = helpers.period(itext)
				if not head:
					if isnoun(item):
						head = lemma(item)
						mycase = headcase(tag(item))
					elif isadj(item) and not posshead:
						posshead = item
				after.append(itext)
			marksubtreedone(current)
		else:
			break
	if after:
		parts.extend(after)
	phrase = " ".join(parts)
	if not head:
		if posshead:
			head = lemma(posshead)
			mycase = headcase(tag(posshead))
		else:
			return "", "", ""
	return phrase, head, mycase
def tag(node):
	tag = helpers.cleantag(node[0].text)
	return tag
def headcase(mytag):
	#Only finds the case from the tag, doesn't have to search for head of phrase
	case = ""
	caseplace = ""
	if "n" in mytag[0]: # Noun
		caseplace = mytag[3]
	elif "l" in mytag[0]: # Adjective
		caseplace = mytag[5]
	elif "f" in mytag[0] or "t" in mytag[0]: # Pronoun
		if mytag in "ta" or mytag in "to":
			return ""
		caseplace = mytag[4]
	elif "g" in mytag[0]:
		caseplace = mytag[3]
	else:
		return ""
	if "n" in caseplace:
		case = "nom"
	elif "o" in caseplace:
		case = "acc"
	elif "e" in caseplace:
		case = "gen"
	elif "þ" in mytag:
		case = "dat"
	else:
		return "" #A stopword, other category than noun.
	return case
def lemma(node):
	mylemma = helpers.clean(node[1].text)
	return mylemma
def text(node):
	text = helpers.clean(node.text)
	return text
def getparentphrase(node, root):
	current = node
	while True:
		if root is current.getparent():
			break
		else:
			current = current.getparent()
			continue
		break
	return current       
def isleaf(node): 
	if len(node) == 0:
		return True
	else:
		return False
def isnoun(node):
	return ("n" in tag(node)[0])
def isadj(node):
	return ("l" in tag(node)[0])
def isnum(node):
	return ("t" in tag(node)[0])
def yester(node):
	words = node.findall(".//WORD")
	if len(words) < 2:
		return False
	elif text(words[0]) in "í" and text(words[1]) in "gær":
		return True
	else:
		return False
def marksubtreedone(node):
	for subnode in node.iter():
		subnode.tag = subnode.tag+"-done"
	return 
def last(root):
	words = root.findall(".//WORD")
	return words[-1]
def isactive(node):
	nodetag = tag(node)
	if "þ" in nodetag[1]:
		return False
	else:
		return True
def istrigger(node):
	nodetag = tag(node)
	wordcat = nodetag[0]
	if "n" in wordcat or "s" in wordcat or "l" in wordcat or "t" in wordcat:
		return True
	else:
		return False
def gettriggertype(node):
	if not istrigger(node):
		return "None"
	if isnoun(node):
		return "noun"
	elif isactive(node):
		return "active"
	else:
		return "passive"
def triggermatch(patt, node):
	#Checks if pattern trigger PoS matches node. If trigger is verb, checks if active/passive matches.
	if not istrigger(node):
		return False
	patttype = helpers.gettriggertype(patt)
	nodetype = gettriggertype(node)
	if patttype is nodetype:
		return True
	else:
		return False
def mainverb(node, root):
    # If inflected verb found check for other verbs. If found, return False. Else return True.
    # If verb not inflected, return True.
	if isnoun(node):
		return True
	verbtype = tag(node)[1]
	if "b" in verbtype or "f" in verbtype or "v" in verbtype:
		parent = getparentphrase(node, root)
		current = parent
		while current.getprevious() is not None:
			current = current.getprevious()
			mytext = text(current)
			if "vp" in mytext and not "advp" in mytext:
				for item in current.findall(".//WORD"):
					newverbtype = tag(item)[1]
					if "b" in newverbtype or "f" in newverbtype or "v" in newverbtype:
						continue
					else:
						return False 
			elif "pp" in mytext or "advp" in mytext:
				continue
			else:
				break
		current = parent
		while current.getnext() is not None:
			current = current.getnext()
			mytext = text(current)
			if "vp" in mytext and not "advp" in mytext:
				for item in current.findall(".//WORD"):
					newverbtype = tag(item)[1]
					if "b" in newverbtype or "f" in newverbtype or "v" in newverbtype:
						continue
					else:
						return False 
			elif "pp" in mytext or "advp" in mytext:
				continue
			else:
				break
		return True
	elif "n" in verbtype or "s" in verbtype or "l" in verbtype or "þ" in verbtype:
		return True
	else:
		return False
if __name__ == "__main__":
	print "to test"
