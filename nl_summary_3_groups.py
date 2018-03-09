# coding=utf-8
import os
import pandas as pd
import csv
import numpy as np

# Default values
dir1_apical = 'D:\\Dropbox\\Sync Data Analysis Computers\\Gulf War Project\\Statistics\\Final Spreadsheets\\nl360 files\\oil_saline\\apical\\analyzed'
dir1_basal = 'D:\\Dropbox\\Sync Data Analysis Computers\\Gulf War Project\\Statistics\\Final Spreadsheets\\nl360 files\\oil_saline\\basal\\analyzed'
dir2_apical = 'D:\\Dropbox\\Sync Data Analysis Computers\\Gulf War Project\\Statistics\\Final Spreadsheets\\nl360 files\\cpf_saline\\apical\\analyzed'
dir2_basal = 'D:\\Dropbox\\Sync Data Analysis Computers\\Gulf War Project\\Statistics\\Final Spreadsheets\\nl360 files\\cpf_saline\\basal\\analyzed'
dir3_apical = 'D:\\Dropbox\\Sync Data Analysis Computers\\Gulf War Project\\Statistics\\Final Spreadsheets\\nl360 files\\cpf_igf\\apical\\analyzed'
dir3_basal = 'D:\\Dropbox\\Sync Data Analysis Computers\\Gulf War Project\\Statistics\\Final Spreadsheets\\nl360 files\\cpf_igf\\basal\\analyzed'

group1 = 'oil_saline'
group2 = 'cpf_saline'
group3 = 'cpf_igf'


	
# Get directory list and iterate through each one
def get_data (dir, group):
	os.chdir (dir)
	n = 0
	branch_points = 0 
	total_spines = 0 
	thin = 0
	stubby = 0 
	mushroom = 0
	filopodia = 0 
	pthin = 0 
	pstubby = 0 
	pshroom = 0 
	ppodia = 0 
	length = 0 
	surface_area = 0 
	volume = 0
	row = {'mouse_id':[], 'group':[], 'branch_points':[],  'total_spines':[], 'thin':[], 'stubby':[], 'mushroom':[], 'filopodia':[],  '%thin':[], '%stubby':[], '%mushroom':[], '%filopodia':[], 'length':[],'surface_area':[], 'volume':[], 'density_0-150':[], 'density_150-300':[], 'density_300-500':[], 'density_500+':[], 'length_0-150':[], 'length_150-300':[], 'length_300-500':[], 'length_500+':[]}
	df_append = pd.DataFrame(row)

	for file in os.listdir(dir):
		if file.endswith(".csv"):
			df = pd.read_csv(file)
			# Makes a row for mouse id for mouse_stats calculations
			f = lambda file: file.split(".")
			mouse_id = f (file)
			mouse_id = mouse_id[0]
			f = lambda mouse_id: mouse_id.split('-')
			mouse_id = mouse_id[-0:3]
		
			row = {'mouse_id':mouse_id, 'group':group, 'branch_points':df.ix[0,1], 'total_spines':df.ix[1,1], 'thin':df.ix[2,1], 'stubby':df.ix[3,1], 'mushroom':df.ix[4,1], 'filopodia':df.ix[5,1],  '%thin':df.ix[6,1], '%stubby':df.ix[7,1], '%mushroom':df.ix[8,1], '%filopodia':df.ix[9,1], 'length':df.ix[10,1], 'surface_area':df.ix[11,1], 'volume':df.ix[12,1],'density_0-150':df.ix[0,5], 'density_150-300':df.ix[1,5], 'density_300-500':df.ix[2,5], 'density_500+':df.ix[3,5], 'length_0-150':df.ix[0,7], 'length_150-300':df.ix[1,7], 'length_300-500':df.ix[2,7], 'length_500+':df.ix[3,7]}
			
			df_append = df_append.append(row, ignore_index=True)
			print(file + ' analysis complete')
			
	df_append = df_append[['mouse_id', 'group', 'branch_points', 'length', 'total_spines', 'thin', 'stubby', 'mushroom', 'filopodia',  '%thin', '%stubby', '%mushroom', '%filopodia', 'surface_area', 'volume', 'density_0-150', 'density_150-300', 'density_300-500', 'density_500+', 'length_0-150', 'length_150-300', 'length_300-500', 'length_500+' ]]
	dir_out = save_data(dir, group, df_append)
	return dir_out
					
					
def save_data (dir, group, df_append):
	file_data = group + '_summary.csv'
	dir_out = dir + '\\analyzed'
	try:
		os.stat(dir_out)
	except:
		os.mkdir(dir_out)
	os.chdir(dir_out)
	df_append.to_csv(file_data, index = False)
	os.chdir(dir)
	return dir_out
	
		
#Run the program
dir_out1_apical = get_data (dir1_apical, group1)
dir_out1_basal = get_data (dir1_basal, group1)
dir_out2_apical = get_data (dir2_apical, group2)
dir_out2_basal = get_data (dir2_basal, group2)
dir_out3_apical = get_data (dir3_apical, group3)
dir_out3_basal = get_data (dir3_basal, group3)
print('')
print('')
print('*********************************')
print('Completed with no errors.')
print('Data saved to:' + dir_out1_apical)
print('Data saved to:' + dir_out1_basal)
print('Data saved to:' + dir_out2_apical)
print('Data saved to:' + dir_out2_basal)
print('Data saved to:' + dir_out3_apical)
print('Data saved to:' + dir_out3_basal)
print('')
print('*********************************')
print('')