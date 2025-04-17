from pathlib import Path
from haplo.analysis import combine_constantinos_kalapotharakos_split_mcmc_output_files_to_xarray_zarr
from haplo.logging import enable_logger

split_mcmc_output_directory = Path('.')
zarr_path = Path('output0.zarr')  # Use a better name, but still use the `.zarr` extension.
enable_logger()  # Optional. Will add printing of some progress information.
combine_constantinos_kalapotharakos_split_mcmc_output_files_to_xarray_zarr(
    split_mcmc_output_directory=split_mcmc_output_directory,
    combined_output_path=zarr_path,
    elements_per_record=13,
    multiprocess_pool_size=50,
    overwrite=True,
)
