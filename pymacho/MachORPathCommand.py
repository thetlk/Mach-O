# encoding: utf-8

from struct import unpack


class MachORPathCommand(object):

    path_offset = 0
    path = ""

    def __init__(self, macho_file=None):
        if macho_file is not None:
            self.parse(macho_file)

    def parse(self, macho_file):
        # get cmdsize
        macho_file.seek(-4, 1)
        cmdsize = unpack('<I', macho_file.read(4))[0]
        # get string offset
        self.path_offset = unpack('<I', macho_file.read(4))[0]
        strlen = cmdsize - self.path_offset
        # get path
        extract = "<%s" % ('s'*strlen)
        self.path = "".join(char if char != "\x00" else "" for char in unpack(extract, macho_file.read(strlen)))
