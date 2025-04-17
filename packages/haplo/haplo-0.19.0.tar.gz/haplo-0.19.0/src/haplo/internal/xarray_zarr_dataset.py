from typing import Self

import xarray
from pathlib import Path

from torch.utils.data import Dataset
from xarray import Dataset as XarrayDataset


class XarrayZarrDataset(Dataset):
    @classmethod
    def new(cls, path: Path) -> Self:
        xarray_dataset: XarrayDataset = xarray.open_zarr(path)
        instance = cls(xarray_dataset=xarray_dataset)
        return instance

    def __init__(self, xarray_dataset: XarrayDataset):
        self.xarray_dataset: XarrayDataset = xarray_dataset

    def __len__(self):
        return self.xarray_dataset['index'].size

    def __getitem__(self, index):
        input_ = self.xarray_dataset['input'][index]
        output = self.xarray_dataset['output'][index]
        return input_, output
