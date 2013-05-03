# encoding: utf-8

from struct import unpack


class MachODYLinkerCommand(object):

    offset = 0
    path = ""

    def __init__(self, macho_file=None):
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
