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
##[ Description ]## Controls the general aspects of the engine

import os
from datetime import datetime
import questylib.various as various
from questylib.statusprinter import StatusPrinter

class SignalDict(dict):
    def add(self, signal, *func_and_args):
        try:
            self.__getitem__(signal).append(func_and_args)
        except Exception:
            self.__setitem__(signal, [func_and_args])

    def remove(self, signal, func):
        d = self.__getitem__(signal)
        for x in d:
            if x[0] == func:
                d.remove(x)
                break

    def run(self, *signal_and_args):
        signal = signal_and_args[0]
        args = signal_and_args[1:]
        try:
            for func in self.__getitem__(signal):
                targs = list(args)
                targs.extend(func[1:])
                func[0](*targs)
        except Exception:
            pass


class System:
    def __init__(self, etc, error=None):
        self.etc = etc
        if error is None:
            self.error = various.usable_error
        else:
            self.error = error
        self.signalactions = SignalDict()
        self.gameactions = SignalDict()

        self.status = StatusPrinter('SYSTEM', self.etc, 'white', 'red')

        self.debugargs = self.etc.debugarguments
        if self.etc.debug is not None:
            action = self.signalactions.add
            exec(self.etc.debug)

        self.emit_signal('aftersysteminit', self)

    def emit_signal(self, *signal_and_args):
            self.signalactions.run(*signal_and_args)

    def emit_event(self, *event_and_type):
        self.gameactions.run(*event_and_type)

    def start(self):
        self.emit_signal('beforesystemstart', self)
        self.status('Starting system...')
        fgame = __import__(self.etc.game + '.game', globals(), locals(),
                           ['Game'], -1)
        os.chdir(os.path.dirname(fgame.__file__))
        self.game = fgame.Game(self)
        self.status('Name of game is: %s' % self.game.name)
        self.emit_signal('aftersystemstart', self)
        self.status('Starting game...')
        self.game.start()
        self.status('Running game...')
        self.game.run()

    def end(self):
        self.emit_signal('beforesystemend', self)
        self.status('Stopping system...')
        self.status('Stopping game...')
        self.game.end()
        self.emit_signal('aftersystemend', self)
