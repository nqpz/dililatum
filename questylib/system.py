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

##[ Name        ]## system
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Controls all major aspects of the engine

import os
from datetime import datetime
import questylib.various as various

class SignalDict(dict):
    def add(self, signal, func):
        try:
            self.__getitem__(signal).append(func)
        except Exception:
            self.__setitem__(signal, [func])

class System:
    def __init__(self, etc, error=None):
        self.etc = etc
        if error is None:
            self.error = various.usable_error
        else:
            self.error = error
        self.signalactions = SignalDict()

        self.debugargs = self.etc.debugarguments
        if self.etc.debug is not None:
            exec(self.etc.debug)

        self.emit_signal('systeminit')

    def emit_signal(self, signalname):
        if signalname in self.signalactions:
            for func in self.signalactions[signalname]:
                try:
                    func(self)
                except Exception:
                    func()

    def status(self, msg):
        print '### ' + str(datetime.now()) + ' ###\n' + msg

    def start(self):
        self.status('Starting system...')
        self.emit_signal('systemstart')
        fgame = __import__(self.etc.game + '.game', globals(), locals(),
                           ['Game'], -1)
        os.chdir(os.path.dirname(fgame.__file__))
        self.game = fgame.Game(self)
        self.status('Name of game is: %s' % self.game.name)
        self.status('Starting game...')
        self.emit_signal('gamestart')
        self.game.start()
        self.status('Running game...')
        self.emit_signal('gamerun')
        self.game.run()

    def end(self):
        self.game.end()
