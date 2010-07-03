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

##[ Name        ]## place
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Contains the generic form of the Place class

import pygame
from pygame.locals import *
from questylib.bitmap import BitMap

class Place:
    def __init__(self, world, imgfile=None, posfile=None, **oargs):
        def get(key, default):
            try: return oargs[key]
            except KeyError: return default
        self.world = world
        self.imgfile = imgfile
        self.posfile = posfile
        self.power = get('power', None)
        self.name = None
        self.objects = []
        self.objects = get('objs', [])
        self.obj_names = {}
        self.dir_objects = {}

        if self.world.sys.etc.loadwait:
            self.load_imgfile()
            self.load_overlays()
            self.load_posfile()
        else:
            self.surf = None
            self.posoks = None

    def load_imgfile(self):
        if self.imgfile is not None:
            try:
                self.surf = pygame.image.load(self.imgfile).convert()
            except Exception:
                pass

    def load_posfile(self):
        if self.posfile is not None:
            try:
                bm = BitMap(*self.world.size)
                bm.load(self.posfile)
                self.posoks = bm
            except Exception:
                pass

    def add_object(self, obj):
        self.objects.append(obj)

    def set_direction_object(self, direction, obj):
        self.dir_objects[direction] = obj

    def remove_object(self, obj):
        self.objects.remove(obj)

    def char_size(self, pos):
        if self.power is None:
            return 1.0
        else:
            return (float(pos[1]) / self.world.size[1]) ** self.power

    def char_pos(self, pos):
        return pos

    def set_char_size(self, inst):
        self.char_size = inst

    def set_char_pos(self, inst):
        self.char_pos = inst

    def pos_ok(self, pos, size, screen_limits=True):
        if screen_limits and \
                pos[0] < 0 or pos[0] + size[0] > self.world.size[0] \
                or pos[1] - size[1] / 20 < 0 or pos[1] > self.world.size[1]:
            return False

        if self.posoks is None:
            self.load_posfile()

        if self.posoks is None: # Still..
            return True
        else:
            height = self.char_size(pos) * \
                self.world.leading_character.get_frame().height / 20
            pos2 = pos[0] + size[0]
            posmh = pos[1] - height
            a2 = (pos[1] + posmh) / 2
            return self.posoks.get(*pos) and \
                self.posoks.get(pos2, pos[1]) and \
                self.posoks.get(pos[0], posmh) and \
                self.posoks.get(pos2, posmh) and \
                self.posoks.get(pos[0] + size[0] / 2, a2) and \
                self.posoks.get(pos[0] + size[0] / 4, a2) and \
                self.posoks.get(pos[0] + size[0] - size[0] / 4, a2)

    def draw(self, surf=None):
        if surf is None:
            surf = self.world
        if self.surf is None:
            self.load_imgfile()
        surf.blit(self.surf, (0, 0))

