#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Questy: a quest system for simple RPGs
# Copyright (C) 2010  Niels Serup

# This file is part of Questy.
#
# Questy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Questy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Questy.  If not, see <http://www.gnu.org/licenses/>.

##[ Name        ]## questy
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Starts the Questy system


import sys
from optparse import OptionParser
from questylib.system import System
import questylib.various as various

class NewOptionParser(OptionParser):
    def error(self, msg, cont=True):
        various.error(msg, cont, self.prog + ': error')

parser = NewOptionParser(
    prog='questy',
    usage='Usage: %prog [OPTION]... GAME',
    description='Runs the Questy game found in the specified directory',
    version='''\
Questy 0.1
Copyright (C) 2010  Niels Serup
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.\
''',
    epilog='''\
This is merely an interpreter. It is not an actual game -- it\'s a
game engine.

About debugging:
  Questy is a program never intended to be finished. Its built-in
  debugging features aid in the opposite.
  When debugging, you can add arguments from the command line. This is
  particularly useful when using a debug file. If both a debug file
  and a debug string is present, the string is prepended to the file
  contents.
  Debug code can be executed at different times using different
  signals that the Questy system emits.

  Examples:\
    Debug a game with a-debug-file.py
      $ questy -d a-debug-file.py A_GAME
    Do the same, but this time send 3 arguments to a-debug-file.py
      $ questy -d a-debug-file.py -a arg1 -a arg2 -a arg3 A_GAME
''')

parser.add_option('-f', '--fullscreen', dest='fullscreen',
                  action='store_true', help='play in fullscreen mode')
parser.add_option('-w', '--windowed', dest='fullscreen',
                  action='store_false', help='play in windowed mode (default)')
parser.add_option('-d', '--debug-with-file', dest='debugfile',
                  metavar='FILE', help='debug Questy using a Python file')
parser.add_option('-D', '--debug-with-string', dest='debugstring',
                  metavar='CODE',
                  help='debug Questy using a string of Python code')
parser.add_option('-a', '--add-debug-argument', dest='debugarguments',
                  default=[], action='append', metavar='STRING',
                  help='add an argument to interact with your debug code')

(options, args) = parser.parse_args()

try:
    options.game = args[0]
except Exception:
    parser.error('no GAME has been specified, quitting.', False)

d_a = options.debugstring is not None
d_b = options.debugfile is not None
if d_a or d_b:
    debugtext = ''
if d_a:
    debugtext += options.debugstring + '\n'
if d_b:
    debugtext += various.read_file(options.debugfile) + '\n'
if d_a or d_b:
    try:
        options.debug = compile(debugtext, '<debugcode>', 'exec')
    except Exception, e:
        parser.error(e, False)
    del debugtext
else:
    options.debug = None

del options.debugfile
del options.debugstring

qs = System(options, parser.error)
try:
    qs.start()
except (KeyboardInterrupt, EOFError):
    print # A newline
finally:
    qs.end()
