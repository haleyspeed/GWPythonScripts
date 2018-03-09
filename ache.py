


import os
import pandas as pd
import csv
import numpy as np
import scipy as sp
import scipy.stats


# Assign Variables
file_in = 'delayed.csv'
dir_in = 'D:\\Dropbox\\Sync Data Analysis Computers\\Gulf War Project\\Statistics\\Final Spreadsheets'
os.chdir(dir_in)
data = pd.read_csv(file_in)
treatment1 = 'oil'
treatment2 = 'cpf'
factor1 = 'group'
factor2 = 'region'
measurement1 = 'activity'
measurement2 = 'normalized'
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
	for index, row in data.iterrows():	
		if treatment1 in row[factor1] and row[factor2] == 'hippocampus':
			n1 = n1 + 1
		elif treatment2 in row[factor1] and row[factor2] == 'hippocampus':
			n2 = n2 + 1
	for index, row in data.iterrows():
		if treatment1 in row[factor1]:
			data.loc[index:index:,'n'] = n1
		elif treatment2 in row[factor1]:
			data.loc[index:index:, 'n'] = n2

# Calculates descriptive stats 
def get_desc (data, factor1, factor2, measurement1, measurement1_std, measurement1_ste, measurement2, measurement2_std, measurement2_ste):
	stats = data.groupby([factor1,factor2]).mean()
	stats_std = data.groupby([factor1,factor2]).std()
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
	stats = stats[[factor1, 'n', factor2, measurement1, measurement1_ste,measurement1_std, lconf1, hconf1, measurement2, measurement2_ste, measurement2_std, lconf2, hconf2 ]]
	return stats	



# Get n
get_n (data)

# Calculate stats per mouse
mouse_stats = get_desc (data, factor1, factor2, measurement1, measurement1_std, measurement1_ste, measurement2, measurement2_std, measurement2_ste)


# Sets up output directory and files
file_out = file_in.replace('.csv', '')
mouse_stats_out = file_out + '_analyzed.csv'
dir_out = dir_in + '\\analyzed'
try:
    os.stat(dir_out)
except:
    os.mkdir(dir_out)

# Write data to file
os.chdir(dir_out)
mouse_stats.to_csv(mouse_stats_out, index = False)



