#!/usr/bin/env python3
"""
merge_counties.py - Filter and merge NC county polygons into a single dissolved polygon.

Usage:
    python merge_counties.py <counties.txt>

Example:
    python merge_counties.py counties.txt

counties.txt format — one county name per line, lines starting with # are ignored:
    Wayne
    Wilson
    Pitt
    # this is a comment
    Lenoir

Requires:
    pip install shapely
"""

import sys
import json
from datetime import datetime
from pathlib import Path
from shapely.ops import unary_union
from shapely.geometry import shape, mapping

GEOJSON_PATH = Path(__file__).parent / "nc_counties.geojson"


def load_county_names(txt_path):
    names = set()
    with open(txt_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                names.add(line.lower())
    return names


def main():
    if len(sys.argv) != 2:
        print("Usage: python merge_counties.py <counties.txt>")
        sys.exit(1)

    counties_path = sys.argv[1]

    target_counties = load_county_names(counties_path)
    if not target_counties:
        print("Error: no county names found in", counties_path)
        sys.exit(1)

    if not GEOJSON_PATH.exists():
        print(f"Error: could not find {GEOJSON_PATH}")
        print("Make sure nc_counties.geojson is in the same directory as this script.")
        sys.exit(1)

    with open(GEOJSON_PATH) as f:
        data = json.load(f)

    if data.get("type") != "FeatureCollection":
        print("Error: nc_counties.geojson must be a GeoJSON FeatureCollection")
        sys.exit(1)

    # Find matching features
    matched_geoms = []
    matched_names = []

    for feature in data["features"]:
        props = feature.get("properties", {})
        county_name = (
            props.get("County")
            or props.get("county")
            or props.get("NAME")
            or props.get("name")
            or ""
        )
        if county_name.lower() in target_counties:
            matched_geoms.append(shape(feature["geometry"]))
            matched_names.append(county_name)

    # Report found/missing
    found_lower = {n.lower() for n in matched_names}
    missing = [n for n in target_counties if n not in found_lower]

    print(f"Found {len(matched_names)} counties: {', '.join(sorted(matched_names))}")
    if missing:
        print(f"WARNING: Could not find: {', '.join(sorted(missing))}")

    if not matched_geoms:
        print("Error: no matching counties found. Check county names and spelling.")
        sys.exit(1)

    # Merge into a single polygon
    merged = unary_union(matched_geoms)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f"output_{timestamp}.geojson")

    result = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": mapping(merged),
                "properties": {
                    "counties": ", ".join(sorted(matched_names))
                }
            }
        ]
    }

    with open(output_path, "w") as f:
        json.dump(result, f)

    print(f"Output written to: {output_path}")
    print(f"Geometry type: {merged.geom_type}")


if __name__ == "__main__":
    main()