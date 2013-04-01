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

class MachOHeader(object):
    """
    Represent a Mach-O Header
    """
    
    def __init__(self, macho_file):
        self.parse_header(macho_file)
        
    def parse_header(self, macho_file):
        assert macho_file.tell() == 0
        magic, cputype, cpusubtype, filetype, ncmds, sizeofcmds, flags = unpack("<IIIIIII", macho_file.read(4*7))
        