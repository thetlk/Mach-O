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


class MachOSection(object):

    arch = 32
    sectname = ""
    segname = ""
    addr = 0
    size = 0
    offset = 0
    align = 0
    reloff = 0
    nreloc = 0
    flags = 0
    reserved1 = 0
    reserved2 = 0

    def __init__(self, macho_file=None, arch=32):
        if arch != 32:
            self.arch = 64
        if macho_file is not None:
            self.parse(macho_file)

    def parse(self, macho_file):
        self.sectname = "".join(char if char != "\x00" else "" for char in unpack("<cccccccccccccccc", macho_file.read(16)))
        self.segname = "".join(char if char != "\x00" else "" for char in unpack("<cccccccccccccccc", macho_file.read(16)))

        if self.arch == 32:
            self.addr, self.size = unpack('<II', macho_file.read(2*4))
        else:
            self.addr, self.size = unpack('<QQ', macho_file.read(8*2))

        self.offset, self.align, self.reloff, self.nreloc = unpack('<IIII', macho_file.read(4*4))
        self.flags, self.reserved1, self.reserved2 = unpack('<III', macho_file.read(3*4))

        if self.arch == 64:
            self.reserved3 = unpack('<I', macho_file.read(4))[0]
