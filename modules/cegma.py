#encoding:utf-8
from modules.report_module import *

def parse_cegma_log(EVAL_DIR):
	log_file = EVAL_DIR + "CEGMA/species.completeness_report"
	cegma_keys = {
		'Complete': 'Complete',
		'Complete+Partial': 'Partial',
				}
	parsed_data = {}	
	if not os.path.exists(log_file):
		return None		
	with open(log_file,'r') as log:
		for line in log:
			attr = line.strip().split()
			for key, string in cegma_keys.items():
				if len(attr) > 0:
					if string in attr[0]:
						parsed_data[key] = (attr[1],attr[2])
	return parsed_data 

def write_cegma_table(parsed_data):

	output_list = ['Complete','Complete+Partial']
	table = [["CEGMA category","Number"]]
	for item in output_list:
		output_item = parsed_data[item][0] + "(" + parsed_data[item][1] + "%)"
		table.append([item,output_item])
	return table

def get_cegma(EVAL_DIR,REPORT_DIR):

	section_name = "cegma"
	section_title = "CEGMA评估"
	section_html = ""
	sub_section = []

	paras = ["CEGMA(Core Eukaryotic Genes Mapping Approach)评估是选取存在于6个真核模式生物中的保守基因（248个gene）构成 core gene库，结合tblastn、genewise和geneid等软件对组装得到的基因组进行评估，以此评估组装基因组的完整性。CEGMA评估结果如下："]
	parsed_data = parse_cegma_log(EVAL_DIR)
	if not parsed_data:
		return None,None
	cegma_score = parsed_data["Complete"][1]
	table = ("CEGMA assessment results",write_cegma_table(parsed_data))

	section_html = add_title(section_name,section_title) + add_paragraph(paras) + add_table(table) + '<br/>'
	return [section_name,section_title,section_html,sub_section],cegma_score