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

# Given trigger, finds extract.
import treeops
import helpers

def findsubjextract(patt, node, root):
	whole, head = "", ""
	parent = treeops.getparentphrase(node, root)
	current = parent
	while current.getprevious() is not None:
		current = current.getprevious()
		text = treeops.text(current)
		if "advp" in text or "pp" in text or "vp" in text or "qual" in text or "timex" in text or text in "np" or text in "nps" or text in "ap" or text in "aps":
			continue
		elif "subj" in text:
			whole, head, excase = treeops.getextractphrase(current, root)
			break
		elif "scp" in text: # =Maðurinn= sem *beit* hestinn
			newcurrent = current.getprevious()
			ntext = treeops.text(current)
			if "advp" in ntext or "pp" in ntext or "qual" in ntext or "timex" in ntext or ntext in "np" or ntext in "nps" or ntext in "ap" or ntext in "aps": 
				continue
			elif "subj" in ntext:
				whole, head, excase = treeops.getextractphrase(current, root)
				break
		else:
			break
	if not head: 
		current = parent
		while current.getnext() is not None:
			current = current.getnext()
			text = treeops.text(current)
			if "advp" in text or "pp" in text or "qual" in text or "timex" in text or "vp" in text or text in "np" or text in "nps" or text in "ap" or text in "aps":
				continue
			elif "subj" in text:
				whole, head, excase = treeops.getextractphrase(current, root)
				break
			else:
				break
	if not head: # Looking  for AP-COMP acting as subj
		current = parent
		while current.getprevious() is not None:
			current = current.getprevious()
			text = treeops.text(current)
			if "advp" in text or "pp" in text or "vp" in text or "qual" in text or "timex" in text or text in "np" or text in "nps":
				continue
			elif text in "ap-comp" or text in "aps-comp":
				whole, head, excase = treeops.getextractphrase(current, root)
				break
			elif "scp" in text: # =Maðurinn= sem *beit* hestinn
				newcurrent = current.getprevious()
				ntext = treeops.text(current)
				if "advp" in ntext or "pp" in ntext or "qual" in ntext or "timex" in ntext or ntext in "np" or ntext in "nps": 
					continue
				elif ntext in "ap-comp" or ntext in "aps-comp":
					whole, head, excase = treeops.getextractphrase(current, root)
					break
			else:
				break
		if head:
			print "yay, ap-comp acting as np-subj! {}".format(whole)
	if not head:
		return "", ""
	pattcase = helpers.getpatterncase(patt)
	if pattcase not in excase and excase not in pattcase: 
		return "", "" 
	else:
		return whole, head

def findiobjextract(patt, node, root):
	whole, head = "", ""
	parent = treeops.getparentphrase(node, root)
	current = parent
	while current.getnext() is not None:
		current = current.getnext()
		text = treeops.text(current)
		if "advp" in text or "qual" in text or "timex" in text or "pp" in text or "vp" in text or text in "obj" or text in "np" or text in "nps" or text in "ap" or text in "aps":
			continue
		elif "iobj" in text:
			whole, head, excase = treeops.getextractphrase(current, root)
			break
		else:
			break
	if not head:
		current = parent
		while current.getprevious() is not None:
			current = current.getprevious()
			text = treeops.text(current)
			if "advp" in text or "pp" in text or "qual" in text or "timex" in text or "vp" in text or text in "obj" or text in "np" or text in "nps" or text in "ap" or text in "aps":
				continue
			elif "iobj" in text:
				whole, head, excase = treeops.getextractphrase(current, root)
				break
			else:
				break
	if not head:
		return "", ""
	pattcase = helpers.getpatterncase(patt)
	if pattcase not in excase and excase not in pattcase:
		return "", ""
	else:
		return whole, head

def findobjextract(patt, node, root):
	whole, head = "", ""
	parent = treeops.getparentphrase(node, root)
	current = parent
	while current.getnext() is not None:
		current = current.getnext()
		text = treeops.text(current)
		if "advp" in text or "pp" in text or "qual" in text or "timex" in text or "vp" in text or "iobj" in text or text in "np" or text in "nps" or text in "ap" or text in "aps":
			continue
		elif "obj" in text:
			whole, head, excase = treeops.getextractphrase(current, root)
			break
		else:
			break
	if not head: 
		current = parent
		while current.getprevious() is not None:
			current = current.getprevious()
			text = treeops.text(current)
			if "advp" in text or "pp" in text or "qual" in text or "timex" in text or "vp" in text or "iobj" in text or text in "np" or text in "nps" or text in "ap" or text in "aps":
				continue
			elif "obj" in text:
				whole, head, excase = treeops.getextractphrase(current, root)
				break
			else:
				break
	if not head:
		return "", ""
	pattcase = helpers.getpatterncase(patt)
	if pattcase not in excase and excase not in pattcase:
		return "", ""
	else:
		return whole, head
def findcompextract(patt, node, root):
	#subj is the trigger; the comp is the extract.
	whole, head = "", ""
	parent = treeops.getparentphrase(node, root)
	current = parent
	while current.getnext() is not None:
		current = current.getnext()
		text = treeops.text(current)
		if "advp" in text or "pp" in text or "qual" in text or "timex" in text or "vp" in text or text in "np" or text in "nps" or text in "ap" or text in "aps":
			continue
		elif "comp" in text:
			whole, head, excase = treeops.getextractphrase(current, root)
			break
		else:
			break
	if not head:
		return "", ""
	pattcase = helpers.getpatterncase(patt)
	if pattcase not in excase and excase not in pattcase:
		return "", "" 
	else:
		return whole, head
def findppextract(patt, node, root):
	whole, head, case = "", "", ""
	parts, prep = [], []
	parent = treeops.getparentphrase(node, root)
	current = parent
	while current.getnext() is not None:
		current = current.getnext()
		text = treeops.text(current)
		if treeops.yester(current): # Deals with "í gær" being categorized as ADVP, not PP
			pp = "í"
			whole = "gær"
			head = "gær"
			case = "nom"
			pattcase = helpers.getpatterncase(patt)
			if pattcase not in case and case not in pattcase: #Wrong pp phrase
				head, case = "", ""
				continue
			pattprep = helpers.getpatternprep(patt)
			if pp not in pattprep or pattprep not in pp:
				pp, head, case = "", "", ""
				continue
			break
		elif "advp" in text:
			for word in current.findall(".//WORD"):
				mytag = treeops.tag(word)
				if "a" in mytag[0]:
					prep.append(treeops.text(word))
					continue
			nowcurrent = current
			while nowcurrent.getnext() is not None:
				nowcurrent = nowcurrent.getnext()
				nowtext = treeops.text(nowcurrent)
				nowtext = nowtext.replace("[", "")
				if nowtext in "np" or nowtext in "nps" or "timex" in nowtext: #Want to treat as a pp phrase
					for word in nowcurrent.findall(".//WORD"):
						parts.append(treeops.lemma(word))
						if not head:
							if treeops.isnoun(word):
								head = treeops.lemma(word)
								case = treeops.headcase(treeops.tag(word))
					continue
				else:
					break
			if not parts or not prep: #Shouldn't be treated as pp phrase
				head, case, parts, prep = "", "", [], []
				continue
			pattcase = helpers.getpatterncase(patt)
			if pattcase not in case and case not in pattcase: #Wrong pp phrase
				head, case, parts, prep = "", "", [], []
				continue
			pp = " ".join(prep)
			pattprep = helpers.getpatternprep(patt)
			if pp not in pattprep or pattprep not in pp:
				pp, head, case, parts, prep = "", "", "", [], []
				continue
			whole = " ".join(parts)
			break
		elif "qual" in text or text in "np" or text in "nps" or text in "ap" or text in "aps" or "timex" in text:
			continue
		elif "pp" in text:
			for word in current.findall(".//WORD"):
				mytag = treeops.tag(word)
				if "a" in mytag[0]:
					prep.append(treeops.text(word))
					continue
				else:
					parts.append(treeops.lemma(word))
					if not head:
						if treeops.isnoun(word):
							head = treeops.lemma(word)
							case = treeops.headcase(treeops.tag(word))
			if not parts or not prep: #Weird pp phrase, continue search
				head, case, parts, prep = "", "", [], []
				continue
			pattcase = helpers.getpatterncase(patt)
			if pattcase not in case and case not in pattcase: #Wrong pp phrase
				head, case, parts, prep = "", "", [], []
				continue
			pp = " ".join(prep)
			pattprep = helpers.getpatternprep(patt)
			if pp not in pattprep or pattprep not in pp: #wrong preposition phrase
				pp, head, case, parts, prep = "", "", "", [], []
				continue
			if current.getnext() is not None and not head: # If I haven't found the head yet
				mynext = current.getnext()
				mytext = treeops.text(mynext)
				if "np" in mytext:
					for word in mynext.findall(".//WORD"):
						parts.append(treeops.lemma(word))
						if treeops.isnoun(word):
							head = treeops.lemma(word)
							case = treeops.headcase(treeops.tag(word))
					pp = " ".join(prep)
					whole = " ".join(parts)
					break
				else:
					break
			if not head:
				return "", ""
			pp = " ".join(prep)
			whole = " ".join(parts)
			break
		else:
			current = parent
			if current.getprevious() is not None:
				current = current.getprevious()
				text = treeops.text(current)
				if "scp" in text:
					if current.getprevious() is not None:
						current = current.getprevious() 
						text = treeops.text(current)
						if "pp" in text:
							for word in current.findall(".//WORD"):
								mytag = treeops.tag(word)
								if "a" in mytag[0]:
									prep.append(treeops.text(word))
									continue
								else:
									parts.append(treeops.lemma(word))
									if not head:
										if treeops.isnoun(word):
											head = treeops.lemma(word)
											case = treeops.headcase(treeops.tag(word))
							if not parts or not prep:
								return "", ""
							pattcase = helpers.getpatterncase(patt)
							if pattcase not in case and case not in pattcase: #Wrong pp phrase
								return "", ""
							pp = " ".join(prep)
							pattprep = helpers.getpatternprep(patt)
							if pp not in pattprep or pattprep not in pp:
								return "", ""
							if current.getnext() is not None and not head: # If I haven't found the head yet
								mynext = current.getnext()
								mytext = treeops.text(mynext)
								if "np" in text:
									for word in current.findall(".//WORD"):
										parts.append(treeops.lemma(word))
										if treeops.isnoun(word):
											head = treeops.lemma(word)
											case = treeops.headcase(treeops.tag(word))
									break
								else:
									break
							whole = " ".join(parts)
							break
						else:
							break
					else:
						break
				else:
					break
			else:
				break
	if not head:
		current = parent
		while current.getprevious() is not None:
			current = current.getprevious()
			text = treeops.text(current)
			text = text.replace("[", "")
			if treeops.yester(current):
				pp = "í"
				whole = "gær"
				head = "gær"
				case = "nom"
				pattcase = helpers.getpatterncase(patt)
				if pattcase not in case and case not in pattcase: #Wrong pp phrase
					head, case = "", ""
					continue
				pattprep = helpers.getpatternprep(patt)
				if pp not in pattprep or pattprep not in pp:
					pp, head, case = "", "", ""
					continue
				break
			elif "advp" in text:
				for word in current.findall(".//WORD"):
					mytag = treeops.tag(word)
					if "a" in mytag[0]:
						prep.append(treeops.text(word))
						continue
				nowcurrent = current
				while nowcurrent.getnext() is not None:
					nowcurrent = nowcurrent.getnext()
					nowtext = treeops.text(nowcurrent)
					nowtext = nowtext.replace("[", "")
					if nowtext in "np" or nowtext in "nps" or "timex" in nowtext: #Want to treat as a pp phrase
						for word in nowcurrent.findall(".//WORD"):
							parts.append(treeops.lemma(word))
							if not head:
								if treeops.isnoun(word):
									head = treeops.lemma(word)
									case = treeops.headcase(treeops.tag(word))
						continue
					else:
						break
				if not parts or not prep: #Shouldn't be treated as pp phrase
					head, case, parts, prep = "", "", [], []
					continue
				pattcase = helpers.getpatterncase(patt)
				if pattcase not in case and case not in pattcase: #Wrong pp phrase
					head, case, parts, prep = "", "", [], []
					continue
				pp = " ".join(prep)
				pattprep = helpers.getpatternprep(patt)
				if pp not in pattprep or pattprep not in pp:
					pp, head, case, parts, prep = "", "", "", [], []
					continue
				whole = " ".join(parts)
				break
			elif "qual" in text or text in "np" or text in "nps" or text in "ap" or text in "aps" or "timex" in text:
				continue
			elif "pp" in text:
				for word in current.findall(".//WORD"):
					mytag = treeops.tag(word)
					if "a" in mytag[0]:
						prep.append(treeops.text(word))
						continue
					else:
						parts.append(treeops.lemma(word))
						if not head:
							if treeops.isnoun(word):
								head = treeops.lemma(word)
								case = treeops.headcase(treeops.tag(word))
				if not parts or not prep: #Weird pp phrase, continue search
					head, case, prep = "", "", []
					continue
				pattcase = helpers.getpatterncase(patt)
				if pattcase not in case and case not in pattcase: #Wrong pp phrase
					head, case, parts, prep = "", "", [], []
					continue
				pp = " ".join(prep)
				pattprep = helpers.getpatternprep(patt)
				if pp not in pattprep or pattprep not in pp: #wrong preposition phrase
					pp, head, case, parts, prep = "", "", "", [], []
					continue
				whole = " ".join(parts)
				break
	if not head:
		return "", ""
	return whole, head
if __name__ == "__main__":
	print "To test implement this."
