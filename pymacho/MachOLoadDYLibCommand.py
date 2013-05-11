# encoding: utf-8

from struct import unpack


class MachOLoadDYLibCommand(object):

    name = ""
    name_offset = 0
    timestamp = 0
    current_version = 0
    compatibility_version = 0

    def __init__(self, macho_file=None):
        if macho_file is not None:
            self.parse(macho_file)

    def parse(self, macho_file):
        # get cmdsize
        macho_file.seek(-4, 1)
        cmdsize = unpack('<I', macho_file.read(4))[0]
        # get the offset of string
        self.name_offset = unpack('<I', macho_file.read(4))[0]
        self.timestamp = unpack('<I', macho_file.read(4))[0]
        self.current_version = unpack('<I', macho_file.read(4))[0]
        self.compatibility_version = unpack('<I', macho_file.read(4))[0]
        # get string
        strlen = cmdsize - self.name_offset
        extract = "<%s" % ('s'*strlen)
        self.name = "".join(char if char != "\x00" else "" for char in unpack(extract, macho_file.read(strlen)))
