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

##[ Name        ]## game
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Contains the generic form of the Game class

from datetime import datetime
import os
from questylib.statusprinter import StatusPrinter

class GenericGame:
    name = 'A game'
    shortname = 'game'
    size = (640, 480)
    datadir = 'data/'

    def __init__(self, stm):
        self.sys = stm
        self.status = StatusPrinter(self.shortname.upper(),
                                    self.sys.etc, 'green', 'grey')
        self.sys.emit_signal('aftergameinit', self)

    def get_data(self, directory):
        path = os.path.join(self.datadir, directory)
        paths = {}
        for root, dirs, files in os.walk(path):
            name = root[len(path)+1:]
            if name == '':
                name = '.'
            paths[name] = dirs, sorted(files)
        return path, paths

    def start(self):
        self.sys.emit_signal('beforegamestart', self)
        self.start_game()
        self.sys.emit_signal('aftergamestart', self)

    def start_game(self):
        pass

    def run(self):
        self.sys.emit_signal('beforegamerun', self)
        self.run_game()
        self.sys.emit_signal('aftergamerun', self)

    def run_game(self):
        pass

    def end(self):
        self.sys.emit_signal('beforegameend', self)
        try: self.world.end()
        except Exception: pass
        self.sys.emit_signal('aftergameend', self)

