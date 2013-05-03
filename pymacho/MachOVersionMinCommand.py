# encoding: utf-8

from struct import unpack


class MachOVersionMinCommand(object):

    version = 0
    reserved = 0

    def __init__(self, macho_file=None):
        if macho_file is not None:
            self.parse(macho_file)

    def parse(self, macho_file):
        self.version, self.reserved = unpack('<II', macho_file.read(4*2))
