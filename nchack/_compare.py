from ._runthis import run_this
from ._runthis import run_nco
from ._temp_file import temp_file
from .flatten import str_flatten
from ._session import nc_safe
import subprocess




def fix_expr(expression):

    # equal constant case
    if expression.startswith("=="):
        if expression.replace("==", "").replace('.','',1).isdigit() == False:
            raise ValueError(expression + " is not valid!")
        expression = expression.replace("==", "eqc")
        expression = expression.replace("eqc", "eqc,")
        return expression

    # not equal constant case
    if expression.startswith("!="):
        if expression.replace("!=", "").replace('.','',1).isdigit() == False:
            raise ValueError(expression + " is not valid!")
        expression = expression.replace("!=", "nec")
        expression = expression.replace("nec", "nec,")
        return expression

    # less than or equal to constant case
    if expression.startswith("<="):
        if expression.replace("<=", "").replace('.','',1).isdigit() == False:
            raise ValueError(expression + " is not valid!")
        expression = expression.replace("<=", "lec")
        expression = expression.replace("lec", "lec,")
        return expression

    # less than or equal to constant case
    if expression.startswith("<"):
        if expression.replace("<", "").replace('.','',1).isdigit() == False:
            raise ValueError(expression + " is not valid!")
        expression = expression.replace("<", "ltc")
        expression = expression.replace("ltc", "ltc,")
        return expression

    # greater than or equal to constant case
    if expression.startswith(">="):
        if expression.replace(">=", "").replace('.','',1).isdigit() == False:
            raise ValueError(expression + " is not valid!")
        expression = expression.replace(">=", "gec")
        expression = expression.replace("gec", "gec,")
        return expression

    # greater than or equal to constant case
    if expression.startswith(">"):
        if expression.replace(">", "").replace('.','',1).isdigit() == False:
            raise ValueError(expression + " is not valid!")
        expression = expression.replace(">", "gtc")
        expression = expression.replace("gtc", "gtc,")
        return expression


    raise ValueError(expression + " is not valid!")


def compare_all(self, expression, cores = 1): 
    """
    Compare all variables to a constant

    Parameters
    -------------
    expression: str
        This a regular comparison such as "<0", ">0", "==0"

    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 
    """

    expression = fix_expr(expression)
    cdo_command = "cdo -" + expression
    run_this(cdo_command, self, output = "ensemble", cores = cores)






   