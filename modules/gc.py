#encoding:utf-8
from modules.report_module import *

def get_gc(EVAL_DIR,REPORT_DIR):

	if not EVAL_DIR:
		return None
	
	PLOT_PATH = EVAL_DIR + "BWA/GC/GC_depth.pos.png"
	section_name = "gc"
	section_title = "GC含量"
	section_html = ""
	sub_section = []

	#sec1
	paras = ["对组装的基因组序列以10k为windows无重复计算GC含量和平均深度并作图，可以根据此图分析测序数据是否存在GC偏向性以及样本是否存在污染。结果如下："]
	comments =  ['Figure&nbsp:&nbspGC distribution','主图：GC含量分布图；横轴：GC含量；纵轴：测序深度','柱状图上：GC含量分布图；柱状图右：测序深度分布图。']

	section_html += add_title(section_name,section_title) + add_paragraph(paras) + add_plot(PLOT_PATH,REPORT_DIR) + add_comment(comments) +'<br/>'

	return [section_name,section_title,section_html,sub_section]