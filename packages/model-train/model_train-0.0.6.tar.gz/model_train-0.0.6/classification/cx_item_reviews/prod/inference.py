from pathlib import Path
import duckdb
import polars as pl
from rich import print
from core_pro.ultilities import make_dir, make_sync_folder, filter_unprocessed_files
from core_pro import AWS
from core_eda import TextEDA
from tqdm.auto import tqdm
import sys

sys.path.extend([str(Path.home() / "PycharmProjects/model_train")])
from src.model_train import FastTextClassifier


# path
path = make_sync_folder("cx/product_review")
file_raw = sorted([*path.glob(f"deploy/raw/*")])

# path export
path_export_inference = path / f"deploy/inference/"
make_dir(path_export_inference)
file_inference = sorted([*path.glob(f"deploy/inference/*")])
file_inference_name = [f.name for f in file_inference]
new_infer_file = filter_unprocessed_files(file_raw, file_inference_name)

# init model
path_model = "kevinkhang2909/product_review"
infer = FastTextClassifier(model_name=path_model)


def run(f: Path):
    # check file
    file_export = path_export_inference / f"{f.stem}.parquet"
    if file_export.exists():
        print(f"Batch Done: {file_export.stem}")
        return None, None, file_export
    print(f"=== START {f.name} ===")

    # data
    query = f"""
    select * exclude(comment_stats)
    , cast(unnest(comment_stats, recursive := true)::json as STRUCT(comment_id bigint, comment VARCHAR, rating_star int, create_date date)) comment_stats
    from read_parquet('{f}')
    """
    df = duckdb.sql(query).pl().unnest("comment_stats")
    print(f"Data Shape: {df.shape}, Total Items: {df['item_id'].n_unique():,.0f}")

    # clean data
    select_cols = ["comment_id", "create_date"]
    text_column = "comment"
    id_cols = select_cols + [text_column]
    lst = {text_column: [TextEDA.clean_text_multi_method(_) for _ in tqdm(df[text_column], desc="Clean text")]}
    df_clean = pl.concat([df[select_cols], pl.DataFrame(lst)], how="horizontal")

    dict_result = infer.predict_with_dataloader(
        texts=df_clean[text_column].to_list(),
        multi_label=True,
    )
    df_result = pl.DataFrame(dict_result)

    # post process
    ds_pred_post = (
        pl.concat([df_clean, df_result], how="horizontal")
        .explode(["labels", "scores"])
        .pivot(index=id_cols, on="labels", values="scores", aggregate_function="first")
    )

    # cast data type to datasuite
    ds_pred_post = (
        ds_pred_post
        .with_columns(pl.col("create_date").alias("grass_date"))
        .with_columns(
            pl.col(i).round(5).cast(pl.Float32).name.keep()
            for i in ds_pred_post.columns
            if i not in id_cols + ["grass_date"]
        )
    )

    # infer
    ds_pred_post.write_parquet(file_export)
    return df, ds_pred_post, file_export


# inference
lst_path = []
for f in new_infer_file:
    df, df_pred, file_export = run(f)
    lst_path.append(file_export)
    # break

# update inference file
file_inference = sorted([*path.glob(f"deploy/inference/*")])

# check file in s3
bucket_name = 'sg-vnbi-ops-kevin'
s3 = AWS(bucket_name)
prefix = "cx/product_review"
# bucket_name = 'sg-vnbi-ops-hive'
# prefix = "dev_vnbi_ops/ds_cx__item_marketplace_listening__s3"
# s3.delete_file(files)
s3_files = s3.get_all_files(prefix)

# upload
s3_file_names = [f.split('/')[-1] for f in s3_files]
new_upload_file = filter_unprocessed_files(file_inference, s3_file_names)
s3.upload_multiple_files(new_upload_file, prefix)
