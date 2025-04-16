import polars as pl


id_cols_dtype = {
    "grass_date": pl.Date,
    "review_id": pl.String,
}

dict_source = {
    "app_review": {
        "text_cols": ["Subject", "Body"],
        "id_cols": {
            "Date": "grass_date",
            "Review ID": "review_id"
        },
        "id_cols_dtype": id_cols_dtype,
        "api_endpoint": 'https://datasuite.shopee.io/datahub/api/v1/usertoken/upload/csv/csv-d354da83-bfe7-437c-b1ca-4fd8546c3256',
        "ingestion_token": '507878de-8603-448f-b2bc-d1113b158655',
    },
    "kompa": {
        "text_cols": ["Title", "Content"],
        "id_cols": {
            "Id": "review_id",
            "PublishedDate": "grass_date",
        },
        "id_cols_dtype": id_cols_dtype,
        "api_endpoint": 'https://datasuite.shopee.io/datahub/api/v1/usertoken/upload/csv/csv-b57ff7d2-31ac-42bd-bb0a-6c429fe3840c',
        "ingestion_token": '507878de-8603-448f-b2bc-d1113b158655',
    },
    "nps": {
        "text_cols": ["user_fill_text"],
        "id_cols": {
            "index": "review_id",
            "date_submitted": "grass_date",
        },
        "id_cols_dtype": id_cols_dtype,
        "api_endpoint": 'https://datasuite.shopee.io/datahub/api/v1/usertoken/upload/csv/csv-f0f8d554-5677-41ac-bcd3-546de55c72cf',
        "ingestion_token": '507878de-8603-448f-b2bc-d1113b158655',
    }
}