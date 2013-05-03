# encoding: utf-8

from struct import unpack


class MachOSymtabCommand(object):

    symoff = 0
    nsyms = 0
    stroff = 0
    strsize = 0

    def __init__(self, macho_file=None):
        if macho_file is not None:
            self.parse(macho_file)

    def parse(self, macho_file):
        self.symoff, self.nsyms = unpack('<II', macho_file.read(4*2))
        self.stroff, self.strsize = unpack('<II', macho_file.read(4*2))
