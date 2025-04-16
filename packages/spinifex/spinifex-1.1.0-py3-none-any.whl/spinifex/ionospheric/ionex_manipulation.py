"""Module of ionex manipulation tools"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np
from astropy.time import Time
from numpy.typing import NDArray

from spinifex.geometry.get_ipp import IPP
from spinifex.ionospheric.index_tools import (
    compute_index_and_weights,
    get_indices_axis,
)
from spinifex.ionospheric.ionex_download import (
    IonexOptions,
    _download_ionex,
)
from spinifex.ionospheric.ionex_parser import (
    IonexData,
    read_ionex,
    unique_days_from_ionex_files,
)
from spinifex.times import get_indexlist_unique_days


class GroupedIPPs(NamedTuple):
    """Grouped IPPs"""

    ipps: list[IPP]
    indices: list[NDArray[np.int32]]


def interpolate_ionex(
    ionex: IonexData,
    lons: NDArray[np.float64],
    lats: NDArray[np.float64],
    times: Time,
    apply_earth_rotation: float = 1,
) -> NDArray[np.float64]:
    """Interpolate ionex data to a given lon/lat/height grid.
    lons, lats, times all should have the same length

    apply_earth_rotation:
    This is assuming that the TEC maps move according to the rotation
    Earth (following method 3 of interpolation described in the IONEX
    document). Experiments with high time resolution ROB data show that
    this is not really the case, resulting in strange wavelike structures
    when applying this smart interpolation.

    Parameters
    ----------
    ionex : IonexData
        ionex object containing the information of the ionex file
    lons : NDArray
        longitudes (deg) of all points to interpolate to
    lats : NDArray
        lattitudes (deg) of all points to interpolate to
    times : Time
        times of all points to interpolate to
    apply_earth_rotation : float, optional
        specify (with a number between 0 and 1) how much of the earth rotation
        is taken in to account in the interpolation step., by default 1

    Returns
    -------
    NDArray
        array with interpolated tec values
    """
    timeindex = compute_index_and_weights(ionex.times.mjd, times.mjd)
    latindex = compute_index_and_weights(ionex.lats, lats)
    # take into account earth rotation
    if apply_earth_rotation > 0:
        rot1 = (
            (times.mjd - ionex.times.mjd[timeindex.idx1]) * 360.0
        ) * apply_earth_rotation
        rot2 = (
            (times.mjd - ionex.times.mjd[timeindex.idx2]) * 360.0
        ) * apply_earth_rotation
        lonindex1 = get_indices_axis(lons + rot1, ionex.lons, wrap_unit=360)
        lonindex2 = get_indices_axis(lons + rot2, ionex.lons, wrap_unit=360)
    else:
        lonindex1 = get_indices_axis(lons, ionex.lons, wrap_unit=360)
        lonindex2 = lonindex1
    tecdata = (
        ionex.tec[timeindex.idx1, lonindex1.idx1, latindex.idx1]
        * lonindex1.w1
        * timeindex.w1
        * latindex.w1
    )
    tecdata += (
        ionex.tec[timeindex.idx1, lonindex1.idx2, latindex.idx1]
        * lonindex1.w2
        * timeindex.w1
        * latindex.w1
    )

    tecdata += (
        ionex.tec[timeindex.idx2, lonindex2.idx1, latindex.idx1]
        * lonindex2.w1
        * timeindex.w2
        * latindex.w1
    )
    tecdata += (
        ionex.tec[timeindex.idx2, lonindex2.idx2, latindex.idx1]
        * lonindex2.w2
        * timeindex.w2
        * latindex.w1
    )

    tecdata += (
        ionex.tec[timeindex.idx1, lonindex1.idx1, latindex.idx2]
        * lonindex1.w1
        * timeindex.w1
        * latindex.w2
    )
    tecdata += (
        ionex.tec[timeindex.idx1, lonindex1.idx2, latindex.idx2]
        * lonindex1.w2
        * timeindex.w1
        * latindex.w2
    )

    tecdata += (
        ionex.tec[timeindex.idx2, lonindex2.idx1, latindex.idx2]
        * lonindex2.w1
        * timeindex.w2
        * latindex.w2
    )
    tecdata += (
        ionex.tec[timeindex.idx2, lonindex2.idx2, latindex.idx2]
        * lonindex2.w2
        * timeindex.w2
        * latindex.w2
    )
    return tecdata


def get_density_ionex(
    ipp: IPP, ionex_options: IonexOptions | None = None
) -> NDArray[np.float64]:
    """read ionex files and interpolate values to ipp locations/times

    Parameters
    ----------
    ipp : IPP
        ionospheric piercepoints
    ionex_options : IonexOptions, optional
        optional arguments for the ionospheric model, by default None

    Returns
    -------
    NDArray
        array with tec values for every entry in ipp

    Raises
    ------
    FileNotFoundError
        if ionex file cannot be downloaded
    """
    # TODO: apply_earth_rotation as option
    sorted_ionex_paths = _download_ionex(times=ipp.times, options=ionex_options)

    unique_days = unique_days_from_ionex_files(sorted_ionex_paths)
    if not unique_days.shape:
        ionex = read_ionex(sorted_ionex_paths[0])
        return interpolate_ionex(ionex, ipp.loc.lon.deg, ipp.loc.lat.deg, ipp.times)
    group_indices = get_indexlist_unique_days(unique_days, ipp.times)
    tec = np.zeros(ipp.loc.shape, dtype=float)
    for indices, ionex_file in zip(group_indices, sorted_ionex_paths):
        if not ionex_file.exists():
            msg = f"Ionex file {ionex_file} not found!"
            raise FileNotFoundError(msg)
        u_loc = ipp.loc[indices]
        u_times = ipp.times[indices]
        ionex = read_ionex(ionex_file)
        tec[indices] = interpolate_ionex(ionex, u_loc.lon.deg, u_loc.lat.deg, u_times)

    return tec
