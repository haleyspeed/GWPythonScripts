# coding=utf-8
import os
import pandas as pd
import xlrd
import numpy as np


# Default values
dir1 = 'D:\\Dropbox\\Sync Data Analysis Computers\\Gulf War Project\\Statistics\\Final Spreadsheets\\nl360 files\\oil_saline\\apical'
dir2 = 'D:\\Dropbox\\Sync Data Analysis Computers\\Gulf War Project\\Statistics\\Final Spreadsheets\\nl360 files\\oil_saline\\basal'
dir3 = 'D:\\Dropbox\\Sync Data Analysis Computers\\Gulf War Project\\Statistics\\Final Spreadsheets\\nl360 files\\cpf_saline\\basal'
dir4 = 'D:\\Dropbox\\Sync Data Analysis Computers\\Gulf War Project\\Statistics\\Final Spreadsheets\\nl360 files\\cpf_saline\\apical'
dir5 = 'D:\\Dropbox\\Sync Data Analysis Computers\\Gulf War Project\\Statistics\\Final Spreadsheets\\nl360 files\\cpf_igf\\basal'
dir6 = 'D:\\Dropbox\\Sync Data Analysis Computers\\Gulf War Project\\Statistics\\Final Spreadsheets\\nl360 files\\cpf_igf\\apical'


microns = 10              # Spine density calculated per 10 microns
sholl_distance1 = 150     # Sholl ring 1 from 0-150
sholl_distance2 = 300     # Sholl ring 2 from 150-300
sholl_distance3 = 500     # Sholl ring 3 from 300-500

data_sholl = {'distance':[], 'spines':[], 'length':[], 'density':[]}

# Import worksheet into dataframe
def get_sheet(x, xls):
	df = pd.DataFrame()
	a = xls.parse(x, header = 0)
	a["Sheet Name"] = x
	df = df.append(a)
	return df
	
# Calculate spine density by distance from soma
def get_spineSholl (df, data):
	# Number indicates start distance of Sholl ring
	sholl_spines1 = 0    # Number of spines from 0 to sholl ring 1
	sholl_spines2 = 0    # Number of spines from sholl ring 1 to sholl ring 2
	sholl_spines3 = 0    # Number of spines from sholl ring 2 to sholl ring 3
	sholl_spines4 = 0    # Number of spines after sholl ring 4
	sholl_length1 = 0    # length of dendrites from 0 to sholl ring 1
	sholl_length2 = 0    # length of dendrites from sholl ring 1 to sholl ring 2
	sholl_length3 = 0    # length of dendrites from sholl ring 2 to sholl ring 3
	sholl_length4 = 0    # length of dendrites after sholl ring 4 
	sholl_density1 = 0
	sholl_density2 = 0
	sholl_density3 = 0
	sholl_density4 = 0
	sholl_label1 = '0' + '-' + str(sholl_distance1)
	sholl_label2 = str(sholl_distance1) + '-' + str(sholl_distance2)
	sholl_label3 = str(sholl_distance2) + '-' + str(sholl_distance3)
	sholl_label4 = str(sholl_distance3) + '+'
	
	#Calculate the sums of spine number and length for each Sholl ring
	row = 0
	for index, row in df.iterrows():	
		# column 0 -> 'Start Distance (µm)'
		# column 5 -> 'Total Distance(µm)'
		if (type(row.ix[0]) is int) == True and row.ix[0] < sholl_distance1: 
			sholl_spines1 = sholl_spines1 + row.ix[3]
			sholl_length1 = sholl_length1 + row.ix[5] 
		if (type(row.ix[0]) is int) == True and row.ix[0] >= sholl_distance1 and row.ix[0] < sholl_distance2: 
			sholl_spines2 = sholl_spines2 + row.ix[3]
			sholl_length2 = sholl_length2 + row.ix[5] 
		if (type(row.ix[0]) is int) == True and row.ix[0] >= sholl_distance2 and row.ix[0] < sholl_distance3: 
			sholl_spines3 = sholl_spines3 + row.ix[3]
			sholl_length3 = sholl_length3 + row.ix[5] 
		if (type(row.ix[0]) is int) == True and row.ix[0] >= sholl_distance3: 
			sholl_spines4 = sholl_spines4 + row.ix[3]
			sholl_length4 = sholl_length4 + row.ix[5] 

			
	#Calculate spine density per sholl ring 
	if sholl_length1 !=0:
		sholl_density1 = sholl_spines1/sholl_length1 * microns
	if sholl_length2 !=0:
		sholl_density2 = sholl_spines2/sholl_length2 * microns
	if sholl_length3 !=0:
		sholl_density3 = sholl_spines3/sholl_length3 * microns
	if sholl_length4 !=0:
		sholl_density4 = sholl_spines4/sholl_length4 * microns
	
	# construct the row
	data = {'distance':[sholl_label1, sholl_label2, sholl_label3, sholl_label4], 'spines':[sholl_spines1, sholl_spines2, sholl_spines3, sholl_spines4], 'length':[sholl_length1, sholl_length2, sholl_length3, sholl_length4], 'density':[sholl_density1, sholl_density2, sholl_density3, sholl_density4]}

	# Construct the dataframe
	df_out = pd.DataFrame(data)
	df_out = df_out[['distance','density','spines','length']]
	return df_out

	# Calculate spine density by distance from soma
def get_dummy (data):
	# Number indicates start distance of Sholl ring
	sholl_spines1 = 0    # Number of spines from 0 to sholl ring 1
	sholl_spines2 = 0    # Number of spines from sholl ring 1 to sholl ring 2
	sholl_spines3 = 0    # Number of spines from sholl ring 2 to sholl ring 3
	sholl_spines4 = 0    # Number of spines after sholl ring 4
	sholl_length1 = 0    # length of dendrites from 0 to sholl ring 1
	sholl_length2 = 0    # length of dendrites from sholl ring 1 to sholl ring 2
	sholl_length3 = 0    # length of dendrites from sholl ring 2 to sholl ring 3
	sholl_length4 = 0    # length of dendrites after sholl ring 4 
	sholl_density1 = 0
	sholl_density2 = 0
	sholl_density3 = 0
	sholl_density4 = 0
	sholl_label1 = '0' + '-' + str(sholl_distance1)
	sholl_label2 = str(sholl_distance1) + '-' + str(sholl_distance2)
	sholl_label3 = str(sholl_distance2) + '-' + str(sholl_distance3)
	sholl_label4 = str(sholl_distance3) + '+'
	
	# construct the row
	data = {'distance':[sholl_label1, sholl_label2, sholl_label3, sholl_label4], 'spines':[sholl_spines1, sholl_spines2, sholl_spines3, sholl_spines4], 'length':[sholl_length1, sholl_length2, sholl_length3, sholl_length4], 'density':[sholl_density1, sholl_density2, sholl_density3, sholl_density4]}

	# Construct the dataframe
	df_out = pd.DataFrame(data)
	df_out = df_out[['distance','density','spines','length']]
	return df_out
	
def get_neuronSummary (df, data):
	branch_pts = df.ix[2,2]
	length = df.ix[2,13]
	total_spines = df.ix[2,4]
	all_spines = df.ix[2,4]/length * microns
	thin = df.ix[2,6]/length * microns
	stubby = df.ix[2,7]/length * microns
	mushroom = df.ix[2,8]/length * microns
	filopodia = df.ix[2,9]/length * microns
	if total_spines != 0:
		pthin = df.ix[2,6]/total_spines * 100
		pstubby = df.ix[2,7]/total_spines * 100
		pshroom = df.ix[2,8]/total_spines * 100
		ppodia = df.ix[2,9]/total_spines * 100
	else:
		pthin = 0
		pstubby = 0
		pshroom = 0
		ppodia = 0
	surface_area = df.ix[2,17]
	volume = df.ix[2,19]
	data = {'measurement':['branch_points', 'total_spines', 'thin', 'stubby', 'mushroom', 'filopodia', '%thin', '%stubby', '%mushroom', '%filopodia', 'length', 'surface_area', 'volume'], 'value': [branch_pts, all_spines, thin, stubby, mushroom, filopodia, pthin, pstubby, pshroom, ppodia, length, surface_area, volume], 'unit': ['', '', 'per 10 um', 'per 10 um', 'per 10 um', 'per 10 um', '%', '%', '%', '%', 'um', 'um^2', 'um^3'],'spines by distance:':['','','','','','','','','','','','','']}
	df_out = pd.DataFrame(data)
	
	return df_out
	
	
# Save the data to file (csv)
def save_data(file, dir, df1, df2):
	df = pd.concat([df1,df2], axis = 1)
	df = df[['measurement', 'value', 'unit', 'spines by distance:', 'distance', 'density', 'spines','length']]
	file_out = file.replace('.xlsx', '')
	file_out = file_out + '_analyzed.csv'
	dir_out = dir + '\\analyzed'
	try:
		os.stat(dir_out)
	except:
		os.mkdir(dir_out)
	os.chdir(dir_out)
	df.to_csv(file_out, index = False)
	os.chdir(dir)
	return dir_out
	
	
	

# Get directory list and iterate through each one
def get_data (dir):
	os.chdir (dir)
	for file in os.listdir(dir):
		if file.endswith(".xlsx"):
			xls = pd.ExcelFile(file)
			for x in xls.sheet_names:
				# construct the output data
				data_neuron = {'measurement':[], 'value': [], 'unit': [],'spines by distance:':[]}
				data_sholl = {'distance':[], 'spines':[], 'length':[], 'density':[]}
				if x == 'Neuron Summary':
					df_neuron = get_sheet(x, xls)
					df_neuronSummary = get_neuronSummary(df_neuron, data_neuron)
				elif x == 'Tortuous Distance-Dendrite' or x == 'Tortuous Distance - Dendrites' :
					df_dist = get_sheet(x, xls)
					df_spineSholl = get_spineSholl(df_dist, data_sholl)		
				elif 'Tortuous Distance-Dendrite'not in xls.sheet_names and 'Tortuous Distance - Dendrites' not in xls.sheet_names:
					df_spineSholl = get_dummy(data_sholl)	
			print(file + ' analysis complete')		
			dir_out = save_data(file, dir, df_neuronSummary, df_spineSholl)
	return dir_out
					

#Run the program
dir_out1 = get_data (dir1)
dir_out2 = get_data (dir2)
dir_out3 = get_data (dir3)
dir_out4 = get_data (dir4)
dir_out5 = get_data (dir5)
dir_out6 = get_data (dir6)

print('')
print('')
print('*********************************')
print('Completed with no errors.')
print('Data saved to:' + dir_out1)
print('Data saved to:' + dir_out2)
print('Data saved to:' + dir_out3)
print('Data saved to:' + dir_out4)
print('Data saved to:' + dir_out5)
print('Data saved to:' + dir_out6)
print('')
print('*********************************')
print('')