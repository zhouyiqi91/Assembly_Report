#encoding:utf-8
from modules.report_module import *

FALCON = ["falcon 软件组装",
"A. 对Pacbio数据进行自我纠错，每条reads之间进行比对，根据碱基质量的插入概率，缺失概率，测序错误概率等进行自我纠错。得到纠错后的pre-assemble reads。通常，纠错后的三代数据的正确率可以达到99.999%。","B. 用纠错后的三代数据进行组装，由于三代数据读长很长（平均读长可达10-15kb，最长>40kb），因此，与二代数据不同，组装采用Overlap-Layout-Consensus算法，即通过reads的overlap关系进行拼接，得到的consensus序列。","C. 对上一步组装结果，使用三代数据基于quiver软件对组装结果进行校正，再用二代数据基于pilon软件进行再次校正，从而提高结果的精确度，最终得到高质量的consensus序列。"
]

TENX = ["10X Genomics辅助组装",
"A. 将10X Genomics文库测序得到Linked-reads与三代组装结果所得consensus序列进行比对，在原有的基础上加上linked reads组装成super-Scaffold。","B. 对于实际距离比较近的consensus，有很多的Linked-reads支持其连接关系；对于实际距离比较远的consensus，则缺少Linked-reads的支持，无法将其连接，最终得到组装序列。"
]

BIONANO = ["Bionano辅助组装","A. BioNano光学图谱单分子荧光成像，获得酶切位点分布光学图谱，通过Irys分析软件组装得到基因内切酶连锁图谱。",
"B. 将初始组装版本进行电子酶切，转化为cmap文件，记为NGS cmap。","C. 通过bionano数据bnx、NGS map和预估基因组大小进行酶位点间距标准化，筛选出最优的组装参数，根据与光学图谱之间的重叠关系，进行bionano数据的组装，生成bionano组装版本，记为BNG cmap。","D. 将bnx、NGS map、BNG map和初始组装版本基于hybridScaffold软件，设置合理参数，得到最终的Hybrid scaffold版本。"
]

LACHESIS = ["Hi-C辅助组装","A. 与组装版本比对：对Hi-C clean data通过BWA软件与初始版本进行比对，只有双端比对上的reads会被用到后续的组装中。","B. 组装校正：将Hi-C短reads比对到初始组装版本的contig/scaffold，通过比对结果的物理覆盖率信息，将初始版本错误组装的地方打断，作为修正。","C. 根据两个contig互作强度和互作reads比对的位置对同类的contig/scaffold进行排序和准确定向。","D. 锚定染色体：根据酶切区域和Hi-C数据提供的link关系，构图并计算权重，将每条染色体的contig或scaffold进行连接，获得染色体水平的基因组组装版本。"

]

ass_steps_dict = {
	'falcon':FALCON,
	'10x':TENX,
	'bionano':BIONANO,
	'lachesis':LACHESIS
}

def get_ass_steps(ass_steps_list):
	sub_section = []
	for item in ass_steps_list:
		if item in ass_steps_dict:
			section_name = item +"_step"
			section_title = ass_steps_dict[item][0]
			section_html = add_title(section_name,section_title) + add_paragraph(ass_steps_dict[item][1:]) + "</br>"
			sub_section.append([section_name,section_title,section_html,[]])

	return sub_section

