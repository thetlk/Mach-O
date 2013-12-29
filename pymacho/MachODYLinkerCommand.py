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
from pymacho.MachOLoadCommand import MachOLoadCommand
from pymacho.Constants import *


class MachODYLinkerCommand(MachOLoadCommand):

    offset = 0
    path = ""

    def __init__(self, macho_file=None, cmd=0):
        self.cmd = cmd
        if macho_file is not None:
            self.parse(macho_file)

    def parse(self, macho_file):
        # get the cmdsize
        macho_file.seek(-4, 1)
        cmdsize = unpack('<I', macho_file.read(4))[0]
        # get the offset
        self.offset = unpack('<I', macho_file.read(4))[0]
        # get the string
        strlen = cmdsize - self.offset
        extract = "<%s" % ('s'*strlen)
        self.path = "".join(char if char != "\x00" else "" for char in unpack(extract, macho_file.read(strlen)))

    def display(self, before=''):
        print before + "[+] %s" % ("LC_DYLD_ENVIRONMENT" if self.cmd == LC_DYLD_ENVIRONMENT else "LC_LOAD_DYLINKER")
        print before + "\t - path : %s" % self.path
