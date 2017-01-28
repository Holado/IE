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

# Given noun phrase, finds trigger.

import treeops

def getsubjtrigger(node, root):
	verbtype, myverb = "active", ""
	current = node
	if ">" in treeops.text(node):
		while current.getnext() is not None:
			current = current.getnext()
			text = treeops.text(current)
			if "advp" in text or "np-qual" in text or "timex" in text or "subj" in text or text in "np" or text in "nps" or text in "ap" or text in "aps":
				continue
			elif "scp" in text:
				newcurrent = current.getnext()
				newtext = treeops.text(newcurrent)
				if "advp" in newtext or newtext in "np" or newtext in "nps" or newtext in "ap" or newtext in "aps" or "np-qual" in newtext or "timex" in text:
					newcurrent = newcurrent.getnext()
					newtext = treeops.text(newcurrent)
				elif "vp" in newtext:
					myverb = treeops.gettriggerverb(newcurrent)
					if "vpb" in newtext:
						loopcurrentnow = current
						while loopcurrentnow.getnext() is not None:
							loopcurrentnow = loopcurrentnow.getnext()
							ltext = treeops.text(loopcurrentnow)
							if "advp" in text or "pp" in text:
								continue
							elif "vpp-comp" in ltext:
								verbtype = "passive"
								myverb = treeops.gettriggerverb(loopcurrentnow)
								break 
							else:
								break
					else:
						loopcurrentnow = current
						while loopcurrentnow.getnext() is not None:
							loopcurrentnow = loopcurrentnow.getnext()
							ltext = treeops.text(loopcurrentnow)
							if "advp" in ltext:
								continue
							elif "vpi" in ltext:
								verbtype = "active"
								myverb = treeops.gettriggerverb(loopcurrentnow)
								break
							else:
								break
				elif "pp" in newtext:
					newcurrent = newcurrent.getnext()
					newtext = treeops.text(newcurrent)
				else:
					break
			elif "vp" in text:
				myverb = treeops.gettriggerverb(current) #the lemma of the main verb
				# I assume vpp-comp always comes with a vpb in the order vpb, vpp-comp.
				if "vpb" in text:
					loopcurrent = current
					while loopcurrent.getnext() is not None:
						loopcurrent = loopcurrent.getnext()
						ltext = treeops.text(loopcurrent)
						if "advp" in ltext or ltext in "np" or ltext in "nps" or ltext in "ap" or ltext in "aps" or "np-qual" in ltext or "timex" in ltext:
							continue
						elif "vpp-comp" in ltext:
							verbtype = "passive"
							myverb = treeops.gettriggerverb(loopcurrent)
							return myverb, verbtype 
						elif "pp" in ltext: #Need to check last because "pp" is in "vpp-comp" !
							continue
						else:
							break
				continue
			elif "pp" in text: #Need to check last because "pp" is in "vpp-comp" !
				continue
			else:
				break
	elif "<" in treeops.text(node):
		while current.getprevious() is not None:
			current = current.getprevious()
			text = treeops.text(current)
			if "advp" in text or text in "np" or text in "nps" or text in "ap" or text in "aps" or "np-qual" in text or "timex" in text:
				continue
			elif "vp" in text:
				myverb = treeops.gettriggerverb(current)
				if "vpp-comp" in text:
					verbtype = "passive" # This is the only verb phrase I need.
				loopcurrent = node # Checking if more to verb phrase
				while loopcurrent.getnext() is not None:
					loopcurrent = loopcurrent.getnext()
					ltext = treeops.text(loopcurrent)
					if "advp" in ltext or "np-qual" in ltext or ltext in "np" or ltext in "nps" or ltext in "ap" or ltext in "aps" or "timex" in ltext:
						continue
					elif "vpp" in ltext:
						myverb = treeops.gettriggerverb(loopcurrent)
						verbtype = "passive"
					elif "vpi" in ltext or "vps" in ltext or "vpg" in ltext:
						myverb = treeops.gettriggerverb(loopcurrent)
						continue # Because might be many in a row, want the last one
					elif "pp" in ltext:
						continue
					else:
						break # Nothing to be found, verb has non-auxiliary meaning
			elif "pp" in text:
				continue
			else:
				break
	else: # If no flag to point to trigger
		# First case: The phrase isn't really subj, it's the obj from active when the iobj is made subject of the passive
		# But I will call it a subj, but make sure I can use two subjs when merging and making active...
		# I can't see the difference between obj and iobj in the passive when acting as subj. Will have to deal with it anyway.
		# Second case: The object in an expletive sentence (leppsetning). Should look directly before.
		# Third case: Two or more NP-SUBJ in a row, only flag on one of them.
		if current.getprevious() is not None:
			before = current.getprevious()
			text = treeops.text(before)
			if "vpp-comp" in text:
				verbtype = "passive"
				myverb = treeops.gettriggerverb(before)
			elif "vpi" in text:
				verbtype = "active"
				myverb = treeops.gettriggerverb(before)				
			elif "subj<" in text or "subj>" in text or "comp<" in text or "comp>" in text:
				myverb, verbtype = getsubjtrigger(before, root)
		current = node
		if current.getnext() is not None and not myverb:
			after = current.getnext()
			text = treeops.text(after)
			if "subj<" in text or "subj>" in text or "comp<" in text or "comp>" in text:
				myverb, verbtype = getsubjtrigger(after, root)
	if not myverb:
		return "", ""
	return myverb, verbtype
def getobjtrigger(node, root):
	verbtype, myverb = "active", ""
	current = node
	if "<" in treeops.text(node):
		while current.getprevious() is not None:
			current = current.getprevious()
			text = treeops.text(current)
			if "iobj" in text or "advp" in text or "np-qual" in text or "timex" in text or text in "np" or text in "nps" or text in "ap" or text in "aps":
				continue
			elif "vp" in text:
				myverb = treeops.gettriggerverb(current)
				if "vpp-comp" in text:
					verbtype = "passive"
					continue 
				break 
			elif "pp" in text:
				continue 
			else:
				break
	elif ">" in node.text:
		while current.getnext() is not None:
			current = current.getnext()
			text = current.text
			if "iobj" in text or "advp" in text or "np" in text or text in "ap" or text in "aps": 
				continue
			elif "vp" in text:
				myverb = treeops.gettriggerverb(current)
				loopcurrent = current
				ltext = treeops.text(loopcurrent)
				while loopcurrent.getnext() is not None:
					loopcurrent = loopcurrent.getnext()
					if "advp" in ltext or "np" in ltext or ltext in "ap" or ltext in "aps": 
						continue
					elif "vpi" in ltext or "vps" in ltext or "vpp" in ltext or "vpg" in ltext:
						myverb = treeops.gettriggerverb(loopcurrent)
						continue #might be many in a row, only want the last one
					elif "pp" in ltext:
						continue
					else:
						break
			elif "pp" in text:
				continue
			else:
				break
	if not myverb:
		return "", ""
	return myverb, verbtype
def getiobjtrigger(node, root):
	verbtype, myverb = "active", ""
	current = node
	if "<" in treeops.text(node):
		while current.getprevious() is not None:
			current = current.getprevious()
			text = treeops.text(current)
			if "obj" in text or "advp" in text or "np-qual" in text or "timex" in text or text in "np" or text in "nps" or text in "ap" or text in "aps":
				continue
			elif "vp" in text:
				myverb = treeops.gettriggerverb(current)
				if "vpp" in text:
					verbtype = "passive"
			elif "pp" in text:
				continue
			else:
				break
	elif ">" in node.text:
		while current.getnext() is not None:
			current = current.getnext()
			text = current.text
			if "obj" in text or "advp" in text or "np" in text or text in "ap" or text in "aps": 
				continue
			elif "vp" in text:
				myverb = treeops.gettriggerverb(current)
				loopcurrent = current
				ltext = treeops.text(loopcurrent)
				while loopcurrent.getnext() is not None:
					loopcurrent = loopcurrent.getnext()
					if "advp" in ltext or "np" in ltext or ltext in "ap" or ltext in "aps":
						continue
					elif "vpi" in ltext or "vps" in ltext or "vpp" in ltext or "vpg" in ltext:
						myverb = treeops.gettriggerverb(loopcurrent)
						continue #might be many in a row, only want the last one
					elif "pp" in ltext:
						continue
					else:
						break
			elif "pp" in text:
				continue
			else:
				break
	if not myverb:
		return "", ""
	return myverb, verbtype
def getcomptrigger(node, root):
	#The flag points to the verb, so no use. The -COMP flag comes on the second NP, so the NP-SUBJ should always be in front.
	current = node
	trigger = ""
	triggertype = "compnoun"
	while current.getprevious() is not None:
		current = current.getprevious()
		text = treeops.text(current)
		if "np-subj" in text:
			trigger = treeops.gettriggernoun(current)
			break   
		elif "ap-comp" in text:
			trigger = treeops.gettriggeradj(current)
			break
	if not trigger: # Dealing with AP-COMP acting as subj
		triggertype = "active"
		while current.getnext() is not None:
			current = current.getnext()
			text = treeops.text(current)
			if "advp" in text or "np-qual" in text or "timex" in text or text in "np" or text in "nps" or text in "ap" or text in "aps":
				continue
			elif "scp" in text:
				newcurrent = current.getnext()
				newtext = treeops.text(newcurrent)
				if "advp" in newtext or newtext in "np" or newtext in "nps" or newtext in "ap" or newtext in "aps" or "np-qual" in newtext or "timex" in text:
					newcurrent = newcurrent.getnext()
					newtext = treeops.text(newcurrent)
				elif "vp" in newtext:
					myverb = treeops.gettriggerverb(newcurrent)
					if "vpb" in newtext:
						loopcurrentnow = current
						while loopcurrentnow.getnext() is not None:
							loopcurrentnow = loopcurrentnow.getnext()
							ltext = treeops.text(loopcurrentnow)
							if "advp" in text or "pp" in text:
								continue
							elif "vpp-comp" in ltext:
								verbtype = "passive"
								myverb = treeops.gettriggerverb(loopcurrentnow)
								break 
							else:
								break
					else:
						loopcurrentnow = current
						while loopcurrentnow.getnext() is not None:
							loopcurrentnow = loopcurrentnow.getnext()
							ltext = treeops.text(loopcurrentnow)
							if "advp" in ltext:
								continue
							elif "vpi" in ltext:
								verbtype = "active"
								myverb = treeops.gettriggerverb(loopcurrentnow)
								break
							else:
								break
				elif "pp" in newtext:
					newcurrent = newcurrent.getnext()
					newtext = treeops.text(newcurrent)
				else:
					break
			elif "vp" in text:
				myverb = treeops.gettriggerverb(current) #the lemma of the main verb
				# I assume vpp-comp always comes with a vpb in the order vpb, vpp-comp.
				if "vpb" in text:
					loopcurrent = current
					while loopcurrent.getnext() is not None:
						loopcurrent = loopcurrent.getnext()
						ltext = treeops.text(loopcurrent)
						if "advp" in ltext or ltext in "np" or ltext in "nps" or ltext in "ap" or ltext in "aps" or "np-qual" in ltext or "timex" in ltext:
							continue
						elif "vpp-comp" in ltext:
							verbtype = "passive"
							myverb = treeops.gettriggerverb(loopcurrent)
							return myverb, verbtype 
						elif "pp" in ltext: #Need to check last because "pp" is in "vpp-comp" !
							continue
						else:
							break
				continue
			elif "pp" in text: #Need to check last because "pp" is in "vpp-comp" !
				continue
			else:
				break
	return trigger, triggertype
def getpreptrigger(node, root):
	parts = [] #To account for multi word prepositions
	trigger, triggertype = "", ""
	parent = treeops.getparentphrase(node, root)
	for word in parent.findall(".//WORD"):
		newword = treeops.text(word)
		mytag = treeops.tag(word)
		if "a" in mytag[0]: #Found preposition
			parts.append(newword)
	if not parts: #No preposition found, have unmarked np to find correct trigger for.
		if parent.getprevious() is not None:
			previousnode = parent.getprevious()
			ptext = treeops.text(previousnode)
			if "pp" in ptext or "advp" in ptext:
				found = False #Checking if I find a noun in the phrase
				for aword in previousnode.findall(".//WORD"):
					newword = treeops.text(aword)
					mytag = treeops.tag(aword)
					if "a" in mytag[0]: #Found preposition
						parts.append(newword)
					elif "n" in mytag[0]: #Only applies to PP phrases
						found = True 
				if found:
					return "", ""
			elif "iobj" in ptext:
				trigger, triggertype = getiobjtrigger(previousnode, root)
				return trigger, triggertype
			elif "obj" in ptext:
				trigger, triggertype = getobjtrigger(previousnode, root)
				return trigger, triggertype
			elif "subj" in ptext:
				trigger, triggertype = getsubjtrigger(previousnode, root)
				return trigger, triggertype
			elif "ap" in ptext:
				if previousnode.getprevious() is not None:
					moreprevious = previousnode.getprevious()
					mtext = treeops.text(moreprevious)
					found = False
					if not "np" in mtext:
						return "", ""
					else:
						for every in moreprevious.findall(".//WORD"):
							etag = treeops.tag(every)
							if "a" in etag[0]:
								getpreptrigger(moreprevious, root)
							elif "n" in etag[0]:
								found = True
							else:
								continue
						if not found: #No noun in NP, can add ap and unmarked np to it
							if "subj" in mtext:
								trigger, triggertype = getsubjtrigger(moreprevious, root)
								return trigger, triggertype
							elif "iobj" in mtext:
								trigger, triggertype = getiobjtrigger(moreprevious, root)
								return trigger, triggertype
							elif "obj" in mtext:
								trigger, triggertype = getobjtrigger(moreprevious, root)
								return trigger, triggertype
						else:
							return "", ""
				else:
					return "", ""
			else:
				return "", ""
		else:
			return "", ""
	if len(parts) == 1:
		prep = parts[0]
	else:
		prep = " ".join(parts)
	# Getting the trigger
	current = parent
	while current.getprevious() is not None:
		current = current.getprevious()
		text = treeops.text(current)
		if "np-qual" in text or "timex" in text or "advp" in text or text in "np" or text in "nps" or text in "ap" or text in "aps":
			continue
		elif "np" in text:
			triggertype = "noun pp|" + prep
			trigger = treeops.gettriggernoun(current)
			break
		elif "vp" in text:
			if "vpp-comp" in text:
				triggertype = "passive pp|" + prep
				trigger = treeops.gettriggerverb(current)
				break
			elif "vpi" in text or "vps" in text or "vpg" in text:
				triggertype = "active pp|" + prep
				trigger = treeops.gettriggerverb(current)
				break
			else: # This verb might be the only one, maybe there's something else to check
				triggertype = "active pp|" + prep
				trigger = treeops.gettriggerverb(current)
				loopcurrent = current
				while loopcurrent.getprevious() is not None:
					loopcurrent = loopcurrent.getprevious()
					ltext = treeops.text(loopcurrent)
					if "advp" in ltext or "np-qual" in ltext or "timex" in ltext or ltext in "np" or ltext in "nps" or ltext in "ap" or ltext in "aps":
						continue
					elif "vpp-comp" in ltext:
						triggertype = "passive pp|" + prep
						trigger = treeops.gettriggerverb(loopcurrent)	
						break
					elif "vpi" in ltext or "vps" in ltext or "vpg" in ltext:
						triggertype = "active pp|" + prep
						trigger = treeops.gettriggerverb(loopcurrent)
						break
					elif "pp" in ltext:
						continue
					else:
						break #this verb is the only one we have.
					break
				break
		elif "pp" in text:
			continue
		else:
			break #nothing found here
	if not trigger: # Looking after the PP
		current = parent
		while current.getnext() is not None:
			current = current.getnext()
			text = treeops.text(current)
			if "np-qual" in text or "nps-qual" in text or "timex" in text or "advp" in text or text in "np" or text in "nps" or text in "ap" or text in "aps": #Change: advp and unmarked NPs added
				continue
			elif "np" in text:
				triggertype = "noun pp|" + prep
				trigger = treeops.gettriggernoun(current)
				break
			elif "vp" in text:
				if "vpp-comp" in text:
					triggertype = "passive pp|" + prep
					trigger = treeops.gettriggerverb(current)
					break
				elif "vpi" in text or "vps" in text or "vpg" in text:
					triggertype = "active pp|" + prep
					trigger = treeops.gettriggerverb(current)
					break
				else:
					triggertype = "active pp|" + prep
					trigger = treeops.gettriggerverb(current)
					loopcurrent = current
					while loopcurrent.getnext() is not None:
						loopcurrent = loopcurrent.getnext()
						ltext = treeops.text(loopcurrent)
						if "advp" in ltext or ltext in "np" or ltext in "nps" or ltext in "ap" or ltext in "aps" or "np-qual" in ltext or "timex" in ltext:
							continue
						elif "vpp-comp" in ltext:
							triggertype = "passive pp|" + prep
							trigger = treeops.gettriggerverb(loopcurrent)
							break
						elif "vpi" in ltext or "vps" in ltext or "vpg" in ltext:
							triggertype = "active pp|" + prep
							trigger = treeops.gettriggerverb(loopcurrent)
							break
						elif "pp" in ltext:
							continue
						else:
							break
					break
			elif "scp" in text:
				newnext = current.getnext()
				newtext = treeops.text(newnext)
				if "subj" in newtext:
					newnext = newnext.getnext()
					newtext = treeops.text(newnext)
				if "vp" in newtext:
					if "vpp-comp" in newtext:
						triggertype = "passive pp|" + prep
						trigger = treeops.gettriggerverb(current)
						break
					elif "vpi" in newtext or "vps" in newtext or "vpg" in newtext:
						triggertype = "active pp|" + prep
						trigger = treeops.gettriggerverb(current)
						break
					else:
						triggertype = "active pp|" + prep
						trigger = treeops.gettriggerverb(current)
						loopcurrent = current
						while loopcurrent.getnext() is not None:
							loopcurrent = loopcurrent.getnext()
							ltext = treeops.text(loopcurrent)
							if "advp" in ltext or ltext in "np" or ltext in "nps" or ltext in "ap" or ltext in "aps" or "np-qual" in ltext or "timex" in ltext:
								continue
							elif "vpp-comp" in ltext:
								triggertype = "passive pp|" + prep
								trigger = treeops.gettriggerverb(loopcurrent)
								break
							elif "vpi" in ltext or "vps" in ltext or "vpg" in ltext:
								triggertype = "active pp|" + prep
								trigger = treeops.gettriggerverb(loopcurrent)
								break
							elif "pp" in ltext:
								continue
							else:
								break
			elif "pp" in text:
				continue
			else:
				break
	if not trigger:
		return "", ""
	return trigger, triggertype
def gettimextrigger(node, root):
	trigger, triggertype = "", ""
	parent = treeops.getparentphrase(node, root)
	current = parent
	while current.getprevious() is not None:
		current = current.getprevious()
		text = treeops.text(current)
		if "np-qual" in text or "nps-qual" in text or "timex" in text or "advp" in text or text in "np" or text in "nps" or text in "ap" or text in "aps":
			continue
		elif "np" in text:
			triggertype = "noun timex|"
			trigger = treeops.gettriggernoun(current)
			break
		elif "vp" in text:
			if "vpp-comp" in text:
				triggertype = "passive timex|"
				trigger = treeops.gettriggerverb(current)
				break
			elif "vpi" in text or "vps" in text or "vpg" in text:
				triggertype = "active timex|"
				trigger = treeops.gettriggerverb(current)
				break
			else: # This verb might be the only one, maybe there's something else to check
				triggertype = "active timex|"
				trigger = treeops.gettriggerverb(current)
				loopcurrent = current
				while loopcurrent.getprevious() is not None:
					loopcurrent = loopcurrent.getprevious()
					ltext = treeops.text(loopcurrent)
					if "advp" in ltext or ltext in "np" or ltext in "nps" or ltext in "ap" or ltext in "aps" or "np-qual" in ltext  or "timex" in ltext:
						continue
					elif "vpp-comp" in ltext:
						triggertype = "passive timex|"
						trigger = treeops.gettriggerverb(loopcurrent)	
						break
					elif "vpi" in ltext or "vps" in ltext or "vpg" in ltext:
						triggertype = "active timex|"
						trigger = treeops.gettriggerverb(loopcurrent)
						break
					elif "pp" in ltext:
						continue
					else:
						break #this verb is the only one we have.
					break
				break
		elif "pp" in text:
			continue
		else:
			break #nothing found here
	if not trigger: # Looking after the PP
		current = parent
		while current.getnext() is not None:
			current = current.getnext()
			text = treeops.text(current)
			if "np-qual" in text or "nps-qual" in text or "timex" in text or "advp" in text or text in "np" or text in "nps" or text in "ap" or text in "aps":
				continue
			elif "np" in text:
				triggertype = "noun timex|"
				trigger = treeops.gettriggernoun(current)
				break
			elif "vp" in text:
				if "vpp-comp" in text:
					triggertype = "passive timex|"
					trigger = treeops.gettriggerverb(current)
					break
				elif "vpi" in text or "vps" in text or "vpg" in text:
					triggertype = "active timex|"
					trigger = treeops.gettriggerverb(current)
					break
				else:
					triggertype = "active timex|"
					trigger = treeops.gettriggerverb(current)
					loopcurrent = current
					while loopcurrent.getnext() is not None:
						loopcurrent = loopcurrent.getnext()
						ltext = treeops.text(loopcurrent)
						if "advp" in ltext or ltext in "np" or ltext in "nps" or ltext in "ap" or ltext in "aps" or "np-qual" in ltext or "timex" in ltext:
							continue
						elif "vpp-comp" in ltext:
							triggertype = "passive timex|"
							trigger = treeops.gettriggerverb(loopcurrent)
							break
						elif "vpi" in ltext or "vps" in ltext or "vpg" in ltext:
							triggertype = "active timex|"
							trigger = treeops.gettriggerverb(loopcurrent)
							break
						elif "pp" in ltext:
							continue
						else:
							break
					break
			elif "scp" in text:
				newnext = current.getnext()
				newtext = treeops.text(newnext)
				if "subj" in newtext:
					newnext = newnext.getnext()
					newtext = treeops.text(newnext)
				if "vp" in newtext:
					if "vpp-comp" in newtext:
						triggertype = "passive timex|"
						trigger = treeops.gettriggerverb(current)
						break
					elif "vpi" in newtext or "vps" in newtext or "vpg" in newtext:
						triggertype = "active timex|"
						trigger = treeops.gettriggerverb(current)
						break
					else:
						triggertype = "active timex|"
						trigger = treeops.gettriggerverb(current)
						loopcurrent = current
						while loopcurrent.getnext() is not None:
							loopcurrent = loopcurrent.getnext()
							ltext = treeops.text(loopcurrent)
							if "advp" in ltext or ltext in "np" or ltext in "nps" or ltext in "ap" or ltext in "aps" or "np-qual" in ltext or "timex" in ltext:
								continue
							elif "vpp-comp" in ltext:
								triggertype = "passive timex|"
								trigger = treeops.gettriggerverb(loopcurrent)
								break
							elif "vpi" in ltext or "vps" in ltext or "vpg" in ltext:
								triggertype = "active timex|"
								trigger = treeops.gettriggerverb(loopcurrent)
								break
							elif "pp" in ltext:
								continue
							else:
								break
			elif "pp" in text:
				continue
			else:
				break
	if not trigger:
		return "", ""
	return trigger, triggertype
def getyestertrigger(node, root):
	prep = "í"
	trigger, triggertype = "", ""
	parent = treeops.getparentphrase(node, root)
	current = parent
	while current.getprevious() is not None:
		current = current.getprevious()
		text = treeops.text(current)
		if "np-qual" in text or text in "np" or text in "nps" or text in "ap" or text in "aps" or "timex" in text:
			continue
		elif "np" in text:
			triggertype = "noun pp|" + prep
			trigger = treeops.gettriggernoun(current)
			break
		elif "vp" in text:
			if "vpp-comp" in text:
				triggertype = "passive pp|" + prep
				trigger = treeops.gettriggerverb(current)
				break
			elif "vpi" in text or "vps" in text or "vpg" in text:
				triggertype = "active pp|" + prep
				trigger = treeops.gettriggerverb(current)
				break
			else: # This verb might be the only one, maybe there's something else to check
				triggertype = "active pp|" + prep
				trigger = treeops.gettriggerverb(current)
				loopcurrent = current
				while loopcurrent.getprevious() is not None:
					loopcurrent = loopcurrent.getprevious()
					ltext = treeops.text(loopcurrent)
					if "advp" in ltext or ltext in "np" or ltext in "nps" or ltext in "ap" or ltext in "aps" or "np-qual" in ltext or "timex" in ltext:
						continue
					elif "vpp-comp" in ltext:
						triggertype = "passive pp|" + prep
						trigger = treeops.gettriggerverb(loopcurrent)	
						break
					elif "vpi" in ltext or "vps" in ltext or "vpg" in ltext:
						triggertype = "active pp|" + prep
						trigger = treeops.gettriggerverb(loopcurrent)
						break
					elif "pp" in ltext:
						continue
					else:
						break #this verb is the only one we have.
					break
				break
		elif "pp" in text:
			continue
		else:
			break #nothing found here
	if not trigger:
		current = parent
		while current.getnext() is not None:
			current = current.getnext()
			text = treeops.text(current)
			if "np-qual" in text or "timex" in text or text in "np" or text in "nps" or text in "ap" or text in "aps" or "np-timex" in text:
				continue
			elif "np" in text:
				triggertype = "noun pp|" + prep
				trigger = treeops.gettriggernoun(current)
				break
			elif "vp" in text:
				if "vpp-comp" in text:
					triggertype = "passive pp|" + prep
					trigger = treeops.gettriggerverb(current)
					break
				elif "vpi" in text or "vps" in text or "vpg" in text:
					triggertype = "active pp|" + prep
					trigger = treeops.gettriggerverb(current)
					break
				else:
					triggertype = "active pp|" + prep
					trigger = treeops.gettriggerverb(current)
					loopcurrent = current
					while loopcurrent.getnext() is not None:
						loopcurrent = loopcurrent.getnext()
						ltext = treeops.text(loopcurrent)
						if "advp" in ltext or ltext in "np" or ltext in "nps" or ltext in "ap" or ltext in "aps" or "np-qual" in ltext or "timex" in ltext:
							continue
						elif "vpp-comp" in ltext:
							triggertype = "passive pp|" + prep
							trigger = treeops.gettriggerverb(loopcurrent)
							break
						elif "vpi" in ltext or "vps" in ltext or "vpg" in ltext:
							triggertype = "active pp|" + prep
							trigger = treeops.gettriggerverb(loopcurrent)
							break
						elif "pp" in ltext:
							continue
						else:
							break
					break
			elif "pp" in text:
				continue
			else:
				break
	if not trigger:
		return "", ""
	return trigger, triggertype
if __name__ == "__main__":
	print "to test, implement this"
