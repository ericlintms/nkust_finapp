from pathlib import Path
import sqlite3

import pandas as pd



# 我想要針對專案根目錄下的 crawldata.sqlite3 股價資料進行篩選，請幫我把這個 db 的 OHLC Table 資料讀為一個 DtaFrame，程式碼放進 week5_pandas/examples/ 下，檔名取為 stock_filter.py 。
# 過濾條件為 StockId 是 4 碼。

# ==========================
# 幫我在 stock_filter.py 裡面，加上一個 function ，可以使用 DataFrame 來過濾特定股號的資料。


def load_filtered_ohlc() -> pd.DataFrame:
    project_root = Path(__file__).resolve().parents[2]
    db_path = project_root / "crawldata.sqlite3"

    query = """
    SELECT *
    FROM OHLC
    WHERE CAST(StockId AS TEXT) GLOB '[0-9][0-9][0-9][0-9]'
    """

    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(
            query,
            conn,
            index_col="TradeDate",
            parse_dates=["TradeDate"],
        )

    return df


def filter_by_stock_id(df: pd.DataFrame, stock_id: str) -> pd.DataFrame:
    return df[df["StockId"].astype(str) == str(stock_id)]


if __name__ == "__main__":
    filtered_df = load_filtered_ohlc()
    print(f"Filtered rows (4-digit StockId): {len(filtered_df)}")
    print(filtered_df.head())

    stock_2330_df = filter_by_stock_id(filtered_df, "2330")
    print(f"\nRows for StockId=2330: {len(stock_2330_df)}")
    print(stock_2330_df.head())