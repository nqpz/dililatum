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

##[ Name        ]## font
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Contains the Font class, which makes it possible
                  # to write text

import pygame
from pygame.locals import *
import math

class Font:
    def __init__(self, world, **oargs):
        def get(key, default):
            try: return oargs[key]
            except KeyError: return default

        self.world = world
        self.path = get('path', None)
        self.size = get('size', 30)

        self.create_font()

    def create_font(self):
        self.font = pygame.font.Font(self.path, self.size)

    def write(self, text, **oargs):
        color = oargs.get('color') or (0, 0, 0)
        split = oargs.get('split') or False
        antialias = oargs.get('antialias') or True
        if not split:
            return self.font.render(text, antialias, color)
        else:
            t = text[:]
            w = split[0]
            ts = []
            while t:
                tt = t[:]
                s = False
                while self.font.size(tt)[0] > w:
                    nf = tt.rfind(' ')
                    if nf != -1:
                        tt = tt[:nf]
                        s = True
                    else:
                        tt = tt[:-1]
                        s = False
                ts.append(tt)
                if s:
                    t = t[len(tt) + 1:]
                else:
                    t = t[len(tt):]

            fh = self.font.size('')[1]
            rows_p_t = int(split[1] / fh)
            rows = len(ts)
            surfs = []
            tslen = len(ts)

            for i in range(int(math.ceil(float(rows) / rows_p_t))):
                surf = pygame.Surface(split).convert_alpha()
                surf.fill(pygame.Color(0, 0, 0, 0))
                for j in range(rows_p_t):
                    n = i * rows_p_t + j
                    if n >= tslen:
                        break
                    surf.blit(self.font.render(ts[n],
                                               antialias, color),
                              (0, fh * j))
                surfs.append(surf)
            return surfs
