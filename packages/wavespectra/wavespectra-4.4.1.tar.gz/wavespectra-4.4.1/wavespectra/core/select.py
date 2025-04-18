"""Interpolate stations."""

import logging

import numpy as np
import xarray as xr

from wavespectra.core.attributes import attrs, set_spec_attributes

logger = logging.getLogger(__name__)


class Coordinates:
    """Slicing of circular coordinates.

    Args:
        dset (xr.Dataset): Dataset object to slice from.
        lons (array): Longitudes to slice.
        lats (array): Latitudes to slice.
        sitename (str): Name of site dimension.
        lonname (str): Name of longitude coordinate.
        latname (str): Name of latitude coordinate.

    """

    def __init__(
        self,
        dset,
        lons,
        lats,
        sitename=attrs.SITENAME,
        lonname=attrs.LONNAME,
        latname=attrs.LATNAME,
    ):
        # Ensure arrays
        lons = lons if not np.isscalar(lons) else [lons]
        lats = lats if not np.isscalar(lats) else [lats]

        self.dset = dset
        self._lons = np.array(lons)
        self.lats = np.array(lats)
        self.sitename = sitename
        self.lonname = lonname
        self.latname = latname

        self.dset_lons = dset[self.lonname].values
        self.dset_lats = dset[self.latname].values

        self._validate()

        if self._is_360(self._lons) == self._is_360(self.dset_lons):
            self.consistent = True
        else:
            self.consistent = False

    def _validate(self):
        """Few input checks."""
        assert len(self._lons) == len(self.lats), "lons and lats must have same size."
        if (
            self.lonname in self.dset.dims
            or self.latname in self.dset.dims
            or self.sitename not in self.dset.dims
        ):
            raise NotImplementedError("sel only supports stations not gridded data.")

    def _is_180(self, array):
        """True if longitudes are in -180 -- 180 convention."""
        if array.min() < 0 and array.max() <= 180:
            return True
        return False

    def _is_360(self, array):
        """True if longitudes are in 0 -- 360 convention."""
        if array.min() >= 0 and array.max() <= 360:
            return True
        return False

    def _swap_longitude_convention(self, longitudes):
        """Swap longitudes between [0 <--> 360] and [-180 <--> 180] conventions."""
        if self._is_180(longitudes):
            return longitudes % 360
        elif self._is_360(longitudes):
            longitudes[longitudes > 180] = longitudes[longitudes > 180] - 360
        return longitudes

    @property
    def lons(self):
        """Longitudes to query, always in same convention as dataset."""
        if self._is_360(self._lons) == self._is_360(self.dset_lons):
            return self._lons
        else:
            return self._swap_longitude_convention(self._lons)

    def distance(self, lon, lat):
        """Distance between each station in (dset_lons, dset_lats) and site (lon, lat).

        Args:
            lon (float): Longitude to locate from lons.
            lat (float): Latitude to locate from lats.

        Returns:
            List of distances between each station and site.

        """
        dist = np.sqrt(
            (self.dset_lons % 360 - np.array(lon) % 360) ** 2
            + (self.dset_lats - np.array(lat)) ** 2
        )
        if isinstance(dist, xr.DataArray):
            dist = dist.values
        return np.abs(dist)

    def nearer(self, lon, lat, tolerance=np.inf, max_sites=None):
        """Nearer stations in (dset_lons, dset_lats) to site (lon, lat).

        Args:
            lon (float): Longitude of of station to locate from lons.
            lat (float): Latitude of of station to locate from lats.
            tolerance (float): Maximum distance for scanning neighbours.
            max_sites (int): Maximum number of neighbours.

        Returns:
            Indices and distances of up to `max_sites` neighbour stations not farther from
                `tolerance`, ordered from closer to farthest station.

        """
        dist = self.distance(lon, lat)
        closest_ids = np.argsort(dist)
        closest_dist = dist[closest_ids]
        keep_ids = closest_ids[closest_dist <= tolerance][:max_sites]
        return keep_ids, dist[keep_ids]

    def nearest(self, lon, lat):
        """Nearest station in (dset_lons, dset_lats) to site (lon, lat).

        Args:
            lon (float): Longitude to locate from lons.
            lat (float): Latitude to locate from lats.

        Returns:
            Index and distance of closest station.

        """
        dist = self.distance(lon, lat)
        closest_id = dist.argmin()
        closest_dist = dist[closest_id]
        return closest_id, closest_dist


def sel_nearest(
    dset,
    lons,
    lats,
    tolerance=2.0,
    unique=False,
    exact=False,
    missing="raise",
    sitename=attrs.SITENAME,
    lonname=attrs.LONNAME,
    latname=attrs.LATNAME,
):
    """Select sites from nearest distance.

    Args:
        dset (Dataset): Stations SpecDataset to select from.
        lons (array): Longitude of sites to interpolate spectra at.
        lats (array): Latitude of sites to interpolate spectra at.
        tolerance (float): Maximum distance to use site for interpolation.
        unique (bool): Only returns unique sites in case of repeated inexact matches.
        exact (bool): Require exact matches.
        missing (str): Action to take if no site is found within tolerance:
            - 'raise': raise an error
            - 'ignore': skip site
        sitename (str): Name of site dimension.
        lonname (str): Name of longitude coordinate.
        latname (str): Name of latitude coordinate.

    Returns:
        Selected SpecDataset at locations defined by (lons, lats).

    Note:
        Args `dset_lons`, `dset_lats` are not required but can improve performance when
        `dset` is chunked with site=1 (expensive to access station coordinates) and
        improve precision if projected coordinates are provided at high latitudes.

    """
    coords = Coordinates(
        dset, lons=lons, lats=lats, sitename=sitename, lonname=lonname, latname=latname
    )

    station_ids = []
    for lon, lat in zip(coords.lons, coords.lats):
        closest_id, closest_dist = coords.nearest(lon, lat)
        if closest_dist > tolerance:
            if missing == "raise":
                raise AssertionError(
                    f"Nearest site in dataset from ({lon, lat}) is {closest_dist:g} "
                    f"deg away but tolerance is {tolerance:g} deg"
                )
            elif missing == "ignore":
                logger.debug(
                    f"No site in dataset within tolerance={tolerance} deg "
                    f"from requested location ({lon, lat}), skipping"
                )
                continue
        if exact and closest_dist > 0:
            raise AssertionError(
                f"Exact match required but no site in dataset at ({lon, lat}), "
                f"nearest site is {closest_dist} deg away."
            )
        if unique and closest_id in station_ids:
            logger.debug(
                f"Nearest site at ({lon, lat}) is repeated, skipping "
                f"because unique=True"
            )
            continue
        station_ids.append(closest_id)
    if not station_ids:
        raise ValueError(
            f"No site in dataset found within tolerance={tolerance} deg of any site "
            f"{list(zip(coords.lons, coords.lats))}"
        )
    dsout = dset.isel(**{sitename: station_ids})

    # Return longitudes in the convention provided
    if coords.consistent is False:
        dsout.lon.values = coords._swap_longitude_convention(dsout.lon.values)

    dsout = dsout.assign_coords({sitename: np.arange(len(station_ids))})

    return dsout


def sel_idw(
    dset,
    lons,
    lats,
    tolerance=2.0,
    max_sites=4,
    sitename=attrs.SITENAME,
    lonname=attrs.LONNAME,
    latname=attrs.LATNAME,
):
    """Select sites from inverse distance weighting.

    Args:
        dset (Dataset): Stations SpecDataset to interpolate from.
        lons (array): Longitude of sites to interpolate spectra at.
        lats (array): Latitude of sites to interpolate spectra at.
        tolerance (float): Maximum distance to use site for interpolation.
        max_sites (int): Maximum number of neighbour sites to use for interpolation.
        sitename (str): Name of site dimension.
        lonname (str): Name of longitude coordinate.
        latname (str): Name of latitude coordinate.

    Returns:
        Selected SpecDataset at locations defined by (lons, lats).

    Note:
        Args `dset_lons`, `dset_lats` are not required but can improve performance when
            `dset` is chunked with site=1 (expensive to access station coordinates) and
            improve precision if projected coordinates are provided at high latitudes.

    """
    coords = Coordinates(
        dset, lons=lons, lats=lats, sitename=sitename, lonname=lonname, latname=latname
    )

    mask = dset.isel({sitename: 0}, drop=True) * np.nan
    dsout = []
    for lon, lat in zip(coords.lons, coords.lats):
        closest_ids, closest_dist = coords.nearer(lon, lat, tolerance, max_sites)
        if len(closest_ids) == 0:
            logger.debug(
                f"No stations within {tolerance} deg of site (lat={lat}, lon={lon}), "
                "this site will be masked."
            )
        # Collect ids and factors of neighbours
        indices = []
        factors = []
        for ind, dist in zip(closest_ids, closest_dist):
            indices.append(ind)
            if dist == 0:
                factors.append(1.0)
                break
            factors.append(1.0 / dist)
        # Mask it if not enough neighbours
        if len(indices) == 0 or (len(indices) == 1 and dist > 0):
            dsout.append(mask)
        else:
            # Inverse distance weighting
            sumfac = float(1.0 / sum(factors))
            ind = indices.pop(0)
            fac = factors.pop(0)
            weighted = float(fac) * dset.isel({sitename: ind}, drop=True)
            for ind, fac in zip(indices, factors):
                weighted += float(fac) * dset.isel({sitename: ind}, drop=True)
            if len(indices) > 0:
                weighted *= sumfac
            dsout.append(weighted)

    # Concat sites into dataset
    dsout = xr.concat(dsout, dim=sitename)
    for dvar in dsout.data_vars:
        if set(dsout[dvar].dims) == set(dset[dvar].dims):
            dsout[dvar] = dsout[dvar].transpose(*dset[dvar].dims)

    # Redefining coordinates and variables
    dsout[sitename] = np.arange(len(coords.lons))
    dsout[lonname] = ((sitename), coords.lons)
    dsout[latname] = ((sitename), coords.lats)

    # Return longitudes in the convention provided
    if coords.consistent is False:
        dsout.lon.values = coords._swap_longitude_convention(dsout.lon.values)

    dsout.attrs = dset.attrs
    set_spec_attributes(dsout)

    return dsout


def sel_bbox(
    dset,
    lons,
    lats,
    tolerance=0.0,
    sitename=attrs.SITENAME,
    lonname=attrs.LONNAME,
    latname=attrs.LATNAME,
):
    """Select sites within bbox.

    Args:
        dset (Dataset): Stations SpecDataset to select from.
        lons (array): Longitude of sites to interpolate spectra at.
        lats (array): Latitude of sites to interpolate spectra at.
        tolerance (float): Extend bbox extents by.
        sitename (str): Name of site dimension.
        lonname (str): Name of longitude coordinate.
        latname (str): Name of latitude coordinate.

    Returns:
        Selected SpecDataset within bbox defined by:
            lower-left=[min(lons), min(lats)], upper-right=[max(lons), max(lats)].

    Note:
        Args `dset_lons`, `dset_lats` are not required but can improve performance when
            `dset` is chunked with site=1 (expensive to access station coordinates) and
            improve precision if projected coordinates are provided at high latitudes.

    """
    coords = Coordinates(
        dset, lons=lons, lats=lats, sitename=sitename, lonname=lonname, latname=latname
    )

    minlon = min(coords.lons) - tolerance
    minlat = min(coords.lats) - tolerance
    maxlon = max(coords.lons) + tolerance
    maxlat = max(coords.lats) + tolerance
    if not (coords._is_360(coords.dset_lons) and not coords.consistent):
        station_ids = np.where(
            (coords.dset_lons >= minlon)
            & (coords.dset_lats >= minlat)
            & (coords.dset_lons <= maxlon)
            & (coords.dset_lats <= maxlat)
        )[0]
    else:
        station_ids = np.where(
            (coords.dset_lons >= maxlon)
            & (coords.dset_lats >= minlat)
            & (coords.dset_lons <= 360)
            & (coords.dset_lats <= maxlat)
        )[0]
        station_ids = np.append(
            station_ids,
            np.where(
                (coords.dset_lons >= 0)
                & (coords.dset_lats >= minlat)
                & (coords.dset_lons <= minlon)
                & (coords.dset_lats <= maxlat)
            )[0],
        )

    if station_ids.size == 0:
        raise ValueError(
            "No site found within bbox defined by "
            f"([{min(coords._lons) - tolerance}, {minlat}], "
            f"[{max(coords._lons) + tolerance}, {maxlat}])"
        )

    dsout = dset.isel(**{sitename: station_ids})

    # Return longitudes in the convention provided
    if coords.consistent is False:
        dsout.lon.values = coords._swap_longitude_convention(dsout.lon.values)

    dsout = dsout.assign_coords({sitename: np.arange(len(station_ids))})

    return dsout
