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

def write_table_line(name,line_number,contig,scaffold,table):
	n50_list = ['Total_length','Total_number','Max_length','N50_length','N50_number']
	if line_number == 1:
		contig_list = [name,'Contig']
		for item in n50_list:
			contig_list.append(contig[item])
		table.append(contig_list)

	if line_number == 2:
		contig_list = [[name,2],'Contig']
		scaffold_list = ['Scaffold']
		for item in n50_list:
			contig_list.append(contig[item])
			scaffold_list.append(scaffold[item])
		table.append(contig_list)
		table.append(scaffold_list)

	return table 

def get_scaffold(FALCON_DIR,TENX_DIR,BIONANO_DIR,LACHESIS_DIR,PILON_DIR):
	
	stats_dic ={
	"Falcon":(FALCON_DIR,1),
	"10X":(TENX_DIR,2),
	"Bionano":(BIONANO_DIR,2),
	"HI-C":(LACHESIS_DIR,2),
	"Pilon":(PILON_DIR,2)
	}

	section_name = "scaffold"
	section_title = "组装结果统计"
	section_html = ""
	sub_section = []

	#sec1
	table = []
	table_header = ['Method','Category','Total_length','Total_number','Max_length','N50_length','N50_number']
	table.append(table_header)
	for item in stats_dic:
		dir_path = stats_dic[item][0]
		line_number = stats_dic[item][1]
		if dir_path:
			contig,scaffold = parse_scaf_n50_log(dir_path)
			table = write_table_line(item,line_number,contig,scaffold,table)

	section_html += add_title(section_name,section_title) + add_table(("Assembly summary",table)) + '<br/>'

	return [section_name,section_title,section_html,sub_section]