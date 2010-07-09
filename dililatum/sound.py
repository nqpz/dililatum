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

##[ Name        ]## sound
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Contains the Sound class, which makes it possible
                  # to play back sound

import pygame
from pygame.locals import *

class Sound(pygame.mixer.Sound):
    def __init__(self, world, path):
        self.world = world
        self.path = path
        self.is_playing = False
        if self.world.sys.etc.loadwait:
            self.load_sound()
        else:
            self.loaded = False

    def load_sound(self):
        pygame.mixer.Sound.__init__(self, self.path)
        self.loaded = True

    def play(self):
        if not self.loaded:
            self.load_sound()
        pygame.mixer.Sound.play(self)
        self.is_playing = True

    def stop(self):
        pygame.mixer.Sound.stop(self)
        self.is_playing = False
