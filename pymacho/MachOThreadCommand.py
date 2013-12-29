# encoding: utf-8

"""
Copyright 2013 Jérémie BOUTOILLE

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from struct import unpack
from pymacho.Constants import *
from pymacho.MachOLoadCommand import MachOLoadCommand


class MachOThreadCommand(MachOLoadCommand):

    flavor = 0
    count = 0

    def __init__(self, macho_file=None, cmd=0):
        self.cmd = cmd
        if macho_file is not None:
            self.parse(macho_file)

    def parse(self, macho_file):
        self.flavor = unpack('<I', macho_file.read(4))[0]
        self.count = unpack('<I', macho_file.read(4))[0]

        if self.flavor == x86_THREAD_STATE32:
            self.eax, self.ebx, self.ecx, self.edx = unpack('<IIII', macho_file.read(4*4))
            self.edi, self.esi, self.ebp, self.esp = unpack('<IIII', macho_file.read(4*4))
            self.ss, self.eflags, self.eip, self.cs = unpack('<IIII', macho_file.read(4*4))
            self.ds, self.es, self.fs, self.gs = unpack('<IIII', macho_file.read(4*4))
        elif self.flavor == x86_THREAD_STATE64:
            self.rax, self.rbx, self.rcx, self.rdx = unpack('<QQQQ', macho_file.read(4*8))
            self.rdi, self.rsi, self.rbp, self.rsp = unpack('<QQQQ', macho_file.read(4*8))
            self.r8, self.r9, self.r10, self.r11 = unpack('<QQQQ', macho_file.read(4*8))
            self.r12, self.r13, self.r14, self.r15 = unpack('<QQQQ', macho_file.read(4*8))
            self.rip, self.rflags, self.cs, self.fs = unpack('<QQQQ', macho_file.read(4*8))
            self.gs = unpack('<Q', macho_file.read(8))[0]
        else:
            raise Exception("MachOThreadCommand : flavor not already supported, please report it!")

    def display(self, before=''):
        print before + "[+] %s" % ("LC_THREAD" if self.cmd == LC_THREAD else "LC_UNIXTHREAD")
