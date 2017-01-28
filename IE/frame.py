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

class Frame(object):
	def __init__(self, trigger, triggertype):
		self.trigger = trigger
		self.triggertype = triggertype
		self.patterns = {} #Pattern is key, value is ["sempref*role"]
		self.extracts = {} #Pattern is key, value is [extract head*extract whole*tag]
	def addpattern(self, pattern, semprefs):
		self.patterns[pattern] = semprefs
		self.extracts[pattern] = []
	def addextract(self, pattern, extract):
		self.extracts[pattern].append(extract)
	def getpatterns(self):
		return self.patterns
	def getextracts(self, pattern):
		return self.extracts[pattern]
	def isnotempty(self):
		if self.patterns:
			return True
		else:
			return False
	def hasextracts(self):
		for pattern in self.patterns:
			if self.patternhasextracts(pattern):
				return True
			else:
				continue
		return False
	def patternhasextracts(self, pattern):
		if self.extracts[pattern]:
			return True
		else:
			return False
	def gettrigger(self):
		return self.trigger
	def gettriggertype(self):
		return self.triggertype
	def printframe(self):
		print "Trigger: {}, {}".format(self.trigger, self.triggertype)
		for pattern in self.patterns.keys():
			print "\t{}".format(pattern)
			for item in self.patterns[pattern]:
				print "\t\t{}".format(item)
			for extract in self.extracts[pattern]:
				print "\t\tEXTRACT: {}".format(extract)	
		return
if __name__ == "__main__":
	print "to be implemented"
