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

##[ Name        ]## world
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Contains the World class, controlling display
                  # output as well as key detection

from datetime import datetime
import pygame
from pygame.locals import *
from questylib.character import Character
from questylib.place import Place

microseconds = lambda tdelta: tdelta.microseconds
class TimeCounter:
    def __init__(self, obj, func):
        self.obj = obj
        self.func = func
        self.start = self.reset

    def reset(self):
        self.time = datetime.now()

    def think(self):
        if microseconds(datetime.now() - self.time) > \
                self.obj.duration:
            self.func()
            self.reset()

class World:
    def __init__(self, stm, size):
        self.sys = stm
        self.size = size
        self.characters = []
        self.counters = []
        self.places = []
        self.current_place = None
        self.running = False

    def status(self, msg):
        print '$$$ ' + str(datetime.now()) + ' $$$\n' + msg

    def start(self):
        pygame.init()
        if self.sys.etc.fullscreen:
            try:
                self.screen = pygame.display.set_mode(
                    self.size, FULLSCREEN, DOUBLEBUF, HWSURFACE)
            except Exception:
                self.screen = pygame.display.set_mode(
                    self.size, FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.size)

        self.bgsurface = pygame.Surface(self.size).convert()
        self.bgsurface.fill((0, 0, 0))
        self.screen.blit(self.bgsurface, (0, 0))

        self.innerclock = pygame.time.Clock()
        self.sys.emit_signal('worldstart')

    def create_character(self, idname, datafiles):
        char = Character(self, idname, datafiles)
        char.create()
        return char

    def add_character(self, char):
        self.characters.append(char)
        counter = TimeCounter(char, char.next_step)
        self.counters.append(counter)
        if self.running:
            counter.start()

    def remove_character(self, char):
        try:
            self.characters.remove(char)
            self.remove_counter(char)
            return True
        except Exception:
            for t in self.characters:
                if t.id == char:
                    self.characters.remove(t)
                    self.remove_counter(t)
                    return True
            return False

    def remove_counter(self, obj):
        try:
            self.counters.remove(obj)
            return True
        except Exception:
            for t in self.counters:
                if t.obj == obj:
                    self.counters.remove(t)
                    return True
            return False

    def create_place(self, *args):
        args = list(args)
        args.insert(0, self)
        place = Place(*args)
        return place

    def add_place(self, place):
        self.places.append(place)

    def set_place(self, place):
        if 'draw' in dir(place):
            self.current_place = place
            return True
        else:
            for t in self.places:
                if t.id == place:
                    self.current_place = t
                    return True
            return False

    def get_center(self):
        return [x / 2 for x in self.size]

    def draw(self):
        self.screen.blit(self.bgsurface, (0, 0))
        self.current_place.draw()
        for char in self.characters:
            char.draw()
        pygame.display.flip()

    def run(self):
        self.running = True
        done = False
        for c in self.counters:
            c.start()

        self.draw()
        while not done:
            self.innerclock.tick(30)

            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        done = True

        for c in self.counters:
            c.think()

    def end(self):
        pass
