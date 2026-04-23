# nc-boundary-maker

A small Python script that merges a subset of NC counties into a single dissolved polygon, using the included `nc_counties.geojson` boundary file. Made with Meshmapper admins in mind

## Web App
Go to https://catnnemo.github.io/nc-boundary-maker/

## Requirements for Running Locally

- Python 3.7+
- [shapely](https://shapely.readthedocs.io/)

```bash
pip install shapely --break-system-packages
```

## Usage

1. Clone the repository
2. run ```bash python merge_counties.py counties.txt ``` in the cloned directory


The output is automatically named `output_YYYYMMDD_HHMMSS.geojson` and written to the current directory.

## County list format

`counties.txt` should have one county name per line. County names are case-insensitive. Lines starting with `#` are treated as comments and ignored.

```
Wayne
Wilson
Greene
Lenoir
Pitt
Edgecombe
Martin
Bertie
Hertford
Gates
Washington
Chowan
Perquimans
Pasquotank
Camden
Currituck
```

## Example

```bash
python merge_counties.py counties.txt
```

```
Found 16 counties: Bertie, Camden, Chowan, Currituck, Edgecombe, ...
Output written to: output_20240422_143201.geojson
Geometry type: Polygon
```

The output is a GeoJSON FeatureCollection with a single feature. If the selected counties are non-contiguous, the geometry will be a `MultiPolygon` rather than a `Polygon`.

## Files

| File | Description |
|---|---|
| `merge_counties.py` | The script |
| `nc_counties.geojson` | NC county boundary source data (from [NC OneMap](https://www.nconemap.com)) |
| `counties.txt` | Example county list |

## License

MIT