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

    def write(self, text, color=(0, 0, 0)):
        return self.font.render(text, True, color)
