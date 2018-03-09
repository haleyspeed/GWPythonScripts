


import os
import pandas as pd
import csv
import numpy as np


file_in = 'mepsc_cunulative.csv'
dir_in = 'D:\\Dropbox\\Sync Data Analysis Computers\\Gulf War Project\\Statistics\\Final Spreadsheets'

os.chdir(dir_in)
data = pd.read_csv(file_in)

treatment1 = 'oil_saline'
treatment2 = 'oil_igf'
treatment3 = 'cpf_saline'
treatment4 = 'cpf_igf'
factor1 = 'group'
measurement1 = 'amp'
measurement2 = 'freq'
measurement1_std = measurement1 + '_std'
measurement1_ste = measurement1 + '_ste'
measurement2_std = measurement2 + '_std'
measurement2_ste = measurement2 + '_ste'

# Calculates n Per Slice

n1 = 0
n2 = 0
n3 = 0
n4 = 0

for index, row in data.iterrows():
	
	if treatment1 in row[factor1]:
		n1 = n1 + 1
	elif treatment2 in row[factor1]:
		n2 = n2 + 1
	elif treatment3 in row[factor1]:
		n3 = n3 + 1  
	elif treatment4 in row[factor1]:
		n4 = n4 + 1  
		
for index, row in data.iterrows():
	if treatment1 in row[factor1]:
		data.loc[index:index:,'n'] = n1
	elif treatment2 in row[factor1]:
		data.loc[index:index:, 'n'] = n2
	elif treatment3 in row[factor1]:
		data.loc[index:index:, 'n'] = n3
	elif treatment4 in row[factor1]:
		data.loc[index:index:, 'n'] = n4


# Makes a row for mouse id for mouse_stats calculations

f = lambda x: x['mouse'].split(" ")
data['mouse_id'] = data.apply(f, axis = 1)
data['mouse_id'] = data['mouse_id'].str[0]



# Calculates descriptive stats per slice

cell_stats = data.groupby([factor1]).mean()
cell_stats_std = data.groupby([factor1]).std()

cell_stats = cell_stats.reset_index()
cell_stats_std = cell_stats_std.reset_index()

cell_stats[measurement1_std] = cell_stats_std[measurement1]
cell_stats[measurement1_ste] = cell_stats[measurement1_std]/np.sqrt(cell_stats['n'])
cell_stats[measurement2_std] = cell_stats_std[measurement2]
cell_stats[measurement2_ste] = cell_stats[measurement2_std]/np.sqrt(cell_stats['n'])


# Calculates data per mouse

per_mouse = data.groupby(['mouse_id',factor1]).mean()
per_mouse = per_mouse.reset_index()
per_mouse = per_mouse.sort_values([factor1, 'mouse_id'], axis = 0)


# Calculates n Per Slice

n1 = 0
n2 = 0
n3 = 0
n4 = 0

for index, row in per_mouse.iterrows():
	
	if treatment1 in row[factor1]:
		n1 = n1 + 1
	elif treatment2 in row[factor1]:
		n2 = n2 + 1
	elif treatment3 in row[factor1]:
		n3 = n3 + 1  
	elif treatment4 in row[factor1]:
		n4 = n4 + 1  
		
for index, row in per_mouse.iterrows():
	if treatment1 in row[factor1]:
		per_mouse.loc[index:index:,'n'] = n1
	elif treatment2 in row[factor1]:
		per_mouse.loc[index:index:, 'n'] = n2
	elif treatment3 in row[factor1]:
		per_mouse.loc[index:index:, 'n'] = n3
	elif treatment4 in row[factor1]:
		per_mouse.loc[index:index:, 'n'] = n4
		
		
# Calculates stats per mouse
mouse_stats = per_mouse.groupby([factor1]).mean()
mouse_stats_std = per_mouse.groupby([factor1]).std()

mouse_stats = mouse_stats.reset_index()
mouse_stats_std = mouse_stats_std.reset_index()

mouse_stats[measurement1_std] = mouse_stats_std[measurement1]
mouse_stats[measurement1_ste] = mouse_stats[measurement1_std]/np.sqrt(mouse_stats['n'])
mouse_stats[measurement2_std] = mouse_stats_std[measurement2]
mouse_stats[measurement2_ste] = mouse_stats[measurement2_std]/np.sqrt(mouse_stats['n'])

mouse_stats = mouse_stats.sort_values(factor1, axis = 0)


# Sets up output directory and files
file_out = file_in.replace('.csv', '')
cell_stats_out = file_out + '_analyzed.csv'
per_mouse_out = file_out + '_per_mouse.csv'
mouse_stats_out = file_out + '_per_mouse_analyzed.csv'
dir_out = dir_in + '\\analyzed'

try:
    os.stat(dir_out)
except:
    os.mkdir(dir_out)

# Write data to file
os.chdir(dir_out)
cell_stats.to_csv(cell_stats_out, index = False)
per_mouse.to_csv(per_mouse_out, index = False)
mouse_stats.to_csv(mouse_stats_out, index = False)