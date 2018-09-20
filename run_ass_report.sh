bin_path = $(cd `dirname $0`; pwd)
source activate report
python ${bin_path}/ass_report.py $1
