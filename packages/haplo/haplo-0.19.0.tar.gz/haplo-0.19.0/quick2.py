import datetime

from haplo.internal.mcmc_output_analysis import mcmc_output_xarray_dataset_to_pandas_data_frame
from pathlib import Path
import xarray
from multiprocessing.pool import ThreadPool
import dask

start_time = datetime.datetime.now()
zarr_path = Path('output0.zarr.zip')
dataset = xarray.open_zarr(zarr_path)
# dask.config.set(schedular='threads', pool=ThreadPool(1))
data_frame = mcmc_output_xarray_dataset_to_pandas_data_frame(dataset, random_sample_size=100_000)
end_time = datetime.datetime.now()
print(data_frame)
print(data_frame.shape)
print(end_time - start_time)
