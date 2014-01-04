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
            raise Exception("MachOThreadCommand : flavor not already supported, please report it! (0x%x)" % self.flavor)

    def display(self, before=''):
        print before + "[+] %s" % ("LC_THREAD" if self.cmd == LC_THREAD else "LC_UNIXTHREAD")
        if self.flavor == x86_THREAD_STATE32:
            print before + "\teax = 0x%08x\tebx = 0x%08x\tecx = 0x%08x\tedx = 0x%08x" % (self.eax, self.ebx, self.ecx, self.edx)
            print before + "\tedi = 0x%08x\tesi = 0x%08x\tebp = 0x%08x\tesp = 0x%08x" % (self.edi, self.esi, self.ebp, self.esp)
            print before + "\tss = 0x%08x\t\teflags = 0x%08x\teip = 0x%08x\tcs = 0x%08x" % (self.ss, self.eflags, self.eip, self.cs)
            print before + "\tds = 0x%08x\t\tes = 0x%08x\t\tfs = 0x%08x\t\tgs = 0x%08x" % (self.ds, self.es, self.fs, self.gs)
        elif self.flavor == x86_THREAD_STATE64:
            print before + "\trax = 0x%016x\trbx = 0x%016x\trcx = 0x%016x\trdx = 0x%016x" % (self.rax, self.rbx, self.rcx, self.rdx)
            print before + "\trdi = 0x%016x\trsi = 0x%016x\trbp = 0x%016x\trsp = 0x%016x" % (self.rdi, self.rsi, self.rbp, self.rsp)
            print before + "\t r8 = 0x%016x\t r9 = 0x%016x\tr10 = 0x%016x\tr11 = 0x%016x" % (self.r8, self.r9, self.r10, self.r11)
            print before + "\tr12 = 0x%016x\tr13 = 0x%016x\tr14 = 0x%016x\tr15 = 0x%016x" % (self.r12, self.r13, self.r14, self.r15)
            print before + "\trip = 0x%016x\trflags = 0x%016x\t cs = 0x%016x\t fs = 0x%016x" % (self.rip, self.rflags, self.cs, self.fs)
            print before + "\t gs = 0x%016x" % self.gs
