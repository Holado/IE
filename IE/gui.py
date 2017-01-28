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

class GUI():
	def __init__(self):
		pass
   	def startGUI(self):
		pass
	def gettext(self):
		#Later, this will respond with the real GUI.
		# Will return text to translate, what language to use.
		secondresponse = raw_input("***What do you want to translate?***\n")
		language = raw_input("***What language? Polish, English or Icelandic?***\n")
		language = language.strip().lower()
		return secondresponse, language

if __name__ == "__main__":
	# Skrifaðu hér.
	print "Implement if needed"
