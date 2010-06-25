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
import os.path
import pygame
from pygame.locals import *

class Frame:
    def __init__(self, img):
        self.surf = img.convert_alpha()
        self.width = img.get_width()
        self.height = img.get_height()

class EmptyCharacter:
    def stop(self):
        pass

    def walk(self, direction):
        pass

class Character:
    def __init__(self, world, idname, datafiles, **oargs):
        def get(key, default):
            try: return oargs[key]
            except KeyError: return default
        self.id = idname
        self.name = None
        self.world = world
        self.data = datafiles
        self.frames = {}
        self.walking = False
        self.step = 0
        self.direction = get('direction', 'cb')
        self.position = get('position', world.get_center())
        self.duration = get('duration', 200) * 1000
        self.movement = get('movement', dict(
                cb=(0, 3),
                ct=(0, -3),
                lm=(-3, 0),
                rm=(3, 0),
                lb=(-2.12, 2.12),
                rt=(2.12, -2.12),
                lt=(-2.12, -2.12),
                rb=(2.12, 2.12)
        ))
        self.position = get('position', (
                self.world.size[0] / 2,
                self.world.size[1] * 0.9))
        self.visible = True

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

    def get_size(self, pos, img=None):
        resize = self.world.current_place.char_size(pos)
        if img is None:
            img = self.get_frame()
        w = int(img.width * resize)
        h = int(img.height * resize)
        return w, h, resize

    def get_frame(self):
        if self.walking:
            return self.frames[self.direction][self.step]
        else:
            return self.frames[self.direction][0]

    def next_step(self):
        self.step = (self.step + 1) % len(self.frames[self.direction])

    def stop(self):
        self.walking = False

    def is_reverse(self, direction):
        a = self.direction
        b = direction
        return (a == 'cb' and b in ('ct', 'rt', 'lt')) \
            or (a == 'ct' and b in ('cb', 'rb', 'lb')) \
            or (a == 'lm' and b in ('rm', 'rt', 'rb')) \
            or (a == 'rm' and b in ('lm', 'lt', 'lb')) \
            or (a == 'lt' and b == 'rb') \
            or (a == 'rt' and b == 'lb') \
            or (a == 'lb' and b == 'rt') \
            or (a == 'rb' and b == 'lt')

    def walk(self, direction, screen_limits=True, scale=1.0):
        w, h, resize = self.get_size(self.position)
        size = w, h
        mov = self.movement[direction]
        pos = self.world.current_place.char_pos(self.position)
        pos_ok = False
        origscale = scale

        while not pos_ok:
            npos = [int(pos[i] + mov[i] * resize * scale *
                        self.world.size[i] / 100.0) for i in range(2)]
            pos_ok = self.world.current_place.pos_ok(npos, size, screen_limits)
            scale -= .1
            if scale < 0.5:
                break
        if pos_ok:
            self.direction = direction
            self.position = npos
            self.walking = True
        else:
            self.stop()

            # Double checking -- character frames are not necessarily
            # of the same dimensions
            f = self.get_frame()
            fw = f.width
            fh = f.height

            if self.position[0] + fw  >= self.world.size[0]:
                self.position[0] = self.world.size[0] - 1 - fw
            if self.position[0] < 0:
                self.position[0] = 0

            if self.position[1] >= self.world.size[1]:
                self.position[1] = self.world.size[1] - 1
            if self.position[1] - fh < 0:
                self.position[1] = 0

    def draw(self, surf=None):
        if not self.visible: return False
        img = self.get_frame()
        pos = self.world.current_place.char_pos(self.position)
        w, h, r = self.get_size(pos, img)
        img = pygame.transform.smoothscale(img.surf, (w, h))
        if surf is None:
            surf = self.world
        surf.blit(img, (pos[0], pos[1] - h))
