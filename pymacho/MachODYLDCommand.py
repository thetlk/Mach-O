# encoding: utf-8

from struct import unpack


class MachODYLDCommand(object):

    rebase_off = 0
    rebase_size = 0
    bind_off = 0
    bind_size = 0
    weak_bind_off = 0
    weak_bind_size = 0
    lazy_bind_off = 0
    lazy_bind_size = 0
    export_off = 0
    export_size = 0

    def __init__(self, macho_file=None):
        if macho_file is not None:
            self.parse(macho_file)

    def parse(self, macho_file):
        self.rebase_off, self.rebase_size, self.bind_off, self.bind_size = unpack('<IIII', macho_file.read(4*4))
        self.weak_bind_off, self.weak_bind_size, self.lazy_bind_off, self.lazy_bind_size = unpack('<IIII', macho_file.read(4*4))
        self.export_off, self.export_size = unpack('<II', macho_file.read(2*4))
