# encoding: utf-8

from struct import unpack


class MachODYLinkerCommand(object):

    path = ""

    def __init__(self, macho_file=None):
        if macho_file is not None:
            self.parse(macho_file)

    def parse(self, macho_file):
        # get the offset
        macho_file.seek(-4, 1)
        cmdsize = unpack('<II', macho_file.read(8))[0]
        # get the string
        strlen = cmdsize - 12
        extract = "<%s" % ('s'*strlen)
        self.path = "".join(char if char != "\x00" else "" for char in unpack(extract, macho_file.read(strlen)))
