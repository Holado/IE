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

******************************************************************

Attn.: IceNLP  needs to be installed so the folder IceNLPCore is inside the folder IE.


*** To get information frames and semantic lexicon for a new corpus ***
File "semlex_seed.in" needs to be in the same folder as the new corpus. It should contain definitions of each semantic category and seed words on the form "category|role\tWord1|Word2|..."

Folder with corpus need to be inside the folder IE
Start program with "python mainprogram.py"
Select "data"
Select folder
After getting the results in file patternsandsemlex.out, they should be reviewed and sorted into files semlex_X.out, where X represents the name of each semantic category, and bestpatterns.out, containing the best patterns. 
Frames can then be found in myframes.out.
*** To translate ***
To use a new corpus for translating, the following files need to be created for each language:
	X_semlex.out: Contains the entire semantic lexicon. One translation per line, "WORD\tTRANSLATION"
	X_prep.out: All prepositions in patterns. One translation per line, "WORD\tTRANSLATION"
	X_patterns.out: All triggers from patterns. One translation per line, "WORD\tTRANSLATION"

Start program with "python mainprogram.py"
Select "translate"
Select your folder - "translate" is the default one
Select a language - "Icelandic", "Polish", and "English" are available for the \corpus folder.
Write text to be translated.
