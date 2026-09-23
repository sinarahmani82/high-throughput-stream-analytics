import pytest
import polars as pl
from src.stream_generator import TelemetryStreamGenerator
from src.polars_pipeline import PolarsStreamProcessor
from src.duckdb_engine import DuckDBAnalyticsEngine

def test_telemetry_stream_batch_generation():
    generator = TelemetryStreamGenerator()
    batch = generator.generate_batch(batch_size=1000)
    assert batch.num_rows == 1000
    assert "vibration" in batch.column_names

def test_polars_stream_anomaly_filtering():
    generator = TelemetryStreamGenerator()
    batch = generator.generate_batch(batch_size=2000)
    
    processor = PolarsStreamProcessor(vibration_threshold=8.0)
    agg_df, anomalies = processor.process_and_detect_anomalies(batch)

    assert agg_df.height > 0
    assert "max_vibration" in agg_df.columns
    if anomalies.height > 0:
        assert anomalies["vibration"].min() > 8.0

def test_duckdb_olap_query_execution():
    generator = TelemetryStreamGenerator()
    batch = generator.generate_batch(batch_size=1000)
    # تبدیل به دیتافریم برای کوئری تحلیلی داک‌دی‌بی
    raw_df = pl.from_arrow(batch)

    engine = DuckDBAnalyticsEngine()
    results = engine.query_sensor_metrics(raw_df)
    assert len(results) > 0
    assert "mean_temperature" in results[0]
