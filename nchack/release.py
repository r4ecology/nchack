from .runthis import run_this
from .session import session_info

def release(self,  run_merge = True):
    """
    Run all stored commands in a dataset

    Parameters
    -------------
    run_merge: boolean
        Ignore this for now. This needs to be replaced by the keywords arg method

    """

    # the first step is to set the run status to true

    if self._run == False and (len(self.history) > len(self._hold_history)):
        self._run = True

        if (len(self.history) > len(self._hold_history)) and session_info["thread_safe"] == False:
            cdo_command = "cdo -L"
        else:
            cdo_command = "cdo "
        if self._zip:
            cdo_command = cdo_command + " -z zip "
    #    cdo_command = "cdo -z zip "

        output_method = "ensemble"

        if self._merged:
            output_method = "one"

        run_this(cdo_command, self,  output = output_method)

        self._run = False
        self._zip = False




