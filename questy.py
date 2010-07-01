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
try:
    from setproctitle import setproctitle
except ImportError:
    setproctitle = lambda x: None
from questylib.system import System
import questylib.various as various

class NewOptionParser(OptionParser):
    def error(self, msg, cont=True):
        various.error(msg, cont, self.prog + ': error')

parser = NewOptionParser(
    prog='questy',
    usage='Usage: %prog [OPTION]... GAME',
    description='Runs a Questy game',
    version='''\
Questy 0.1
Copyright (C) 2010  Niels Serup
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.\
''',
    epilog='This is merely an interpreter. It is not an actual game -- it\'s a game engine.')

parser.add_option('-f', '--fullscreen', dest='fullscreen',
                  action='store_true', default=False,
                  help='play in fullscreen mode (windowed mode is default')
parser.add_option('-z', '--zoom', dest='zoom', type='float', default=1,
                  help='scale game window (not applicable in fullscreen mode)',
                  metavar='NUMBER')
parser.add_option('-F', '--fakefullscreen', dest='fakefullscreen',
                  action='store_true', default=False,
                  help='play in a "fake" fullscreen mode using the zooming feature (substantially slower than "true" fullscreen mode)')
parser.add_option('-s', '--size', dest='size', metavar='[WIDTH]x[HEIGHT]',
                  default=None,
                  help='scale the game window using the zooming feature and change the canvas size if needed (a manual version of --fakefullscreen)')
parser.add_option('-b', '--noborder', dest='border',
                  action='store_false', default=True,
                  help='do not show a border on the game window')
parser.add_option('-H', '--nohwaccel', dest='hwaccel',
                  action='store_false', default=True,
                  help='do not attempt to use hardware acceleration (hardware acceleration is only attempted in fullscreen mode)')
parser.add_option('-B', '--nodoublebuf', dest='doublebuf',
                  action='store_false', default=True,
                  help='do not attempt to use double buffering (faster but perhaps uglier)')
parser.add_option('-w', '--wait-for-complete-loading', dest='loadwait',
                  action='store_true', default=False,
                  help='do not autoload data as needed -- load it all at startup instead')
parser.add_option('-q', '--quiet', dest='verbose',
                  action='store_false', default=True,
                  help='don\'t print status messages')
parser.add_option('-C', '--nocolorprint', dest='colorprint',
                  action='store_false', default=True,
                  help='don\'t attempt to color status messages in the terminal')
parser.add_option('-S', '--simpleprint', dest='simpleprint',
                  action='store_true', default=False,
                  help='simplify the design of status messages in the terminal')
parser.add_option('-E', '--nocolorerrors', dest='colorerrors',
                  action='store_false', default=True,
                  help='do not attempt to print error messages in the terminal in a red color')
parser.add_option('-d', '--debug-with-file', dest='debugfile',
                  metavar='FILE', help='debug Questy using a Python file')
parser.add_option('-D', '--debug-with-string', dest='debugstring',
                  metavar='CODE',
                  help='debug Questy using a string of Python code')
parser.add_option('-a', '--add-debug-argument', dest='debugarguments',
                  default=[], action='append', metavar='STRING',
                  help='add an argument to interact with your debug code')

(options, args) = parser.parse_args()

if options.colorerrors:
    try:
        from termcolor import colored
    except ImportError:
        colored = lambda x: x
    class ColoredErrors:
        def write(self, msg):
            sys.__stderr__.write(colored(msg, 'red'))
    sys.stderr = ColoredErrors()

try:
    options.game = args[0]
except IndexError:
    parser.error('no GAME has been specified, quitting.', False)

if options.size is not None:
    try:
        spl = options.size.split('x')
        options.size = []
        for i in range(2):
            if spl[i] == '':
                options.size.append(None)
            else:
                options.size.append(int(spl[i]))
        if len(options.size) < 2:
            raise Exception()
    except Exception:
        parser.error('size syntax is wrong, use [WIDTH]x[HEIGHT], quitting', False)

# Debug options
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
        parser.error(str(e), False)
    del debugtext
else:
    options.debug = None

del options.debugfile
del options.debugstring

setproctitle(parser.prog)

qs = System(options, parser.error)
qs.start()
qs.end()

# try:
#     qs.start()
# except (KeyboardInterrupt, EOFError):
#     print
# except Exception, error:
#     parser.error(str(error))
# finally:
#     qs.end()
