
import copy
import warnings
import subprocess

from nctoolkit.cleanup import cleanup, disk_clean
from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_this, run_nco
from nctoolkit.session import nc_safe
from nctoolkit.temp_file import temp_file


def cdo_version():
    """Function to find cdo version"""
    cdo_check = subprocess.run("cdo --version", shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cdo_check = str(cdo_check.stderr).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()
    return cdo_check.split("(")[0].strip().split(" ")[-1]




def ensemble_percentile(self, p=None):
    """
    Calculate an ensemble percentile
    This will calculate the percentles for each time step in the files. For example, if you had an ensemble of files where each file included 12 months of data, it would calculate the percentile for each month.

    Parameters
    -------------
    p : float or int
        percentile to calculate. 0<=p<=100.
    """

    # make sure p is a number

    if p is None:
        raise ValueError("p was not supplied")

    if type(p) not in [int, float]:
        raise TypeError(f"p is a {type(p)}, not an int or float")

    # check p is between 0 and 100
    if (p < 0) or (p > 100):
        raise ValueError("p is not between 0 and 100!")

    # This method cannot possibly be chained. Release it
    self.run()

    # Throw an error if there is only a single file in the tracker
    if type(self.current) is not list:
        warnings.warn(message="There is only one file in the dataset")

    # create the cdo command and run it
    cdo_command = f"cdo --sortname -enspctl,{p}"
    run_this(cdo_command, self, output="one")

    # set the _merged attribute to True
    self._merged = True


def ensemble_nco(self, method, vars=None, ignore_time=False):
    """
    NCO Method to calculate an ensemble stat from a list of files
    """
    # Throw an error if there is only a single file in the tracker

    if vars is not None:
        if type(vars) == str:
            vars = [vars]

        if type(vars) is not list:
            raise TypeError("vars supplied is not a list or str!")
    # This method cannot possibly be chained. Release it

    self.run()

    ff_ensemble = copy.deepcopy(self.current)

    if type(ff_ensemble) is not list:
        warnings.warn(message="There is only one file in the dataset")

    if type(self.current) is str:
        ff_ensemble = [copy.deepcopy(self.current)]

    # generate a temp files
    target = temp_file("nc")

    # generate the nco call
    if ignore_time == False:
        if vars is None:
            nco_command = f'ncea -y {method} {str_flatten(ff_ensemble, " ")} {target}'
        else:
            nco_command = f'ncea -y {method} -v {str_flatten(vars, ",")} {str_flatten(ff_ensemble, " ")} {target}'
    else:
        if vars is None:
            nco_command = f'ncra -y {method} {str_flatten(ff_ensemble, " ")} {target}'
        else:
            nco_command = f'ncra -y {method} -v {str_flatten(vars, ",")} {str_flatten(ff_ensemble, " ")} {target}'

    # run the call
    target = run_nco(nco_command, target)

    # add the call to the history and tempfile to nc_safe
    self.history.append(nco_command)
    self._hold_history = copy.deepcopy(self.history)

    self.current = target

    self._merged = True

    cleanup()
    self.disk_clean()


def ensemble_max(self, nco = False, ignore_time=False):
    """
    Calculate an ensemble maximum

    Parameters
    -------------
    nco : boolean
        Do you want to use NCO for the calculation? Default is False, i.e. CDO is used. Modify default if run time is an issue.
    ignore_time : boolean
        If True the max is calculated over all time steps. If False, the ensemble max is calculated for each time steps; for example, if the ensemble is made up of monthly files the max for each month will be calculated.
    """

    if nco is False:
        self.run()

        if type(self.current) is not list:
            warnings.warn(message="There is only one file in the dataset")


        if ignore_time is False:
            cdo_command = "cdo --sortname -ensmax"
        else:
            if cdo_version() != "1.9.3":
                cdo_command = "cdo -timmax --sortname -ensmax"
            else:
                cdo_command = "cdo --sortname -ensmax"

        run_this(cdo_command, self)

        self._merged = True

        if cdo_version() == "1.9.3":
            self.run()
            self.max()

        return None

    ensemble_nco(self, "max", ignore_time=ignore_time)




def ensemble_min(self, nco = False, ignore_time=False):
    """
    Calculate an ensemble min

    Parameters
    -------------
    nco : boolean
        Do you want to use NCO for the calculation? Default is False, i.e. CDO is used. Modify default if run time is an issue.
    ignore_time : boolean
        If True the min is calculated over all time steps. If False, the ensemble min is calculated for each time steps; for example, if the ensemble is made up of monthly files the min for each month will be calculated.
    """

    if nco is False:
        self.run()

        if type(self.current) is not list:
            warnings.warn(message="There is only one file in the dataset")


        if ignore_time is False:
            cdo_command = "cdo --sortname -ensmin"
        else:
            if cdo_version() != "1.9.3":
                cdo_command = "cdo -timmin --sortname -ensmin"
            else:
                cdo_command = "cdo --sortname -ensmin"

        run_this(cdo_command, self)

        self._merged = True
        if cdo_version() == "1.9.3":
            self.run()
            if ignore_time:
                self.min()

        return None

    ensemble_nco(self, "min", ignore_time=ignore_time)


def ensemble_mean(self, nco = False, ignore_time=False):
    """
    Calculate an ensemble mean

    Parameters
    -------------
    nco : boolean
        Do you want to use NCO for the calculation? Default is False, i.e. CDO is used. Modify default if run time is an issue.
    ignore_time : boolean
        If True the mean is calculated over all time steps. If False, the ensemble mean is calculated for each time steps; for example, if the ensemble is made up of monthly files the mean for each month will be calculated.
    """

    if nco is False:
        self.run()

        if type(self.current) is not list:
            warnings.warn(message="There is only one file in the dataset")

        if ignore_time is False:
            cdo_command = "cdo --sortname -ensmean"
        else:
            if cdo_version() != "1.9.3":
                cdo_command = "cdo -timmean --sortname -ensmean"
            else:
                cdo_command = "cdo --sortname -ensmean"

        run_this(cdo_command, self)

        self._merged = True
        if cdo_version() == "1.9.3":
            self.run()
            self.mean()

        return None

    ensemble_nco(self, "mean", ignore_time=ignore_time)


def ensemble_range(self):
    """
    Calculate an ensemble range
    The range is calculated for each time step; for example, if each file in the ensemble has 12 months of data the statistic will be calculated for each month.
    """
    self.run()

    if type(self.current) is not list:
        warnings.warn(message="There is only one file in the dataset")

    cdo_command = "cdo --sortname -ensrange"

    run_this(cdo_command, self)

    self._merged = True




