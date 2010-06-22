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
    def __init__(self, world, idname, imgfile=None, posfile=None):
        self.world = world
        self.id = idname
        self.objects = []
        if imgfile is not None:
            self.surf = self.load_imgfile(imgfile)
        else:
            self.surf = None

        if posfile is not None:
            self.posoks = self.load_posfile(posfile)
        else:
            self.posoks = None

    def char_size(self, pos):
        return 1

    def char_pos(self, pos):
        return pos

    def pos_ok(self, pos):
        if self.posoks is None:
            return True
        else:
            return self.posoks.get(*pos)

    def load_imgfile(self, filename):
        return pygame.image.load(filename).convert()

    def load_posfile(self, filename):
        bm = BitMap(*self.world.size)
        bm.load(filename)
        return bm

    def draw(self, surf=None):
        if surf is None:
            surf = self.world.screen
        surf.blit(self.surf, (0, 0))
        for obj in self.objects:
            obj.draw()

