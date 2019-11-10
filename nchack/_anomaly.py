
from ._temp_file import temp_file
from ._session import nc_safe
from ._runthis import run_cdo

def annual_anomaly(self,  baseline = None):
    """

    Calculate annual anomalies based on a baseline period
    The anomoly is calculated by first calculating the climatological mean for the given baseline period. Annual means are then calculated for each year and the anomaly is calculated compared with the baseline mean.
    
    Parameters
    -------------
    baseline: list
        Baseline years. This needs to be the first and last year of the climatological period, Example [1985,2005] will give you a 20 year climatology from 1986 to 2005. 

    """

    # release if set to lazy

    if self.run == False:
        lazy_eval = True
        self.release()
    else:
        lazy_eval = False

    if type(self.current) is not str:
        raise ValueError("Splitting the file by year did not work!")

    if type(baseline) is not list:
        raise ValueError("baseline years supplied is not a list")

    if len(baseline) > 2:
        raise ValueError("More than 2 years in baseline. Please check.")
    if type(baseline[0]) is not int:
        raise ValueError("Provide a valid baseline")
    if type(baseline[1]) is not int:
        raise ValueError("Provide a vaid baseline")

    target = temp_file("nc")

    cdo_command = "cdo -L sub -yearmean " + self.current + " -timmean -selyear," + str(baseline[0]) + "/" + str(baseline[1]) + " " + self.current  + " " + target

    target = run_cdo(cdo_command, target)

    self.history.append(cdo_command)

    if self.current in nc_safe:
        nc_safe.remove(self.current)

    self.current = target
    nc_safe.append(target)


    if lazy_eval:
        self.run = False


