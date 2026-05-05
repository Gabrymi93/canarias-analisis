"""
fetch_canarias.py
Downloads datasets from the CKAN portal of Gobierno de Canarias (ISTAC).

Usage:
    python -m src.fetch --dataset <package_id_or_name> --output data/raw/
    python -m src.fetch --dataset <package_id_or_name> --output data/raw/ --format JSON
"""

import argparse
import json
import urllib.request
from pathlib import Path
import re

CKAN_BASE = "https://datos.canarias.es/catalogos/general/api/action"


def get_resource_url(package_id: str, fmt: str = "CSV") -> tuple[str, str]:
    """
    Find download URL for a specific format within a CKAN dataset.

    Logic:
      1. Look for exact format match (case-insensitive). If found and format
         code looks right (CSV, JSON, XLSX, etc.), use it.
      2. If no exact match, look for resources where the format string
         CONTAINS the requested fmt. If found, warn but use it.
      3. If nothing matches at all, raise ValueError.

    Args:
        package_id: CKAN dataset ID or name
        fmt: desired format (CSV, JSON, PC-Axis)

    Returns:
        (download_url, resource_name)
    """
    pkg_url = f"{CKAN_BASE}/package_show?id={package_id}"
    with urllib.request.urlopen(pkg_url, timeout=30) as resp:
        pkg = json.loads(resp.read())

    resources = pkg["result"]["resources"]
    fmt_upper = fmt.upper()

    # Step 1: exact format match
    for r in resources:
        if r["format"].upper() == fmt_upper:
            return r["url"], r["name"]

    # Step 2: partial match (format string contains fmt)
    for r in resources:
        if fmt_upper in r["format"].upper():
            print(f"  [WARNING] Exact '{fmt}' not found. Using '{r['format']}' resource instead: {r['name']}")
            return r["url"], r["name"]

    # Step 3: nothing found
    available = [r["format"] for r in resources]
    raise ValueError(
        f"No resource in format '{fmt}' for dataset '{package_id}'. "
        f"Available formats: {available}"
    )


def sanitize(name: str) -> str:
    """Make a string safe for use as a filename."""
    # Remove characters that are problematic in filenames
    name = re.sub(r"[^\w\-]", "_", name)
    name = re.sub(r"_+", "_", name)
    name = name.strip("_")
    # Limit length to avoid overly long filenames (120 chars keeps words whole for typical dataset names)
    return name[:120]


def download_resource(url: str, output_dir: Path, chunk_size: int = 8192) -> Path:
    """
    Download a file from URL and save to disk.

    Args:
        url: file URL
        output_dir: destination directory
        chunk_size: stream chunk size

    Returns:
        Path of downloaded file
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = Path(url.split("/")[-1])
    out_path = output_dir / filename

    req = urllib.request.Request(url, headers={"User-Agent": "canarias-analisis/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        with open(out_path, "wb") as f:
            while True:
                chunk = resp.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)

    return out_path


def rename_for_clarity(raw_path: Path, package_name: str, fmt: str = "CSV") -> Path:
    """
    Rename an opaquely-named downloaded file to something more descriptive.

    The CKAN download URL often contains an internal ID (e.g. e70048a_dsc_0003.csv
    or 1.4.csv). After download, this function tries to derive a more human-readable
    name based on the package name and the requested format extension.

    Args:
        raw_path: Path of the freshly downloaded file
        package_name: CKAN package name (used to generate a better name)
        fmt: requested format (used for extension, e.g. CSV -> .csv)

    Returns:
        New Path (may be same as raw_path if rename not needed or not possible)
    """
    # Use the requested format for extension, not the opaque one from URL
    ext = f".{fmt.lower()}"
    base = sanitize(package_name)
    if not base:
        base = "dataset"
    new_name = f"{base}{ext}"
    new_path = raw_path.parent / new_name

    if new_path == raw_path:
        return raw_path

    if new_path.exists():
        counter = 1
        while new_path.exists():
            new_path = raw_path.parent / f"{base}_{counter}{ext}"
            counter += 1

    raw_path.rename(new_path)
    print(f"  Renamed: {raw_path.name} -> {new_path.name}")
    return new_path


def main():
    parser = argparse.ArgumentParser(description="Download dataset from datos.canarias.es")
    parser.add_argument("--dataset", required=True, help="CKAN dataset ID or name")
    parser.add_argument("--output", default="data/raw", help="Output directory")
    parser.add_argument(
        "--format", default="CSV", help="Format: CSV (default), JSON, PC-Axis"
    )
    parser.add_argument(
        "--no-rename", action="store_true", default=False,
        help="Disable auto-rename of downloaded files"
    )
    args = parser.parse_args()

    out_dir = Path(args.output)
    print(f"Downloading {args.dataset} (format={args.format})...")

    url, name = get_resource_url(args.dataset, args.format)
    print(f"Resource: {name}")

    path = download_resource(url, out_dir)
    print(f"Downloaded: {path}")

    if not args.no_rename:
        path = rename_for_clarity(path, args.dataset, args.format)
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()