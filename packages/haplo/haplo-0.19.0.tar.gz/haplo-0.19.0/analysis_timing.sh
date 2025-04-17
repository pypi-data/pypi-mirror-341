#PBS -l select=1:ncpus=28:model=bro:mem=100GB
#PBS -l place=scatter:excl
#PBS -l walltime=2:00:00
#PBS -j oe
#PBS -k eod
#PBS -r n
#PBS -W group_list=s2853
#PBS -q devel@pbspl1
job_description="analysis_timing"
current_time=$(date "+%Y_%m_%d_%H_%M_%S")
qalter -o "${current_time}_${job_description}_${PBS_JOBID}.log" $PBS_JOBID

source /usr/local/lib/init/global.profile

export OMP_NUM_THREADS=56

module use -a /swbuild/analytix/tools/modulefiles
module load miniconda3/v4
source activate haplo_env

python analysis_timing.py
