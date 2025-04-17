#PBS -l select=16:model=mil_a100:ncpus=44:ngpus=4:mem=250GB
#PBS -l place=scatter:excl
#PBS -l walltime=120:00:00
#PBS -j oe
#PBS -W group_list=s2853
#PBS -q gpu_long@pbspl4
session_name="16_node"
current_time=$(date "+%Y_%m_%d_%H_%M_%S")
export HAPLO_SESSION_DIRECTORY="sessions/${current_time}_${session_name}"
mkdir -p "${HAPLO_SESSION_DIRECTORY}"
qalter -o "${HAPLO_SESSION_DIRECTORY}/${PBS_JOBID}.log" $PBS_JOBID

source /usr/local/lib/init/global.profile

module use -a /swbuild/analytix/tools/modulefiles
module load miniconda3/v4
source activate haplo_env

module load mpi-hpe/mpt

head_node_hostname=`/bin/hostname -s`

export MPI_SHEPHERD=true
export MPI_DSM_DISTRIBUTE=0
export OMP_NUM_THREADS=11
export CUDA_VISIBLE_DEVICES=0,1,2,3

mpiexec -perhost 1 python -m torch.distributed.run \
--nnodes 32 \
--nproc_per_node 4 \
--rdzv_id $RANDOM \
--rdzv_backend c10d \
--rdzv_endpoint $head_node_hostname \
scripts/example_train_session.py
