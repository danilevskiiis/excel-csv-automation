
import argparse
from pathlib import Path

import pandas as pd


SUPPORTED_EXTENSIONS = {".csv", ".xlsx"}


def read_file(file: Path) -> pd.DataFrame:
    """Read a CSV or Excel file."""

    if file.suffix.lower() == ".xlsx":
        return pd.read_excel(file)

    if file.suffix.lower() == ".csv":
        return pd.read_csv(
            file,
            sep=None,
            engine="python",
            encoding="utf-8-sig",
        )

    raise ValueError(f"Unsupported file format: {file.name}")


def process_files(input_dir: Path, output_file: Path) -> None:
    """Merge, clean, and export tabular data."""

    if not input_dir.is_dir():
        raise ValueError(
            f"Input directory does not exist: {input_dir}"
        )

    files = sorted(
        file
        for file in input_dir.iterdir()
        if file.is_file()
        and file.suffix.lower() in SUPPORTED_EXTENSIONS
        and not file.name.startswith("~$")
        and file.resolve() != output_file.resolve()
    )

    if not files:
        raise ValueError("No supported files found")

    dataframes = []
    expected_columns = None

    for file in files:
        print(f"Reading: {file.name}")

        df = read_file(file)

        df = df.dropna(how="all")

        if expected_columns is None:
            expected_columns = list(df.columns)
        elif set(df.columns) != set(expected_columns):
            raise ValueError(
                f"Column mismatch in file: {file.name}"
            )

        df = df[expected_columns]
        dataframes.append(df)

    combined = pd.concat(dataframes, ignore_index=True)

    original_rows = len(combined)

    combined = combined.drop_duplicates()

    removed_duplicates = original_rows - len(combined)

    if output_file.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "Output format must be .csv or .xlsx"
        )

    output_file.parent.mkdir(parents=True, exist_ok=True)

    if output_file.suffix.lower() == ".xlsx":
        combined.to_excel(output_file, index=False)
    else:
        combined.to_csv(
            output_file,
            index=False,
            encoding="utf-8-sig",
        )

    print()
    print("Processing completed")
    print(f"Files processed: {len(files)}")
    print(f"Rows before deduplication: {original_rows}")
    print(f"Duplicates removed: {removed_duplicates}")
    print(f"Final rows: {len(combined)}")
    print(f"Saved to: {output_file}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Excel & CSV Automation Tool"
    )

    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Directory containing CSV and Excel files",
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output .csv or .xlsx file",
    )

    args = parser.parse_args()

    try:
        process_files(args.input, args.output)
    except (ValueError, OSError, pd.errors.ParserError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
