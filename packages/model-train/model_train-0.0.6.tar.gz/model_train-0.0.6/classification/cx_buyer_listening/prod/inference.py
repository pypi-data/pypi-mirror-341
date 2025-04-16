from pathlib import Path
import polars as pl
from rich import print
from core_pro.ultilities import make_sync_folder
from core_eda import TextEDA
from tqdm.auto import tqdm
from collections import defaultdict
import sys

sys.path.extend([str(Path.home() / "PycharmProjects/model_train")])
from config import dict_source
from func import handle_path, inference, export


# path
path = make_sync_folder("cx/buyer_listening/inference/2025")
files = sorted([*path.glob("*/*.xlsx")])


# init source:
def run(file_path: Path):
    folder = file_path.parts[-2]
    print(f"=== START {file_path.name} ===")

    # create path
    file_export = handle_path(path, folder, file_path)
    if file_export.exists():
        print(f"Batch Done: {file_export.stem}")
        return None, pl.read_parquet(file_export), file_export

    # data
    if folder == "nps":
        df = pl.read_parquet(file_path)
    else:
        df = pl.read_excel(file_path, engine="openpyxl")

    # select cols
    text_cols = dict_source[folder]["text_cols"]
    id_cols = dict_source[folder]["id_cols"]
    id_dtypes = dict_source[folder]["id_cols_dtype"]

    # clean data
    lst = {
        col: [TextEDA.clean_text_multi_method(_) for _ in df[col]]
        for col in tqdm(text_cols, desc="[TextEDA] Clean Text")
    }
    df_clean = df[list(id_cols.keys())].rename(id_cols)
    df_clean = (
        pl.concat([df_clean, pl.DataFrame(lst)], how="horizontal")
        .with_columns(pl.concat_str([pl.col(i) for i in text_cols], separator=". ").alias("text"))
        .with_columns(pl.col(i).cast(v) for i, v in id_dtypes.items())
        .drop(text_cols)
        .filter(pl.col("text") != "")
    )

    # infer
    ds_pred = inference(
        pretrain_name="kevinkhang2909/buyer_listening",
        data=df_clean,
        col_name="category",
    )
    ds_pred_sentiment = inference(
        pretrain_name="kevinkhang2909/sentiment",
        data=df_clean,
        col_name="sentiment",
    )

    # post process
    df_clean = (
        pl.concat([
            df_clean,
            ds_pred[["pred_category", "score_category"]],
            ds_pred_sentiment[["pred_sentiment", "score_sentiment"]]
        ], how="horizontal")
    )
    df_clean.write_parquet(file_export)
    return df, df_clean, file_export


# tag
lst = defaultdict(list)
for f in sorted(files, reverse=True):
    df, df_tag, file_export = run(f)
    folder = file_export.parts[-3]
    lst[folder].append(file_export)
    # break

# export
for folder in lst:
    df_csv = pl.concat([pl.read_parquet(f) for f in lst[folder]])
    export(path, df_csv, folder, dict_source)

file = path / "nps/free_text.parquet"
df = pl.read_parquet(file)
df, df_csv, file_export = run(file)
folder = "nps"
df_csv = pl.read_parquet(file_export)
export(path, df_csv, folder, dict_source)
