


import os
import pandas as pd
import csv
import numpy as np
import scipy as sp
import scipy.stats


file_in = 'mepsc_cunulative.csv'
dir_in = 'D:\\Dropbox\\Sync Data Analysis Computers\\Gulf War Project\\Statistics\\Final Spreadsheets'

os.chdir(dir_in)
data = pd.read_csv(file_in)

treatment1 = 'oil_saline'
treatment2 = 'cpf_saline'
treatment3 = 'cpf_igf'
factor1 = 'group'
measurement1 = 'amp'
measurement2 = 'freq'
measurement1_std = measurement1 + '_std'
measurement1_ste = measurement1 + '_ste'
measurement2_std = measurement2 + '_std'
measurement2_ste = measurement2 + '_ste'
confidence = 0.95
lconf1 = measurement1 + '_5%'
hconf1 = measurement1 + '_95%'
lconf2 = measurement2 + '_5%'
hconf2 = measurement2 + '_95%'

# Calculates n 
def get_n (data):
	n1 = 0
	n2 = 0
	n3 = 0
	for index, row in data.iterrows():
	
		if treatment1 in row[factor1]:
			n1 = n1 + 1
		elif treatment2 in row[factor1]:
			n2 = n2 + 1
		elif treatment3 in row[factor1]:
			n3 = n3 + 1  	
	for index, row in data.iterrows():
		if treatment1 in row[factor1]:
			data.loc[index:index:,'n'] = n1
		elif treatment2 in row[factor1]:
			data.loc[index:index:, 'n'] = n2
		elif treatment3 in row[factor1]:
			data.loc[index:index:, 'n'] = n3

# Calculates descriptive stats 
def get_desc (data, factor1, measurement1, measurement1_std, measurement1_ste, measurement2, measurement2_std, measurement2_ste):
	stats = data.groupby([factor1]).mean()
	stats_std = data.groupby([factor1]).std()
	stats = stats.reset_index()
	stats_std = stats_std.reset_index()
	stats[measurement1_std] = stats_std[measurement1]
	stats[measurement1_ste] = stats[measurement1_std]/np.sqrt(stats['n'])
	stats[measurement2_std] = stats_std[measurement2]
	stats[measurement2_ste] = stats[measurement2_std]/np.sqrt(stats['n'])
	stats['conf1'] = stats[measurement1_ste] * sp.stats.t._ppf((1+confidence)/2., stats['n']-1)
	stats[lconf1] = stats[measurement1] - stats['conf1']
	stats[hconf1] = stats[measurement1] + stats['conf1']
	stats['conf2'] = stats[measurement1_ste] * sp.stats.t._ppf((1+confidence)/2., stats['n']-1)
	stats[lconf2] = stats[measurement2] - stats['conf2']
	stats[hconf2] = stats[measurement2] + stats['conf2']
	stats = stats[[factor1, 'n', measurement1, measurement1_ste,measurement1_std, lconf1, hconf1, measurement2, measurement2_ste, measurement2_std, lconf2, hconf2 ]]
	return stats	


# Get n per slice
get_n (data)
			
# Makes a row for mouse id for mouse_stats calculations
f = lambda x: x['mouse'].split(".")
data['mouse_id'] = data.apply(f, axis = 1)
data['mouse_id'] = data['mouse_id'].str[0]

# Calculate stats per slice
slice_stats = get_desc (data, factor1, measurement1, measurement1_std, measurement1_ste, measurement2, measurement2_std, measurement2_ste)

# Calculates data per mouse
per_mouse = data.groupby(['mouse_id',factor1]).mean()
per_mouse = per_mouse.reset_index()
per_mouse = per_mouse[['mouse_id', factor1, 'n', measurement2, measurement1]] 

# Calculates n per mouse
get_n (per_mouse)

# Calculates stats per mouse
mouse_stats = get_desc (per_mouse, factor1,measurement1, measurement1_std, measurement1_ste, measurement2, measurement2_std, measurement2_ste)

# Sets up output directory and files
file_out = file_in.replace('.csv', '')
slice_stats_out = file_out + '_analyzed.csv'
per_mouse_out = file_out + '_per_mouse.csv'
mouse_stats_out = file_out + '_per_mouse_analyzed.csv'
dir_out = dir_in + '\\analyzed'

try:
    os.stat(dir_out)
except:
    os.mkdir(dir_out)

# Write data to file
os.chdir(dir_out)
slice_stats.to_csv(slice_stats_out, index = False)
per_mouse.to_csv(per_mouse_out, index = False)
mouse_stats.to_csv(mouse_stats_out, index = False)

