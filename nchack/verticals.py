
import subprocess
import warnings

from .runthis import run_this
from .flatten import str_flatten

def bottom(self):
    """
    Extract the bottom level from a dataset


    """

    # extract the number of the bottom level
    # Use the first file for an ensemble
    # pull the cdo command together, then run it or store it
    if type(self.current) is list:
        ff = self.current[0]
        warnings.warn(message = "The first file in ensemble used to determine number of vertical levels")
    else:
        ff = self.current

    cdo_result = subprocess.run("cdo nlevel " + ff, shell = True, capture_output = True)
    n_levels = int(str(cdo_result.stdout).replace("b'", "").strip().replace("'", "").split("\\n")[0])

    cdo_command = "cdo -sellevidx," + str(n_levels)

    run_this(cdo_command, self,  output = "ensemble")


def surface(self):
    """
    Extract the top/surface level from a dataset

    """

    cdo_command = "cdo -sellevidx,1 "
    run_this(cdo_command, self,  output = "ensemble")


def vertical_interp(self, vert_depths = None):
    """
    Verticaly interpolate a dataset based on given depths

    Parameters
    -------------
    vert_depths : list
        list of depths to vertical interpolate to

    """

    # below used for checking whether vertical remapping occurs

    vertical_remap = True

    # first a quick fix for the case when there is only one vertical depth

    if vert_depths != None:
        if (type(vert_depths) == int) or (type(vert_depths) == float):
            vert_depths = {vert_depths}

  #  if vert_depths == None:
  #      vertical_remap = False
  #
  #  if vert_depths != None:
  #      num_depths = len(self.depths())
  #      if num_depths < 2:
  #          print("There are none or one vertical depths in the file. Vertical interpolation not carried out.")
  #          vertical_remap = False
  #  if ((vert_depths != None) and vertical_remap):
  #      available_depths = self.depths()

    # Check if min/max depths are outside valid ranges. This should possibly be a warning, not error
    if vertical_remap:
   #     if (min(vert_depths) < min(available_depths)):
   #          raise ValueError("error:minimum depth supplied is too low")
   #     if (max(vert_depths) > max(available_depths)):
   #          raise ValueError("error: maximum depth supplied is too low")

        vert_depths = str_flatten(vert_depths, ",")
        cdo_command = "cdo intlevel," + vert_depths

        run_this(cdo_command, self,  output = "ensemble")

     # throw error if cdo fails at this point




def vertstat(self, stat = "mean"):
    """Method to calculate the vertical mean from a function"""
    cdo_command = "cdo -vert" + stat

    run_this(cdo_command, self,  output = "ensemble")

    # clean up the directory

def vertical_mean(self):
    """
    Calculate the depth-averaged mean

    """

    return vertstat(self, stat = "mean")

def vertical_min(self):
    """
    Calculate the depth-averaged minimum

    """

    return vertstat(self, stat = "min")

def vertical_max(self):
    """
    Calculate the depth-averaged maximum

    """

    return vertstat(self, stat = "max")

def vertical_range(self):
    """
    Calculate the depth-averaged range


    """

    return vertstat(self, stat = "range")