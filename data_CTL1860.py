#!/usr/bin/env python
import os, os.path, datetime
import xarray as xr
import pandas as pd

dirin = '/tigress/wenchang/MODEL_OUT/PIctl_CMIP6volc/POSTP'
year_shift = 1859
ens_default = range(1,31)

def open_data(data_name=None, nctag='atmos_month', year_start=1, n_years=201):
    ncfiles = [os.path.join(dirin, f'{year:04d}0101.{nctag}.nc') for year in range(year_start, year_start + n_years)]
    ds = xr.open_mfdataset(ncfiles)
    if data_name is None:
        return ds
    da = ds[data_name]
    time = da['time'].values
    time_new = [datetime.datetime(*t.replace(year=t.year+year_shift).timetuple()[0:6]) for t in time]
    da['time'] = time_new

    return da.resample(time='MS').mean('time')

def open_ensemble(data_name, nctag='atmos_month', ens=None, year_start_ens1=51, n_years=3, year_volcano=1963):
    if ens is None:
        ens = ens_default
    das = []
    for en in ens:
        year_start = year_start_ens1 -1 + en
        da = open_data(data_name, nctag=nctag, year_start=year_start, n_years=3)
        da['time'] = da['time'].to_index().shift(12*(year_volcano - year_start - year_shift), 'MS')
        das.append(da)

    dae = xr.concat(das, pd.Index(ens, name='en'))

    return dae

if __name__ == '__main__':
    ds = open_data()
    print(ds)
