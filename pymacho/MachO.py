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
from pymacho.MachOHeader import MachOHeader
from pymacho.Constants import *

class MachO(object):
    """
    Represent a Mach-O file
    """
    
    def __init__(self, filename):
        with open(filename, "rb") as macho_file:
            self.load_file(macho_file)
            
    def load_file(self, macho_file):
        self.header = MachOHeader(macho_file)
        self.load_commands(macho_file)

    def load_commands(self, macho_file):
        assert macho_file.tell() == 28 or macho_file.tell() == 32 # 32 or 64 bits (reserved field)
        self.segments = []
        for i in range(self.header.ncmds):
            cmd, cmdsize = unpack('<II', macho_file.read(4*2))
            if cmd == LC_SEGMENT:
                segname = "".join(char if char != "\x00" else "" for char in unpack("<cccccccccccccccc", macho_file.read(16)))
                vmaddr, vmsize, fileoff, filesize = unpack('<IIII', macho_file.read(4*4))
                maxprot, initprot, nsects, flags = unpack('<IIII', macho_file.read(4*4))
                sections = []
                for i in range(nsects):
                    sectname = "".join(char if char != "\x00" else "" for char in unpack("<cccccccccccccccc", macho_file.read(16)))
                    sec_segname = "".join(char if char != "\x00" else "" for char in unpack("<cccccccccccccccc", macho_file.read(16)))
                    addr, size, offset, align = unpack('<IIII', macho_file.read(4*4))
                    reloff, nreloc, flags, reserved1 = unpack('<IIII', macho_file.read(4*4))
                    reserved2 = unpack('<I', macho_file.read(4))[0]
                    sections.append((sectname, sec_segname, addr, size, offset, align, reloff, nreloc, flags, reserved1, reserved2))
                self.segments.append((segname, vmaddr, vmsize, fileoff, filesize, maxprot, initprot, nsects, flags, sections))
            elif cmd == LC_SEGMENT_64:
                segname = "".join(char if char != "\x00" else "" for char in unpack("<cccccccccccccccc", macho_file.read(16)))
                vmaddr, vmsize, fileoff, filesize = unpack('<QQQQ', macho_file.read(8*4))
                maxprot, initprot, nsects, flags = unpack('<IIII', macho_file.read(4*4))
                sections = []
                for i in range(nsects):
                    sectname = "".join(char if char != "\x00" else "" for char in unpack("<cccccccccccccccc", macho_file.read(16)))
                    sec_segname = "".join(char if char != "\x00" else "" for char in unpack("<cccccccccccccccc", macho_file.read(16)))
                    addr, size = unpack('<QQ', macho_file.read(8*2))
                    offset, align, reloff, nreloc = unpack('<IIII', macho_file.read(4*4))
                    flags, reserved1, reserved2, reserved3 = unpack('<IIII', macho_file.read(4*4))
                    sections.append((sectname, sec_segname, addr, size, offset, align, reloff, nreloc, flags, reserved1, reserved2, reserved3))
                self.segments.append((segname, vmaddr, vmsize, fileoff, filesize, maxprot, initprot, nsects, flags, sections))
            elif cmd == LC_DYLD_INFO_ONLY:
                rebase_off, rebase_size, bind_off, bind_size = unpack('<IIII', macho_file.read(4*4))
                weak_bind_off, weak_bind_size, lazy_bind_off, lazy_bind_size = unpack('<IIII', macho_file.read(4*4))
                export_off, export_size = unpack('<II', macho_file.read(2*4))
            elif cmd == LC_SYMTAB:
                symoff, nsyms, stroff, strsize = unpack('<IIII', macho_file.read(4*4))
                self.symboltable = (symoff, nsyms, stroff, strsize)
            else:
                print "unknow load cmd : %x" % cmd
                return
