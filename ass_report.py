#!/usr/bin/env python
#encoding:utf-8
from modules.report_module import *
import os
import sys
from modules.project_info import *
from modules.shortread import *
from modules.gc import *
from modules.busco import *
from modules.cegma import *
from modules.hicup import *
from modules.lachesis import *

import argparse
def parse_input():

	parser = argparse.ArgumentParser(description='Novogene assembly report generation')
	parser.add_argument('--eval', required = False, dest = "EVAL_DIR", help = "组装评估目录路径")
	parser.add_argument('--info', required = False, dest = "info", help = "项目信息文本文件路径")
	parser.add_argument('--out_yaml', required = False, dest = "out_yaml", help = "如果指定此参数，则输出yaml文件")
	parser.add_argument('--in_yaml',  required = False, dest = "in_yaml",  help = "读入yaml,生成html报告;多个yaml文件用逗号分割")
	parser.add_argument('--hicup', required = False, dest = "HICUP_DIR", help = "HICUP目录路径")
	parser.add_argument('--lachesis', required = False, dest = "LACHESIS_DIR",help = "LACHESIS目录路径")
	parser.add_argument('-n', '--name',required = True,dest = "NAME", help= "物种名称")
	parser.add_argument('-v', '--version', action = 'version', version = '%(prog)s 1.0')
        #parser.add_argument('input_file',action="store",type=str)
	args = parser.parse_args()
        
	return args

#report路径
args = parse_input()
NAME = args.NAME
EVAL_DIR = norm_dir(args.EVAL_DIR)
HICUP_DIR = norm_dir(args.HICUP_DIR)
LACHESIS_DIR = norm_dir(args.LACHESIS_DIR)
PWD = os.getcwd()
REPORT_DIR = PWD + "/" + NAME + "_report/"
dirname, filename = os.path.split(os.path.abspath(sys.argv[0])) 
TEMPLATE_DIR = dirname + "/template"
try:
	os.mkdir(REPORT_DIR)
except:
	pass
os.system("cp -r "+TEMPLATE_DIR+"/* "+REPORT_DIR)
PIC_PATH = "pictures/"

#section_lists中存储输出的section
section_lists = []

#项目信息section
info_name = "info"
info_title = "项目信息"
info_section = [info_name,info_title,add_h3_title(info_name,info_title)+get_project_info(args.info),[]]
add_section(section_lists,info_section)

#测序数据统计section
data_name = "data"
data_title = "测序数据统计"
data_section = [data_name,data_title,add_h3_title(data_name,data_title),[]]
#get sub_section
hicup_section = get_hicup(HICUP_DIR,REPORT_DIR)
#add sections to evaluation sub_section
DATA_LIST = [hicup_section]
data_list = DATA_LIST
for item in data_list:
	if item:
		data_section[3].append(item)
add_section(section_lists,data_section)

#组装步骤section
step_name = "step"
step_title = "组装步骤"
step_section = [step_name,step_title,add_h3_title(step_name,step_title),[]]
#get sub_section
lachesis_section = get_lachesis(LACHESIS_DIR,REPORT_DIR)
#add sections to evaluation sub_section
STEP_LIST = [lachesis_section]
step_list = STEP_LIST
for item in step_list:
	if item:
		step_section[3].append(item)
add_section(section_lists,step_section)



#组装结果section
result_name = "result"
result_title = "组装结果"
result_section = [result_name,result_title,add_h3_title(result_name,result_title),[]]
add_section(section_lists,result_section)


#组装评估 section
evaluation_name = "evaluation"
evaluation_title = "组装评估"
evaluation_section = [evaluation_name,evaluation_title,add_h3_title(evaluation_name,evaluation_title),[]]
#get sub_section
cegma_section,cegma_score = get_cegma(EVAL_DIR,REPORT_DIR)
shortread_section,mapping_rate,coverage = get_shortread(EVAL_DIR,REPORT_DIR)
gc_section = get_gc(EVAL_DIR,REPORT_DIR)
busco_section,busco_score = get_busco(EVAL_DIR,REPORT_DIR)
#add sections to evaluation sub_section
EVAL_LIST = [shortread_section,gc_section,cegma_section,busco_section]
eval_list = EVAL_LIST
for item in eval_list:
	if item:
		evaluation_section[3].append(item)
#add evaluation section to section_lists
add_section(section_lists,evaluation_section)

if args.out_yaml:
	with open(REPORT_DIR + args.out_yaml,'w',encoding = "utf-8") as output_yaml:
		import yaml
		yaml.dump(section_lists,output_yaml,allow_unicode=True)
		print ("Yaml done.")

if args.in_yaml:
	import yaml
	yaml_list = args.in_yaml.strip().split(",")
	for yaml_file in yaml_list:
		with open( yaml_file,'r',encoding = "utf-8") as in_yaml:
			in_yaml_section = yaml.load(in_yaml)
			for index in range(len(in_yaml_section)):
				new_sub_sections = in_yaml_section[index][3]
				old_sub_sections = section_lists[index][3]
				old_subsection_name = []
				for old_sub_section in old_sub_sections:
					old_subsection_name.append(old_sub_section[0])
				if new_sub_sections:   #sub_section不为空
					for new_sub_section in new_sub_sections:						
						if new_sub_section[0] not in old_subsection_name:
							section_lists[index][3].append(new_sub_section)
							
			
		
if not args.out_yaml:
	with open(REPORT_DIR+NAME+"_report.html",'w') as out_html:
		out_html.write(list2report(section_lists,REPORT_DIR))
	os.remove(REPORT_DIR+"index.html")
	print ("Reports done.")




"""
eval_list = ["busco"]
for item in eval_list:
	return_section = eval("get_"+item+"(EVAL_DIR,PIC_PATH)")
	add_section(section_lists,return_section)
"""

#evaluation