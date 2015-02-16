#!/usr/bin/env python3
#
# PEP8 compliant
#
# Module configuration recommended for SOM:
# module purge; module load gcc/gcc-4.9.0 python/3.4.0

# Python2 compatibility
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
try:
    input = raw_input
except NameError:
    pass

# Packages
import sys
import argparse
import pandas as pd

# Release information
__version__ = '0.0.4'
_scriptname = 'sl_mode'
_verdata = 'Feb 2015'
_devflag = True


def slmode(sheet, dfsheet, size):
    """Apply sliding window to sheet."""
    with pd.ExcelWriter('sw_mode_' + str(size) + 't_' + sheet +
                        '.xlsx') as writer:
        columnas = dfsheet.columns  # store columns names
        dfsheet.index.name = ''
        for i in range(len(columnas)-size+1):
            dfsheet.to_excel(excel_writer=writer,
                             sheet_name='set_' + str(i+1),
                             columns=columnas[i:i+size])


def sw_authomatic_mode(xl_file):
    """Process sheets of XLSX file.

    NOTE: Skip sheets starting by underscore."""
    dfs = {sheet: xl_file.parse(sheet, index_col=0)
           for sheet in xl_file.sheet_names if (sheet[0] != '_')}
    for sheet in dfs:
        print('> Processing sheet', sheet, '... ', end='')
        sys.stdout.flush()
        try:
            slmode(sheet, dfs[sheet], wind_size)
        except (IndexError):
            print('\033[91m ERROR! \033[0m Window too wide!')
        except:
            print('\033[91m ERROR! \033[0m')
            raise
        else:
            print('\033[92m OK! \033[0m')

# lets select which sheets we want to process

def sw_interactive_mode(xl_file):
    """Allows to select sheets to process

    NOTE: Skip sheet starting by underscore"""
    dfs = {sheet: xl_file.parse(sheet, index_col=0)
           for sheet in xl_file.sheet_names if (sheet[0] != '_')}
    print("Which one do you want to process: ")
    sheet_list = list(dfs.keys())
    for sheet in sheet_list:
        print(sheet, "\t", "[" + str(sheet_list.index(sheet)) + "]")
    algo = input("Select the sheet: ")
    print(algo)


# Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument(
    '-v', '--version',
    action='version',
    version=_scriptname + '.py ver. ' + __version__ + ' - ' + _verdata
)
parser.add_argument(
    '-i', '--input',
    help='input file',
    metavar='FILE.XLSX',
    type=str,
    required=True
)
parser.add_argument(
    '-s', '--size',
    help='set the window size',
    type=int,
    default=5
)
args = parser.parse_args()
file_name = args.input
wind_size = args.size

# Program Header
print('\n=-= ' + _scriptname + ' =-= v' + __version__ + ' =-= ' +
      _verdata + ' =-= by DLS team =-=')
if(_devflag):
    print('\n>>> WARNING! THIS IS JUST A DEVELOPMENT SUBRELEASE.' +
          ' USE IT AT YOUR OWN RISK!\n')

# slow slmode version (as R script)
xl_file = pd.ExcelFile(file_name)
sw_authomatic_mode(xl_file)
print()
