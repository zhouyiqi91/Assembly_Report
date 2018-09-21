#!/usr/bin/env python3
#encoding:utf-8
import os
import sys
import argparse
import configparser as cp

from modules.report_module import *
from modules.project_info import *
from modules.shortread import *
from modules.gc import *
from modules.busco import *
from modules.cegma import *
from modules.hicup import *
from modules.lachesis import *
from modules.scaffold import *
from modules.ass_steps import *
from modules.seq_info import *
from modules.background import *
from modules.library import *

#解析参数
conf_file = sys.argv[1]
config = cp.ConfigParser()
config.read(conf_file)

Project = config["project"]
Raw_data = config["raw_data"]
Assembly = config["assembly"]
Yaml = config["yaml"]

NAME = Project["name"]
info_file = Project["info"]

SEQ_INFO = Raw_data["seq_info"]
HICUP_DIR = norm_dir(Raw_data["hicup"])

ASS_STEPS = Assembly["assembly_steps"]
FALCON_DIR = norm_dir(Assembly["falcon"])
TENX_DIR = norm_dir(Assembly["tenx"])
BIONANO_DIR = norm_dir(Assembly["bionano"])
LACHESIS_DIR = norm_dir(Assembly["lachesis"])
PILON_DIR = norm_dir(Assembly["pilon"])
EVAL_DIR = norm_dir(Assembly["eval"])

Out_yaml = Yaml["out_yaml"]
In_yaml = Yaml["in_yaml"]

if ASS_STEPS:
	ASS_STEPS_LIST = ASS_STEPS.split(",")
else:
	ASS_STEPS_LIST = []
background_list = ASS_STEPS_LIST
lb_list = background_list

#report路径
PWD = os.getcwd()
REPORT_DIR = PWD + "/" + NAME + "_report/"
dirname, filename = os.path.split(os.path.abspath(sys.argv[0])) 
TEMPLATE_DIR = dirname + "/template"
try:
	os.mkdir(REPORT_DIR)
except:
	pass
os.system("cp -r "+TEMPLATE_DIR+"/* "+REPORT_DIR)

#section_lists中存储输出的section
section_lists = []

#项目信息section
info_name = "info"
info_title = "项目信息"
info_section = [info_name,info_title,add_h3_title(info_name,info_title)+get_project_info(info_file),[]]
add_section(section_lists,info_section)

#背景介绍
bg_name = "bg"
bg_title = "背景介绍"
bg_subsections = get_background(background_list)
bg_section = [bg_name,bg_title,add_h3_title(bg_name,bg_title)+bg_text(),bg_subsections]
add_section(section_lists,bg_section)

#建库测序
lb_name = "lb"
lb_title = "建库测序"
lb_subsections = get_lb(background_list)
lb_section = [lb_name,lb_title,add_h3_title(lb_name,lb_title),lb_subsections]
add_section(section_lists,lb_section)

#测序数据section
data_name = "data"
data_title = "测序数据"
data_section = [data_name,data_title,add_h3_title(data_name,data_title),[]]
#get sub_section
seqinfo_section = get_seqinfo(SEQ_INFO,REPORT_DIR)
hicup_section = get_hicup(HICUP_DIR,REPORT_DIR)
#add sections to evaluation sub_section
DATA_LIST = [seqinfo_section,hicup_section]
data_list = DATA_LIST
for item in data_list:
	if item:
		data_section[3].append(item)
add_section(section_lists,data_section)

#组装步骤section
step_name = "step"
step_title = "组装步骤"
step_subsections = get_ass_steps(ASS_STEPS_LIST)
step_section = [step_name,step_title,add_h3_title(step_name,step_title),step_subsections]
add_section(section_lists,step_section)

#组装结果section
result_name = "result"
result_title = "组装结果"
result_section = [result_name,result_title,add_h3_title(result_name,result_title),[]]
#get sub_section
scaffold_section = get_scaffold(FALCON_DIR,TENX_DIR,BIONANO_DIR,LACHESIS_DIR,PILON_DIR)
lachesis_section = get_lachesis(LACHESIS_DIR,REPORT_DIR)
#add sections to evaluation sub_section
RESULT_LIST = [scaffold_section,lachesis_section]
result_list = RESULT_LIST
for item in result_list:
	if item:
		result_section[3].append(item)
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

#输出yaml
if Out_yaml:
	with open(REPORT_DIR + Out_yaml,'w',encoding = "utf-8") as output_yaml:
		import yaml
		yaml.dump(section_lists,output_yaml,allow_unicode=True)
		print ("Yaml done.")

#读入yaml,更新section_lists
if In_yaml:
	import yaml
	yaml_list = In_yaml.strip().split(",")
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
		
#生成html报告		
if not Out_yaml:
	with open(REPORT_DIR+NAME+"_report.html",'w') as out_html:
		out_html.write(list2report(section_lists,REPORT_DIR))
	os.remove(REPORT_DIR+"index.html")
	print ("Reports done.")

