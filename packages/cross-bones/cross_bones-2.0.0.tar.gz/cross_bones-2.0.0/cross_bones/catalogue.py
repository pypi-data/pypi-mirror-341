from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import astropy.units as u
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.table import Table
from numpy.typing import NDArray

from cross_bones.logging import logger

Paths = tuple[Path, ...]


@dataclass
class Offset:
    """Contains offsets in the RA and Dec directions in arcsec"""

    ra: float = 0.0
    """Offset in RA direction"""
    dec: float = 0.0
    """Offset in Dec direction"""


@dataclass
class CatalogueKeys:
    """Contains catalogue column names/keys. Defaults are aegean-based."""

    ra: str = "ra"
    """RA column key."""
    dec: str = "dec"
    """DEC column key."""
    int_flux: str = "int_flux"
    """Integrated flux density column key."""
    peak_flux: str = "peak_flux"
    """Peak flux density column key."""
    local_rms: str = "local_rms"
    """Local rms column key."""


@dataclass
class Catalogue:
    """Represent a per-beam ASKAP component catalogue"""

    table: Table
    """The table loaded"""
    path: Path
    """Original path to the loaded catalogue"""
    center: SkyCoord
    """Rough beam center derived from coordinates of componetns in catalogue"""
    sky_coords: SkyCoord | None = None
    """The positions from the table loaded"""
    fixed: bool = False
    """Indicates whether beam has been fixed into a place"""
    offset: Offset = field(default_factory=Offset)
    """Per beam offsets, if known, in arcsec"""
    idx: int | None = None
    """Some optional identifier"""
    table_keys: CatalogueKeys = field(default_factory=CatalogueKeys)
    """Column names/keys with defaults from aegean component lists."""

    def __repr__(self) -> str:
        return f"Catalogue(idx={self.idx}, table={len(self.table)} sources, path={self.path}, fixed={self.fixed})"


@dataclass
class TableKeys:
    """Generic keys for a table"""

    ra: str = "ra"
    """RA column key."""
    dec: str = "dec"
    """DEC column key."""
    int_flux: str = "int_flux"
    """Integrated flux density column key."""
    peak_flux: str = "peak_flux"
    """Peak flux density column key."""
    local_rms: str = "local_rms"
    """Local rms column key."""


Catalogues = list[Catalogue]


def make_sky_coords(
    table: Table | Catalogue, ra_key: str = "ra", dec_key: str = "dec"
) -> SkyCoord:
    """Create the sky-coordinates from a cataloguue table

    Args:
        table (Table | Catalogue): Loaded table or catalogue
        ra_key (str): RA column key name
        dec_key (str): DEC column key name

    Returns:
        SkyCoord: Sky-positions loaded
    """
    if isinstance(table, Catalogue) and table.sky_coords:
        return table.sky_coords

    table = table.table if isinstance(table, Catalogue) else table
    return SkyCoord(table[ra_key], table[dec_key], unit=(u.deg, u.deg))


def estimate_skycoord_centre(
    sky_positions: SkyCoord, final_frame: str = "fk5"
) -> SkyCoord:
    """Estimate the central position of a set of positions by taking the
    mean of sky-coordinates in their XYZ geocentric frame. Quick approach
    not intended for accuracy.

    Args:
        sky_positions (SkyCoord): A set of sky positions to get the rough center of
        final_frame (str, optional): The final frame to convert the mean position to. Defaults to "fk5".

    Returns:
        SkyCoord: The rough center position
    """

    xyz_positions = sky_positions.cartesian.xyz
    xyz_mean_position = np.median(xyz_positions, axis=1)

    return SkyCoord(*xyz_mean_position, representation_type="cartesian").transform_to(
        final_frame
    )


def filter_table(
    table: Table,
    table_keys: TableKeys,
    min_snr: float = 10.0,
    min_iso: float = 36.0,
) -> NDArray[np.bool_]:
    """Filter radio components out of a radio catalogue
    based on their distance to neighbouring components, compactness,
    and optionally minimum SNR.

    Args:
        table (Table): Aegean radio component catalogue
        table_keys (TableKeys): Table column keys
        min_snr (float): Minimum SNR of component. Default 10.
        min_iso (float): Minimum separation from a neighbour in arcsec. Default 30.

    Returns:
        np.ndarray: Boolean array of components to keep.
    """

    sky_coord = SkyCoord(
        ra=table[table_keys.ra], dec=table[table_keys.dec], unit=(u.deg, u.deg)
    )

    isolation_mask = sky_coord.match_to_catalog_sky(sky_coord, nthneighbor=2)[1] > (
        min_iso * u.arcsec
    )

    ratio = table[table_keys.int_flux] / table[table_keys.peak_flux]
    ratio_mask = (ratio > 0.8) & (ratio < 1.2)

    snr = table[table_keys.peak_flux] / table[table_keys.local_rms]
    snr_mask = snr > min_snr

    return isolation_mask & ratio_mask & snr_mask


def load_catalogue(
    catalogue_path: Path,
    table_keys: TableKeys,
    idx: int | None = None,
    min_snr: float = 5.0,
    min_iso: float = 36.0,
) -> Catalogue:
    """Load a beam catalogue astropy table

    Args:
        catalogue_path (Path): Path to load catalogue from
        table_keys (TableKeys): Table column keys
        idx (int | None, optional): Some optional identifier added to Catalogue. Defaults to None.
        min_snr (float): Minimum SNR of component. Default 10.
        min_iso (float): Minimum separation from a neighbour in arcsec. Default 30.

    Returns:
        Catalogue: Loaded catalogue
    """
    logger.debug(f"Loading {catalogue_path}")
    table = Table.read(catalogue_path)

    table_mask = filter_table(
        table=table, table_keys=table_keys, min_snr=min_snr, min_iso=min_iso
    )
    sub_table = table[table_mask]

    sky_coords = make_sky_coords(
        table=sub_table, ra_key=table_keys.ra, dec_key=table_keys.dec
    )

    center = estimate_skycoord_centre(
        SkyCoord(
            ra=table[table_keys.ra],
            dec=table[table_keys.dec],
            unit=(u.deg, u.deg),
        )
    )

    catalogue_keys = CatalogueKeys(
        ra=table_keys.ra,
        dec=table_keys.dec,
        int_flux=table_keys.int_flux,
        peak_flux=table_keys.peak_flux,
        local_rms=table_keys.local_rms,
    )

    return Catalogue(
        table=sub_table,
        path=catalogue_path,
        sky_coords=sky_coords,
        center=center,
        idx=idx,
        table_keys=catalogue_keys,
    )


def load_catalogues(
    catalogue_paths: Paths,
    table_keys: TableKeys,
    min_snr: float = 5.0,
    min_iso: float = 36.0,
) -> Catalogues:
    """Load in all of the catalgues"""

    return [
        load_catalogue(
            catalogue_path=catalogue_path,
            idx=idx,
            table_keys=table_keys,
            min_snr=min_snr,
            min_iso=min_iso,
        )
        for idx, catalogue_path in enumerate(catalogue_paths)
    ]


def save_catalogue_shift_positions(
    catalogues: Catalogues, output_path: Path | None = None
) -> Path:
    from pandas import DataFrame

    output_path = output_path if output_path else Path("shifts.csv")

    shifts_df = DataFrame(
        [
            {
                "path": catalogue.path,
                "d_ra": catalogue.offset.ra,
                "d_dec": catalogue.offset.dec,
            }
            for catalogue in catalogues
        ]
    )

    logger.info(f"Writing {output_path}")
    shifts_df.to_csv(output_path, index=False)

    return output_path


def guess_sbid_and_field_racs(
    catalogue_path: str | Path,
) -> tuple[int, str]:
    """Attempt to extract the SBID and field name from a file path.
    The filenames assumes some deliminted name scheme, with '.' as
    the field marker.

    The field name is the second item, and it taken as it. The SBID
    is taken as the first field, and requires a 'SB' prefix.

    Args:
        catalogue_path (str | Path): The file path to extract

    Raises:
        RuntimeError: Raised when a path does not follow expectations

    Returns:
        tuple[int, str]: And SBID and field name
    """
    name_components = str(Path(catalogue_path).name).split(".")
    logger.debug(f"These are the split name components: {name_components}")
    field_name = name_components[1]

    if name_components[0][:2] != "SB":
        msg = f"SBID is not found in {name_components=}"
        raise RuntimeError(msg)

    sbid_str = name_components[0][2:]
    try:
        sbid = int(sbid_str)
    except ValueError as err:
        msg = f"Can not convert {sbid_str=} to an int"
        raise RuntimeError(msg) from err

    return sbid, field_name
