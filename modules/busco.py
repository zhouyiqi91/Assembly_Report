#encoding:utf-8
from modules.report_module import *

def parse_busco_log(EVAL_DIR):

	if not EVAL_DIR:
		return None
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
	if not os.path.exists(log_file):
		return None		
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

def get_busco(EVAL_DIR,REPORT_DIR):

	section_name = "busco"
	section_title = "BUSCO评估"
	section_html = ""
	sub_section = []

	paras = ["BUSCO（Benchmarking Universal Single-Copy Orthologs：http://busco.ezlab.org/）评估是使用单拷贝直系同源基因库，结合tblastn、augustus和hmmer等软件对组装得到的基因组进行评估，以此评估组装基因组的完整性。BUSCO评估结果如下："]
	parsed_data = parse_busco_log(EVAL_DIR)
	if not parsed_data:
		return None,None
	busco_score = parsed_data["Complete"]
	table = ("BUSCO notation assessment results",write_busco_table(parsed_data))

	section_html = add_title(section_name,section_title) + add_paragraph(paras) + add_table(table) + '<br/>'
	return [section_name,section_title,section_html,sub_section],busco_score

