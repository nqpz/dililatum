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

##[ Name        ]## posmarker
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Shows a background for marking where characters
                  # can safely walk

from questylib.tools.posmarker import *

args = sys.argv[1:]
if len(args) == 1:
    if args[0] == '-H' or args[0] == '--help':
        print """\
Usage: mark-where-pos-ok [OPTION] IMGFILE POSFILE
Shows a background for marking where characters can safely walk

Options:
  -H, --help        show this help and exit
  -V, --version     show version information and exit

Use the left mouse button to mark, PageUp and PageDown to adjust the
"brush" size and the right mouse button to unmark."""
        sys.exit()
    elif args[0] == '-V' or args[0] == '--version':
        print """\
Questy 0.1
Copyright (C) 2010  Niels Serup
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.\
"""
        sys.exit()
    else:
        sys.stderr.write('mark-where-pos-ok: error: you didn\'t specify a POSFILE\n')
        sys.exit(1)
elif len(args) == 0:
    sys.stderr.write('mark-where-pos-ok: error: you didn\'t specify any files!\n')
    sys.exit(1)
else:
    imgfile = args[0]
    posfile = args[1]

pm = OKPositionsMarker(imgfile, posfile)
try:
    pm.start()
except (KeyboardInterrupt, EOFError):
    print # A newline
finally:
    pm.end()
