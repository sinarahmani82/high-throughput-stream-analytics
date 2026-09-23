import duckdb
import polars as pl
from typing import List, Dict, Any

class DuckDBAnalyticsEngine:
    """موتور پردازش کوئری‌های تحلیلی OLAP با DuckDB بدون نیاز به پانداس"""
    def __init__(self):
        self.con = duckdb.connect(database=':memory:')

    def query_sensor_metrics(self, df: pl.DataFrame) -> List[Dict[str, Any]]:
        self.con.register("telemetry_data", df.to_arrow())

        query = """
            SELECT 
                sensor_id,
                ROUND(AVG(temperature), 2) AS mean_temperature,
                ROUND(AVG(voltage), 2) AS mean_voltage,
                ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY vibration), 2) AS p95_vibration,
                COUNT(*) AS total_events
            FROM telemetry_data
            GROUP BY sensor_id
            ORDER BY sensor_id;
        """
        # دریافت مستقیم به صورت Polars DataFrame و تبدیل به لیست دیکشنری
        return self.con.execute(query).pl().to_dicts()
