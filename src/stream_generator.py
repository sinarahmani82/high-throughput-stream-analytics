import numpy as np
import pyarrow as pa
from typing import Dict, Any

class TelemetryStreamGenerator:
    """تولید جریان داده‌های با سرعت بالا از سنسورهای صنعتی IoT"""
    def __init__(self, seed: int = 42):
        np.random.seed(seed)

    def generate_batch(self, batch_size: int = 100_000) -> pa.Table:
        sensor_ids = np.random.choice(["SENSOR_A", "SENSOR_B", "SENSOR_C", "SENSOR_D"], size=batch_size)
        temperature = np.random.normal(70.0, 5.0, size=batch_size)
        vibration = np.random.exponential(1.5, size=batch_size)
        voltage = np.random.normal(220.0, 2.0, size=batch_size)

        # تزریق تعمدی ناهنجاری برای سنجش پایپ‌لاین (Anomaly Injection)
        anomaly_indices = np.random.choice(batch_size, size=int(batch_size * 0.01), replace=False)
        vibration[anomaly_indices] += 15.0

        data = {
            "sensor_id": pa.array(sensor_ids),
            "temperature": pa.array(temperature, type=pa.float32()),
            "vibration": pa.array(vibration, type=pa.float32()),
            "voltage": pa.array(voltage, type=pa.float32())
        }
        return pa.Table.from_pydict(data)
