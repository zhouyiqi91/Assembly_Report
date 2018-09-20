#encoding:utf-8
from modules.report_module import *

PACBIO = ["Pacbio 建库测序","首先对DNA 进行检测，检测合格后将基因组DNA 经26G Needle 片段化，使用BluePippin 选择20kb 以上的片段，经末端修复和加A尾后，再在片段两端分别连接接头，制备DNA文库，如图所示。库检合格，根据文库的有效浓度及数据产出需求使用Pacbio Sequel 平台进行测序。"]


TENX = ["10X Genomics 建库测序","10X Genomics的文库构建核心原理是利用Chromium平台的微流控芯片对微量（1ng）基因组DNA进行精确分区，然后对每个胶珠内的特定barcode序列和DNA 序列进行二代测序。构建好的文库通过Illumina Hiseq测序仪进行双末端测序。"] 


BIONANO = ["Bionano 建库测序","1）提取长片段DNA（>300Kb），用内切酶识别特定的位点，单链切割，荧光标记，用聚合酶修复单链缺口；","2）荧光标记的DNA 分子在电场下的纳米通道内被拉直荧光成像；","3）单分子荧光成像，获得酶切位点分布图谱CMAP；","4）通过Irys分析软件组装得到全基因组的连锁图谱。"]

HIC = ["Hi-C 建库测序","1）用甲醛固定细胞核染色质后进行酶切，经末端修复后加入生物素标记；","2）用连接酶连接、蛋白酶K 消化；","3）将DNA 片段打断，磁珠捕获带生物素标记的DNA片段（图5），构建文库，库捡合格后通过Illumina HiSeq PE150 测序。"]

ILLUMINA = ["Illumina 建库测序","首先将检测合格的DNA样品通过Covaris超声波破碎仪随机打断成片段，经末端修复、加A尾、加测序接头、纯化、PCR扩增等步骤完成。构建好的文库通过Illumina Hiseq测序仪进行双末端测序。"]

bg_dict = {
	'falcon':PACBIO,
	'10x':TENX,
	'bionano':BIONANO,
	'lachesis':HIC,
	'pilon':ILLUMINA
}


def get_lb(lb_list):
	sub_section = []
	for lb_item in lb_list:
		if lb_item in bg_dict:
			section_name = lb_item+"_lb"
			section_title = bg_dict[lb_item][0]
			section_html = add_title(section_name,section_title) + add_paragraph(bg_dict[lb_item][1:]) + "</br>"
			sub_section.append([section_name,section_title,section_html,[]])

	return sub_section