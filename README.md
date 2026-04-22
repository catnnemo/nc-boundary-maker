# merge_counties

A small Python script that takes a GeoJSON file of county boundaries and merges a subset of counties into a single dissolved polygon.

## Requirements

- Python 3.7+
- [shapely](https://shapely.readthedocs.io/)

```bash
pip install shapely
```

## Usage

```bash
python merge_counties.py <input.geojson> <output.geojson> <counties.txt>
```

| Argument | Description |
|---|---|
| `input.geojson` | GeoJSON FeatureCollection of county boundaries |
| `output.geojson` | Path to write the merged output |
| `counties.txt` | Text file with one county name per line |

## County list format

`counties.txt` should have one county name per line. County names are case-insensitive. Lines starting with `#` are treated as comments and ignored.

```
Wayne
Wilson
Pitt
# Eastern counties
Edgecombe
Martin
Bertie
```

## Example

```bash
python merge_counties.py nc_counties.geojson merged.geojson counties.txt
```

```
Found 16 counties: Bertie, Camden, Chowan, Currituck, Edgecombe, ...
Output written to: merged.geojson
Geometry type: Polygon
```

The output is a GeoJSON FeatureCollection with a single feature. If the selected counties are non-contiguous, the geometry will be a `MultiPolygon` rather than a `Polygon`.

## Getting county GeoJSON

A few free sources for US county boundary GeoJSON:

- **NC OneMap** — [nconemap.com](https://www.nconemap.com) — official NC GIS data, used to build this tool
- **US Census TIGER** — [census.gov](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html) — authoritative national source
- **Eric Celeste** — [eric.clst.org/tech/usafips](https://eric.clst.org/tech/usafips) — pre-made GeoJSON, no conversion needed

The script looks for the county name in the following GeoJSON property keys (in order): `County`, `county`, `NAME`, `name` — so it should work with files from any of these sources without modification.

## License

MIT