#encoding:utf-8
from modules.report_module import *

def parse_seqinfo_log(SEQ_INFO):
	if not SEQ_INFO:
		return None,None
	if not os.path.exists(SEQ_INFO):
		print (SEQ_INFO + "not exist!")
		return None,None
	log = open(SEQ_INFO,'r').readlines()
	size = log[0].strip()
	if size[-1].upper() not in ['M','G']:
		print ("invalid genome size in ",SEQ_INFO)
		return None,None
	else:
		if size[-1].upper() == 'M':
			realsize = float(size[0:-1])/1000
		else:
			realsize = float(size[0:-1])
	table_cont = [["Library","Average Read Length","Data(G)","Coverage(X)"]]
	for line in log[1:]:
		attr = line.strip().split()
		data = float(attr[2])
		coverage = round(data/realsize,2)
		output_list = [attr[0],attr[1],attr[2],str(coverage)]
		table_cont.append(output_list)

	return size,table_cont

def get_seqinfo(SEQ_INFO,REPORT_DIR):

	section_name = "seq_info"
	section_title = "测序数据统计"
	section_html = ""
	sub_section = []

	size,table_cont = parse_seqinfo_log(SEQ_INFO)
	if not table_cont:
		return None
	table = ("Sequencing raw data summary",table_cont)
	comments = ["* Coverage按照survey预估的基因组大小"+size+"计算"]
	section_html = add_title(section_name,section_title)  + add_table(table) + add_comment(comments) +'<br/>'
	return [section_name,section_title,section_html,sub_section]