import warnings
import subprocess
from .flatten import str_flatten
from .session import nc_safe
from .runthis import run_this
from .cleanup import cleanup

def select_season(self, season):
    """
    Select season from a dataset

    Parameters
    -------------
    season : str
        Season to select. One of "DJF", "MAM", "JJA", "SON"
    """

    cdo_command = "cdo -select,season=" + season
    run_this(cdo_command, self,  output = "ensemble")


def select_months(self, months):
    """
    Select months from a dataset
    This method will subset the data to only contains months within the list given. A warning message will be provided when there are missing months.

    Parameters
    -------------
    months : list, range or int
        Month(s) to select.
    """

    # check validity of months
    if type(months) is range:
        months = list(months)

    if type(months) is not list:
        months = [months]
    # all of the variables in months need to be converted to ints, just in case floats have been provided

    months = [int(x) for x in months]

    for x in months:
        if x not in list(range(1, 13)):
            raise ValueError("Months supplied are not valid!")

    months = str_flatten(months, ",")

    cdo_command = "cdo -selmonth," + months + " "
    run_this(cdo_command, self,  output = "ensemble")


def select_years(self, years):
    """
    Select years from a dataset
    This method will subset the data to only contains years within the list given. A warning message will be provided when there are missing years.
    Parameters
    -------------
    months : list,range or int
        Month(s) to select.

    """

    if type(years) is range:
        years = list(years)

    if type(years) is not list:
        years = [years]

    # convert years to int
    years = [int(x) for x in years]


    select_years = False


    if type(self.current) is str:
        self.current = [self.current]


    missing_files = 0

    n_removed = 0
    new_current = []
    for ff in self.current:
        out = subprocess.Popen("cdo showyear " + ff,shell = True, stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        cdo_result,ignore = out.communicate()
        cdo_result = str(cdo_result)
        cdo_result = cdo_result.replace("'", "").split("\\n")[1].strip()
        cdo_result = cdo_result.replace("\n", "")
        cdo_result = cdo_result.split()
        cdo_result = list(set(cdo_result))
        cdo_result =  [int(v) for v in cdo_result]
        inter = [element for element in cdo_result if element in years]

        if len(inter) > 0:
            new_current.append(ff)
        if len(inter) == 0:
            n_removed+=1
            if ff in nc_safe:
                nc_safe.remove(ff)

        # figure out if any of the files actually have years outide the period required
        if len(inter) >0:
            if len([element for element in cdo_result if element not in years])  >0:
                missing_files+=1

    if len(new_current) == 0:
        raise ValueError("Data for none of the years is available!")

    if n_removed >0:
        warnings.warn(message = "A total of " +  str(n_removed) +  " files did not have valid years, so were removed from the dataset!")

    self.current = new_current


    if len(self.current) == 1:
        self.current = self.current[0]


    if missing_files >0:
        years = str_flatten(years, ",")

        cdo_command = "cdo -selyear," + years

        run_this(cdo_command, self,  output = "ensemble")

    cleanup()



def select_variables(self, vars = None):
    """
    Select variables from a dataset

    Parameters
    -------------
    months : list or int
        Month(s) to select.

    """


    if type(vars) is str:
        vars_list = [vars]
    else:
        vars_list = vars

    vars_list = str_flatten(vars_list, ",")

    cdo_command = "cdo -selname," + vars_list

    run_this(cdo_command, self,  output = "ensemble")


def select_timestep(self, times):
    """
    This method should probably be removed

    """

    if type(times) is range:
        times = list(times)

    if type(times) is not list:
        times = [times]
    # all of the variables in months need to be converted to ints, just in case floats have been provided

    times = [int(x) + 1 for x in times]
    times = [str(x) for x in times]
    times = str_flatten(times)

    cdo_command = "cdo -seltimestep," + times

    run_this(cdo_command, self,  output = "ensemble")



