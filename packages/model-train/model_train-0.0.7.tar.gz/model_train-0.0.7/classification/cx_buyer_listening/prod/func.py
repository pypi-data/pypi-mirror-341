from pathlib import Path
import re
from core_pro.ultilities import make_dir, upload_to_datahub
import polars as pl
from src.model_train import FastTextClassifier


def clean_file_name(file_path: Path) -> str:
    file_name = file_path.stem
    file_name = '_'.join(re.sub(r"\.", "", file_name.lower()).split(' '))
    return file_name


def handle_path(path, folder, file_path) -> Path:
    path_export = path / folder / "result"
    make_dir(path_export)
    file_name = clean_file_name(file_path)
    return path_export / f"{file_name}.parquet"


def inference(pretrain_name: str, data: pl.DataFrame, col_name: str, text_column: str = "text") -> pl.DataFrame:
    infer = FastTextClassifier(model_name=pretrain_name)
    dict_result = infer.predict_with_dataloader(
        texts=data[text_column].to_list(),
    )
    df_result = pl.DataFrame(dict_result)
    return (
        pl.concat([data, df_result], how="horizontal")
        .rename({"labels": f"pred_{col_name}", "scores": f"score_{col_name}"})
        .with_columns(pl.col(f"score_{col_name}").cast(pl.Float32))
    )


def export(path, df_csv, folder: str, dict_source: dict):
    path_export = path / folder / 'export'
    make_dir(path_export)
    file_csv = path_export / f"{folder}.csv"
    df_csv.write_csv(file_csv)

    api_endpoint = dict_source[folder]["api_endpoint"]
    ingestion_token = dict_source[folder]["ingestion_token"]
    upload_to_datahub(file_path=file_csv, api_endpoint=api_endpoint, ingestion_token=ingestion_token)
