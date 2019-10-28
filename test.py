import unittest
import nchack as nc
import pandas as pd
import xarray as xr
import os


class TestSelect(unittest.TestCase):

    def test_select(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1959))) 
        tracker.select_months([1,2,3,4,5])
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        tracker.annual_mean()
        tracker.mean()
        tracker.spatial_mean()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, 18.360414505004883)

    def test_lazy1(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.lazy()
        tracker.select_years(list(range(1950, 1959))) 
        tracker.select_months([1,2,3,4,5])
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        tracker.annual_mean()
        tracker.mean()
        tracker.spatial_mean()
        tracker.release()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        y = len(tracker.history)
        self.assertEqual(x, 18.360414505004883)
        self.assertEqual(y, 1)

    def test_split1(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.split_year()
        n_files = len(tracker.current)
        tracker.merge_time()
        tracker.select_years(list(range(1950, 1959))) 
        tracker.select_months([1,2,3,4,5])
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        tracker.annual_mean()
        tracker.mean()
        tracker.spatial_mean()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, 18.360414505004883)
        self.assertEqual(n_files, 169)


    def test_mergetime1(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.split_year()
        n_files = len(tracker.current)
        tracker.lazy()
        tracker.merge_time()
        tracker.select_years(list(range(1950, 1959))) 
        tracker.select_months([1,2,3,4,5])
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        tracker.annual_mean()
        tracker.mean()
        tracker.spatial_mean()
        tracker.release()
        y = len(tracker.history)
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, 18.360414505004883)
        self.assertEqual(n_files, 169)
        self.assertEqual(y, 2)

    def test_ensemble_mean_1(self):
        ff = nc.create_ensemble("data/ensemble/")
        tracker = nc.open_data(ff)
        tracker.mean()
        tracker.ensemble_mean()
        tracker.spatial_mean()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, 17.881811141967773)

    def test_transmute_1(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.lazy()
        tracker.transmute({"sst":"sst+273.15"})
        tracker.select_years(list(range(1950, 1959))) 
        tracker.select_months([1,2,3,4,5])
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        tracker.annual_mean()
        tracker.mean()
        tracker.spatial_mean()
        tracker.transmute({"sst":"sst-273.15"})
        tracker.release()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        y = len(tracker.history)
        self.assertEqual(x, 18.360414505004883)

    def test_mutate_1(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.lazy()
        tracker.mutate({"sst1":"sst+273.15"})
        tracker.select_years(list(range(1950, 1959))) 
        tracker.select_months([1,2,3,4,5])
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        tracker.annual_mean()
        tracker.mean()
        tracker.spatial_mean()
        tracker.transmute({"sst2":"sst1-273.15"})
        tracker.release()
        x = tracker.to_xarray().sst2.values[0][0][0].astype("float")
        y = len(tracker.history)
        self.assertEqual(x, 18.360414505004883)

    def test_seasonal_clim1(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.seasonal_mean_climatology()
        tracker.select_months(2)
        tracker.spatial_mean()
        x = tracker.to_xarray().sst.values[0][0][0].astype("float")
        self.assertEqual(x, 17.8525390625)

    def test_merge_rename(self):
        ff = "data/sst.mon.mean.nc"
        tracker1 = nc.open_data(ff)
        tracker2 = nc.open_data(ff)
        tracker2.rename({"sst": "tos"})
        tracker = nc.merge(tracker1, tracker2)
        tracker.transmute({"bias":"sst-tos"})
        tracker.mean()
        tracker.spatial_mean()
        x = tracker.to_xarray().bias.values[0][0][0].astype("float")
        self.assertEqual(x, 0)

    def test_anomaly(self):
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        tracker.select_years(list(range(1950, 1959)))
        tracker.select_months([1,2,3,4,5])
        tracker.clip(lon = [0,90])
        tracker.clip(lat = [0,90])
        tracker.annual_anomaly(baseline = list(range(1950, 1979)))
        x = (os.path.exists(tracker.current))
#        tracker.annual_mean()
#        tracker.spatial_mean()
#        tracker.mean()
#        x = tracker.to_xarray().anomaly.values[0][0][0].astype("float")
        self.assertEqual(x, True)
        #self.assertEqual(x, -8.278422947149977e-10)



if __name__ == '__main__':
    unittest.main()

