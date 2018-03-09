import os
import pandas as pd
import csv
import numpy as np
import scipy as sp
import scipy.stats

# Default values

file = 'apical_spines_100um.csv'
#dir = 'D:\\Dropbox\\Sync Data Analysis Computers\\Gulf War Project\\Statistics\\Final Spreadsheets\\'
dir = 'C:\\Users\\hspeed\\Dropbox\\Sync Data Analysis Computers\\Gulf War Project\\Statistics\\Final Spreadsheets\\'
factor = 'group'
treatment1 = 'oil_saline'
treatment2 = 'cpf_saline'
treatment3 = 'cpf_igf'
treatment3 = 'oil_igf'
confidence = 0.95

# Calculates n 
def get_n (data):
	n1 = 0
	n2 = 0
	n3 = 0
	n4 = 0
	for index, row in data.iterrows():
	
		if treatment1 in row[factor]:
			n1 = n1 + 1
		elif treatment2 in row[factor]:
			n2 = n2 + 1
		elif treatment3 in row[factor]:
			n3 = n3 + 1 
		elif treatment4 in row[factor]:
			n4 = n4 + 1  			
	for index, row in data.iterrows():
		if treatment1 in row[factor]:
			data.loc[index:index:,'n'] = n1
		elif treatment2 in row[factor]:
			data.loc[index:index:, 'n'] = n2
		elif treatment3 in row[factor]:
			data.loc[index:index:, 'n'] = n3
		elif treatment4 in row[factor]:
			data.loc[index:index:, 'n'] = n4	
def save_data (file, dir, measurement, df_out):
	file_out = file.replace('.csv', '')
	file_out = file_out + '_' + measurement + '_analyzed.csv'
	dir_out = dir + '\\analyzed' + '\\' + measurement
	try:
		os.stat(dir_out)
	except:
		os.mkdir(dir_out)
	os.chdir(dir_out)
	df_out.to_csv(file_out, index = False)
	os.chdir(dir)
	return dir_out
	
def save_mouse (file, dir, df_mouse):
	file_out = file + '.csv'
	try:
		os.stat(dir)
	except:
		os.mkdir(dir)
	os.chdir(dir)
	df_mouse.to_csv(file_out, index = False)
	os.chdir(dir)
	return dir
	

# Calculates descriptive stats 
def get_desc (file, dir, stats_mean, stats_std, factor, measurement, df_out):
	stats_mean['test'] = measurement
	stats_mean['std'] = stats_std[measurement]
	stats_mean['ste'] = stats_mean['std']/np.sqrt(stats_mean['n'])
	stats_mean['conf'] = stats_mean['ste'] * sp.stats.t._ppf((1+confidence)/2., stats_mean['n']-1)
	stats_mean['5% CI'] = stats_mean[measurement] - stats_mean['conf']
	stats_mean['95% CI'] = stats_mean[measurement] + stats_mean['conf']
	df = stats_mean[['test', factor, 'n', measurement, 'ste', 'std', '5% CI', '95% CI']]
	row1 = {'measurement':df.ix[0,0], factor:df.ix[0,1], 'n':df.ix[0,2], 'mean':df.ix[0,3], 'ste':df.ix[0,4], 'std':df.ix[0,5], '5% CI':df.ix[0,6], '95% CI':df.ix[0,7]}
	row2 = {'measurement':df.ix[1,0], factor:df.ix[1,1], 'n':df.ix[1,2], 'mean':df.ix[1,3], 'ste':df.ix[1,4], 'std':df.ix[1,5], '5% CI':df.ix[1,6], '95% CI':df.ix[1,7]}
	row3 = {'measurement':df.ix[2,0], factor:df.ix[2,1], 'n':df.ix[2,2], 'mean':df.ix[2,3], 'ste':df.ix[2,4], 'std':df.ix[2,5], '5% CI':df.ix[2,6], '95% CI':df.ix[2,7]}
	df_out = df_out.append(row1, ignore_index=True)
	df_out = df_out.append(row2, ignore_index=True)
	df_out = df_out.append(row3, ignore_index=True)
	df_out = df_out[['measurement', factor, 'n', 'mean', 'ste', 'std', '5% CI', '95% CI']]
	dir_out = save_data(file, dir, measurement, df_out) 
	return dir_out

# Import data from file
os.chdir(dir)
data = pd.read_csv(file)
	
# Get n per cell
get_n (data)
			
# Calculate stats per cell
df_out = pd.DataFrame({'measurement':[], factor:[], 'n':[], 'mean':[], 'ste':[], 'std':[], '5% CI':[], '95% CI':[]})
stats_mean = data.groupby([factor]).mean()
stats_std = data.groupby([factor]).std()
stats_mean = stats_mean.reset_index()
stats_std = stats_std.reset_index()
colnames = list(data)
for i in colnames:
	if i != 'mouse_id' and i != 'group':
		dir_out = get_desc(file, dir, stats_mean, stats_std, factor, i, df_out)

# Calculate stats per mouse
df_out = pd.DataFrame({'measurement':[], factor:[], 'n':[], 'mean':[], 'ste':[], 'std':[], '5% CI':[], '95% CI':[]})
file_mouse = file.replace('.csv', '')
file_mouse = file_mouse + '_per_mouse'
stats_mouse = data.groupby([factor, 'mouse_id']).mean()
stats_mouse = stats_mouse.reset_index()
get_n (stats_mouse)
save_mouse(file_mouse, dir, stats_mouse)
stats_mean = stats_mouse.groupby([factor]).mean()
stats_std = stats_mouse.groupby([factor]).std()
stats_mean = stats_mean.reset_index()
stats_std = stats_std.reset_index()
colnames = list(data)
for i in colnames:
	if i != 'mouse_id' and i != 'group':
		dir_out = get_desc(file_mouse, dir, stats_mean, stats_std, factor, i, df_out)

print('')
print('')
print('*********************************')
print('Completed with no errors.')
print('Data saved to:' + dir_out)
print('')
print('*********************************')
print('')
	





