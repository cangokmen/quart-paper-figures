import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ── Load data ────────────────────────────────────────────────────────────────
df = pd.read_csv("data/quit_experiments.csv")

N = 500_000_000  # encoded in workload name

# Parse K and L from workload string, e.g. "workload_N500000000_K25_L100"
def parse_kl(w):
    m = re.search(r"_K(\d+)_L(\d+)", w)
    return int(m.group(1)), int(m.group(2))

df[["k", "l"]] = df["workload"].apply(lambda w: pd.Series(parse_kl(w)))

# Convert insertion_time_ns to numeric, turning "ERROR" → NaN
df["insertion_time_ns"] = pd.to_numeric(df["insertion_time_ns"], errors="coerce")

# Throughput in M ops/sec
df["throughput_Mops"] = N / df["insertion_time_ns"] * 1e9 / 1e6  # → M ops/sec

# ── Define x-axis order ──────────────────────────────────────────────────────
# Group by k descending, then l descending within each k group
k_order = sorted(df["k"].unique(), reverse=True)   # [100, 25, 10, 5, 1, 0]
l_order = sorted(df["l"].unique(), reverse=True)   # [100, 25, 10, 5, 1, 0]

workload_order = []
for k in k_order:
    for l in l_order:
        if ((df["k"] == k) & (df["l"] == l)).any():
            workload_order.append((k, l))

x_index = {kl: i for i, kl in enumerate(workload_order)}
x_labels = [f"k={k},l={l}" for k, l in workload_order]

# ── Plot ─────────────────────────────────────────────────────────────────────
TREE_STYLES = {
    "ART":                    dict(color="#1f77b4", marker="o",  linestyle="-",  label="ART"),
    "QuART_stail_reset_bidir":dict(color="#ff7f0e", marker="s",  linestyle="--", label="QuART"),
    "QuIT":                   dict(color="#2ca02c", marker="^",  linestyle="-.", label="QuIT"),
}

fig, ax = plt.subplots(figsize=(16, 5))

for tree_type, style in TREE_STYLES.items():
    sub = df[df["tree_type"] == tree_type].copy()
    sub["x"] = sub.apply(lambda r: x_index.get((r["k"], r["l"]), None), axis=1)
    sub = sub.dropna(subset=["x"]).sort_values("x")
    ax.plot(
        sub["x"],
        sub["throughput_Mops"],
        marker=style["marker"],
        color=style["color"],
        linestyle=style["linestyle"],
        linewidth=1.6,
        markersize=5,
        label=style["label"],
    )

# ── Vertical separators between k groups ─────────────────────────────────────
prev_k = workload_order[0][0]
for i, (k, l) in enumerate(workload_order[1:], start=1):
    if k != prev_k:
        ax.axvline(x=i - 0.5, color="gray", linestyle=":", linewidth=0.8, alpha=0.7)
    prev_k = k

# ── Axes formatting ───────────────────────────────────────────────────────────
ax.set_xticks(range(len(workload_order)))
ax.set_xticklabels(x_labels, rotation=45, ha="right", fontsize=7.5)
ax.set_ylabel("Insert Throughput (M ops/sec)")
ax.set_xlabel("Workload")
ax.set_title("Insert Throughput across QuIT Workloads")
ax.legend(loc="upper left")
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.set_xlim(-0.5, len(workload_order) - 0.5)

plt.tight_layout()
os.makedirs("figures", exist_ok=True)
plt.savefig("figures/quit_insert_throughput.png", dpi=150)
plt.show()
print("Saved → figures/quit_insert_throughput.png")
