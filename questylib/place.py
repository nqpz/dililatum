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
    def __init__(self, world, imgfile=None, posfile=None, power=None):
        self.world = world
        self.name = None
        self.objects = []
        self.dir_objects = {}
        if imgfile is not None:
            self.surf = self.load_imgfile(imgfile)
        else:
            self.surf = None
        self.power = power

        if posfile is not None:
            self.posoks = self.load_posfile(posfile)
        else:
            self.posoks = None

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

    def set_char_size(self, cls):
        self.char_size = cls(self.world)

    def set_char_pos(self, cls):
        self.char_pos = cls(self.world)

    def pos_ok(self, pos, size, screen_limits=True):
        if screen_limits and \
                pos[0] < 0 or pos[0] + size[0] > self.world.size[0] \
                or pos[1] - size[1] < 0 or pos[1] > self.world.size[1]:
            return False

        if self.posoks is None:
            return True
        else:
            return self.posoks.get(*pos) and \
                self.posoks.get(pos[0] + size[0], pos[1])

    def load_imgfile(self, filename):
        return pygame.image.load(filename).convert()

    def load_posfile(self, filename):
        bm = BitMap(*self.world.size)
        bm.load(filename)
        return bm

    def draw(self, surf=None):
        if surf is None:
            surf = self.world
        surf.blit(self.surf, (0, 0))
        for obj in self.objects:
            obj.draw()

