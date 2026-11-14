
import argparse
from pathlib import Path

import pandas as pd


def process_files(input_dir: Path, output_file: Path) -> None:
    """Merge CSV files, remove duplicates, and export the result."""

    if not input_dir.is_dir():
        raise ValueError(f"Input directory does not exist: {input_dir}")

    files = sorted(input_dir.glob("*.csv"))

    if not files:
        raise ValueError(f"No CSV files found in {input_dir}")

    dataframes = []

    for file in files:
        print(f"Reading: {file.name}")
        df = pd.read_csv(file, encoding="utf-8-sig")
        dataframes.append(df)

    combined = pd.concat(dataframes, ignore_index=True)

    original_rows = len(combined)
    combined = combined.drop_duplicates()
    removed_rows = original_rows - len(combined)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    if output_file.suffix.lower() == ".xlsx":
        combined.to_excel(output_file, index=False)
    elif output_file.suffix.lower() == ".csv":
        combined.to_csv(output_file, index=False, encoding="utf-8-sig")
    else:
        raise ValueError("Output must be .xlsx or .csv")

    print(f"Files processed: {len(files)}")
    print(f"Rows before cleaning: {original_rows}")
    print(f"Duplicates removed: {removed_rows}")
    print(f"Final rows: {len(combined)}")
    print(f"Saved to: {output_file}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Merge and clean CSV files"
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Directory containing CSV files"
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output .xlsx or .csv file"
    )

    args = parser.parse_args()
    process_files(args.input, args.output)


if __name__ == "__main__":
    main()
