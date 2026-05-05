"""
fetch_canarias.py
Downloads datasets from the CKAN portal of Gobierno de Canarias (ISTAC).

Usage:
    python -m src.fetch --dataset <package_id_or_name> --output data/raw/
"""

import argparse
import json
import urllib.request
from pathlib import Path

CKAN_BASE = "https://datos.canarias.es/catalogos/general/api/action"


def get_resource_url(package_id: str, fmt: str = "CSV") -> tuple[str, str]:
    """
    Find download URL for a specific format within a CKAN dataset.

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
    for r in resources:
        if r["format"].upper() == fmt.upper():
            return r["url"], r["name"]

    # fallback: first resource matching format
    for r in resources:
        if fmt.upper() in r["format"].upper():
            return r["url"], r["name"]

    raise ValueError(f"No resource in format {fmt} for dataset {package_id}")


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


def main():
    parser = argparse.ArgumentParser(description="Download dataset from datos.canarias.es")
    parser.add_argument("--dataset", required=True, help="CKAN dataset ID or name")
    parser.add_argument("--output", default="data/raw", help="Output directory")
    parser.add_argument(
        "--format", default="CSV", help="Format: CSV (default), JSON, PC-Axis"
    )
    args = parser.parse_args()

    out_dir = Path(args.output)
    print(f"Downloading {args.dataset} (format={args.format})...")

    url, name = get_resource_url(args.dataset, args.format)
    print(f"Resource URL: {url}")
    print(f"Name: {name}")

    path = download_resource(url, out_dir)
    print(f"Saved to: {path}")


if __name__ == "__main__":
    main()