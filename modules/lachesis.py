#encoding:utf-8
from modules.report_module import *
import glob
"""
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
	table.append(contig_list)
	table.append(scaffold_list)

	return table
"""
def parse_la_report_log(LACHESIS_DIR):
	log_file = LACHESIS_DIR + "REPORT.txt"
	table = [["LACHESIS category","Number"]]
	report_list = ['Number of contigs in clusters','Length of contigs in clusters','Number of contigs in orderings','Length of contigs in orderings','Number of contigs in trunks','Length of contigs in trunks']	
	try:	
		log = open(log_file,'r').readlines()
	except:
		print (LACHESIS_DIR + "REPORT.txt not exist! Continue anyway.")
		return None
	for line in log:
		line = line.strip()
		for item in report_list:
			if line.find(item) != -1:
				attr = line.split(":")
				table.append([attr[0],attr[1]])
	return table

def get_lachesis(LACHESIS_DIR,REPORT_DIR):
	
	section_name = "lachesis"
	section_title = "HI-C 辅助组装结果(LACHESIS)"
	section_html = ""
	sub_section = []
	section_html += add_title(section_name,section_title)

	"""
	#sec1
	paras = ["利用LACHESIS软件进行HI-C辅助组装结果："]
	contig,scaffold = parse_la_n50_log(LACHESIS_DIR)
	if not contig:
		return None
	table = ("HI-C assisted assembly summary(LACHESIS)",write_la_n50_table(contig,scaffold))
	section_html += add_title(section_name,section_title) + add_paragraph(paras) + add_table(table) + '<br/>'
	"""
	
	#sec2
	sec2_table = ("LACHESIS detail",parse_la_report_log(LACHESIS_DIR))
	section_html += add_table(sec2_table) + '<br/>'

	#sec3
	sec3_comments = ["Figure&nbsp.&nbspHI-C heatmap"]
	PLOT_PATH = ""
	PLOT_LIST = glob.glob(LACHESIS_DIR + "*_HiC_heatmap.jpg")
	if PLOT_LIST:
		PLOT_PATH = PLOT_LIST[0]
	else:
		print (LACHESIS_DIR + "*_HiC_heatmap.jpg not exist! Continue anyway.")

	section_html += add_plot(PLOT_PATH,REPORT_DIR) + add_center(sec3_comments) + '<br/>'
	return [section_name,section_title,section_html,sub_section]