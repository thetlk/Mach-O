# encoding: utf-8

from struct import unpack


class MachOLinkeditDataCommand(object):

    dataoff = 0
    datasize = 0

    def __init__(self, macho_file=None):
        if macho_file is not None:
            self.parse(macho_file)

    def parse(self, macho_file):
        self.dataoff, self.datasize = unpack('<II', macho_file.read(4*2))
