#encoding:utf-8
from modules.report_module import *

def parse_hicup_log(HICUP_DIR):
	import pandas as pd
	import glob
	if HICUP_DIR:
		log_files = glob.glob(HICUP_DIR + "/HiCUP_summary_report*")
	else:
		return None,None
	if len(log_files) >1:
		print ("hicop log file number >1,use only one")
	log_file = log_files[0]
	hicup_keys_1 = {
		'Total pairs': 'Total_Reads_1',
		'Align and paired':'Paired_Read_1',
		'Valid pairs':'Valid_Pairs',
				}
	hicup_keys_2 = {
		'Unique pairs': 'Deduplication_Read_Pairs_Uniques',
		'Cis-close (< 10Kbp)':'Deduplication_Cis_Close_Uniques',
		'Cis-far (> 10Kbp)':'Deduplication_Cis_Far_Uniques',
		'Trans':'Deduplication_Trans_Uniques'
				}
	parsed_data_1 = {}
	parsed_data_2 = {}
	if not os.path.exists(log_file):
		return None,None
	log = pd.read_csv(log_file,sep="\t")
	for item in log:
		for key, string in hicup_keys_1.items():
			if string == item:
				parsed_data_1[key] = log[item][0]
		for key, string in hicup_keys_2.items():
			if string == item:
				parsed_data_2[key] = log[item][0]

	return parsed_data_1,parsed_data_2

def write_hicup_table(parsed_data_1,parsed_data_2):

	output_list = ['Total pairs','Align and paired','Valid pairs','<b><i> Among vaild pairs:</i></b>','Unique pairs','Cis-close (< 10Kbp)','Cis-far (> 10Kbp)','Trans','Cis-Trans ratio']
	table = [["HICUP category","Number"]]
	parsed_data_2['<b><i> Among vaild pairs:</i></b>'] = ""
	cis = float(parsed_data_2['Cis-close (< 10Kbp)']) + float(parsed_data_2['Cis-far (> 10Kbp)'])
	trans = float(parsed_data_2['Trans'])
	parsed_data_2['Cis-Trans ratio'] = str(round(cis/trans*100,2)) + '%'
	total1 = float(parsed_data_1['Total pairs'])
	total2 = float(parsed_data_1['Valid pairs'])
	for item in parsed_data_1:
		percent = str(round(parsed_data_1[item]/total1*100,2)) + '%'
		parsed_data_1[item] = str(parsed_data_1[item]) + "(" + percent + ")"
	for item in parsed_data_2:
		if parsed_data_2[item] and item !='Cis-Trans ratio':
			percent = str(round(parsed_data_2[item]/total2*100,2)) + '%'
			parsed_data_2[item] = str(parsed_data_2[item]) + "(" + percent + ")"	

	for item in output_list:
		if item in parsed_data_1:
			output_item = str(parsed_data_1[item])
		elif item in parsed_data_2:
			output_item = str(parsed_data_2[item])
		table.append([item,output_item])

	return table

def get_hicup(HICUP_DIR,REPORT_DIR):

	section_name = "hicup"	
	section_title = "HI-C数据统计(HICUP)"
	section_html = ""
	sub_section = []

	#sec
	paras = ["HI-C数据："]
	parsed_data_1,parsed_data_2 = parse_hicup_log(HICUP_DIR)
	if not parsed_data_1:
		return None
	table = ("HI-C data overview(HICUP)",write_hicup_table(parsed_data_1,parsed_data_2))
	section_html = add_title(section_name,section_title) + add_table(table) + '<br/>'

	return [section_name,section_title,section_html,sub_section]