import unittest
import nchack as nc
import pandas as pd
import xarray as xr
import os

nc.options(lazy = True)

ff = "data/sst.mon.mean.nc"

class TestRelease(unittest.TestCase):
    def test_empty(self):
        n = len(nc.session_files())
        self.assertEqual(n, 0)

    def test_release(self):
        tracker = nc.open_data(ff)
        tracker.split(("year"))
        tracker.merge_time()
        tracker.select_timestep(0)
        tracker.spatial_mean()
        tracker.release()
        x = tracker.to_dataframe().sst.values[0]
        tracker = nc.open_data(ff)
        tracker.select_timestep(0)
        tracker.spatial_mean()
        tracker.release()
        y = tracker.to_dataframe().sst.values[0]

        self.assertEqual(x,y)

        n = len(nc.session_files())
        self.assertEqual(n, 1)


if __name__ == '__main__':
    unittest.main()

