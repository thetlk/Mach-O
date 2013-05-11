# encoding: utf-8

from struct import unpack
from pymacho.Constants import *


class MachOThreadCommand(object):

    flavor = 0
    count = 0

    def __init__(self, macho_file=None):
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

        if self.flavor == x86_THREAD_STATE64:
            self.rax, self.rbx, self.rcx, self.rdx = unpack('<QQQQ', macho_file.read(4*8))
            self.rdi, self.rsi, self.rbp, self.rsp = unpack('<QQQQ', macho_file.read(4*8))
            self.r8, self.r9, self.r10, self.r11 = unpack('<QQQQ', macho_file.read(4*8))
            self.r12, self.r13, self.r14, self.r15 = unpack('<QQQQ', macho_file.read(4*8))
            self.rip, self.rflags, self.cs, self.fs = unpack('<QQQQ', macho_file.read(4*8))
            self.gs = unpack('<Q', macho_file.read(8))[0]
