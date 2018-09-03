import os
import shutil

TEMPLATE_DIR = "/ifs/TJPROJ3/RAD/zhouyiqi/assembly_report/soft/template"
PIC_PATH = "pictures/"

def add_title(name,title):
	out = ""
	if title:
		out = '<h4><a name=' + name + '>&nbsp;&nbsp;' + title + '</a></h4>'
	return out

def add_h3_title(name,title):
	out = ""
	if title:
		out = '<h3><a name=' + name + '>' + title + '</a></h3><br/>'
	return out

def add_paragraph(paras): #paras是一个列表，每个元素是一个段落
	out = ""
	if paras:
		for para in paras:
			out += '<p class=paragraph>'+ para + '</p>'
		#out += '<br/>'
	return out

def add_plot(plot,REPORT_DIR):  #plot原图片路径,REPORT_DIR是报告目录名称
	out = ""
	if plot:
		plot_file_name = plot.split("/")[-1]
		shutil.copy(plot,REPORT_DIR+PIC_PATH+plot_file_name)
		plot_final_path = PIC_PATH+"/"+plot_file_name
		#out = '<p class="name_table">' + plot[0] + '</p>'
		out = '<center><img class="w85" src=' + plot_final_path +' height="400" width="400"/></center>'
	return out

def add_table(table): #table是一个元组：（名称，列表） 列表第一个元素为表头
	if table:
		table_list = table[1]
		out = '<p class="name_table">' + table[0] + '</p>'
		out += '<table class="tf1">'
		for i in range(len(table_list)):
			out += '<tr>'
			if i == 0:
				for item in table_list[i]:
					out += '<th>' + item + '</th>'
			else:
				for item in table_list[i]:
					out += '<td>'+ item + '</td>'
			out += '</tr>'
		out += '</table>'
	return out

def add_comment(comments):
	if comments:
		out = ""
		for comment in comments:
			out += comment + '<br/>'
		#out += '<br/>'
	return out


def add_section(section_lists,new_section):
	#new_section : [section_name,section_title,section_html,sub_section]
	if new_section[3]:
		last_sub_section = new_section[3][-1]
		last_sub_section[2] += '<br/>'
	section_lists.append(new_section)

def list2report(section_lists,REPORT_DIR):
	from jinja2 import PackageLoader,Environment,FileSystemLoader
	env = Environment(loader=FileSystemLoader(REPORT_DIR))    
	template = env.get_template('index.html')    # 获取一个模板文件
	html = (template.render(section_lists=section_lists)) 
	return html

def yaml2report(yaml):
	pass

def list2yaml(list):
	pass

class Base_Module(object):

	def __init__(self):
		self.sections = list()

	def add_section(self,section_list):
		self.sections.append(section_list)

	def gen_report(self):
		print (self.sections)





