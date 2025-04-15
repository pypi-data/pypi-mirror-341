import logging
from importlib import import_module
from pandas import DataFrame
from xarray import Dataset
from datetime import datetime, timedelta
from pint import UnitRegistry


logger = logging.getLogger(__name__)


def find_previous_cycle_time(time: datetime, cycle_period_hours: int) -> datetime:
    """Find the previous rounded cycle time given the current time.

    Args:
        time (datetime): The current time
        cycle_period_hours (int): The cycle period in hours

    Returns:
        datetime: The previous time in the cycle

    """
    midnight = time.replace(hour=0, minute=0, second=0, microsecond=0)
    hours_passed = (time - midnight).total_seconds() / 3600
    cycles_passed = int(hours_passed / cycle_period_hours)
    return midnight + timedelta(hours=cycles_passed * cycle_period_hours)


def import_function(function_name):
    """Import function from string."""
    module = ".".join(function_name.split(".")[0:-1])
    function = function_name.split(".")[-1]
    try:
        module = import_module(module)
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            f"Ensure derived function module {module} is installed"
        )
    return getattr(module, function)


def add_derived(dset, md):
    for config in md.get("derived_variables", []):
        args = []
        for var in config["input_variables"]:
            args.append(dset[var])
            kwargs = config.get("kwargs", {})
        logger.info(f" -- Adding derived field {config['name']}")
        code = config.get("code", None)
        if code:
            exec(code)
            dset[config["name"]] = locals()[config["function"]](*args, **kwargs)
        else:
            dset[config["name"]] = import_function(config["function"])(*args, **kwargs)
        if "attrs" in config:
            dset[config["name"]].attrs = config["attrs"]
    return dset


def adjust_to_utc(dset, md):
    if "utcoffset" in md:
        logger.info(" --Adjusting to UTC")
        try:
            dset.index += timedelta(hours=md["utcoffset"])
        except Exception:
            dset["time"] = dset.time.to_index() + timedelta(hours=md["utcoffset"])
    return dset


def apply_varmappings(dset, md):
    if "variable_mappings" in md:
        if isinstance(dset, DataFrame):
            dset = dset.rename(columns=md["variable_mappings"], inplace=False)
        elif isinstance(dset, Dataset):
            dset = dset.rename(md["variable_mappings"])
        else:
            raise (f"Type {dset} not supported")
    return dset


def apply_aliases(dset, md):
    if "variable_aliases" in md:
        for var, alias in md["variable_aliases"].items():
            dset[alias] = dset[var]
    return dset


def apply_assignments(dset, md):
    if "variable_assignments" in md:
        for var, assignment in md["variable_assignments"].items():
            dset[var] = dset[assignment]
    return dset


def apply_unit_conversions(dset, md):
    if "unit_conversions" in md:
        for var, units in md["unit_conversions"].items():
            from_unit, to_unit = units.split(",")
            logger.info(f" --converting from {from_unit} to {to_unit}")
            convert_unit(dset, var, from_unit, to_unit)
    return dset


def convert_unit(dset, variable, from_unit, to_unit):
    ureg = UnitRegistry()
    dset[variable] *= 1 * ureg(from_unit).to(to_unit)
    dset[variable].attrs["units"] = to_unit


def enhance(dset, md):
    dset = adjust_to_utc(dset, md)
    dset = apply_varmappings(dset, md)
    dset = apply_aliases(dset, md)
    dset = apply_assignments(dset, md)
    dset = add_derived(dset, md)
    dset = apply_unit_conversions(dset, md)
    return dset
