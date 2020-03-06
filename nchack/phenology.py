import copy

from .temp_file import temp_file
from .session import nc_safe
from .flatten import str_flatten
from .select import select_variables
from .setters import set_longnames
from .cleanup import cleanup
from .cleanup import disk_clean
from .runthis import run_cdo
import copy


def phenology(self, var = None):
    """
    Calculate phenologies from a dataset. Each file in an ensemble must only cover a single year, and ideally have all days.
    This method currently only calculcates the day of year of the annual maximum.

    Parameters
    -------------
    var : str
        Variable to analyze.
    """

    if var is None:
        raise ValueError("No var was supplied")
    if type(var) is not str:
        raise TypeError("var is not a str")

    # First step is to check if the current file exists
    if type(self.current) is not str:
        raise TypeError("This method only works on single files")

    #  create a new tracker for the phenologies
    # Then restrict the file to the var selected

    self.release()

    start_files = copy.deepcopy(self.current)

    new_self = self.copy()

    new_self.select_variables(var)

    # Create the day of year

    doy_nc = temp_file("nc")

    #cdo_command = "cdo -L -timcumsum -chname," + var +   ",peak -setclonlatbox,1,-180,180,-90,90 -selname," + var + " " + new_self.current + " " + doy_nc
    cdo_command = f"cdo -L -timcumsum -chname,{var},peak -setclonlatbox,1,-180,180,-90,90 -selname,{var} {new_self.current} {doy_nc}"

    new_self.history.append(cdo_command)

    doy_nc = run_cdo(cdo_command, doy_nc)

    # Find the max value of the var

    max_nc = temp_file("nc")

    cdo_command = f"cdo -L -timmax -chname,{var},{var}_max -selname,{var} {new_self.current} {max_nc}"

    new_self.history.append(cdo_command)
    max_nc = run_cdo(cdo_command, max_nc)

    # We now need to merge the three  netcdf files

    out_nc = temp_file("nc")

    cdo_command = f"cdo merge {new_self.current} {max_nc} {doy_nc} {out_nc}"

    new_self.history.append(cdo_command)
    out_nc = run_cdo(cdo_command, out_nc)

    # Now, calculate the timing of the annual maximum

    phen_nc = temp_file("nc")

    cdo_command = f"cdo -L -timmin -selname,peak -expr,'peak=peak + 365*({var}<{var}_max)' {out_nc} {phen_nc}"

    new_self.history.append(cdo_command)
    phen_nc = run_cdo(cdo_command, phen_nc)

    nc_safe.remove(new_self.current)

    nc_safe.append(phen_nc)

    new_self.current = phen_nc

    # set the long name and unit


    new_self._hold_history = copy.deepcopy(new_self.history)

    new_self.set_longnames({"peak": "Timing of annual maximum"})

    new_self.set_units({"peak": "Day of year"})
    new_self.release()

    self.current = copy.deepcopy(new_self.current )
    self.history+=copy.deepcopy(new_self.history)
    self._hold_history = copy.deepcopy(self.history)
    nc_safe.append(self.current)

    nc_safe.remove(start_files)

    cleanup(self.current)

    self.disk_clean()



