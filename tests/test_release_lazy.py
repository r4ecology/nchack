import unittest
import nctoolkit as nc
import pandas as pd
import xarray as xr
import os

nc.options(lazy = True)

ff = "data/sst.mon.mean.nc"

class Testrun(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_run(self):
        tracker = nc.open_data(ff)
        tracker.split(("year"))
        tracker.merge_time()
        tracker.select_timestep(0)
        tracker.spatial_mean()
        tracker.run()
        x = tracker.to_dataframe().sst.values[0]
        tracker = nc.open_data(ff)
        tracker.select_timestep(0)
        tracker.spatial_mean()
        tracker.run()
        y = tracker.to_dataframe().sst.values[0]

        self.assertEqual(x,y)

        n = len(nc.session_files())
        self.assertEqual(n, 1)

        tracker = nc.open_data(ff)
        tracker.mean()
        tracker._safe.append("asdfkjasdkfj.nc")
        nc.session.nc_safe.append("asdfkjasdkfj.nc")
        tracker.run()
        del tracker
        assert len(nc.session.nc_safe) == 0



if __name__ == '__main__':
    unittest.main()

