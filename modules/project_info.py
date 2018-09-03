#encoding:utf-8
from modules.report_module import *

def get_project_info(info_file):
	if not info_file:
		return None
	paras = []
	with open(info_file,'r') as info:
		for line in info:
			line = line.strip()
			paras.append(line)
	return paras
