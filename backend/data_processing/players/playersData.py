import polars as pl
from pathlib import Path

    # Get base and data directories
base_dir = Path(__file__).resolve().parent.parent.parent
data_dir = base_dir / "datasets"