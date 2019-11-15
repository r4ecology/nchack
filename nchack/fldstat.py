
from .runthis import run_this

def fldstat(self, stat = "mean",):
    """Method to calculate the spatial stat from a netcdf"""

    #cdo_command = "cdo --reduce_dim -fld" + stat
    cdo_command = "cdo -fld" + stat

    run_this(cdo_command, self,  output = "ensemble")

def spatial_mean(self):
    """
    Calculate an area weighted spatial mean of variables. This is performed for each time step.

    """
    return fldstat(self, stat = "mean")

def spatial_mean(self):
    """
    Calculate an area weighted spatial mean of variables. This is performed for each time step.

    """
    return fldstat(self, stat = "mean")

def spatial_min(self):
    """
    Calculate a spatial minimum of variables. This is performed for each time step.

    """
    return fldstat(self, stat = "min")

def spatial_max(self):
    """
    Calculate a spatial maximum of variables. This is performed for each time step.


    """

    return fldstat(self, stat = "max")

def spatial_range(self):
    """
    Calculate a spatial range of variables. This is performed for each time step.


    """
    return fldstat(self, stat = "range")

def spatial_sum(self):
    """
    Calculate the spatial sum of variables. This is performed for each time step.


    """
    return fldstat(self, stat = "sum")

def spatial_percentile(self, p = 50):
    """
    Calculate the spatial sum of variables. This is performed for each time step.

    Parameters
    -------------
    p: int or float
        Percentile to calculate

    """
    if type(p) not in (int, float):
        raise ValueError(p + " is not a valid percentile")

    cdo_command = "cdo -fldpctl," + str(p)

    run_this(cdo_command, self,  output = "ensemble")



