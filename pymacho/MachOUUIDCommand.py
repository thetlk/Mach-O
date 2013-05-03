# encoding: utf-8

from struct import unpack


class MachOUUIDCommand(object):

    uuid = ()

    def __init__(self, macho_file=None):
        if macho_file is not None:
            self.parse(macho_file)

    def parse(self, macho_file):
        self.uuid = unpack("<BBBBBBBBBBBBBBBB", macho_file.read(16))
