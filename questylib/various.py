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

##[ Name        ]## various
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Various minor parts


import sys

def read_file(filename, throw_exceptions=False):
    if not throw_exceptions:
        try:
            f = open(filename, 'U')
            return f.read()
        except Exception:
            return ''
    else:
        f = open(filename)
        return f.read()

def error(msg, cont=True, pre=None):
    errstr = msg + '\n'
    if pre is not None:
        errstr = pre + ': ' + errstr
    sys.stderr.write(errstr)
    if cont is not True:
        try:
            sys.exit(cont)
        except Exception:
            sys.exit(1)

def usable_error(msg, cont=True):
    error(msg, cont, 'questy: ')
