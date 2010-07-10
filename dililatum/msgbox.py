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
        self.default_pos = get('pos', None)
        self.headtextrel = get('headtextrel', 0)
        # 0: | HEAD | TEXT... |
        # 1: | TEXT... | HEAD |
        # 2: |   HEAD  |
        #    | TEXT... |
        # 3: | TEXT... |
        #    |   HEAD  |
        self.size = get('size', (620, 120))
        self.visible = False

        self.msgcontainers = []

        if self.path is not None:
            self.surf = \
                self.world.load_image(os.path.normpath(self.path), True)
            self.size = self.surf.get_size()
            if self.default_pos is None:
                self.default_pos = ((self.world.size[0] - self.size[0]) / 2, 10)
            if self.headtextrel == 0:
                self.headpos = (10, (self.size[1] - HEADSIZE) / 2)
                self.textpos = (20 + HEADSIZE, 10)
                self.textsize = (self.size[0] - 35 - HEADSIZE,
                                 self.size[1] - 20)
        else:
            self.surf = None
            if self.default_pos is None:
                self.default_pos = (10, 10)
            self.headpos = (20, 20)
            self.textpos = (20 + HEADSIZE, 20)

    def draw(self):
        for x in self.msgcontainers:
            x.draw()

class MessageContainer:
    def __init__(self, msgbox, pos=None):
        self.msgbox = msgbox
        self.world = self.msgbox.world
        self.head = None
        self.text = None

        self.visible = False

    def show(self, head=None, text=None, pos=None, **oargs):
        self.msgbox.msgcontainers.append(self)
        if head is not None:
            self.head = head
        if text is not None:
            self.text = text
            self.textsurfs = self.msgbox.font.write(
                text, split=self.msgbox.textsize)
            self.textnum = 0
            self.world.link_event(KEYDOWN, self.show_more_text)
        if pos is not None:
            self.pos = pos
        else:
            self.pos = self.msgbox.default_pos
        self.temp_endaction = oargs.get('endaction') or None
        if self.head or self.text:
            self.visible = True

    def show_more_text(self, event):
        if event.key == K_RETURN or event.key == K_KP_ENTER or \
                event.key == K_SPACE:
            self.textnum += 1
        if self.textnum == len(self.textsurfs):
            self.hide()
            self.world.unlink_event(KEYDOWN, self.show_more_text)
            self.temp_endaction()
            del self.temp_endaction

    def hide(self):
        self.msgbox.msgcontainers.remove(self)
        self.visible = False

    def draw(self):
        if not self.visible: return

        if self.msgbox.surf is not None:
            self.world.blit(self.msgbox.surf, self.pos)

        if self.head is not None:
            self.world.blit(self.head,
                            [self.msgbox.headpos[i] +
                             self.pos[i]
                             for i in range(2)])

        if self.text is not None:
            surf = self.textsurfs[self.textnum]
            pos = (self.msgbox.textpos[0] + self.pos[0],
                   self.pos[1] + self.msgbox.textpos[1] +
                   (self.msgbox.size[1] - surf.get_size()[1]) / 2)
            self.world.blit(surf, pos)
