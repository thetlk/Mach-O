#!/usr/bin/env python
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

import argparse
from pymacho.MachO import MachO

def main():
    parser = argparse.ArgumentParser(description="Read Mach-O file")
    parser.add_argument('filename', help='Mach-O file to parse and print')
    parser.add_argument('--headers', '-hd', help='show informations about header', action='store_true')
    parser.add_argument('--verbose', '-v', help='display many informations', action='store_true')
    args = parser.parse_args()
    
    m = MachO(args.filename)
    if args.headers:
        print "[*] Headers :"
        print "\t[+] magic : 0x%x %s" % (m.header.magic, "- " + m.header.display_magic() if args.verbose else "")
        print "\t[+] cputype : 0x%x %s" % (m.header.cputype, "- " + m.header.display_cputype() if args.verbose else "")
        print "\t[+] cpusubtype : 0x%s" % (m.header.cpusubtype)
        print "\t[+] filetype : 0x%x %s" % (m.header.filetype, "- " + m.header.display_filetype() if args.verbose else "")
        print "\t[+] ncmds : %d" % (m.header.ncmds)
        print "\t[+] sizeofcmds : %d byte%s" % (m.header.sizeofcmds, "s" if m.header.sizeofcmds > 1 else "")
        print "\t[+] flags : 0x%x %s" % (m.header.flags, "- " + ", ".join(m.header.display_flags()) if args.verbose else "")
        if m.header.is_64():
            print "\t[+] reserved : 0x%x" % (m.header.reserved)


if __name__ == '__main__':
    main()

