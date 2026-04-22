#!/usr/bin/env python3
"""
merge_counties.py - Filter and merge GeoJSON county polygons into a single polygon.

Usage:
    python merge_counties.py <input.geojson> <output.geojson> <counties.txt>

Example:
    python merge_counties.py nc_counties.geojson merged.geojson counties.txt

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
from shapely.ops import unary_union
from shapely.geometry import shape, mapping


def load_county_names(txt_path):
    names = set()
    with open(txt_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                names.add(line.lower())
    return names


def main():
    if len(sys.argv) != 4:
        print("Usage: python merge_counties.py <input.geojson> <output.geojson> <counties.txt>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    counties_path = sys.argv[3]

    target_counties = load_county_names(counties_path)
    if not target_counties:
        print("Error: no county names found in", counties_path)
        sys.exit(1)

    # Load GeoJSON
    with open(input_path) as f:
        data = json.load(f)

    if data.get("type") != "FeatureCollection":
        print("Error: input file must be a GeoJSON FeatureCollection")
        sys.exit(1)

    # Find matching features
    matched_geoms = []
    matched_names = []

    for feature in data["features"]:
        props = feature.get("properties", {})
        # Try common property names for county name
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
        print("Error: no matching counties found. Check county names and the 'County' property field.")
        sys.exit(1)

    # Merge into a single polygon
    merged = unary_union(matched_geoms)

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