import glob
import os
import shutil
import platform
import tempfile

from nctoolkit.remove import nc_remove
from nctoolkit.session import session_info, nc_safe, temp_dirs

# keep is a file you do not want to delete


def cleanup():
    """
    Temp file cleaner

    Remove all files created during the session that are now out of use

    """

    # Step 1 is to find the files we potentially need to delete
    # These are files that we know nctoolkit has either created
    # or would attempt to create after
    # operation failure
    # It also finds temp files generated by ncea that are still on the system

    candidates = []

    for directory in temp_dirs:
        mylist = [f for f in glob.glob(f"{directory}/*")]
        mylist = [f for f in mylist if session_info["stamp"] in f]
        for ff in mylist:
            candidates.append(ff)

    candidates = list(set(candidates))
    candidates = [x for x in candidates if os.path.exists(x)]

    valid_files = nc_safe

    delete_these = [v for v in candidates if v not in valid_files]

    delete_these = list(set(delete_these))

    # finally, to be ultra-safe, we will make sure all of
    # the files to be deleted are in the temporary folder

    delete_these = [x for x in delete_these if os.path.exists(x)]

    if len(delete_these) == 0:
        return None

    for dd in delete_these:
        if os.path.exists(dd):
            nc_remove(dd)

    # only update the session size on linux
    if platform.system() == "Linux":
        result = os.statvfs("/tmp/")
        result = result.f_frsize * result.f_bavail
        if result > session_info["size"]:
            if session_info["temp_dir"] == "/var/tmp/":
                session_info["temp_dir"] = "/tmp/"
        session_info["size"] = result

        if session_info["size"] > (1.5 * session_info["latest_size"]):
            session_info["temp_dir"] = "/tmp/"


def clean_all():
    """
    Remove all temporary files created by nctoolkit in the present session
    """

    # Step 1 is to find the files we potentially need to delete
    # These are files that we know nctoolkit has either created
    # or would attempt to create after
    # operation failure
    # It also finds temp files generated by ncea that are still on the system

    candidates = []
    for directory in temp_dirs:
        mylist = [f for f in glob.glob(f"{directory}/*")]
        mylist = [f for f in mylist if session_info["stamp"] in f]
        for ff in mylist:
            candidates.append(ff)

    candidates = list(set(candidates))
    candidates = [x for x in candidates if os.path.exists(x)]
    candidates
    delete_these = set(candidates)
    delete_these = list(delete_these)

    # finally, to be ultra-safe, we will make sure all of the
    # files to be deleted are in a temporary folder

    for dd in delete_these:
        if os.path.exists(dd):
            nc_remove(dd, deep=True)


def deep_clean():
    """
    Deep temp file cleaner
    Remove all temporary files ever created by nctoolkit
    across all previous and current sesions
    """

    candidates = []
    for directory in temp_dirs:
        mylist = [f for f in glob.glob(f"{directory}/*")]
        for ff in mylist:
            candidates.append(ff)

    mylist = [f for f in candidates if "nctoolkit" in f]
    for ff in mylist:
        nc_remove(ff, deep=True)


def temp_check():
    """
    Function to check temp files
    """

    if platform.system() == "Linux":
        mylist = [f for f in glob.glob("/tmp/*")]
        mylist = mylist + [f for f in glob.glob("/var/tmp/*")]
        mylist = mylist + [f for f in glob.glob("/usr/tmp/*")]
        mylist = [f for f in mylist if "nctoolkit" in f]

        if len(mylist) > 0:
            if len(mylist) == 1:
                print(
                    f"{len(mylist)} file was created by nctoolkit in prior or current "
                    f"sessions. Consider running deep_clean!"
                )
            else:
                print(
                    f"{len(mylist)} files were created by nctoolkit in prior or current"
                    f" sessions. Consider running deep_clean!"
                )

    else:

        temp_folder = tempfile.gettempdir()

        mylist = [f for f in glob.glob(f"{temp_folder}/*")]
        mylist = [f for f in mylist if "nctoolkit" in f]

        if len(mylist) > 0:
            if len(mylist) == 1:
                print(
                    f"{len(mylist)} file was created by nctoolkit in prior or current "
                    f"sessions. Consider running deep_clean!"
                )
            else:
                print(
                    f"{len(mylist)} files were created by nctoolkit in prior or "
                    f"current sessions. Consider running deep_clean!"
                )


def disk_clean(self):
    """
    Method to make sure /tmp is not clogged up after running an operation
    """

    # only use this on linux
    if platform.system() == "Linux":

        # get files as a list

        if type(self.current) is str:
            ff_list = [self.current]
        else:
            ff_list = self.current

        # First step is to figure out how much space is in /tmp
        # Do nothing if it is less than 0.5 GB

        if session_info["temp_dir"] == "/tmp/":
            result = os.statvfs("/tmp/")
            result = result.f_frsize * result.f_bavail

            if result > 0.5 * 1e9:
                return None

        if session_info["temp_dir"] not in  ["/tmp/", "/var/tmp", "/usr/tmp"]:
            return None

        # at this point we want to change the temp dir,
        # though it probably has been already
        session_info["temp_dir"] = "/var/tmp/"
        # get a list of the new file names

        # loop through the existing ones
        for ff in ff_list:
            # check if the file is in /var/tmp
            # if it is, keep it that way
            # check the space remaining the /tmp
            result = os.statvfs("/tmp/")
            result = result.f_frsize * result.f_bavail
            # if there is less than 0.5 GB left, move the file to /var/tmp
            if result < 0.5 * 1e9:
                if ff.startswith("/tmp/"):
                    new_ff = ff.replace("/tmp/", "/var/tmp/")
                    nc_safe.append(new_ff)
                    nc_safe.remove(ff)
                    shutil.copyfile(ff, new_ff)
                    self.current = [
                        new_ff if file == ff else file for file in self.current
                    ]

        if type(self.current) is list:
            self.current = self.current
        else:
            self.current = self.current[0]

        cleanup()
