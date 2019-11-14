
import os
import copy

from ._runthis import run_this
from ._session import session_info

def release(self,  run_merge = True):
    """
    Run all stored commands in a dataset

    Parameters
    -------------
    run_merge: boolean
        Ignore this for now. This needs to be replaced by the keywords arg method

    """

    # the first step is to set the run status to true
    if self.run:
        return("Warning: dataset is in run mode. Nothing to release")
    if self.run == False and len(self.hold_history) == len(self.history):
        return("Warning: dataset is in run mode. Nothing to release")

    if self.run == False:
        self.run = True
        self.released = True

        if (len(self.history) > len(self.hold_history)) and session_info["thread_safe"] == False:
            cdo_command = "cdo -L"
        else:
            cdo_command = "cdo "

        output_method = "ensemble"

        if self.merged:
            output_method = "one"

        run_this(cdo_command, self,  output = output_method)
        self.released = False

        self.run = False



