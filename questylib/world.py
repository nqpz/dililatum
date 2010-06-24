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
from questylib.character import Character, EmptyCharacter
from questylib.place import Place
from questylib.statusprinter import StatusPrinter

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
        self.leading_character = EmptyCharacter()
        self.counters = []
        self.places = []
        self.current_place = None
        self.running = False
        self.quitting = False
        self.status = StatusPrinter('WORLD', self.sys.etc, 'magenta', 'cyan')
        self.link_event = self.sys.gameactions.add
        self.sys.emit_signal('afterworldinit', self)

    def start(self):
        self.sys.emit_signal('beforeworldstart', self)
        self.status('Starting up...')

        self.link_event(QUIT, self.quit)
        self.link_event(KEYDOWN, self.lead_walk)
        self.link_event(KEYUP, self.lead_walk)

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
        self.sys.emit_signal('afterworldstart', self)

    def create_character(self, idname, datafiles):
        self.sys.emit_signal('beforecharactercreate', idname, self)
        char = Character(self, idname, datafiles)
        char.create()
        self.sys.emit_signal('aftercharactercreate', char)
        return char

    def add_character(self, char):
        self.sys.emit_signal('beforecharacteradd', char)
        self.characters.append(char)
        counter = TimeCounter(char, char.next_step)
        self.counters.append(counter)
        if self.running:
            counter.start()
        self.sys.emit_signal('aftercharacteradd', char)

    def set_leading_character(self, char):
        self.leading_character = char

    def lead_walk(self, event):
        self.leading_character.walk(event)

    def remove_character(self, char):
        if 'id' not in dir(char):
            char = None
            for t in self.characters:
                if t.id == char:
                    char = t
            if char is None:
                return False

        self.sys.emit_signal('beforecharacterremove', char)
        self.characters.remove(char)
        self.remove_counter(char)
        self.sys.emit_signal('aftercharacterremove', char)
        return True

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
        self.sys.emit_signal('beforeplacecreate', self)
        args = list(args)
        args.insert(0, self)
        place = Place(*args)
        self.sys.emit_signal('afterplacecreate', place)
        return place

    def add_place(self, place):
        self.sys.emit_signal('beforeplaceadd', place)
        self.places.append(place)
        self.sys.emit_signal('afterplaceadd', place)

    def set_place(self, place):
        if 'draw' in dir(place):
            self.current_place = place
            return True
        else:
            try:
                self.current_place = self.places[place]
                return True
            except Exception:
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
        self.sys.emit_signal('beforeworldrun', self)
        self.status('Running...')
        self.running = True

        for c in self.counters:
            c.start()

        while not self.quitting:
            self.innerclock.tick(30)
            self.draw()

            for event in pygame.event.get():
                self.sys.emit_event(event.type, event)

            for c in self.counters:
                c.think()

        self.sys.emit_signal('afterworldrun', self)

    def quit(self, event):
        self.quitting = True

    def end(self):
        self.sys.emit_signal('beforeworldend', self)
        self.status('Stopping...')
        self.sys.emit_signal('afterworldend', self)
