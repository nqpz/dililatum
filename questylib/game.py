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
from questylib.world import World
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

    def create_world(self):
        self.world = World(self.sys, self.size)

    def get_path_data(self, path):
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

    def load_places(self, imgpath, posokpath, objspath, num=None):
        if num is None:
            num = min(
                len(self.get_path_data(imgpath)[1]['.'][1]),
                len(self.get_path_data(posokpath)[1]['.'][1]),
            )
        numm = num - 1
        pref = '%0' + str(len(str(numm))) + 'd'

        self.sys.emit_signal('beforeplacesload', self, numm, pref % numm)
 
        overlays = {}
        for x in self.get_path_data(objspath)[1]['.'][1]:
            i = x.split('-')
            inum = i[0]
            pos = [int(y) for y in i[1].split(',')]
            rel = int(i[2])
            spl = i[3].split(',')
            for y in range(2):
                try:
                    spl[y] = int(spl[y])
                except Exception:
                    spl[y] = None
            end_or_start = spl
            if len(i) < 6:
                start = [None, 0]
                end = end_or_start
                name = i[4].split('.')[0]
            else:
                start = end_or_start
                end = [int(y) for y in i[3].split(',')]
                name = i[5].split('.')[0]
            inf = (x, pos, rel, start, end, name)
            try:
                overlays[inum].append(inf)
            except Exception:
                overlays[inum] = [inf]

        for i in range(num):
            prefi = pref % i
            self.sys.emit_signal('beforeplaceload', self, i, prefi)
            okbg = False
            suffs = ['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG', \
                'gif', 'GIF', 'tga', 'TGA']
            while not okbg:
                suff = suffs[0]
                del suffs[0]
                backgroundpath = os.path.join(imgpath, prefi + '.' + suff)
                okbg = os.path.isfile(backgroundpath)
                if not okbg and len(suffs) == 0:
                    break
            if not okbg:
                self.sys.error('cannot find image for place ' + prefi)
                continue

            okpospath = os.path.join(posokpath, prefi + '.questypos')
            place = self.world.create_place(
                backgroundpath,
                okpospath
            )
            try:
                ovobjs = overlays[prefi]
            except KeyError:
                ovobjs = []
            for i in range(len(ovobjs)):
                c = ovobjs[i]
                ovobjs[i] = self.world.create_object(
                    rel=c[2], pos=c[1], area=(c[3], c[4]),
                    imgfile=os.path.join(objspath, c[0]),
                    visible=False)
                ovobjs[i].action = [ovobjs[i].show]
                ovobjs[i].unaction = [ovobjs[i].hide]
                place.add_object(ovobjs[i])
                place.obj_names[c[5]] = ovobjs[i]
            self.world.add_place(place)
            self.sys.emit_signal('afterplaceload', self, i, prefi)
        self.sys.emit_signal('afterplacesload', self)

    def use_data_from_map(self, path):
        plcmap = self.load_map_data(path)
        self.use_map_data(plcmap)

    def load_map_data(self, detailsfile):
        self.sys.emit_signal('beforemapload', self)
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
                tdet = y.split('|')
                try:
                    direction = dirs[tdet[0]]
                except KeyError:
                    direction = tdet[0]

                try:
                    target = int(tdet[1])
                except Exception:
                    target = None
                tdett = tdet[3].split(' ')
                objpos = eval('[' + tdett[0] + ']')
                objsize = eval('[' + tdett[1] + ']')
                try:
                    targetpos = eval('[' + tdet[2] + ']')
                except Exception:
                    targetpos = None
                targetdir = tdet[4]
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
            if x is None: continue
            for key, vals in x.items():
                if vals[0] is None or vals[3] is None or vals[4] == '':
                    actwhat = None
                else:
                    actwhat = [self.world.set_place, places[vals[0]], vals[3], vals[4]]
                obj = self.world.create_object(
                    pos=vals[1], size=vals[2], area=vals[1:3],
                    action=actwhat, walkonact=False)
                obj.isdirobj = True
                places[i].add_object(obj)
                if key:
                    places[i].set_direction_object(key, obj)
            i += 1

        if fix_poss:
            self.fix_places_with_minus_x_positions()
        self.sys.emit_signal('aftermapload', self)

    def fix_places_with_minus_x_positions(self):
        places = self.world.places
        for p in places:
            for o in p.objects:
                if not 'isdirobj' in dir(o) or o.action is None:
                    continue
                targetpos = o.action[2]
                targetdir = o.action[3]
                if targetpos[0] < 0:
                    targetpos[0] = int(
                        self.size[0] + targetpos[0] -
                        o.action[1].char_size(targetpos) *
                        self.world.leading_character.get_frame().width
                    )
                elif targetdir[0] == 'l':
                    targetpos[0] = int(
                        targetpos[0] -
                        o.action[1].char_size(targetpos) *
                        self.world.leading_character.get_frame().width
                    )
                elif targetdir in ('ct', 'cb', 'lt', 'lb', 'rt', 'rb'):
                    targetpos[0] = int(
                        targetpos[0] -
                        o.action[1].char_size(targetpos) / 2 *
                        self.world.leading_character.get_frame().width
                    )

    def load(self):
        pass

    def save(self):
        pass

    def end(self):
        self.sys.emit_signal('beforegameend', self)
        self.world.end()
        self.sys.emit_signal('aftergameend', self)

