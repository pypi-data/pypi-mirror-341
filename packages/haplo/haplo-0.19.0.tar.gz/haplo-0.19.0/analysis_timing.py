import datetime

from haplo.internal.mcmc_output_analysis import mcmc_output_xarray_dataset_to_pandas_data_frame, \
    extract_windowed_median_log_likelihood_series
from pathlib import Path
import xarray
from multiprocessing.pool import ThreadPool
import dask

start_time = datetime.datetime.now()
zarr_path = Path('output0.zarr.zip')
dataset = xarray.open_zarr(zarr_path)
dask.config.set(schedular='threads', pool=ThreadPool(1))
medians = extract_windowed_median_log_likelihood_series(dataset)
end_time = datetime.datetime.now()
print(medians)
print(medians.shape)
print(end_time - start_time)
print('medians without threads')
