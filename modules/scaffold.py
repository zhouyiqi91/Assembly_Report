from modules.report_module import *
import glob

def parse_scaf_n50_log(SCAFFOLD_DIR):
	if not SCAFFOLD_DIR:
		return None,None
	n50_file = SCAFFOLD_DIR + "N50.out"
	if not os.path.exists(n50_file):
		print (SCAFFOLD_DIR + "N50.out not exist! Continue anyway." )
		return None,None
	contig,scaffold = parse_N50_log(n50_file)

	return contig,scaffold

def write_scaf_n50_table(contig,scaffold):

	n50_list = ['N50_length','N50_number','Total_length','Total_number']
	parsed_data = {}
	table = [['','N50_length','N50_number','Total_length','Total_number']]
	contig_list = ['Contig']
	scaffold_list = ['Scaffold']
	for item in n50_list:
		contig_list.append(contig[item])
		scaffold_list.append(scaffold[item])
	table.append(contig_list)
	table.append(scaffold_list)

	return table

def get_scaffold(SCAFFOLD_DIR,REPORT_DIR):
	
	section_name = "scaffold"
	section_title = "Scaffold版本组装结果"
	section_html = ""
	sub_section = []

	#sec1
	paras = ["组装结果统计："]
	contig,scaffold = parse_scaf_n50_log(SCAFFOLD_DIR)
	if not contig:
		return None
	table = ("Scaffold version summary",write_scaf_n50_table(contig,scaffold))
	section_html += add_title(section_name,section_title) + add_paragraph(paras) + add_table(table) + '<br/>'

	return [section_name,section_title,section_html,sub_section]