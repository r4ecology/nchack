import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"



class TestPercentile:
    def test_crop(self):

        byes = []
        byes.append("time")
        byes.append(["month", "year"])
        byes.append(["day", "year"])
        byes.append(["day"])
        byes.append(["year"])
        byes.append(["month"])
        byes.append(["season"])
        byes.append(["season", "year"])

        for by in byes:

            data = nc.open_data(ff)

            data.percentile(p = 50, by = by)
            print(data.history)
            commands = data.history[0].split(" ")

            data = nc.open_data(ff)
            data.min(by = by)
            part1 = data.history[0].split(" ")[-1]

            data = nc.open_data(ff)
            data.max(by = by)
            part2 = data.history[0].split(" ")[-1]

            assert commands[4] == part1

            assert commands[6] == part2



