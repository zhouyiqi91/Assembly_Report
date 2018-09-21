#encoding:utf-8
from modules.report_module import *

REFERENCE = [
"1.Eid, John, et al. Real-time DNA sequencing from single polymerase molecules. 2009, Science.",
"2.Lieberman-Aiden E, van Berkum N L, Williams L, et al. Comprehensive mapping of long-range interactions reveals folding principles of the human genome[J]. science, 2009, 326(5950): 289-293.",
"3.Cock, P.J.A., Fields, C.J., Goto, N., Heuer, M.L., and Rice, P.M. (2010). The Sanger FASTQ file format for sequences with quality scores, and the Solexa/Illumina FASTQ variants. Nucleic acids research 38, 1767-1771.",
"4.Hansen, K.D., Brenner, S.E., and Dudoit, S. (2010). Biases in Illuminatranscriptome sequencing caused by random hexamer priming. Nucleic acids research 38, e131-e131.",
"5.Jiang, L., Schlesinger, F., Davis, C.A., Zhang, Y., Li, R., Salit, M., Gingeras, T.R., and Oliver, B.(2011). Synthetic spike-in standards for RNA-seq experiments. Genome research 21,1543-1551.",
"6.Li H, Durbin R: Fast and accurate short read alignment with Burrows-Wheeler transform. Bioinformatics 2009, 25(14):1754-1760."]

def get_ref():
	out_html = add_paragraph(REFERENCE)
	return out_html
