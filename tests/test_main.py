
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import process_files


def test_merge_and_remove_duplicates(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    pd.DataFrame({
        "name": ["Ivan", "Anna"],
        "age": [22, 25],
    }).to_csv(input_dir / "first.csv", index=False)

    pd.DataFrame({
        "name": ["Anna", "Petr"],
        "age": [25, 30],
    }).to_csv(input_dir / "second.csv", index=False)

    output_file = tmp_path / "result.xlsx"
    process_files(input_dir, output_file)

    result = pd.read_excel(output_file)

    assert len(result) == 3
    assert set(result["name"]) == {"Ivan", "Anna", "Petr"}


def test_excel_input(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    pd.DataFrame({
        "name": ["Ivan", "Anna"],
        "age": [22, 25],
    }).to_excel(input_dir / "employees.xlsx", index=False)

    output_file = tmp_path / "result.csv"
    process_files(input_dir, output_file)

    result = pd.read_csv(output_file)

    assert len(result) == 2
    assert set(result["name"]) == {"Ivan", "Anna"}


def test_semicolon_csv(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    (input_dir / "employees.csv").write_text(
        "name;age\nIvan;22\nAnna;25\n",
        encoding="utf-8",
    )

    output_file = tmp_path / "result.xlsx"
    process_files(input_dir, output_file)

    result = pd.read_excel(output_file)

    assert len(result) == 2
    assert list(result.columns) == ["name", "age"]


def test_column_mismatch(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    pd.DataFrame({
        "name": ["Ivan"],
        "age": [22],
    }).to_csv(input_dir / "first.csv", index=False)

    pd.DataFrame({
        "product": ["Laptop"],
        "price": [1000],
    }).to_csv(input_dir / "second.csv", index=False)

    with pytest.raises(ValueError, match="Column mismatch"):
        process_files(input_dir, tmp_path / "result.xlsx")


def test_empty_rows_removed(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    (input_dir / "employees.csv").write_text(
        "name,age\nIvan,22\n,\nAnna,25\n",
        encoding="utf-8",
    )

    output_file = tmp_path / "result.xlsx"
    process_files(input_dir, output_file)

    result = pd.read_excel(output_file)

    assert len(result) == 2


def test_missing_input_directory(tmp_path):
    input_dir = tmp_path / "missing"

    with pytest.raises(ValueError, match="does not exist"):
        process_files(input_dir, tmp_path / "result.xlsx")
