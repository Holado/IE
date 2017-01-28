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
import os.path
from data import Data
from shell import Shell
from pw import FrameMaker
from gui import GUI
from translate import Translator

class Center:
	def __init__(self):
		self.starting = "*****Starting program*****\nThis file is part of IE.\nIE is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nIE is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with IE.  If not, see <http://www.gnu.org/licenses/>.\n"
	def start(self):
		print self.starting
		data = Data()
		devdir = "corpus/"
		transdir = "translate/"
		dataread = False
		while True:
			response = raw_input("***What do you want to do?***\n")
			response = response.strip().lower()
			if response == "data": # Make frames and other data files for new texts
				while True:
					newresponse = raw_input("Which corpus folder do you want to work with?\n")
					possdir = newresponse+"/"
					if os.path.exists(possdir):
						devdir = possdir
						print "new devdir is {}".format(possdir)
						break
					print "Directory does not exist. Try again."
					continue
				startsemlex, catroles = data.getstartsemlex(devdir)
				starter = FrameMaker(devdir, startsemlex, catroles)
				starter.generateframes()
				print "Frames have been generated.\n"
				continue
			elif response == "translate":
				while True:
					newresponse = raw_input("Which corpus folder do you want to work with?\n")
					possdir = newresponse+"/"
					if os.path.exists(possdir):
						transdir = possdir
						break
					print "Directory does not exist. Try again."
					continue
				#Start GUI, get info from and to it.
				while True:
					if dataread:
						pass
					else:
						frames, triggerdict = data.readframesfromfile(transdir)
						semlex_collection = data.readsemlextranslationsfromfile(transdir)
						pattern_collection = data.readpatterntranslationsfromfile(transdir)
						prep_collection = data.readpreptranslationsfromfile(transdir)
						dataread = True
					gui = GUI()
					totranslate, language = gui.gettext()
					if totranslate == "exit":
						"Exiting translating part\n"
						break
					translator = Translator(frames, semlex_collection, pattern_collection, prep_collection, language)	
					translator.translate(totranslate, language, triggerdict)
					continue
			elif response == "help":
				print "\"data\" makes frames.\n\"translate\" opens the translation window.\n\"help\" shows the help information.\n\"\exit\" exits the program."
				continue
			elif response == "exit":
				print "Exiting program. Good bye.\n"
				break
			else:
				print "Invalid response. Try again.\n"
				continue
if __name__ == "__main__":
	program = Center()
	program.start()
