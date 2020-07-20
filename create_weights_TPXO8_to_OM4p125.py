#!/usr/bin/env python

import xarray as xr
import xesmf

# get TPXO grid
tpxodir = '/net2/rnd/TPXO/'
tpxo_gridfile = f'{tpxodir}/TPXO8/grid_tpxo8atlas_30.nc'
tpxo8_grid = xr.open_dataset(tpxo_gridfile)
tpxo8_grid = tpxo8_grid.assign_coords({'lon_u': xr.DataArray(tpxo8_grid['lon_u'], dims=['lon_u']),
                                       'lat_u': xr.DataArray(tpxo8_grid['lat_u'], dims=['lat_u']),
                                       'lon_v': xr.DataArray(tpxo8_grid['lon_v'], dims=['lon_v']),
                                       'lat_v': xr.DataArray(tpxo8_grid['lat_v'], dims=['lat_v']),
                                       'lon_z': xr.DataArray(tpxo8_grid['lon_z'], dims=['lon_z']),
                                       'lat_z': xr.DataArray(tpxo8_grid['lat_z'], dims=['lat_z'])})

tpxo8_grid['hz'] = tpxo8_grid['hz'].rename({'nx': 'lon_z', 'ny': 'lat_z'})
tpxo8_grid['hu'] = tpxo8_grid['hu'].rename({'nx': 'lon_u', 'ny': 'lat_u'})
tpxo8_grid['hv'] = tpxo8_grid['hv'].rename({'nx': 'lon_v', 'ny': 'lat_v'})

# get OM4p125 grid
OM4gridfile = '/work/Raphael.Dussin/inputfiles/OM4_125_Coupled_HighRes_WIP/grid/topog_merged.nc'
OM4grid = xr.open_dataset(OM4gridfile)

# Regridding step
OM4grid = OM4grid.rename({'x': 'lon', 'y': 'lat'})
tpxo8_grid = tpxo8_grid.rename({'lon_z': 'lon', 'lat_z': 'lat'})

print("creating weights")

regrid = xesmf.Regridder(tpxo8_grid, OM4grid, 'bilinear',
                         periodic=True, reuse_weights=False)
