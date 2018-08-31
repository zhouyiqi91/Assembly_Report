#encoding:utf-8
from modules.report_module import *

def parse_shortread_log(EVAL_DIR):
	log_file = EVAL_DIR + "BWA/map_rate/result.out"
	shortread_keys = {
		'Average_sequencing_depth': 'Average_sequencing_depth',
		'Coverage':'Coverage',
		'Coverage_at_least_4X':'Coverage_at_least_4X',
		'Coverage_at_least_10X': 'Coverage_at_least_10X',
		'Coverage_at_least_20X': 'Coverage_at_least_20X',
				}
	parsed_data = {}			
	with open(log_file,'r') as log:
		for line in log:
			if line.find("mapped (") != -1:
				parsed_data['Mapping_rate'] = line.split("(")[1].split(':')[0]
			for key, string in shortread_keys.items():
				if string in line:
					s = line.strip().split(':')
					parsed_data[key] = s[1].strip()

	return parsed_data

def write_shortread_table(parsed_data):

	output_list = ['Mapping_rate','Coverage','Coverage_at_least_4X','Coverage_at_least_10X','Coverage_at_least_20X']
	table = [["Short read mapping_rate and coverage","Percentage"]]
	for item in output_list:
		output_item = parsed_data[item]
		table.append([item,output_item])
	return table

def get_shortread(EVAL_DIR,PIC_PATH):
	
	PLOT_PATH = EVAL_DIR + "BWA/map_rate/histPlot.png"
	section_name = "shortread"
	section_title = "短reads比对"
	section_html = ""
	sub_section = []

	paras = ["为了评估组装的准确性，选取小片段文库reads采用BWA软件(http://bio-bwa.sourceforge.net/)比对到组装的基因组上，统计reads的比对率、覆盖基因组的程度及深度的分布情况，评估组装的完整性和测序的均匀性，结果如下："]
	parsed_data = parse_shortread_log(EVAL_DIR)
	if not parsed_data:
		return None,None,None
	mapping_rate = parsed_data["Mapping_rate"]
	coverage = parsed_data["Coverage"]
	table = ("Short read mapping status",write_shortread_table(parsed_data))

	section_html = add_title(section_name,section_title) + add_paragraph(paras) + add_table(table)
	section_html += add_plot()
	return [section_name,section_title,section_html,sub_section],mapping_rate,coverage




def parse_busco_log(EVAL_DIR):
	log_file = EVAL_DIR + "BUSCO/run_BUSCO/short_summary_BUSCO.txt"
	busco_keys = {
		'Complete': 'Complete BUSCOs',
		'Complete_single_copy': 'Complete and single-copy BUSCOs',
		'Complete_duplicated': 'Complete and duplicated BUSCOs',
		'Fragmented': 'Fragmented BUSCOs',
		'Missing': 'Missing BUSCOs',
		'Total': 'Total BUSCO groups searched'
				}
	parsed_data = {}			
	with open(log_file,'r') as log:
		for line in log:
			for key, string in busco_keys.items():
				if string in line:
					s = line.strip().split("\t")
					parsed_data[key] = int(s[0])
	return parsed_data 

def write_busco_table(parsed_data):

	output_list = ['Complete','Complete_single_copy','Complete_duplicated','Fragmented','Missing','Total']
	table = [["BUSCO category","Number"]]
	for item in output_list:
		percent = str(round(parsed_data[item]/float(parsed_data['Total'])*100,2)) + "%"
		output_item = str(parsed_data[item]) + "(" + percent + ")"
		table.append([item,output_item])
	return table

def get_busco(EVAL_DIR,PIC_PATH):

	section_name = "busco"
	section_title = "BUSCO评估"
	section_html = ""
	sub_section = []

	paras = ["BUSCO（Benchmarking Universal Single-Copy Orthologs：http://busco.ezlab.org/）评估是使用单拷贝直系同源基因库，结合tblastn、augustus和hmmer等软件对组装得到的基因组进行评估，以此评估组装基因组的完整性。最终组装版本的BUSCO评估结果如下："]
	try:
		parsed_data = parse_busco_log(EVAL_DIR)
	except:
		return None,None
	busco_score = parsed_data["Complete"]
	table = ("BUSCO notation assessment results",write_busco_table(parsed_data))

	section_html = add_title(section_name,section_title) + add_paragraph(paras) + add_table(table)
	return [section_name,section_title,section_html,sub_section],busco_score

