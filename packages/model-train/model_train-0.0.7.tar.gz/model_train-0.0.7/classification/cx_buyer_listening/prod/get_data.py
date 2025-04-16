from core_pro import Drive, Sheet
from core_pro.ultilities import make_sync_folder, make_dir
from tqdm.auto import tqdm
import polars as pl

# path
path = make_sync_folder("cx/buyer_listening/inference")

dict_source = {
    "kompa": "13NV7g5alO6RUqah5YOTRVKADeIq1IH3p",
    "app_review": "1k6ocTl-1YFFX6zFM5v1C0VCbmPBMzRP1",
}
drive = Drive(verbose=False)
for name, folder_id in dict_source.items():
    path_raw = path / f"2025/{name}"
    make_dir(path_raw)
    add_files = drive.search_files(folder_id=folder_id)
    for i in tqdm(add_files, desc=f"Downloading Data from {name}"):
        drive.download_file(file_id=i["id"], download_dir=path_raw)


sh = "1kdQZzzq4fPbD1phpcKQvUDCRoMGZE-TdWGeOWUBF9zo"
df_free_text = (
    Sheet(sh)
    .google_sheet_into_df("data_raw", "A:L")
    .select(["date_submitted", "userid", "user_fill_text"])
    .with_row_index()
    .filter(pl.col("user_fill_text") != "")
)
df_free_text.write_parquet(path / f"2025/nps/free_text.parquet")
