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
from pymacho.MachOSegment import MachOSegment
from pymacho.MachODYLDInfoCommand import MachODYLDInfoCommand
from pymacho.MachOSymtabCommand import MachOSymtabCommand
from pymacho.MachODYSymtabCommand import MachODYSymtabCommand
from pymacho.MachODYLinkerCommand import MachODYLinkerCommand
from pymacho.MachOUUIDCommand import MachOUUIDCommand
from pymacho.Constants import *


class MachO(object):
    """
    Represent a Mach-O file
    """

    header = MachOHeader()
    segments = []
    commands = []

    def __init__(self, filename=None):
        if filename is not None:
            with open(filename, "rb") as macho_file:
                self.load_file(macho_file)

    def load_file(self, macho_file):
        self.header = MachOHeader(macho_file)
        self.load_commands(macho_file)

    def load_commands(self, macho_file):
        assert macho_file.tell() == 28 or macho_file.tell() == 32
        for i in range(self.header.ncmds):
            cmd, cmdsize = unpack('<II', macho_file.read(4*2))
            if cmd == LC_SEGMENT:
                self.segments.append(MachOSegment(macho_file))
            elif cmd == LC_SEGMENT_64:
                self.segments.append(MachOSegment(macho_file, arch=64))
            elif cmd == LC_DYLD_INFO_ONLY or cmd == LC_DYLD_INFO:
                self.commands.append(MachODYLDInfoCommand(macho_file))
            elif cmd == LC_SYMTAB:
                self.commands.append(MachOSymtabCommand(macho_file))
            elif cmd == LC_DYSYMTAB:
                self.commands.append(MachODYSymtabCommand(macho_file))
            elif cmd == LC_LOAD_DYLINKER:
                self.commands.append(MachODYLinkerCommand(macho_file))
            elif cmd == LC_UUID:
                self.commands.append(MachOUUIDCommand(macho_file))
            else:
                print "unknow load cmd : %x" % cmd
                return
