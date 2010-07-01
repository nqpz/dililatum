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

##[ Name        ]## walk-test-advanced
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Shows an animated walk sequence in several
                  # directions, forcing the user to use the arrow
                  # keys to control the character.


from optparse import OptionParser
from questylib.tools.walktest import WalkTestAdvanced

parser = OptionParser(prog='walk-test-advanced',
                      usage='Usage: %prog [OPTION]... [DIRECTORY]',
                      description='\
Shows an animated walk sequence in several directions, \
forcing the user to use the arrow keys to control the character.',
                      version='''\
Questy 0.1
Copyright (C) 2010  Niels Serup
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.''', epilog='\
Navigate the character using the keypad keys or the number keys.')
parser.add_option('-t', '--time', dest='time', type='int',
                  metavar='MILLISECONDS', default=250,
                  help='amount of time allocated to show a frame')
parser.add_option('-r', '--rate', dest='rate', type='int',
                  metavar='NUMBER',
                  help='frame rate of animation, overrides \
--time if set')
parser.add_option('-x', '--width', dest='width', type='int',
                  metavar='NUMBER', default=300,
                  help='set width')
parser.add_option('-y', '--height', dest='height', type='int',
                  metavar='NUMBER', default=600,
                  help='set height')
parser.add_option('-d', '--direction', dest='direction',
                  metavar='lt|ct|rt|lm|rm|lb|cb|rb', default='cb',
                  help='set walking direction')
parser.add_option('-S', '--noshadow', dest='shadow',
                  action='store_false', default=True,
                  help='do not show a shadow underneath the character')
parser.add_option('-b', '--background', dest='background',
                  metavar='R,G,B|SPECIAL', default='colorflow',
                  help='set background color using RGB triplets \
or one of the predefined special values: black (0,0,0), white \
(255,255,255) and colorflow (changing between all colors with \
saturation and lightness set to default values)')
(options, args) = parser.parse_args()

try:
    options.directory = args[0]
except Exception:
    options.directory = '.'

if options.rate is not None:
    options.time = 1000000 / options.rate
else:
    options.time *= 1000
del options.rate

if options.background.find(',') != -1:
    options.background = tuple([int(x) for x in options.background.split(',')])
elif options.background == 'black':
    options.background = (0,0,0)
elif options.background == 'white':
    options.background = (255,255,255)

options.size = (options.width, options.height)

wt = WalkTestAdvanced(options)
try:
    wt.start()
except (KeyboardInterrupt, EOFError):
    print # A newline
