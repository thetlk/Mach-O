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
from pymacho.MachOSection import MachOSection
from pymacho.Constants import *


class MachOSegment(object):

    arch = 32
    segname = ""
    vmaddr = 0
    vmsize = 0
    fileoff = 0
    filesize = 0
    maxprot = 0
    initprot = 0
    nsects = 0
    flags = 0
    sections = []

    def __init__(self, macho_file=None, arch=32):
        if arch != 32:
            self.arch = 64
        if macho_file is not None:
            self.parse(macho_file)

    def parse(self, macho_file):
        self.segname = "".join(char if char != "\x00" else "" for char in unpack("<cccccccccccccccc", macho_file.read(16)))

        if self.arch == 32:
            self.vmaddr, self.vmsize, self.fileoff, self.filesize = unpack('<IIII', macho_file.read(4*4))
        else:
            self.vmaddr, self.vmsize, self.fileoff, self.filesize = unpack('<QQQQ', macho_file.read(8*4))

        self.maxprot, self.initprot, self.nsects, self.flags = unpack('<IIII', macho_file.read(4*4))
        for i in range(self.nsects):
            self.sections.append(MachOSection(macho_file, arch=self.arch))

    def display_flags(self):
        rflags = []
        flags = self.flags
        if flags & SG_HIGHVM:
            rflags.append("HIGHVM")
            flags &= ~SG_HIGHVM
        if flags & SG_FVMLIB:
            rflags.append("FVMLIB")
            flags &= ~SG_FVMLIB
        if flags & SG_NORELOC:
            rflags.append("NORELOC")
            flags &= ~SG_NORELOC
        if flags & SG_PROTECTED_VERSION_1:
            rflags.append("PROTECTED_VERSION_1")
            flags &= ~SG_PROTECTED_VERSION_1
        return rflags

    def display(self, before=''):
        print before + "[+] %s" % self.segname
        print before + "\t- vmaddr : 0x%x" % self.vmaddr
        print before + "\t- vmsize : 0x%x" % self.vmsize
        print before + "\t- fileoff : 0x%x" % self.fileoff
        print before + "\t- filesize : 0x%x" % self.filesize
        print before + "\t- maxprot : 0x%x" % self.maxprot
        print before + "\t- initprot : 0x%x" % self.initprot
        print before + "\t- nsects : %d" % self.nsects
        print before + "\t- flags : 0x%x - %s" % (self.flags, self.display_flags())
