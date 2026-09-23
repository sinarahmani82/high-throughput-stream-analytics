import time
from tabulate import tabulate
from src.stream_generator import TelemetryStreamGenerator
from src.polars_pipeline import PolarsStreamProcessor
from src.duckdb_engine import DuckDBAnalyticsEngine

def main():
    print("=== High-Throughput Stream Processing & OLAP Benchmark ===\n")

    batch_size = 200_000
    print(f"Ingesting high-velocity stream batch: {batch_size:,} events...")

    generator = TelemetryStreamGenerator()
    start_time = time.time()
    arrow_batch = generator.generate_batch(batch_size)
    gen_time = time.time() - start_time

    # پردازش و کشف ناهنجاری با Polars
    processor = PolarsStreamProcessor(vibration_threshold=8.0)
    start_proc = time.time()
    agg_df, anomalies = processor.process_and_detect_anomalies(arrow_batch)
    proc_time = time.time() - start_proc

    throughput = batch_size / proc_time

    print(f"Stream processing completed in: {proc_time:.4f} seconds")
    print(f"Sustained Processing Throughput: {throughput:,.0f} rows/sec")
    print(f"Detected Critical Anomalies: {anomalies.shape[0]:,} events\n")

    # تحلیل داده‌ها با DuckDB
    duck_engine = DuckDBAnalyticsEngine()
    analytics_results = duck_engine.query_sensor_metrics(agg_df)

    print("--- In-Process OLAP Analytical Results (DuckDB) ---")
    table_data = [[r["sensor_id"], r["mean_temperature"], r["mean_voltage"], r["p95_vibration"], f"{r['total_events']:,}"] for r in analytics_results]
    print(tabulate(table_data, headers=["Sensor ID", "Avg Temp (°C)", "Avg Voltage (V)", "P95 Vibration", "Events"], tablefmt="grid"))

if __name__ == "__main__":
    main()
