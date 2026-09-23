import polars as pl
import pyarrow as pa
from typing import Tuple

class PolarsStreamProcessor:
    """موتور پردازش موازی و فوق‌سریع داده‌های جریانی با Polars"""
    def __init__(self, vibration_threshold: float = 8.0):
        self.threshold = vibration_threshold

    def process_and_detect_anomalies(self, arrow_table: pa.Table) -> Tuple[pl.DataFrame, pl.DataFrame]:
        # تبدیل بدون کپی (Zero-Copy) از Arrow به Polars
        df = pl.from_arrow(arrow_table)

        # ۱. محاسبات آماری تجمعی روی سنسورها
        aggregated = df.group_by("sensor_id").agg([
            pl.col("temperature").mean().alias("avg_temp"),
            pl.col("vibration").max().alias("max_vibration"),
            pl.col("voltage").mean().alias("avg_voltage"),
            pl.len().alias("sample_count")
        ])

        # ۲. فیلترینگ برداری ناهنجاری‌ها با سرعت فوق‌العاده
        anomalies = df.filter(pl.col("vibration") > self.threshold)

        return aggregated, anomalies
