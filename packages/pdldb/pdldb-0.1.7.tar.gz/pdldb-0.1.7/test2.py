import polars as pl
from pathlib import Path
from pdldb import S3LakeManager
from examples.example_utils.synth_data import generate_synthetic_data
import os


lake = S3LakeManager(
    base_path=os.environ.get("S3_URI"),
    aws_region=os.environ.get("AWS_REGION"),
    aws_access_key=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    dynamodb_locking_table=os.environ.get("DYNAMODB_LOCKING_TABLE"),
)

data = generate_synthetic_data(target_size_mb=10)

schema = {
        "sequence": pl.Int32,
        "id": pl.Int64,
        "value_1": pl.Float32,
        "value_2": pl.Float32,
        "value_3": pl.Utf8,
        "value_4": pl.Float32,
        "value_5": pl.Datetime,
    }

data = pl.read_parquet(
    Path("examples/example_data/synthetic_data.parquet"),
    schema=schema,
)

lake.create_table(
    table_name="my_table_3",
    table_schema=schema,
    primary_keys=["sequence", "value_5"],
)

lake.append_table("my_table_3", data)

print(lake.get_data_frame("my_table_3"))

lake.merge_table("my_table_3", data)

print(lake.get_data_frame(table_name="my_table_3"))