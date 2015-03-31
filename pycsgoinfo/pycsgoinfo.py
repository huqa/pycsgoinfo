# -*- coding: utf-8 -*-


"""pycsgoinfo.pycsgoinfo: provides entry point main()."""

__version__ = "0.2.0"

import sys, os
from .parser import Parser


def main():
    print("pycsgoinfo version %s." % __version__)
    arg = sys.argv[1]
    print("List of argument strings: %s" % arg)
    parser = Parser(arg)
