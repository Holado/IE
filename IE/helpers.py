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
import re

def clean(s):
    # Returns string without caps
	s = s.strip().lower()
	if isinstance(s, unicode):
		s = s.encode('utf-8')
	myre = {"Á":"á", "É":"é", "Í":"í", "Ó":"ó", "Ú":"ú", "Ý":"ý", "Æ":"æ", "Ö":"ö", "Þ":"þ", "Ð":"ð"}
	myre = dict((re.escape(k), v) for k, v in myre.iteritems())
	mypatt = re.compile("|".join(myre.keys()))
	mytext = mypatt.sub(lambda m: myre[re.escape(m.group())], s)
	return mytext

def cleantag(s):
	s = s.strip().lower()
	if isinstance(s, unicode):
		s = s.encode('utf-8')
	return s

def cleanfunction(s):
	#Cleans function labels such as "[np-subj<", returns "subj"
	s = s.strip()
	s = s.replace("nps-", "")	
	s = s.replace("np-", "")
	s = s.replace("aps-", "")	
	s = s.replace("ap-", "")		
	s = s.replace("[", "")	
	s = s.replace("<", "")	
	s = s.replace(">", "")	
	return s

def period(s):
	s = s.replace(".", "")	
	return s

def getextracttype(pattern):
	mytype = pattern.split('|')[0]
	return mytype

def gettriggertype(pattern):
	mytype = pattern.split('|')[3]
	if "active" in mytype:
		return "active"
	elif "passive" in mytype:
		return "passive"
	elif "noun" in mytype:
		return "noun"
	else:
		print "Can't find trigger for {}".format(pattern)
	return mytype

def getpatterncase(pattern):
	mycase = pattern.split('|')[1]
	return mycase

def getpatternprep(pattern):
	if len(pattern.split('|')) < 5:
		return ""
	myprep = pattern.split('|')[4]
	return myprep

def getpatterntrigger(pattern):
	mytype = pattern.split('|')[2]
	return mytype

if __name__ == "__main__":
	print "to be implemented"
