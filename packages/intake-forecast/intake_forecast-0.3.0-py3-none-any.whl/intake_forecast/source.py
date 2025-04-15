import logging
from typing import Optional
from datetime import datetime, timedelta
from intake.source.base import DataSource, PatternMixin
from intake.source.utils import reverse_format
from intake_xarray.xzarr import ZarrSource
from intake.catalog.utils import coerce_datetime

from intake_forecast.utils import find_previous_cycle_time, enhance


logger = logging.getLogger(__name__)


class ForecastSource(DataSource):
    name = "forecast"

    def __init__(
        self,
        urlpath: str,
        cycle: datetime,
        cycle_period: int = 6,
        maxstepback: int = 4,
        xarray_kwargs: dict = {},
        metadata: dict = None,
    ):
        """Intake driver for cyclic zarr sources.

        Parameters
        ----------
        urlpath : str
            URL path template for zarr files
        cycle : datetime
            Cycle time
        cycle_period : int
            Cycle period in hours, it should be a positive factor of 24
        maxstepback : int
            Maximum number of cycles to step back when searching for past cycles
        xarray_kwargs : dict
            Keyword arguments for opening zarr files with xarray.open_zarr
        metadata : dict
            Metadata for the dataset

        """
        super().__init__(metadata=metadata)
        self.cycle = find_previous_cycle_time(coerce_datetime(cycle), cycle_period)
        self.cycle_period = cycle_period
        self.maxstepback = maxstepback
        self.xarray_kwargs = xarray_kwargs
        self._template = urlpath
        self._stepback = maxstepback

    @property
    def kwargs(self):
        return self.xarray_kwargs

    @property
    def reader(self):
        import xarray as xr

        return xr.open_dataset

    def to_dask(self):
        urlpath = self.cycle.strftime(self._template)
        try:
            ds = self.reader(urlpath, **self.kwargs)
        except (FileNotFoundError, OSError) as err:
            if self._stepback == 0:
                raise ValueError(
                    f"{urlpath} not found and maxstepback {self.maxstepback} reached"
                ) from err
            logger.warning(f"{urlpath} not found, stepping back {self.cycle_period}h")
            self.cycle -= timedelta(hours=self.cycle_period)
            self._stepback -= 1
            ds = self.to_dask()
        return enhance(ds, self.metadata)

    read = to_dask

    discover = read

    read_chunked = to_dask


class ZarrForecastSource(ForecastSource):
    name = "zarr_forecast"

    def __init__(
        self,
        storage_options: Optional[dict] = None,
        consolidated: Optional[bool] = None,
        **kwargs,
    ):
        """Intake driver for cyclic zarr sources.

        Parameters
        ----------
        storage_options : Optional[dict], deprecated
            Legacy parameter for storage options for opening zarr files with
            xarray.open_zarr, it should now be provided in xarray_kwargs
        consolidated : Optional[bool], deprecated
            Legacy parameter for opening consolidated zarr files with
            xarray.open_zarr, it should now be provided in xarray_kwargs

        """
        super().__init__(**kwargs)
        # For backward compatibility with the old onzarr driver
        if storage_options is not None:
            self.xarray_kwargs["storage_options"] = storage_options
        if consolidated is not None:
            self.xarray_kwargs["consolidated"] = consolidated

    @property
    def reader(self):
        import xarray as xr

        return xr.open_zarr


class EnhancedZarrSource(ZarrSource):
    name = "zarr_enhanced"

    def __init__(self, **kwargs):
        """Zarr source with additional functionality specified from the metadata.

        Parameters
        ----------
        **kwargs
            Keyword arguments for the ZarrSource constructor

        """
        super().__init__(**kwargs)
        self.metadata = self.reader.metadata

    def to_dask(self):
        ds = super().to_dask()
        return enhance(ds, self.metadata)


class NCDapSource(ForecastSource, PatternMixin):
    name = "ncdap"

    def __init__(
        self,
        engine: str = "netcdf4",
        chunks: Optional[dict] = None,
        combine: Optional[str] = None,
        concat_dim: Optional[str] = None,
        path_as_pattern: bool = True,
        **kwargs,
    ):
        """Open a opendap datasource with netcdf4 driver

        Parameters
        ----------
        engine : str, optional
            Engine to use for opening the dataset
        chunks : int or dict, optional
            Chunks is used to load the new dataset into dask
            arrays. ``chunks={}`` loads the dataset with dask using a single
            chunk for all arrays.
        combine : ({'by_coords', 'nested'}, optional)
            Which function is used to concatenate all the files when urlpath
            has a wildcard. It is recommended to set this argument in all
            your catalogs because the default has changed and is going to change.
            It was "nested", and is now the default of xarray.open_mfdataset
            which is "auto_combine", and is planed to change from "auto" to
            "by_corrds" in a near future.
        concat_dim : str, optional
            Name of dimension along which to concatenate the files. Can
            be new or pre-existing if combine is "nested". Must be None or new if
            combine is "by_coords".
        path_as_pattern : bool or str, optional
            Whether to treat the path as a pattern (ie. ``data_{field}.nc``)
            and create new coodinates in the output corresponding to pattern
            fields. If str, is treated as pattern to match on. Default is True.

        """
        super().__init__(**kwargs)
        self.path_as_pattern = path_as_pattern
        self.xarray_kwargs["engine"] = engine
        if chunks is not None:
            self.xarray_kwargs["chunks"] = chunks
        if combine is not None:
            self.xarray_kwargs["combine"] = combine
        if concat_dim is not None:
            self.xarray_kwargs["concat_dim"] = concat_dim
        # Remove undesired kwargs
        self.xarray_kwargs.pop("storage_options", None)
        self.xarray_kwargs.pop("consolidated", None)

    @property
    def reader(self):
        import xarray as xr

        if "*" in self._template or isinstance(self._template, list):
            if self.pattern:
                self.xarray_kwargs["preprocess"] = self._add_path_to_ds
            return xr.open_mfdataset
        return xr.open_dataset

    def _add_path_to_ds(self, ds):
        """Adding path info to a coord for a particular file"""
        var = next(var for var in ds)
        new_coords = reverse_format(self.pattern, ds[var].encoding["source"])
        return ds.assign_coords(**new_coords)
