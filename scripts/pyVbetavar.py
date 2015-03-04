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
__version__ = '0.0.8'
_scriptname = 'pyVbetavar'
_verdata = 'Mar 2015'
_devflag = True


def swmode(sheet, dfsheet, size):
    """Apply sliding window to sheet."""
    A = dfsheet
    _Asum = A.sum(axis=0)
    for column in A.columns:
        A.loc[:, column] = A.loc[:, column].div(_Asum[column])
    _Amean = A.mean(axis=1)
    A['mean'] = _Amean
    A.sort(columns='mean', axis=0, ascending=False, inplace=True)
    A.drop('mean', axis=1, inplace=True)
    with pd.ExcelWriter('sw_mode_' + str(size) + 't_' + sheet +
                        '.xlsx') as writer:
        columnas = A.columns  # store columns names
        A.index.name = ''
        for i in range(len(columnas) - size + 1):
            A.to_excel(excel_writer=writer,
                       sheet_name='set_' + str(i + 1),
                       columns=columnas[i:i + size])


def sigma_auth(xl_file):
    """ Process sheets of XLSX file to calculate sigma.

    NOTE: Skip sheets starting by underscore."""
    df_mean = pd.DataFrame()
    df_std = pd.DataFrame()
    dfs = {sheet: xl_file.parse(sheet, index_col=0)
           for sheet in xl_file.sheet_names if (sheet[0] != '_')}
    print('> Processing sheets')
    for sheet in dfs:
        A = dfs[sheet]
        _Amean = A.mean(axis=1)
        _Astd = A.std(axis=1)
        df_mean[sheet] = _Amean
        df_std[sheet] = _Astd
    df_mean.sort_index(axis=1, inplace=True)
    df_std.sort_index(axis=1, inplace=True)
    with pd.ExcelWriter('variance_mean.xlsx') as writer:
        df_mean.to_excel(excel_writer=writer, sheet_name='average')
        df_std.to_excel(excel_writer=writer, sheet_name='std_dev')


def sw_authomatic_mode(xl_file):
    """Process sheets of XLSX file.

    NOTE: Skip sheets starting by underscore."""
    dfs = {sheet: xl_file.parse(sheet, index_col=0)
           for sheet in xl_file.sheet_names if (sheet[0] != '_')}
    for sheet in dfs:
        print('> Processing sheet', sheet, '... ', end='')
        sys.stdout.flush()
        try:
            swmode(sheet, dfs[sheet], wind_size)
        except (IndexError):
            print('\033[91m \t ERROR! \033[0m Window too wide!')
        except:
            print('\033[91m \t ERROR! \033[0m')
            raise
        else:
            print('\033[92m \t OK! \033[0m')


def sw_interactive_mode(xl_file):
    """Allows to select sheets to process

    NOTE: Skip sheet starting by underscore"""
    dfs = {sheet: xl_file.parse(sheet, index_col=0)
           for sheet in xl_file.sheet_names if (sheet[0] != '_')}
    print("Which one do you want to process: ")
    sheet_list = list(dfs.keys())
    for sheet in sheet_list:
        print(sheet, "\t", "[" + str(sheet_list.index(sheet)) + "]")
    num_sheet = input("Select the sheet: ")
    try:
        swmode(sheet_list[int(num_sheet)],
               dfs[sheet_list[int(num_sheet)]], wind_size)
    except (IndexError):
        print('> Processing sheet', sheet_list[int(num_sheet)],
              '...', '\033[91m \t ERROR! \033[0m Window too wide!')
    except:
        print('> Processing sheet', sheet_list[int(num_sheet)],
              '...', '\033[91m \t ERROR! \033[0m')
        raise
    else:
        print('> Processing sheet', sheet_list[int(num_sheet)],
              '...', '\033[92m \t OK! \033[0m')


# Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument(
    '-V', '--version',
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
    '-w', '--window',
    help='set the window size',
    type=int,
    default=5
)
parser.add_argument(
    '-a', '--automatic',
    action='store_true',
    help='automatic mode',
)
parser.add_argument(
    '-s', '--sheets',
    action='store_true',
    help='select sheets to process',
)
parser.add_argument(
    '-d', '--variance',
    action='store_true',
    help='sigma and mean of every sheet',
)
args = parser.parse_args()
file_name = args.input
wind_size = args.window


# Program Header
print('\n=-= ' + _scriptname + ' =-= v' + __version__ + ' =-= ' +
      _verdata + ' =-= by DLS team =-=')
if(_devflag):
    print('\n>>> WARNING! THIS IS JUST A DEVELOPMENT SUBRELEASE.' +
          ' USE IT AT YOUR OWN RISK!\n')

# slow swmode version (as R script)
xl_file = pd.ExcelFile(file_name)

if args.authomatic:
    sw_authomatic_mode(xl_file)
elif args.sheets:
    sw_interactive_mode(xl_file)
elif args.variance:
    sigma_auth(xl_file)

print()
