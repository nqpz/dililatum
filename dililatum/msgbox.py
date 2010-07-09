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

##[ Name        ]## msgbox
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Makes it possible to display messages and speech
                  # throughout the game

import pygame
from pygame.locals import *
import os.path

HEADSIZE = 75

class MessageBox:
    def __init__(self, world, **oargs):
        def get(key, default):
            try: return oargs[key]
            except KeyError: return default

        self.world = world
        self.path = get('bgimg', None)
        self.font = get('font', None)
        self.pos = get('pos', (10, 10))
        self.headplace = get('headplace', 'lm')
        self.textplace = get('textplace', 'rm')
        self.size = get('size', (620, 120))
        self.visible = False

        if self.path is not None:
            self.surf = \
                self.world.load_image(os.path.normpath(self.path), True)
            self.size = self.surf.get_size()
            self.pos = ((self.world.size[0] - self.size[0]) / 2, self.pos[1])
            if self.headplace == 'lm':
                self.headpos = (self.pos[0] + 10,
                                self.pos[1] + (self.size[1] -
                                               HEADSIZE) / 2)
                self.textpos = (self.pos[0] + 20 + HEADSIZE,
                                self.pos[1] + 10)
                self.textsize = (self.size[0] - 30 - HEADSIZE,
                                 self.size[1] - 20)
        else:
            self.surf = None
            self.headpos = (20, 20)
            self.textpos = (20 + HEADSIZE, 20)

        self.head = None
        self.text = None

    def show(self, head=None, text=None):
        if head is not None:
            self.head = head
        if text is not None:
            self.text = text
            self.textsurf = self.font.write(text)
        if self.head and self.text:
            self.visible = True

    def hide(self):
        self.visible = False

    def draw(self):
        if not self.visible: return

        if self.surf is not None:
            self.world.blit(self.surf, self.pos)

        if self.head is not None:
            self.world.blit(self.head, self.headpos)

        if self.text is not None:
            self.world.blit(self.textsurf, self.textpos)
