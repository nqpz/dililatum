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
from questylib.various import *

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

    def load_places(self, imgpath, posokpath, num=None):
        if num is None:
            num = min(
                len(self.get_data(imgpath)[1]['.'][1]),
                len(self.get_data(posokpath)[1]['.'][1]),
            )
        for i in range(num):
            place = self.world.create_place(
                os.path.join(self.datadir, imgpath, '%03d.jpg' % i),
                os.path.join(self.datadir, posokpath, '%03d.questypos' % i)
            )
            self.world.add_place(place)

    def use_data_from_map(self, path):
        plcmap = self.load_map_data(os.path.join(self.datadir, path))
        self.use_map_data(plcmap)

    def load_map_data(self, detailsfile):
        det = read_file(detailsfile)
        dirs = {
            '^': 'up',
            '>': 'right',
            'v': 'down',
            '<': 'left'
        }
        spl = det.split('\n\n')
        info = []
        for i in range(len(spl)):
            info.append(None)
        for x in spl:
            t = x.split('\n')
            num = int(t[0])
            sinfo = {}
            for y in t[1:]:
                if y == '': continue
                direction = dirs[y[0]]
                tdet = y[1:].split('|')
                target = int(tdet[0])
                tdett = tdet[1].split(' ')
                objpos = eval('[' + tdett[0] + ']')
                objsize = eval('[' + tdett[1] + ']')
                targetpos = eval('[' + tdet[2] + ']')
                targetdir = tdet[3]
                sinfo[direction] = (target, objpos, objsize,
                                    targetpos, targetdir)
            try:
                info[num] = sinfo
            except IndexError:
                pass

        return info

    def use_map_data(self, data, fix_poss=True):
        places = self.world.places
        i = 0
        for x in data:
            for key, vals in x.items():
                obj = self.world.create_object(
                    pos=vals[1], size=vals[2],
                    action=[self.world.set_place, vals[0], vals[3], vals[4]])
                places[i].add_object(obj)
                places[i].set_direction_object(key, obj)
            i += 1

        if fix_poss:
            self.fix_places_with_minus_x_positions()

    def fix_places_with_minus_x_positions(self):
        places = self.world.places
        for p in places:
            for o in p.objects:
                targetpos = o.action[2]
                if targetpos[0] < 0:
                    targetpos[0] = int(
                        self.size[0] + targetpos[0] -
                        places[o.action[1]].char_size(targetpos)
                        * self.world.leading_character.get_frame().width)

    def end(self):
        self.sys.emit_signal('beforegameend', self)
        try: self.world.end()
        except Exception: pass
        self.sys.emit_signal('aftergameend', self)

