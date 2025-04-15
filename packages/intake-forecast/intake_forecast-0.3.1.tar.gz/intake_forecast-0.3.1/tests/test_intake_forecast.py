from pathlib import Path
import pytest
import intake
import numpy as np
import xarray as xr
from datetime import datetime, timedelta, timezone
import shutil

from intake_forecast.source import (
    ZarrForecastSource,
    EnhancedZarrSource,
    find_previous_cycle_time,
)


HERE = Path(__file__).parent
TIME = datetime(2025, 4, 1, 0)
TEST_ZARR_PATH = HERE / f"test_{TIME:%Y%m%dT%H}.zarr"


@pytest.fixture(scope="module")
def cat():
    return intake.open_catalog(HERE / "catalog.yml")


def create_test_zarr(path, date=TIME):
    """Create a test zarr store for testing."""
    times = [date + timedelta(days=i) for i in range(7)]
    lats = np.linspace(90, -90, 37)
    lons = np.linspace(-175, 180, 72)
    data = np.random.rand(len(times), len(lats), len(lons))
    ds = xr.Dataset(
        data_vars={
            "u10": (["time", "latitude", "longitude"], data),
            "v10": (["time", "latitude", "longitude"], data),
        },
        coords={
            "time": times,
            "latitude": lats,
            "longitude": lons,
        },
    )
    ds.to_zarr(path, mode="w")
    return ds


def setup_module(module):
    """Setup test module - create test zarr stores."""
    # Create the main test zarr store if it doesn't exist
    if not TEST_ZARR_PATH.exists():
        create_test_zarr(TEST_ZARR_PATH)


def test_find_previous_cycle_time():
    """Test the find_previous_cycle_time function."""
    # Test with exact cycle time
    dt = datetime(2025, 4, 1, 6, 0, 0)
    result = find_previous_cycle_time(dt, 6)
    assert result == dt

    # Test with time between cycles
    dt = datetime(2025, 4, 1, 8, 30, 0)
    result = find_previous_cycle_time(dt, 6)
    assert result == datetime(2025, 4, 1, 6, 0, 0)

    # Test with midnight
    dt = datetime(2025, 4, 1, 0, 0, 0)
    result = find_previous_cycle_time(dt, 6)
    assert result == dt

    # Test with different cycle period
    dt = datetime(2025, 4, 1, 7, 0, 0)
    result = find_previous_cycle_time(dt, 3)
    assert result == datetime(2025, 4, 1, 6, 0, 0)


def test_zarr_forecast_source_init():
    """Test ZarrForecastSource initialization."""
    # Test with datetime object
    source = ZarrForecastSource(
        urlpath="file:///test_%Y%m%dT%H.zarr",
        cycle=datetime(2025, 4, 1, 6),
        cycle_period=6,
    )

    assert source.cycle == datetime(2025, 4, 1, 6)
    assert source.cycle_period == 6
    assert source.maxstepback == 4
    assert source._template == "file:///test_%Y%m%dT%H.zarr"

    # Test with string cycle
    source = ZarrForecastSource(
        urlpath="file:///test_%Y%m%dT%H.zarr",
        cycle="2025-04-01T12",
        cycle_period=6,
    )

    assert source.cycle == datetime(2025, 4, 1, 12)


def test_zarr_forecast_source_to_dask():
    """Test ZarrForecastSource to_dask method."""
    # Create a test zarr store for a specific cycle
    cycle_date = datetime(2025, 4, 1, 0)

    # Test with existing cycle
    source = ZarrForecastSource(
        urlpath=f"file:///{HERE}/test_%Y%m%dT%H.zarr",
        cycle=cycle_date,
        cycle_period=6,
    )
    ds = source.to_dask()
    assert isinstance(ds, xr.Dataset)
    assert "u10" in ds.data_vars
    assert "v10" in ds.data_vars


def test_zarr_forecast_source_stepback():
    """Test ZarrForecastSource stepping back to previous cycles."""
    # Create a test zarr store for a specific cycle
    cycle_date = datetime(2025, 4, 1, 0)
    test_path = HERE / f"test_{cycle_date.strftime('%Y%m%dT%H')}.zarr"

    # Ensure the test zarr store exists
    if not test_path.exists():
        create_test_zarr(test_path, cycle_date)

    # Create a source with a cycle time that doesn't have a corresponding zarr file
    non_existent_cycle = datetime(2025, 4, 1, 6)  # This cycle doesn't exist
    non_existent_path = HERE / f"test_{non_existent_cycle.strftime('%Y%m%dT%H')}.zarr"

    # Make sure the non-existent path doesn't actually exist
    if non_existent_path.exists():
        shutil.rmtree(non_existent_path)

    # Create the source with the non-existent cycle
    source = ZarrForecastSource(
        urlpath=f"file:///{HERE}/test_%Y%m%dT%H.zarr",
        cycle=non_existent_cycle,
        cycle_period=6,
        maxstepback=1,  # Allow stepping back once
    )

    # This should trigger the stepping back mechanism
    ds = source.to_dask()

    assert isinstance(ds, xr.Dataset)

    # Convert to datetime for comparison if it's a pandas Timestamp
    if hasattr(source.cycle, "to_pydatetime"):
        current_cycle = source.cycle.to_pydatetime()
    else:
        current_cycle = source.cycle

    # The cycle should have stepped back by 6 hours (from 06:00 to 00:00)
    expected_cycle = datetime(2025, 4, 1, 0)
    assert (
        current_cycle == expected_cycle
    ), f"Expected {expected_cycle}, got {current_cycle}"


def test_zarr_forecast_source_stepback_limit():
    """Test ZarrForecastSource stepping back limit."""
    # Create a test zarr store for a specific cycle
    cycle_date = datetime(2025, 4, 1, 0)
    test_path = HERE / f"test_{cycle_date.strftime('%Y%m%dT%H')}.zarr"

    # Ensure the test zarr store exists
    if not test_path.exists():
        create_test_zarr(test_path, cycle_date)

    # Create a source with a cycle time that doesn't have a corresponding zarr file
    # and is too far in the future for the maxstepback to reach the existing file
    non_existent_cycle = datetime(2025, 4, 1, 18)  # This cycle doesn't exist
    non_existent_path = HERE / f"test_{non_existent_cycle.strftime('%Y%m%dT%H')}.zarr"

    # Make sure the non-existent path doesn't actually exist
    if non_existent_path.exists():
        shutil.rmtree(non_existent_path)

    # Also make sure intermediate paths don't exist
    for hour in [6, 12]:
        intermediate_path = (
            HERE / f"test_{datetime(2025, 4, 1, hour).strftime('%Y%m%dT%H')}.zarr"
        )
        if intermediate_path.exists():
            shutil.rmtree(intermediate_path)

    # Create the source with the non-existent cycle and limited stepback
    source = ZarrForecastSource(
        urlpath=f"file:///{HERE}/test_%Y%m%dT%H.zarr",
        cycle=non_existent_cycle,
        cycle_period=6,
        maxstepback=2,  # Allow stepping back twice (not enough to reach 00)
    )

    # This should raise a ValueError because we can't step back far enough
    with pytest.raises(ValueError) as excinfo:
        source.to_dask()

    # Check that the error message contains the expected text
    assert "not found and maxstepback" in str(excinfo.value)
    assert str(source.maxstepback) in str(excinfo.value)


def test_zarr_forecast_source_with_zarr_options():
    """Test ZarrForecastSource with zarr options."""
    # Test with custom zarr options
    source = ZarrForecastSource(
        urlpath=f"file:///{HERE}/test_%Y%m%dT%H.zarr",
        cycle=datetime(2025, 4, 1, 0),
        xarray_kwargs={"consolidated": True},
    )

    ds = source.to_dask()
    assert isinstance(ds, xr.Dataset)


def test_enhanced_zarr_source_bare():
    """Test EnhancedZarrSource."""
    source = EnhancedZarrSource(
        urlpath=f"file:///{HERE}/test_{TIME:%Y%m%dT%H}.zarr",
    )
    ds = source.to_dask()
    assert isinstance(ds, xr.Dataset)


def test_enhanced_zarr_source_varmapping():
    """Test EnhancedZarrSource with variable mapping."""
    source = EnhancedZarrSource(
        urlpath=f"file:///{HERE}/test_{TIME:%Y%m%dT%H}.zarr",
        metadata=dict(variable_mappings={"u10": "ugrd", "v10": "vgrd"}),
    )
    ds = source.to_dask()
    assert "ugrd" in ds.data_vars
    assert "vgrd" in ds.data_vars


def test_enhanced_zarr_source_derived_variables():
    """Test EnhancedZarrSource with add derived."""
    source = EnhancedZarrSource(
        urlpath=f"file:///{HERE}/test_{TIME:%Y%m%dT%H}.zarr",
        metadata=dict(
            derived_variables=[
                dict(
                    name="spd",
                    input_variables=["u10", "v10"],
                    function="intake_forecast.functions.speed",
                )
            ],
        ),
    )
    ds = source.to_dask()
    assert "spd" in ds.data_vars


def test_enhanced_zarr_source_adjusted_to_utc():
    """Test EnhancedZarrSource with utcoffset."""
    source = EnhancedZarrSource(
        urlpath=f"file:///{HERE}/test_{TIME:%Y%m%dT%H}.zarr",
        metadata=dict(utcoffset=1),
    )
    ds = source.to_dask()
    assert ds.coords["time"].to_index()[0] == TIME + timedelta(hours=1)


def test_enhanced_zarr_source_applied_aliases():
    """Test EnhancedZarrSource with variable aliases."""
    source = EnhancedZarrSource(
        urlpath=f"file:///{HERE}/test_{TIME:%Y%m%dT%H}.zarr",
        metadata=dict(variable_aliases={"u10": "ugrd"}),
    )
    ds = source.to_dask()
    assert "ugrd" in ds.data_vars
    assert "u10" in ds.data_vars


def test_enhanced_zarr_source_applied_assignments():
    """Test EnhancedZarrSource with variable assignments."""
    source = EnhancedZarrSource(
        urlpath=f"file:///{HERE}/test_{TIME:%Y%m%dT%H}.zarr",
        metadata=dict(variable_assignments={"ugrd": "u10"}),
    )
    ds = source.to_dask()
    assert "ugrd" in ds.data_vars
    assert "u10" in ds.data_vars


def test_enhanced_zarr_source_applied_units_conversion():
    """Test EnhancedZarrSource with unit conversions."""
    source = EnhancedZarrSource(
        urlpath=f"file:///{HERE}/test_{TIME:%Y%m%dT%H}.zarr",
        metadata=dict(unit_conversions={"u10": "m/s,kts"}),
    )
    ds = source.to_dask()
    assert ds["u10"].attrs["units"] == "kts"


def test_catalog_cyclic_forecast(cat):
    """Test loading from catalog."""
    dset = cat.test_cyclic_forecast(cycle="2025-04-01T00").to_dask()
    assert "u10" in dset.data_vars
    assert "v10" in dset.data_vars
    assert "ugrd" in dset.data_vars
    assert "vgrd" in dset.data_vars


def test_catalog_enhanced(cat):
    """Test loading from catalog."""
    dset = cat.test_enhanced_zarr.to_dask()
    assert isinstance(dset, xr.Dataset)
    assert "ugrd" in dset.data_vars
    assert "vgrd" in dset.data_vars
    assert "u10" in dset.data_vars
    assert "v10" in dset.data_vars
    assert "spd" in dset.data_vars
    assert "u_assigned" in dset.data_vars
    assert "v_assigned" in dset.data_vars
    assert dset.coords["time"].to_index()[0] == TIME + timedelta(hours=1)
    assert dset["u10"].attrs["units"] == "kts"
    assert dset["v10"].attrs["units"] == "kts"


def test_zarr_forecast_source_with_legacy_options():
    """Test ZarrForecastSource with legacy options."""
    # Test with legacy options
    source = ZarrForecastSource(
        urlpath=f"file:///{HERE}/test_%Y%m%dT%H.zarr",
        cycle=datetime(2025, 4, 1, 0),
        storage_options={"token": None},
        consolidated=True,
    )
    ds = source.to_dask()
    assert source.xarray_kwargs["storage_options"] == {"token": None}
    assert source.xarray_kwargs["consolidated"] is True
    assert isinstance(ds, xr.Dataset)


def test_ncdap(cat):
    cycle = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0, tzinfo=None
    )
    dset = cat["gfs_glob05"](cycle=cycle).to_dask()
    assert "ugrd10m" in dset.data_vars
    assert "vgrd10m" in dset.data_vars
    assert "wndsp" in dset.data_vars


def teardown_module(module):
    """Clean up after tests."""
    shutil.rmtree(TEST_ZARR_PATH)
