
from .runthis import run_this
import sys
import inspect



def transmute(self, operations = None):
    """
    Create new variables using mathematical expressions, and drop original variables

    Parameters
    -------------
    operations : dict
        operations to apply. The keys are the new variables to generate. The values are the mathematical operations to carry out.

    """

    method = "expr"

    if type(operations) is not dict:
        raise TypeError("No expression was provided")

    # first,we need to convert the operations dictionary to a cdo expression

    expr = []

    for key,value in operations.items():

        new_x = ''.join((' {} '.format(el) if el in '=><+-/*^()' else el for el in value))
        expr_split = new_x.split(" ")
        new_expr = ""

        for x in expr_split:
            if x.startswith("@"):
                # We need to first check the local variable supplied is a numeric
                new_x = inspect.currentframe().f_back.f_locals[x.replace("@", "")]
                if isinstance(new_x, (int, float)) == False:
                    raise TypeError(x +  " is not numeric!")
                new_expr +=  str(new_x)
            else:
                new_expr +=  x

        expr.append(key + "=" + new_expr)


    expr = ";".join(expr)
    expr = expr.replace(" ", "" )
    expr = '"' + expr + '"'


    cdo_command = "cdo -" + method + "," + expr
    run_this(cdo_command, self, output = "ensemble")

def mutate(self, operations = None):
    """
    Create new variables using mathematical expressions, and keep original variables

    Parameters
    -------------
    operations : dict
        operations to apply. The keys are the new variables to generate. The values are the mathematical operations to carry out.

    """

    method = "aexpr"

    if type(operations) is not dict:
        raise TypeError("No expression was provided")

    # first,we need to convert the operations dictionary to a cdo expression

    expr = []

    for key,value in operations.items():

        new_x = ''.join((' {} '.format(el) if el in '=><+-/*^()' else el for el in value))
        expr_split = new_x.split(" ")
        new_expr = ""

        for x in expr_split:
            if x.startswith("@"):
                # We need to first check the local variable supplied is a numeric
                new_x = inspect.currentframe().f_back.f_locals[x.replace("@", "")]
                if isinstance(new_x, (int, float)) == False:
                    raise TypeError(x +  " is not numeric!")
                new_expr +=  str(new_x)
            else:
                new_expr +=  x

        expr.append(key + "=" + new_expr)


    expr = ";".join(expr)
    expr = expr.replace(" ", "" )
    expr = '"' + expr + '"'


    cdo_command = "cdo -" + method + "," + expr
    run_this(cdo_command, self, output = "ensemble")




