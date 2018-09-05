#encoding:utf-8
from modules.report_module import *

FALCON = [
"首先进行三代数据的自身纠错，利用FALCON进行基因组的纯三代组装，其原理是依照HGAP原理优化而来，通过已矫正的长读长互相比对，将重叠的长读长序列连接，然后经FALCON-Unzip分析寻找其中杂合性差异，并对这些杂合性差异序列定相分类，整合“haplotype-fused” Contigs，重新组装到haplotigs，得到构成二倍体基因组组装的Updated primary Contigs（p-Contig）和haplotigs（h-Contig）。然后利用二代小片段或三代数据进行纠错，得到Contig版本。"
]
TENX = [
"将获得的10X Genomics Linked-reads数据与基因组草图的Contig序列比对，对于实际距离比较近的Contig，有很多的Linked-reads支持其连接关系；对于实际距离比较远的Contig，则缺少Linked-reads的支持，无法将其连接。依照该原理，利用fragScaff软件延伸Contig，获得Scaffold。"
]
BIONANO = [
"利用irys-scaffolding软件将BioNano得到的基因组图谱与基因组草图进行比对，对拼接结果进行修正，并进一步延长Scaffold序列。"
]
LACHESIS = [
"利用LACHESIS软件将Hi-C测序Reads与最终版本的Scaffold序列进行比对后，利用Hi-C有效Mapping reads对Scaffold序列进行聚类（分到不同染色体），之后对每个染色体上的Scaffold序列进行排序和定向，从而获得最终的染色体级别的组装结果。"
]
ass_steps_dict = {
	'falcon':FALCON,
	'10x':TENX,
	'bionano':BIONANO,
	'lachesis':LACHESIS
}

def get_ass_steps(ass_steps_list):
	out_html = ""
	index = 0
	for step in ass_steps_list:
		if step in ass_steps_dict:
			index += 1
			ass_steps_dict[step][0] = str(index) + ". " + ass_steps_dict[step][0]
			out_html += add_paragraph(ass_steps_dict[step])
	out_html += "<br/>"

	return out_html

