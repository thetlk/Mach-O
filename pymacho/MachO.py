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

class MachO(object):
    """
    Represent a Mach-O file
    """
    
    def __init__(self, filename):
        with open(filename, "rb") as macho_file:
            self.load_file(macho_file)
            
    def load_file(self, macho_file):
        self.header = MachOHeader(macho_file)

