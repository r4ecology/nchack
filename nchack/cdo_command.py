
import subprocess
from .flatten import str_flatten
from .runthis import run_this

def cdo_command(self, command):
    """
    Apply a cdo command

    Parameters
    -------------
    command : string
        cdo command to call. This must be of the form cdo command infile outfile, where cdo, infile and outfile are attached later.
    """

    # First, check that the command is valid

    if type(command) is not str:
        raise TypeError("Command supplied is not a str")

    read = subprocess.run("cdo --operators", shell = True,stdout=subprocess.PIPE,  stderr = subprocess.PIPE).stdout

    cdo_methods = [x.split(" ")[0].replace("b'", "") for x in str(read).split("\\n")]

    cdo_methods = [mm for mm in cdo_methods if len(mm) > 0]

    n_methods = 0

    for x in command.split(" "):
        y = x.split(",")[0].replace("-", "")
        if y not in cdo_methods:
            raise ValueError("You have supplied an invalid cdo method:" + y )

    # remove cdo from the command
    if command.startswith("cdo "):
        command = command.replace("cdo ", " ")

    cdo_command = "cdo " + command + " "

    if "merge " in command or "mergetime " in command:
        output = "one"

    for mm in cdo_methods:
        if " " + mm + " " in cdo_command:
            cdo_command = cdo_command.replace(" " + mm + " ", " -" + mm + " ")

        if " " + mm + "," in cdo_command:
            cdo_command = cdo_command.replace(" " + mm + ","," -" + mm + ",")

    run_this(cdo_command, self, output = "ensemble")

