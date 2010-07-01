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
    def __init__(self, world, **oargs):
        def get(key, default):
            try: return oargs[key]
            except KeyError: return default

        self.world = world
        self.type = get('type', 0)
        ##### DIFFERENT TYPES #####
        # 0: Simple overlay object
        self.rel = get('rel', 0) # 1 for real position, 0 for
                                 # modified (visible) position
        self.action = get('action', None)
        self.position = get('pos', None)
        self.size = get('size', None)
        if self.size is None and self.position is not None:
            if len(self.position) > 1:
                self.size = self.position[1]
                self.position = self.position[0]
        self.surf = None
        imgfile = get('image', None)
        if imgfile is not None:
            self.load_image(imgfile)

    def load_image(self, filename):
        pass

    def check_if_action_needed(self, pos, size, act_if_true=True):
        if self.type == 0:
            if self.rel == 0:
                npos = self.world.current_place.char_pos(pos)
            return self.char_in_obj_check(npos, size, act_if_true)

    def char_in_obj_check(self, pos, size, act_if_true=True):
        if self.position is None:
            return False
        pos1 = [pos[0], pos[1] - size[1] / 20]
        pos2 = [pos[0] + size[0], pos[1]]
        xos1 = self.position
        xos2 = [self.position[i] + self.size[i] for i in range(2)]
        touch = pos1[0] < xos2[0] and pos2[0] > xos1[0] and \
            pos1[1] < xos2[1] and pos2[1] > xos1[1]
        if touch and act_if_true:
            self.do_action()

        return touch

    def do_action(self):
        if self.action is not None:
            self.action[0](*self.action[1:])

    def draw(self, surf=None):
        if self.surf is None: return
        if surf is None:
            surf = self.world.screen
        surf.blit(self.surf, (0, 0))
        for obj in self.objects:
            obj.draw()

