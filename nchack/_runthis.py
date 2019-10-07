import os
import copy
import tempfile
import multiprocessing
import math

from ._filetracker import nc_created
from .flatten import str_flatten


def split_list(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


def run_it(command, target):
    os.system(command)
    if os.path.exists(target) == False:
        raise ValueError(command + " was not successful. Check output")
    return target

def run_this(os_command, self, silent = False, output = "one", cores = 1, n_operations = 1):

    """Method to run an nco/cdo system command and check output was generated"""
    # Works on multiple files
    run = self.run
    # Step one

    # Step 2: run the system command
    
    if run == False:
        self.history.append(os_command)

    if run:

        if type(self.current) is str:
            if os.path.exists(self.current) == False:
                raise ValueError("The file " + self.current + " does not exist!")
            # single file case
            if silent:
                os_command = os_command.replace("cdo ", "cdo -s ")

            target = tempfile.NamedTemporaryFile().name + ".nc"
            target = target.replace("tmp/", "tmp/nchack")
            nc_created.append(target)
            os_command = os_command + " " + self.current + " " + target

            run_history = [x for x in self.history if x.endswith(".nc")]
            self.history = copy.deepcopy(run_history)
            self.history.append(os_command)

            os.system(os_command)
            
            # check the file was actually created
            # Raise error if it wasn't

            if os.path.exists(target) == False:
                raise ValueError(os_command + " was not successful. Check output")
            self.current = target
        else:
            # multiple file case

            if output == "one":
                
                if n_operations > 128:
                    read = os.popen("cdo --operators").read()
                    cdo_methods = [x.split(" ")[0] for x in read.split("\n")]
                    cdo_methods = [mm for mm in cdo_methods if len(mm) > 0]

                    # mergetime case
                    # operations after merging need to be chunked by file
                    
                    if "mergetime " in os_command or "merge " in os_command:

                        if "mergetime " in os_command:
                            merge_op = "mergetime "

                        if "merge " in os_command:
                            merge_op = "merge "
                        
                        post_merge = 0
                        for x in os_command.split(merge_op)[0].split(" "):
                            for y in x.split(","):
                                if y.replace("-", "") in cdo_methods:
                                    post_merge +=1
                        n_files = len(self.current)
                        n_split = n_operations - post_merge - 1
                        max_split = 127 - post_merge
                        file_chunks = split_list(self.current, math.ceil(n_split / max_split) + 1)
                        
                        os_commands = []
                        start_chunk = os_command.split(merge_op)[1]
                        tracker = 0
                        targets = []
                        for cc in file_chunks:
                            end_file = file_chunks[tracker][-1]
                            tracker+=1
                            
                            os_commands.append(start_chunk.split(end_file)[0] + " " + end_file)
                            start_chunk = start_chunk.split(end_file)[1] 
                        
                        for x in os_commands:
                            target = tempfile.NamedTemporaryFile().name + ".nc"
                            target = target.replace("tmp/", "tmp/nchack")
                            a_command = "cdo -L -" + merge_op + x + " " + target
                            nc_created.append(target)
                            os.system(a_command)
                            
                            if os.path.exists(target) == False:
                                raise ValueError(a_command + " was not successful. Check output")
                            self.history.append(a_command)
                            targets.append(target)

                        target = tempfile.NamedTemporaryFile().name + ".nc"
                        target = target.replace("tmp/", "tmp/nchack")
                        a_command = "cdo -L -" + merge_op +  str_flatten(targets, " ") + " " + target
                        nc_created.append(target)
                        os.system(a_command)
                            
                        if os.path.exists(target) == False:
                            raise ValueError(a_command + " was not successful. Check output")
                        self.history.append(a_command)
                        
                        if post_merge > 0:
                            post_merge = os_command.split(merge_op)[0] + " " 
                            out_file  = tempfile.NamedTemporaryFile().name + ".nc"
                            out_file = out_file.replace("tmp/", "tmp/nchack")
                            nc_created.append(out_file)

                            post_merge = post_merge.replace(" - ", " ") + target + " " + out_file
                            os.system(post_merge)
                            if os.path.exists(out_file) == False:
                                raise ValueError(post_merge + " was not successful. Check output")
                            self.history.append(post_merge)
                            self.current = out_file
                        else:
                            self.current = target
                        return None
                
        
                    if "merge " in os_command:
                        if n_operations > 128:
                            raise ValueError("More than 128 operations have been chained")

                for ff in self.current:
                    if os.path.exists(ff) == False:
                        raise ValueError("The file " + ff + " does not exist!")

                if silent:
                    ff_command = os_command.replace("cdo ", "cdo -s ")
                else:
                    ff_command = copy.deepcopy(os_command)

                target = tempfile.NamedTemporaryFile().name + ".nc"
                target = target.replace("tmp/", "tmp/nchack")
                nc_created.append(target)
                flat_ensemble = str_flatten(self.current, " ")
                if (self.merged == False) or (".nc" not in ff_command):
                    ff_command = ff_command + " " + flat_ensemble + " " + target
                else:
                    ff_command = ff_command + " "  + target

                run_history = copy.deepcopy(self.history)
                run_history = [x for x in run_history if x.endswith(".nc")]
                self.history = copy.deepcopy(run_history)

                if "merge" in ff_command:
                    ff_command = ff_command.replace(" merge ", " -merge ")
                    ff_command = ff_command.replace(" mergetime ", " -mergetime ")
                    #ff_command = ff_command.replace("cdo ", "cdo -z zip ")
                    ff_command = ff_command.replace(" -s ", " ")
                    ff_command = ff_command.replace("cdo ", "cdo -s ")

                self.history.append(ff_command)
                os.system(ff_command)
                
                # check the file was actually created
                # Raise error if it wasn't

                if os.path.exists(target) == False:
                    raise ValueError(ff_command + " was not successful. Check output")
                self.current = target

            else:
                if cores == 1:
                    target_list = []
                    for ff in self.current:
                    
                        if os.path.exists(ff) == False:
                            raise ValueError("The file " + ff + " does not exist!")
                        if silent:
                            ff_command = os_command.replace("cdo ", "cdo -s ")
                        else:
                            ff_command = copy.deepcopy(os_command)

                        target = tempfile.NamedTemporaryFile().name + ".nc"
                        target = target.replace("tmp/", "tmp/nchack")
                        nc_created.append(target)
                        ff_command = ff_command + " " + ff + " " + target

                        self.history.append(ff_command)
                        os.system(ff_command)
                        
                        # check the file was actually created
                        # Raise error if it wasn't

                        if os.path.exists(target) == False:
                            raise ValueError(ff_command + " was not successful. Check output")
                        target_list.append(target) 

                    self.current = copy.deepcopy(target_list)

                else:
                # multi-core case

                    pool = multiprocessing.Pool(cores)
                    target_list = []
                    results = dict()
                    for ff in self.current:
                    
                        if silent:
                            ff_command = os_command.replace("cdo ", "cdo -s ")
                        else:
                            ff_command = copy.deepcopy(os_command)

                        target = tempfile.NamedTemporaryFile().name + ".nc"
                        target = target.replace("tmp/", "tmp/nchack")
                        nc_created.append(target)
                        ff_command = ff_command + " " + ff + " " + target

                        self.history.append(ff_command)
                        temp = pool.apply_async(run_it,[ff_command, target])
                        results[ff] = temp 

                    pool.close()
                    pool.join()
                    new_current = []
                    for k,v in results.items():
                        target_list.append(v.get())

                    self.current = copy.deepcopy(target_list)


    else:
        # Now, if this is not a cdo command we need throw an error

        if os_command.strip().startswith("cdo") == False:
            raise ValueError("You can only use cdo commands in hold mode")
        # Now, we need to throw an error if the command is generating a grid
        
#        commas = [x for x in os_command.split(" ") if "," in x]
#        commas = "".join(commas)
#        if "gen" in commas:
#            raise ValueError("You cannot generate weights as part of a chain!")
#


