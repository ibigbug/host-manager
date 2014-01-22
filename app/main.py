#!/usr/bin/env python

from __future__ import print_function

import sys

from manager import HostManager

def main():
    if len(sys.argv) < 2:
        print('Usage: host-gen [config_file_path]')
        sys.exit(0)
    config = sys.argv[1]
    M = HostManager(config)
    M.run()


if __name__ == '__main__':
    main()
