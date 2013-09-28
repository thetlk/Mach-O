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


class MachODYSymtabCommand(object):

    ilocalsym = 0
    nlocalsym = 0
    iextdefsym = 0
    nextdefsym = 0
    iundefsym = 0
    nundefsym = 0
    tocoff = 0
    ntoc = 0
    modtaboff = 0
    nmodtab = 0
    extrefsymoff = 0
    nextrefsym = 0
    indirectsymoff = 0
    nindirectsyms = 0
    extreloff = 0
    nextrel = 0
    locreloff = 0
    nlocrel = 0

    def __init__(self, macho_file=None):
        if macho_file is not None:
            self.parse(macho_file)

    def parse(self, macho_file):
        self.ilocalsym, self.nlocalsym = unpack('<II', macho_file.read(4*2))
        self.iextdefsym, self.nextdefsym = unpack('<II', macho_file.read(4*2))
        self.iundefsym, self.nundefsym = unpack('<II', macho_file.read(4*2))
        self.tocoff, self.ntoc = unpack('<II', macho_file.read(4*2))
        self.modtaboff, self.nmodtab = unpack('<II', macho_file.read(4*2))
        self.extrefsymoff, self.nextrefsym = unpack('<II', macho_file.read(4*2))
        self.indirectsymoff, self.nindirectsyms = unpack('<II', macho_file.read(4*2))
        self.extreloff, self.nextrel = unpack('<II', macho_file.read(4*2))
        self.locreloff, self.nlocrel = unpack('<II', macho_file.read(4*2))
