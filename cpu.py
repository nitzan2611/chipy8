#!/usr/bin/python
#* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#*   chipy8 - cpu.py                                                       *
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
import array
import random
from memory import Memory

class Cpu:
    def __init__(self):
        # CPU properties
        # 16 general purpose 8-bit registers
        self._reg = array.array('B', [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        # 16-bit register
        self._I = array.array('H', [0])
        # Timers delay = 0 / sound = 1
        self._timer = array.array('B', [0,0])
        # Stack
        self._stack = array.array('H', [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        # Program Counter
        self._PC = array.array('H', [0x0200])
        # Memory
        self.memory = Memory()

        # other properties
        self.__fps = 60
        self.__color_on = (0, 0, 0) # Black
        self.__color_off = (255, 255, 255) # White
        
        # Setup the environment
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.window = pygame.display.set_mode((64, 32))
        pygame.display.set_caption('pyC8')
        self.clock = pygame.time.Clock()
        self._screen = pygame.display.get_surface() # get the display surface representing a screen
        self._pxarray = pygame.PixelArray(self._screen)
        self.erase()
    
    def key_value(key):
        value = -1
        if key == K_0:
            value = 0
        elif key == K_1:
            value = 1
        elif key == K_2:
            value = 2
        elif key == K_3:
            value = 3
        elif key == K_4:
            value = 4
        elif key == K_5:
            value = 5
        elif key == K_6:
            value = 6
        elif key == K_7:
            value = 7
        elif key == K_8:
            value = 8
        elif key == K_9:
            value = 9
        elif key == K_a:
            value = 0xa
        elif key == K_b:
            value = 0xb
        elif key == K_c:
            value = 0xc
        elif key == K_d:
            value = 0xd
        elif key == K_e:
            value = 0xe
        elif key == K_f:
            value = 0xf
        return value

    def execute(self):
        word = (self.memory.read(self._PC[0]) << 8) | (self.memory.read(self._PC[0] + 1))
        n1 = (word >> 12) & 0x0f
        n2 = (word >> 8) & 0x0f
        n3 = (word >> 4) & 0x0f
        n4 = word & 0x0f
        print "Opcode: %x" % (word)
        self._PC[0] = self._PC[0] + 2
        
        if n1 == 0x0:
            if n2 == 0:
                if n3 == 0xc:
                    print "00CN	Scroll down %i lines (***)" % (n4)
                    sys.exit(1)
                elif n3 == 0xf and n4 == 0xb:
                    print "00FB	Scroll 4 pixels right (***)"
                    sys.exit(1)
                elif n3 == 0xf and n4 == 0xc:
                    print "00FC	Scroll 4 pixels left (***)"
                    sys.exit(1)
                elif n3 == 0xf and n4 == 0xd: # 00FD Quit the emulator (***)
                    sys.exit(1)
                elif n3 == 0xf and n4 == 0xe: # 00FE Set CHIP-8 graphic mode (***)
                    print "TODO: not implemented"
                    sys.exit(1)
                elif n3 == 0xf and n4 == 0xf: # 00FF Set SCHIP graphic mode (***)
                    print "TODO: not implemented"
                    sys.exit(1)
                elif n3 == 0xe and n4 == 0x0: # 00E0 Erase the screen
                    self.erase()
                elif n3 == 0xe and n4 == 0xe: # 00EE Return from a CHIP-8 sub-routine
                    self._PC[0] = stack.pop()
                else:
                    print "Error %2x%2x%2x%2x" % (n1,n2,n3,n4)
                    sys.exit(1)
            else:   # 0NNN Call 1802 machine code program at NNN (not implemented)
                print "0NNN	Call 1802 machine code program at NNN (not implemented)"
                sys.exit(1)
        elif n1 == 0x1: # 1NNN Jump to NNN
            self._PC[0] = word & 0x0fff
        elif n1 == 0x2: # 2NNN Call CHIP-8 sub-routine at NNN (16 successive calls max)
            self.stack.append(self._PC[0])
            self._PC[0] = word & 0x0fff
        elif n1 == 0x3: # 3XKK	Skip next instruction if VX == KK
            if self._reg[n2] == (word & 0x00ff):
                self._PC[0] = self._PC[0] + 2
        elif n1 == 0x4: # 4XKK	Skip next instruction if VX != KK
            if self._reg[n2] != (word & 0x00ff):
                self._PC[0] = self._PC[0] + 2
        elif n1 == 0x5 and n4 == 0x0: # 5XY0 Skip next instruction if VX == VY
            if self._reg[n2] == self._reg[n3]:
                self._PC[0] = self._PC[0] + 2
        elif n1 == 0x6: # 6XKK VX = KK
            self._reg[n2] = word & 0x00ff
        elif n1 == 0x7: # 7XKK	VX = VX + KK
            self._reg[n2] = (self._reg[n2] + (word & 0x00ff)) & 0xff
        elif n1 == 0x8:
            if n4 == 0x0: # 8XY0 VX = VY
                self._reg[n2] = self._reg[n3]
            elif n4 == 0x1: # 8XY1 VX = VX OR VY
                self._reg[n2] = self._reg[n2] | self._reg[n3]
            elif n4 == 0x2: # 8XY2	VX = VX AND VY
                self._reg[n2] = self._reg[n2] & self._reg[n3]
            elif n4 == 0x3: #8XY3 VX = VX XOR VY (*)
                self._reg[n2] = self._reg[n2] ^ self._reg[n3]
            elif n4 == 0x4: # 8XY4	VX = VX + VY, VF = carry
                if (self._reg[n2] + self._reg[n3]) > 0xff:
                    self._reg[0xf] = 1
                else:
                    self._reg[0xf] = 0
                self._reg[n2] = (self._reg[n2] + self._reg[n3]) & 0xff
            elif n4 == 0x5: # 8XY5	VX = VX - VY, VF = not borrow (**)
                if self._reg[n2] < self._reg[n3]:
                    self._reg[0xf] = 0
                    self._reg[n2] = (0x100 - (self._reg[n3] - self._reg[n2])) & 0xff
                else:
                    self._reg[0xf] = 1
                    self._reg[n2] = (self._reg[n2] - self._reg[n3]) & 0xff
            elif n4 == 0x6: # 8XY6 VX = VX SHR 1 (VX=VX/2), VF = carry
                if self._reg[n2] > 127:
                    self._reg[0xf] = 1
                else:
                    self._reg[0xf] = 0
                self._reg[n2] = (self._reg[n2] * 2) & 0xff
            elif n4 == 0x7: # 8XY7 VX = VY - VX, VF = not borrow (*) (**)
                if self._reg[n3] < self._reg[n2]:
                    self._reg[0xf] = 0
                    self._reg[n2] = (0x100 - (self._reg[n2] - self._reg[n3])) & 0xff
                else:
                    self._reg[0xf] = 1
                    self._reg[n2] = (self._reg[n3] - self._reg[n2]) & 0xff
            elif n4 == 0xe: # 8XYE	VX = VX SHL 1 (VX=VX*2), VF = carry
                if (self._reg[n2] * 2) > 0xff:
                    self._reg[0xf] = 1
                else:
                    self._reg[0xf] = 0
                self._reg[n2] = (self._reg[n2] * 2) & 0xff
            else:
                print "Error %1x%1x%1x%1x" % (n1,n2,n3,n4)
                sys.exit(1)
        elif n1 == 0x9 and n4 == 0x0: # 9XY0 Skip next instruction if VX != VY
            if self._reg[n2] != self._reg[n3]:
                self._PC[0] = self._PC[0] + 2
        elif n1 == 0xa: # ANNN I = NNN
            self._I[0] = word & 0x0fff
        elif n1 == 0xb: # BNNN Jump to NNN + V0
            self._PC[0] = (word & 0x0fff) + self._reg[0]
        elif n1 == 0xc: # CXKK VX = Random number AND KK
            self._reg[n2] = random.randint(0, word & 0xff)
        elif n1 == 0xd and n4 == 0: #DXYN Draws a sprite at (VX,VY) starting at M(I). VF = collision. If N=0, draws the 16 x 16 sprite, else an 8 x N sprite.
            print "TODO: not implemented"
            sys.exit(1)
        elif n1 == 0xd: # DXYN Draws a sprite at (VX,VY) starting at M(I). VF = collision. If N=0, draws the 16 x 16 sprite, else an 8 x N sprite.
            self._reg[0xf] = 0
            print "%x - %x" % (self._reg[n2], self._reg[n3])
            for yline in range(n4):
                byte = self.memory.read(self._I[0] + yline)
                for xline in range(8):
                    if (byte & (0x80>>xline)) != 0:
                        x = (self._reg[n2] + xline) % 64
                        y = (self._reg[n3] + yline) % 32
                        if self._pxarray[x][y] == self.__color_on:
                            self._pxarray[x][y] = self.__color_off
                            self._reg[0xf] = 1
                        else:
                            self._pxarray[x][y] = self.__color_on
            pygame.display.flip()
        elif n1 == 0xe and n3 == 0x9 and n4 == 0xe: # EX9E skip next instruction if key VX pressed
            event = pygame.event.poll()
            if event.type != pygame.NOEVENT:
                if key_value(event.key) == self._reg[n2]:
                    self._PC[0] = self._PC[0] + 2
        elif n1 == 0xe and n3 == 0xa and n4 == 0x1: # EXA1 Skip next instruction if key VX not pressed
            event = pygame.event.poll()
            if event.type == pygame.NOEVENT:
                self._PC[0] = self._PC[0] + 2
            elif key_value(event.key) != self._reg[n2]:
                self._PC[0] = self._PC[0] + 2
        elif n1 == 0xf and n3 == 0x0 and n4 == 0x7: # FX07 VX = Delay timer
            self._reg[n2] = self._timer[0] & 0xff
        elif n1 == 0xf and n3 == 0x0 and n4 == 0xa: # FX0A Waits a keypress and stores it in VX
            while True:
                event = pygame.event.wait()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(1)
                if key_value(event.key) >= 0:
                    self._reg[n2] = self.key_value(event.key)
                    break
        elif n1 == 0xf and n3 == 0x1 and n4 == 0x5: # FX15 Delay timer = VX
            self._timer[0] = self._reg[n2] & 0xff
        elif n1 == 0xf and n3 == 0x1 and n4 == 0x8: # FX18 Sound timer = VX
            self._timer[1] = self._reg[n2]
        elif n1 == 0xf and n3 == 0x1 and n4 == 0xe: # FX1E I = I + VX
            self._I[0] = self._I[0] + self._reg[n2] & 0xffff
        elif n1 == 0xf and n3 == 0x2 and n4 == 0x9: # FX29	I points to the 4 x 5 font sprite of hex char in VX
            self._I[0] = (self._reg[n2] * 5) & 0xffff
        elif n1 == 0xf and n3 == 0x3 and n4 == 0x3: # FX33 Store BCD representation of VX in M(I)...M(I+2)
            self.memory.write(self.memory.read(self._I[0]), self._reg[n2] / 100)
            self.memory.write(self.memory.read(self._I[0]+1), (self._reg[n2] % 10) / 10)
            self.memory.write(self.memory.read(self._I[0]+2), self._reg[n2] % 10)
        elif n1 == 0xf and n3 == 0x5 and n4 == 0x5: # FX55 Save V0...VX in memory starting at M(I)
            for i in range(n2 + 1):
                self.memory.write(self.memory.read(self._I[0] + i), self._reg[i])
        elif n1 == 0xf and n3 == 0x6 and n4 == 0x5: # FX65 Load V0...VX from memory starting at M(I)
            for i in range(n2 + 1):
                self._reg[i] = self.memory.read(self._I[0] + i) & 0xff
        elif n1 == 0xf and n3 == 0x7 and n4 == 0x5:
            print "FX75	Save V0...VX (X<8) in the HP48 flags (***)"
            sys.exit(1)
        elif n1 == 0xf and n3 == 0x8 and n4 == 0x5:
            print "FX85	Load V0...VX (X<8) from the HP48 flags (***)"
            sys.exit(1)
        else:
            print "Error %1x%1x%1x%1x" % (n1,n2,n3,n4)
            sys.exit(1)

        if self._timer[0] > 0:
            self._timer[0] = self._timer[0] - 1
        if self._timer[1] > 0:
            self._timer[1] = self._timer[1] - 1
    
    def read_rom(self, filename):
        self.memory.read_rom(filename)

    def input(self, events): 
        for event in events: 
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)
            else:
                print event 

    def erase(self):
        for x in range (64):
            for y in range (32):
                self._pxarray[x][y] = self.__color_off
        pygame.display.flip()

    def run(self, fps = 60):
        self.__fps = fps
        while True:
            self.clock.tick(self.__fps)
            self.input(pygame.event.get())
            self.execute()

