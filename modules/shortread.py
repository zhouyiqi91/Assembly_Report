#encoding:utf-8
from modules.report_module import *

def parse_shortread_log(EVAL_DIR):
	if not EVAL_DIR:
		return None
	log_file = EVAL_DIR + "BWA/map_rate/result.out"
	shortread_keys = {
		'Average_sequencing_depth': 'Average_sequencing_depth',
		'Coverage':'Coverage',
		'Coverage_at_least_4X':'Coverage_at_least_4X',
		'Coverage_at_least_10X': 'Coverage_at_least_10X',
		'Coverage_at_least_20X': 'Coverage_at_least_20X',
				}
	parsed_data = {}
	if not os.path.exists(log_file):
		return None
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


def get_shortread(EVAL_DIR,REPORT_DIR):
	
	section_name = "shortread"
	section_title = "短reads比对"
	section_html = ""
	sub_section = []

	#sec1
	paras = ["选取小片段文库reads采用BWA软件比对到组装的基因组上，统计reads的比对率、覆盖基因组的程度及深度的分布情况，以此评估组装的完整性和测序的均匀性。","然后利用samtools软件对BWA比对结果经过染色体坐标排序、去掉重复的reads等处理，进行SNP Calling，并对原始结果进行过滤，得到SNP统计结果，以此评估组装的单碱基正确率。","结果如下："]
	parsed_data = parse_shortread_log(EVAL_DIR)
	if not parsed_data:
		return None,None,None
	mapping_rate = parsed_data["Mapping_rate"]
	coverage = parsed_data["Coverage"]
	table = ("Short read mapping summary",write_shortread_table(parsed_data))
	section_html = add_title(section_name,section_title) + add_paragraph(paras) + add_table(table) + '<br/>'

	#sec2
	comments = ["Figure&nbsp.&nbspSequencing depth distribution(Average_sequencing_depth&nbsp:&nbsp"+parsed_data['Average_sequencing_depth']+')','横轴：测序深度，单位X；纵轴：碱基占基因组（无N）的比率']
	PLOT_PATH = EVAL_DIR + "BWA/map_rate/histPlot.png"
	section_html += add_plot(PLOT_PATH,REPORT_DIR) + add_center(comments) + '<br/>'

	#sec3
	snp_comments = ["一般认为纯合SNP比率可以反映基因组组装的正确率"]
	snp_data = parse_snp_log(EVAL_DIR)
	snp_table = ("SNP summary",write_snp_table(snp_data))
	section_html += add_table(snp_table) + add_comment(snp_comments) + '<br/>'


	return [section_name,section_title,section_html,sub_section],mapping_rate,coverage
