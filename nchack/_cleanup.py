
import os
import glob
import sys

from ._filetracker import nc_created

# keep is a file you do not want to delete

def cleanup(keep = None):
    """Function to remove temporary files created that are no longer in use"""

    # Step 1 is to find the files we potentially need to delete
    # These are files that we know nchack has either created or would attempt to create after
    # operation failure
    # It also finds temp files generated by ncea that are still on the system

    temp_dir = "/tmp/"
    candidates = nc_created
    mylist = [f for f in glob.glob(temp_dir + "*.nc*")]
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
    objects = dir(sys.modules["__main__"])
    for i in ([v for v in objects if not v.startswith('_')]):
        i_class = str(eval("type(sys.modules['__main__']." +i + ")"))
        if "NCTracker" in i_class:
            i_current =eval("sys.modules['__main__']." +i + ".current")
            i_start =eval("sys.modules['__main__']." +i + ".start")
            if i_current != i_start:
                valid_files.append(i_current)
    
    delete_these = [v for v in candidates if v not in valid_files]            
    if keep is not None:
        delete_these = [v for v in delete_these if v != keep]            

    delete_these = set(delete_these)
    delete_these = list(delete_these)

    
    for dd in delete_these:
        os.remove(dd)
    
