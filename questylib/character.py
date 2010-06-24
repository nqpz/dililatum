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

##[ Name        ]## character
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Contains the Character class, controlling how
                  # people and monsters alike move

from datetime import datetime
import pygame
from pygame.locals import *
import os.path

class Frame:
    def __init__(self, img):
        self.surf = img.convert_alpha()
        self.width = img.get_width()
        self.height = img.get_height()

class EmptyCharacter:
    def walk(self, event):
        pass

class Character:
    def __init__(self, world, idname, datafiles, **oargs):
        self.id = idname
        self.name = None
        self.world = world
        self.data = datafiles
        self.frames = {}
        self.walking = False
        self.step = 0
        def get(key, default):
            try: return oargs[key]
            except KeyError: return default
        self.direction = get('direction', 'cb')
        self.position = get('position', world.get_center())
        self.duration = get('duration', 250) * 1000

    def convert_files_to_surfaces(self, *files):
        frames = []
        for f in files:
            img = pygame.image.load(f)
            frames.append(Frame(img))
        return frames

    def create(self):
        for x in 'lt', 'ct', 'rt', 'lm', 'rm', 'lb', 'cb', 'rb':
            if x in self.data[1]: # Files and directories
                files = self.data[1][x][1] # 1 = files
                files = [os.path.join(self.data[0], x, t) for t in files]
                self.frames[x] = \
                    self.convert_files_to_surfaces(*files)

    def status(self, msg):
        print '!!! ' + str(datetime.now()) + ' !!!\n' + msg

    def next_step(self):
        self.step = (self.step + 1) % len(self.frames[self.direction])

    def walk(self, event):
        print event.type

    def draw(self, surf=None, pos=None):
        if self.walking:
            img = self.frames[self.direction][self.step]
        else:
            img = self.frames[self.direction][0]
        if surf is None:
            surf = self.world.screen
        if pos is None:
            pos = ((self.world.size[0] - img.width) / 2,
                   (self.world.size[1] - img.height) / 2)
        surf.blit(img.surf, pos)

