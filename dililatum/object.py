#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Dililatum: a quest system for simple RPGs
# Copyright (C) 2010  Niels Serup

# This file is part of Dililatum.
#
# Dililatum is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Dililatum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Dililatum.  If not, see <http://www.gnu.org/licenses/>.

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
        # 0: Simple overlay object, is always present, used for
        # transparent objects linking places together
        self.rel = get('rel', 0) # 1 for real position, 0 for
                                 # modified (visible) position
        self.action = get('action', None)
        self.unaction = get('unaction', None)
        self.visible = get('visible', True)
        self.pos = get('pos', (0, 0))
        self.size = get('size', None)
        self.area = get('area', None)
        self.in_area = False
        if self.size is None and self.pos is not None and \
                'append' in dir(self.pos[0]) and len(self.pos) > 1:
            self.size = self.pos[1]
            self.pos = self.pos[0]
        self.imgfile = get('imgfile', None)
        if self.imgfile is not None and self.world.sys.etc.loadwait:
            self.load_image()
        else:
            self.surf = None
        self.walkonact = get('walkonact', True)

    def load_image(self):
        if self.imgfile is None: return
        self.surf = pygame.image.load(self.imgfile).convert_alpha()
        self.size = self.surf.get_size()
        for i in range(2):
            if self.area[0][i] is None:
                self.area[0][i] = self.pos[i]
            if self.area[1][i] is None:
                self.area[1][i] = self.area[0][i] + self.size[i]
            else:
                self.area[1][i] -= self.area[0][i]

    def check_if_action_needed(self, pos, size, act_if_wanted=True):
        if self.surf is None: self.load_image()
        retval = True

        if self.rel == 0:
            npos = self.world.current_place.char_pos(pos)
        else:
            npos = pos

        if self.type == 0:
            touch = self.feet_in_obj_check(self.area[0], self.area[1],
                                           pos, size)
            if touch:
                retval = self.walkonact

        if act_if_wanted:
            if touch and not self.in_area:
                self.in_area = True
                self.do_action()
            elif not touch and self.in_area:
                self.in_area = False
                self.do_unaction()

        return retval

    def feet_in_obj_check(self, spos, ssize, cpos, csize):
        pos1 = [cpos[0], cpos[1] - csize[1] / 15]
        pos2 = [cpos[0] + csize[0], cpos[1]]
        xos1 = spos
        xos2 = [spos[i] + ssize[i] for i in range(2)]
        return pos1[0] < xos2[0] and pos2[0] > xos1[0] and \
            pos1[1] < xos2[1] and pos2[1] > xos1[1]

    def do_action(self):
        if self.action is not None:
            self.action[0](*self.action[1:])

    def do_unaction(self):
        if self.unaction is not None:
            self.unaction[0](*self.unaction[1:])

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self, surf=None):
        if not self.visible: return
        if self.surf is None: self.load_image()
        if self.surf is None: return
        if surf is None:
            surf = self.world

        surf.blit(self.surf, self.pos)
