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

class MachOHeader(object):
    """
    Represent a Mach-O Header
    
    struct mach_header
    {
        uint32_t magic;
        cpu_type_t cputype;
        cpu_subtype_t cpusubtype;
        uint32_t filetype;
        uint32_t ncmds;
        uint32_t sizeofcmds;
        uint32_t flags;
    };
    
    struct mach_header_64
    {
        uint32_t magic;
        cpu_type_t cputype;
        cpu_subtype_t cpusubtype;
        uint32_t filetype;
        uint32_t ncmds;
        uint32_t sizeofcmds;
        uint32_t flags;
        uint32_t reserved;
    };
    
    """
    
    def __init__(self, macho_file):
        self.parse_header(macho_file)
        
    def parse_header(self, macho_file):
        assert macho_file.tell() == 0
        self.magic, self.cputype, self.cpusubtype, self.filetype = unpack("<IIII", macho_file.read(4*4))
        self.ncmds, self.sizeofcmds, self.flags = unpack('<III', macho_file.read(4*3))
        if self.is_64() is True:
            unpack('<I', macho_file.read(4)) #  uint32_t reserved on mac_header_64
        
    def is_64(self):
        return (self.magic == MH_MAGIC_64 or self.magic == MH_CIGAM_64)
        