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
from questylib.object import Object
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

class Duration:
    def __init__(self, dur):
        self.duration = dur * 1000

class World:
    default_character_moving_keys = dict(
        cb=[K_DOWN],
        ct=[K_UP],
        lm=[K_LEFT],
        rm=[K_RIGHT],
        lb=[K_LEFT, K_DOWN],
        rt=[K_RIGHT, K_UP],
        lt=[K_LEFT, K_UP],
        rb=[K_RIGHT, K_DOWN]
    )

    def __init__(self, stm, size, **oargs):
        def get(key, default):
            try: return oargs[key]
            except KeyError: return default
        self.sys = stm
        self.size = size
        self.real_size = tuple(self.size)
        self.objects = []
        self.characters = []
        self.leading_character = EmptyCharacter()
        self.leading_character_direction = None
        self.character_moving_keys = get('charkeys',
                                         self.default_character_moving_keys)
        self.walking_speed = get('walkspeed', Duration(100))
        self.counters = []
        self.places = []
        self.current_place = None
        self.running = False
        self.quitting = False
        self.status = StatusPrinter('WORLD', self.sys.etc, 'cyan', 'blue')
        self.link_event = self.sys.gameactions.add
        self.keys_down = []
        self.screen_offset = [0, 0]
        self.screen_bars = [None, None]
        self.sys.emit_signal('afterworldinit', self)

    def start(self):
        self.sys.emit_signal('beforeworldstart', self)
        self.status('Starting up...')

        self.link_event(QUIT, self.quit)
        self.link_event(KEYDOWN, self.key_builtin)
        self.link_event(KEYDOWN, self.lead_walk)
        self.link_event(KEYUP, self.lead_walk)

        self.counters.append(TimeCounter(self.walking_speed, self.check_lead_walk))

        pygame.init()
        self.create_screen()
        self.fill_background((0, 0, 0))
        self.set_caption(self.sys.game.name)

        self.innerclock = pygame.time.Clock()
        self.sys.emit_signal('afterworldstart', self)

    def create_screen(self):
        self.screen_bars = [None, None]
        etc = self.sys.etc
        if etc.fullscreen:
            flags = FULLSCREEN
            if etc.hwaccel:
                flags = flags | HWSURFACE
            if etc.doublebuf:
                flags = flags | DOUBLEBUF
            self.screen = pygame.display.set_mode(self.size, flags)
        elif etc.fakefullscreen or etc.size is not None:
            barsize = None
            if etc.fakefullscreen or (etc.size is not None and etc.size[0] is None and etc.size[1] is None):
                try:
                    info = pygame.display.Info()
                    size = info.current_w, info.current_h
                    if size[0] == -1: # in this case, size[1] will also be -1
                        self.sys.error('your SDL is too old for width and height detection', False)
                except Exception:
                    self.sys.error('your PyGame is too old for width and height detection', False)
            else:
                size = list(etc.size)
            if size[0] is None:
                self.sys.etc.zoom = size[1] / float(self.size[1])
                size[0] = int(self.size[0] * etc.zoom)
            elif size[1] is None:
                self.sys.etc.zoom = size[0] / float(self.size[0])
                size[1] = int(self.size[1] * etc.zoom)
            else:
                scales = [size[i] / float(self.size[i]) for i in range(2)]
                if scales[0] < scales[1]: a = 0; b = 1
                else:                     a = 1; b = 0

                self.sys.etc.zoom = scales[a]
                self.screen_offset[b] = int((size[b] - self.size[b] * etc.zoom) / 2)
                barsize = [0, 0]
                barsize[a] = size[a]
                barsize[b] = self.screen_offset[b]
            self.real_size = size
            self.status('Modified size of game is: %dx%d' % tuple(self.real_size))
            flags = None
            if not etc.border or etc.fakefullscreen:
                flags = NOFRAME
            if etc.doublebuf:
                if flags is not None:
                    flags = flags | DOUBLEBUF
                else:
                    flags = DOUBLEBUF
            try:
                self.screen = pygame.display.set_mode(self.real_size, flags)
            except pygame.error:
                if not etc.border or etc.fakefullscreen:
                    flags = NOFRAME
                else:
                    flags = 0
                self.screen = pygame.display.set_mode(self.real_size, flags)
            if barsize is not None:
                self.screen_bars[b] = pygame.Surface(barsize).convert()
        else:
            if etc.zoom != 1:
                self.real_size = [int(x * etc.zoom) for x in self.size]
                self.status('Scaled size of game is: %dx%d' % tuple(self.real_size))
            flags = None
            if not etc.border or etc.fakefullscreen:
                flags = NOFRAME
            if etc.doublebuf:
                if flags is not None:
                    flags = flags | DOUBLEBUF
                else:
                    flags = DOUBLEBUF
            try:
                self.screen = pygame.display.set_mode(self.real_size, flags)
            except pygame.error:
                if not etc.border or etc.fakefullscreen:
                    flags = NOFRAME
                else:
                    flags = 0
                self.screen = pygame.display.set_mode(self.real_size, flags)

        self.bgsurface = pygame.Surface(self.real_size).convert()

    def fill_background(self, color):
        self.bgsurface.fill(color)
        for x in self.screen_bars:
            if x is not None:
                x.fill(color)

    def set_caption(self, caption):
        pygame.display.set_caption(caption)

    def set_icon(self, surf):
        pygame.display.set_icon(surf)

    def load_icon(self, path):
        self.set_icon(pygame.image.load(path).convert_alpha())

    def blit(self, surf, pos):
        surf = pygame.transform.smoothscale(surf, [int(x * self.sys.etc.zoom) for x in surf.get_size()])
        self.screen.blit(surf, [self.screen_offset[i] + pos[i] * self.sys.etc.zoom for i in range(2)])

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

    def check_lead_walk(self):
        if self.leading_character_direction is None:
            self.leading_character.stop()
        else:
            self.leading_character.walk(self.leading_character_direction)

    def lead_walk(self, event):
        if event.type == KEYDOWN:
            self.keys_down.append(event.key)
        elif event.type == KEYUP:
            try:
                self.keys_down.remove(event.key)
            except ValueError:
                pass

        self.leading_character_direction = \
            self.get_value_of_key_dict(self.character_moving_keys)

    def get_value_of_key_dict(self, keydict):
        result = None
        result_key_numbers = None
        result_points = None
        for value, keys in keydict.items():
            p = []
            tp = 0
            tn = 0
            ok = True
            for k in keys:
                i = 0
                ok = False
                for d in self.keys_down:
                    if k == d:
                        tp += i
                        tn += 1
                        ok = True
                        break
                    i += 1
                if not ok:
                    break
            if ok:
                if result_key_numbers is not None:
                    tngo = tn > result_key_numbers
                    tn2go = tn == result_key_numbers
                else:
                    tngo = True
                if not tngo:
                    if result_points is not None:
                        tpgo = tp < result_points
                    else:
                        tpgo = True

                if tngo or (tn2go and tpgo):
                    result = value
                    result_points = tp
                    result_key_numbers = tn

        return result

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

    def create_object(self, *args, **oargs):
        self.sys.emit_signal('beforeobjectcreate', self)
        args = list(args)
        args.insert(0, self)
        obj = Object(*args, **oargs)
        self.sys.emit_signal('afterobjectcreate', obj)
        return obj

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

    def set_place(self, place, npos=None, direction=None):
        if 'draw' in dir(place):
            self.current_place = place
        else:
            try:
                self.current_place = self.places[place]
            except IndexError:
                pass
        if npos is None:
            npos = self.leading_character.default_position
        self.leading_character.original_position = npos
        self.leading_character.position = npos[:]
        self.leading_character.modified_position = npos[:]
        if direction is not None:
            self.leading_character.direction = direction
            self.leading_character_direction = direction
        self.leading_character.stop()

    def get_center(self):
        return [x / 2 for x in self.size]

    def draw(self):
        self.screen.blit(self.bgsurface, (0, 0))
        self.current_place.draw()
        for char in self.characters:
            char.draw()

        if self.screen_bars[0] is not None:
            self.screen.blit(self.screen_bars[0], (0, 0))
            self.screen.blit(self.screen_bars[0],
                             (self.real_size[0] -
                              self.screen_bars[0].get_size()[0], 0))
        if self.screen_bars[1] is not None:
            self.screen.blit(self.screen_bars[1], (0, 0))
            self.screen.blit(self.screen_bars[1],
                             (0, self.real_size[1] -
                              self.screen_bars[1].get_size()[1]))

        pygame.display.flip()

    def run(self):
        self.sys.emit_signal('beforeworldrun', self)
        self.status('Running...')
        self.running = True

        for c in self.counters:
            c.start()

        while not self.quitting:
            self.innerclock.tick(30)
            self.sys.emit_signal('beforegameloop', self)

            for event in pygame.event.get():
                self.sys.emit_event(event.type, event)

            for c in self.counters:
                c.think()

            self.draw()
            self.sys.emit_signal('aftergameloop', self)

        self.sys.emit_signal('afterworldrun', self)

    def quit(self, event):
        self.quitting = True

    def key_builtin(self, event):
        if event.key == K_SCROLLOCK:
            self.leading_character.reset_position()
        if event.key == K_ESCAPE:
            self.quit(event)

    def end(self):
        self.sys.emit_signal('beforeworldend', self)
        self.status('Stopping...')
        self.sys.emit_signal('afterworldend', self)
