#!/usr/bin/python
#* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#*   chipy8 - video.py                                                     *
#*   chipy8 homepage: http://code.google.com/p/chipy8/                     *
#*   Copyright (C) 2009 olejl77@gmail.com                                  *
#*                                                                         *
#*   This program is free software: you can redistribute it and/or modify  *
#*   it under the terms of the GNU General Public License as published by  *
#*   the Free Software Foundation, either version 3 of the License, or     *
#*   (at your option) any later version.                                   *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          *
#*   GNU General Public License for more details.                          *
#*                                                                         *
#*   You should have received a copy of the GNU General Public License     *
#*   along with this program.  If not, see <http://www.gnu.org/licenses/>. *
#* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
import pygame
import os
import sys

class Video:
    def __init__(self):
        self.__color_on = (0, 0, 0) # Black
        self.__color_off = (255, 255, 255) # White
        
        # Setup the pygame environment
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.window = pygame.display.set_mode((64, 32))
        pygame.display.set_caption('pyC8')
        self._screen = pygame.display.get_surface() # get the display surface representing a screen
        self._pxarray = pygame.PixelArray(self._screen)
        self.erase()    # Call this to make sure we have the correct background color
        
    def draw8(self, ylines, regX, regY):
        collision = 0
        yline = 0
        for byte in ylines:
            byte = ylines[yline]
            for xline in range(8):
                if (byte & (0x80>>xline)) != 0:
                    x = (regX + xline) % 64
                    y = (regY + yline) % 32
                    if self._pxarray[x][y] == self.__color_on:
                        self._pxarray[x][y] = self.__color_off
                        collision = 1
                    else:
                        self._pxarray[x][y] = self.__color_on
            yline = yline + 1
        pygame.display.flip()
        return collision
        
    def erase(self):
        for x in range (64):
            for y in range (32):
                self._pxarray[x][y] = self.__color_off
        pygame.display.flip()

