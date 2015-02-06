#!/usr/bin/python
# module load gcc/gcc-4.8.0
# module load python/2.7.5

import pandas as pd 
from pandas import ExcelWriter
import argparse

# py_slidingWindow_xlsx release information
__version__ = '0.0.3'
_verdata = 'Feb 2015'
_devflag = True


#########################################################################> MAIN

# Program Header
print('\n=-= py_slidingWindow_xlsx =-= v' + __version__ + ' =-= ' +
      _verdata + ' =-= by DLS team =-=')
if(_devflag): 
    print('\n>>> WARNING! THIS IS JUST A DEVELOPMENT SUBRELEASE.' + 
          ' USE IT AT YOUR OWN RISK!')  


# flags
parser = argparse.ArgumentParser()
parser.add_argument('-i','-input', help="input file", type=str)
parser.add_argument('-s', '-size', help='set the window size', 
	type=int, default=5)
args = parser.parse_args()


file_name = args.i
xl_file = pd.ExcelFile(file_name)
dfs = {sheet_name: xl_file.parse(sheet_name)
	for sheet_name in xl_file.sheet_names}

# slow slmode version (as R script)

def slmode(sheet, size):
	writer = ExcelWriter("sw_mode_" + str(size) + "t_" + 
		sheet + ".xlsx")
	columnas = dfs[str(sheet)].columns # store columns names
	length = len(dfs[str(sheet)].columns)
	new_df = pd.DataFrame(dfs[str(sheet)].iloc[:,0])
	for i in range(1,length-(size-1)):
		for j in range(0,(size)):
			new_df[str(columnas[j+i])] = dfs[str(sheet)].iloc[:,j+i]
		new_df.to_excel(writer,"set_" + str(i), index=False)
		new_df = pd.DataFrame(dfs[str(sheet)].iloc[:,0])
	writer.save()

def sw_authomatic_mode():
	sheets = xl_file.sheet_names
	for name in sheets:
		print "processing sheet", name
		slmode(name, args.s)
		print name, "finished!"

sw_authomatic_mode()

