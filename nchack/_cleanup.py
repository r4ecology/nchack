
import os
import glob
import sys
import copy

from ._filetracker import nc_created
from ._filetracker import nc_safe
from ._remove import nc_remove

# keep is a file you do not want to delete

def cleanup(keep = None):
    """Function to remove temporary files created that are no longer in use"""

    # Step 1 is to find the files we potentially need to delete
    # These are files that we know nchack has either created or would attempt to create after
    # operation failure
    # It also finds temp files generated by ncea that are still on the system

    candidates = copy.deepcopy(nc_created)
    # nc_created needs to only be files on the system for speed purposes
    for x in candidates:
        if os.path.exists(x) == False:
            nc_created.remove(x)

    mylist = [f for f in glob.glob("/tmp/" + "*.nc*")]
    mylist = mylist + [f for f in glob.glob("/var/tmp/" + "*.nc*")]
    mylist = mylist + [f for f in glob.glob("/usr/tmp/" + "*.nc*")]

    other_files = []
    for ff in mylist:
        for cc in candidates:
            if cc in ff:
                other_files.append(ff)
      
    candidates = list(set(candidates + other_files))
    candidates = [x for x in candidates if os.path.exists(x)]
    candidates

    # Step 2 is to find the trackers in the locals
    
    valid_files = []
    valid_files = valid_files + nc_safe
    objects = dir(sys.modules["__main__"])
    for i in ([v for v in objects if not v.startswith('_')]):
        i_class = str(eval("type(sys.modules['__main__']." +i + ")"))
        if "NCTracker" in i_class and "List" not in i_class:
            i_current =eval("sys.modules['__main__']." +i + ".current")
            i_start = eval("sys.modules['__main__']." +i + ".start")
            # add the current files to valid_files
            if type(i_current) is str:
                valid_files.append(i_current)
            else:
                for ff in i_current:
                    valid_files.append(ff)

            # add the start files to valid_files
            if type(i_start) is str:
                if i_start not in nc_created:
                    valid_files.append(i_start)
            else:
                for ff in i_start:
                    if ff not in nc_created:
                        valid_files.append(ff)

            i_grid = eval("sys.modules['__main__']." +i + ".grid")
            i_weights = eval("sys.modules['__main__']." +i + ".weights")
            if i_grid is not None:
                valid_files.append(i_grid)
                valid_files.append(i_weights)
    valid_files = list(set(valid_files))

    delete_these = [v for v in candidates if v not in valid_files]            
    if keep is not None:
        if type(keep) is str:
            keep = (keep)
        delete_these = [v for v in delete_these if v not in keep]            

    delete_these = set(delete_these)
    delete_these = list(delete_these)

    # finally, to be ultra-safe, we will make sure all of the files to be deleted are in the temporary folder

    delete_these = [v for v in delete_these if v.startswith("/tmp/") or v.startswith("/var/tmp/") or v.startswith("/usr/tmp/")]
    
    for dd in delete_these:
        if os.path.exists(dd):
            nc_remove(dd)
    



def clean_all():
    """Function to remove all temporary files created"""

    # Step 1 is to find the files we potentially need to delete
    # These are files that we know nchack has either created or would attempt to create after
    # operation failure
    # It also finds temp files generated by ncea that are still on the system

    candidates = nc_created
    mylist = [f for f in glob.glob("/tmp/" + "*.nc*")]
    mylist = mylist + [f for f in glob.glob("/var/tmp/" + "*.nc*")]
    mylist = mylist + [f for f in glob.glob("/usr/tmp/" + "*.nc*")]
    other_files = []
    for ff in mylist:
        for cc in candidates:
            if cc in ff:
                other_files.append(ff)
      
    candidates = list(set(candidates + other_files))
    candidates = [x for x in candidates if os.path.exists(x)]
    candidates
    delete_these = set(candidates)
    delete_these = list(delete_these)

    # finally, to be ultra-safe, we will make sure all of the files to be deleted are in a temporary folder

    delete_these = [v for v in delete_these if v.startswith("/tmp/") or v.startswith("/var/tmp/") or v.startswith("/usr/tmp/")]

    for dd in delete_these:
        if os.path.exists(dd):
            nc_remove(dd)
    

def deep_clean():
    """
    Function to do a deep clean of all temporary files ever created by nchack
    """
    mylist = [f for f in glob.glob("/tmp/" + "*.nc*")]
    mylist = mylist + [f for f in glob.glob("/var/tmp/" + "*.nc*")]
    mylist = mylist + [f for f in glob.glob("/usr/tmp/" + "*.nc*")]
    mylist = [f for f in mylist if "nchack" in f]
    for ff in mylist:
        os.remove(ff)

def temp_check():
    """
    Function to do a deep clean of all temporary files ever created by nchack
    """
    mylist = [f for f in glob.glob("/tmp/" + "*.nc*")]
    mylist = mylist + [f for f in glob.glob("/var/tmp/" + "*.nc*")]
    mylist = mylist + [f for f in glob.glob("/usr/tmp/" + "*.nc*")]
    mylist = [f for f in mylist if "nchack" in f]
    if len(mylist) > 0:
        if len(mylist) == 1:
            print(str(len(mylist)) +  " file was created by nchack in prior or current sessions. Consider running deep_clean!")
        else:
            print(str(len(mylist)) +  " files were created by nchack in prior or current sessions. Consider running deep_clean!")












