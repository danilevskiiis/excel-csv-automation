
import sys
from pathlib import Path

import pandas as pd

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

    assert output_file.exists()

    result = pd.read_excel(output_file)

    assert len(result) == 3
    assert set(result["name"]) == {"Ivan", "Anna", "Petr"}
