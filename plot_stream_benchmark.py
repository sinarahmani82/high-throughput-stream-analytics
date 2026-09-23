import matplotlib.pyplot as plt
import numpy as np

# داده‌های بنچمارک مقیاس‌پذیری
scales = ["100K Rows", "500K Rows", "1M Rows", "2M Rows"]
throughput_polars = [1_850_000, 2_100_000, 2_450_000, 2_600_000] # rows/sec
memory_polars = [28, 64, 118, 225] # MB RAM
memory_pandas = [95, 380, 790, 1620] # MB RAM (Standard Pandas baseline)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# نمودار ۱: Processing Throughput
colors = ['#007acc', '#0099ff', '#33adff', '#66c2ff']
bars = ax1.bar(scales, [t/1e6 for t in throughput_polars], color='#007acc', edgecolor='black', alpha=0.85, width=0.5)
ax1.set_ylabel('Throughput (Million Rows / Sec)', fontsize=11, fontweight='bold')
ax1.set_title('A. Vectorized Streaming Throughput (Polars Engine)', fontsize=12, fontweight='bold', pad=12)
ax1.set_ylim(0, 3.2)

for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.08, f"{yval:.2f}M/s", ha='center', fontweight='bold', fontsize=10)

# نمودار ۲: Memory Footprint Comparison (Polars vs Pandas)
x = np.arange(len(scales))
width = 0.35
ax2.bar(x - width/2, memory_polars, width, label='Polars (Zero-Copy Arrow)', color='#2ecc71', edgecolor='black', alpha=0.9)
ax2.bar(x + width/2, memory_pandas, width, label='Traditional Pandas', color='#e74c3c', edgecolor='black', alpha=0.9)

ax2.set_ylabel('Peak RAM Usage (MB)', fontsize=11, fontweight='bold')
ax2.set_title('B. Memory Footprint: Polars vs. Pandas Baseline', fontsize=12, fontweight='bold', pad=12)
ax2.set_xticks(x)
ax2.set_xticklabels(scales, fontsize=10, fontweight='bold')
ax2.legend(frameon=True, loc='upper left')

plt.tight_layout()
output_filename = "stream_benchmarks.png"
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
plt.close()
print(f"Benchmark plot successfully saved as: {output_filename}")
