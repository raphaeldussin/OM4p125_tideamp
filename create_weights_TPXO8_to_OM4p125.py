#!/usr/bin/env python

import xarray as xr
import xesmf

domain='OM4p125'
TPXO='v8'

# get TPXO grid
tpxodir = '/net2/rnd/TPXO/'
if TPXO == 'v8':
    tpxo_gridfile = f'{tpxodir}/TPXO8/grid_tpxo8atlas_30.nc'
elif TPXO == 'v9':
    tpxo_gridfile = f'{tpxodir}/TPXO9/grid_tpxo9_atlas_30_v2.nc'

tpxo_grid = xr.open_dataset(tpxo_gridfile)
tpxo_grid = tpxo_grid.assign_coords({'lon_u': xr.DataArray(tpxo_grid['lon_u'], dims=['lon_u']),
                                     'lat_u': xr.DataArray(tpxo_grid['lat_u'], dims=['lat_u']),
                                     'lon_v': xr.DataArray(tpxo_grid['lon_v'], dims=['lon_v']),
                                     'lat_v': xr.DataArray(tpxo_grid['lat_v'], dims=['lat_v']),
                                     'lon_z': xr.DataArray(tpxo_grid['lon_z'], dims=['lon_z']),
                                     'lat_z': xr.DataArray(tpxo_grid['lat_z'], dims=['lat_z'])})

tpxo_grid['hz'] = tpxo_grid['hz'].rename({'nx': 'lon_z', 'ny': 'lat_z'})
tpxo_grid['hu'] = tpxo_grid['hu'].rename({'nx': 'lon_u', 'ny': 'lat_u'})
tpxo_grid['hv'] = tpxo_grid['hv'].rename({'nx': 'lon_v', 'ny': 'lat_v'})

tpxo_grid['mask'] = xr.where(tpxo_grid['hz'] >0, 1, 0).transpose(*('lat_z', 'lon_z'))
tpxo_grid = tpxo_grid.rename({'lon_z': 'lon', 'lat_z': 'lat'})

# get OM4 grid
if domain == 'OM4p25':
    OM4gridfile = '/archive/gold/datasets/OM4_025/mosaic.v20170622.unpacked/ocean_static.nc'
    OM4grid = xr.open_dataset(OM4gridfile)
    OM4grid = OM4grid.rename({'geolon': 'lon', 'geolat': 'lat'})
    OM4grid['mask'] = OM4grid['wet']
elif domain == 'OM4p125':
    OM4gridfile = '/work/Raphael.Dussin/inputfiles/OM4_125_Coupled_HighRes_WIP/grid/topog_merged.nc'
    OM4grid = xr.open_dataset(OM4gridfile)
    OM4grid = OM4grid.rename({'x': 'lon', 'y': 'lat'})
    OM4grid['mask'] = xr.where(OM4grid['depth'] > 0, 1, 0)

# Regridding step
wgtsfile=f'regrid_wgts_TPXO{TPXO}_{domain}.nc'
print(f"creating weights {wgtsfile}")

regrid = xesmf.Regridder(tpxo_grid, OM4grid, 'bilinear',
                         periodic=True, reuse_weights=False,
                         filename=wgtsfile)
