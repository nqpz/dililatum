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

##[ Name        ]## convertlinkedplacestootherinternalformat
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Converts files created with link-places to the
                  # simpler internal format used by Questy

import sys
try:
    import cPickle as pickle
except ImportError:
    import pickle

def convert_from_internal_to_other_internal(path):
    f = open(path, 'rb')
    data = pickle.load(f)
    f.close()
    out = ''

    return out

###################
args = sys.argv[1:]
if len(args) == 1:
    if args[0] == '-H' or args[0] == '--help':
        print """\
Usage: convertlinkedplacestootherinternalformat FILE
Converts any linkplaces file to the internal format used by Questy

Options:
  -H, --help        show this help and exit
  -V, --version     show version information and exit

Converted content is written to standard out.\
"""
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
        path = args[0]
else:
    path = args[1]

print convert_from_internal_to_other_internal(path)
