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

##[ Name        ]## object
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Contains the Object class whose purpose is to be
                  # drawn onto instances of Place classes (and thereby
                  # the screen)

import pygame
from pygame.locals import *

class Object:
    def __init__(self, world, otype=0, imgfile=None):
        self.world = world
        self.type = otype
        self.surf = None
        if imgfile is not None:
            self.load_image(imgfile)

    def load_image(self, filename):
        pass

    def draw(self, surf=None):
        if self.surf is None: return
        if surf is None:
            surf = self.world.screen
        surf.blit(self.surf, (0, 0))
        for obj in self.objects:
            obj.draw()

