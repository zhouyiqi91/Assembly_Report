#encoding:utf-8
from modules.report_module import *

BG_TEXT = ["近年来，随着高通量测序技术的发展，三代测序逐渐成为基因组研究的新兴手段。由于二代测序读长短，不能跨过高重复和低复杂度区域，而以PacBio 为代表的第三代测序技术有效的解决了这个问题。该平台利用单分子实时测序，又称SMRT（SingleMolecule Real-Time）测序，构建超长片段的文库，得到超长的reads。","同时，随着测序新技术的不断涌现，三代PacBio 测序技术，结合10X Genomics、BioNano、Hi-C 等新技术，使得基因组可以组装到Super-Scaffold水平。"]

#PACBIO_TITLE = "Pacbio Sequel 测序简介"
PACBIO = ["Pacbio Sequel 测序简介","SMRT（Single-Molecule, Real-Time）测序即单分子实时测序（边合成边测序），其原理是：当DNA与聚合酶形成的复合物被ZMW（零模波导孔）捕获后，4种不同荧光标记的dNTP 通过布朗运动随机进入检测区域并与聚合酶结合，与模板匹配的碱基生成化学键的时间远远长于其他碱基停留的时间。因此统计荧光信号存在时间的长短，可区分匹配的碱基与游离碱基。通过统计4种荧光信号与时间的关系图，即可测定DNA 模板序列。"]

#TENX_TITLE = "10X Genomics 测序简介"
TENX = ["10X Genomics 测序简介","10X Genomics 的linked reads 技术本质上是将barcode 序列引入长序列片段，通过将长片段分配到不同的油滴微粒中，利用GemCode平台对长片段序列进行扩增引入barcode序列以及测序接头引物，然后将序列打断成适合测序大小的片段进行测序，通过barcode序列信息追踪来自每个大片段DNA 模板的多个Reads，从而获得大片段的遗传信息。"] 

#BIONANO_TITLE = "Bionano 光学图谱简介"
BIONANO = ["Bionano 光学图谱简介","BioNano 光学图谱系统基于单分子光学图谱技术，通过其特有的芯片技术使完整的单一DNA分子可以在纳米通道中平行排列，拍照成像，展示更完整的基因图谱。它是唯一一种可以将自身系统产生的光学信号与测序数据进行联合组装和分析的物理图谱技术，成本低、耗时少、成效高，对于获取高复杂区域重复序列信息、检测基因组结构变异有着无与伦比的技术优势，成为当前基因组研究的有力武器。","Irys系统利用内切酶对DNA进行识别、酶切、再次合成并标记荧光，在基因组上添加多个特异性的酶切标记位点，再利用电极将DNA分子导入纳米孔并拉直，使得每个DNA单分子线性化展开，然后进行超长单分子高分辨率扫描荧光成像，经核心算法将酶切位点分布图转化成基因组图谱数据。"]

#HIC_TITLE = "Hi-C 技术简介"
HIC = ["Hi-C 技术简介","Hi-C 技术是染色体构象捕获（Chromosome conformation capture，简称为3C）的一种衍生技术，以整个细胞核为研究对象，基于高通量测序进行染色体构象的捕获，获得全基因组范围内整个染色质DNA 在空间位置上的关系，在辅助基因组组装和染色体三维结构的研究方面被广泛应用。"]

ILLUMINA = ["Illumina 测序简介","Illumina新一代测序技术可以高通量、并行对核酸片段进行深度测序，测序的技术原理是采用可逆性末端边合成边测序反应，首先在DNA片段两端加上序列已知的通用接头构建文库，文库加载到测序芯片Flowcell上，文库两端的已知序列与Flowcell基底上的Oligo序列互补，每条文库片段都经过桥式PCR扩增形成一个簇，测序时采用边合成边测序反应，即在碱基延伸过程中，每个循环反应只能延伸一个正确互补的碱基，根据四种不同的荧光信号确认碱基种类，保证最终的核酸序列质量，经过多个循环后，完整读取核酸序列。"]

bg_dict = {
	'falcon':PACBIO,
	'10x':TENX,
	'bionano':BIONANO,
	'lachesis':HIC,
	'pilon':ILLUMINA
}

def bg_text():
	out_html = add_paragraph(BG_TEXT) + "</br>"
	return out_html

def get_background(background_list):
	sub_section = []
	for bg_item in background_list:
		if bg_item in bg_dict:
			section_name = bg_item+"_bg"
			section_title = bg_dict[bg_item][0]
			section_html = add_title(section_name,section_title) + add_paragraph(bg_dict[bg_item][1:]) + "</br>"
			sub_section.append([section_name,section_title,section_html,[]])

	return sub_section



"""
def parse_input():

	parser = argparse.ArgumentParser(description='Novogene assembly report generation')
	parser.add_argument('-n', '--name',required = True,dest = "NAME", help= "物种名称")
	parser.add_argument('--info', required = False, dest = "info", help = "项目信息文本文件路径")
	parser.add_argument('--seq_info', required = False, dest = "SEQ_INFO", help = "测序数据文本文件，第一行为基因组大小，其余行为输出信息")
	parser.add_argument('--hicup', required = False, dest = "HICUP_DIR", help = "HICUP目录路径")
	parser.add_argument('--ass_steps', required = False, dest = "ASS_STEPS", help = "组装步骤，逗号分割。示例：falcon,10x,bionano,lachesis,pilon")	
	parser.add_argument('--scaffold',required = False,dest = "SCAFFOLD_DIR", help= "Scaffold组装版本路径")
	parser.add_argument('--lachesis', required = False, dest = "LACHESIS_DIR",help = "LACHESIS目录路径")
	parser.add_argument('--eval', required = False, dest = "EVAL_DIR", help = "组装评估目录路径")
	parser.add_argument('--out_yaml', required = False, dest = "out_yaml", help = "如果指定此参数，则输出yaml文件")
	parser.add_argument('--in_yaml',  required = False, dest = "in_yaml",  help = "读入yaml,生成html报告;多个yaml文件用逗号分割")
	parser.add_argument('-v', '--version', action = 'version', version = '%(prog)s 1.0')
	args = parser.parse_args()
        
	return args

#解析参数
args = parse_input()
NAME = args.NAME
SEQ_INFO = args.SEQ_INFO
EVAL_DIR = norm_dir(args.EVAL_DIR)
HICUP_DIR = norm_dir(args.HICUP_DIR)
LACHESIS_DIR = norm_dir(args.LACHESIS_DIR)
SCAFFOLD_DIR = norm_dir(args.SCAFFOLD_DIR)
info_file = args.info
"""



