#PBS -l select=1:model=mil_a100:ncpus=40:ngpus=4:mem=500GB
#PBS -l place=scatter:excl
#PBS -l walltime=0:05:00
#PBS -j oe
#PBS -W group_list=s2853
#PBS -q gpu_devel@pbspl4

source /usr/local/lib/init/global.profile

module use -a /swbuild/analytix/tools/modulefiles
module load miniconda3/v4
source activate haplo_env

module load mpi-hpe/mpt

export MPI_SHEPHERD=true
export MPI_DSM_DISTRIBUTE=0
export CUDA_VISIBLE_DEVICES=0,1,2,3

mpiexec -perhost 1 echo $CUDA_VISIBLE_DEVICES
mpiexec -perhost 1 python -c "import torch; print(torch.cuda.is_available())"
