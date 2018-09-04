#encoding:utf-8
from modules.report_module import *

def parse_la_n50_log(LACHESIS_DIR):
	if not LACHESIS_DIR:
		return None,None
	n50_file = LACHESIS_DIR + "N50.out"
	if not os.path.exists(n50_file):
		return None,None
	contig,scaffold = parse_N50_log(n50_file)

	return contig,scaffold

def write_la_n50_table(contig,scaffold):

	n50_list = ['N50_length','N50_number','Total_length','Total_number']
	parsed_data = {}
	table = [['','N50_length','N50_number','Total_length','Total_number']]
	contig_list = ['Contig']
	scaffold_list = ['Scaffold']
	for item in n50_list:
		contig_list.append(contig[item])
		scaffold_list.append(scaffold[item])
	table.entend([contig_list,scaffold_list])

	return table
'''
def parse_snp_log(EVAL_DIR):
	log_file = EVAL_DIR + "BWA/SNP/samtools_snp.stat"
	parsed_data = {}			
	log = open(log_file,'r').readlines()
	attr = log[1].strip().split("\t")
	parsed_data['All_SNP'] = (attr[0],attr[1])
	parsed_data['Heterozygous_SNP'] = (attr[2],attr[3])
	parsed_data['Homologous_SNP'] = (attr[4],attr[5])
	return parsed_data

def write_snp_table(parsed_data):

	output_list = ['All_SNP','Heterozygous_SNP','Homologous_SNP']
	table = [["SNP category","Number","Percentage"]]
	for item in output_list:
		number = str(parsed_data[item][0])
		percent = round(float(parsed_data[item][1])*100,7)
		percent = str(percent) + "%"
		table.append([item,number,percent])
	return table
'''

def get_lachesis(LACHESIS_DIR,REPORT_DIR):
	
	section_name = "lachesis"
	section_title = "HI-C 辅助组装结果(LACHESIS)"
	section_html = ""
	sub_section = []

	#sec1
	paras = ["利用LACHESIS软件进行HI-C辅助组装结果："]
	contig,scaffold = parse_la_n50_log(LACHESIS_DIR)
	if not contig:
		return None
	table = ("HI-C assisted assembly summary(LACHESIS)",write_la_n50_table(contig,scaffold))
	section_html = add_title(section_name,section_title) + add_paragraph(paras) + add_table(table) + '<br/>'

	"""
	#sec2
	comments = ["Figure&nbsp:&nbspSequencing depth distribution(Average_sequencing_depth&nbsp:&nbsp"+parsed_data['Average_sequencing_depth']+')','横轴：测序深度，单位X；纵轴：碱基占基因组（无N）的比率']
	PLOT_PATH = EVAL_DIR + "BWA/map_rate/histPlot.png"
	section_html += add_plot(PLOT_PATH,REPORT_DIR) + add_comment(comments) + '<br/>'

	#sec3
	snp_comments = ["一般认为纯合SNP比率可以反映基因组组装的正确率"]
	snp_data = parse_snp_log(EVAL_DIR)
	snp_table = ("SNP summary",write_snp_table(snp_data))
	section_html += add_table(snp_table) + add_comment(snp_comments) + '<br/>'
	"""

	return [section_name,section_title,section_html,sub_section],mapping_rate,coverage