import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/insert_figure_data.csv")

x_order = [100, 50, 25, 10, 5, 3, 1, 0]
x_pos = {v: i for i, v in enumerate(x_order)}

fig, ax = plt.subplots(figsize=(8, 5))

for tree_type, group in df.groupby("tree_type"):
    group_sorted = group.sort_values("k_sortedness", ascending=False)
    xs = [x_pos[v] for v in group_sorted["k_sortedness"]]
    ax.plot(
        xs,
        group_sorted["ingestion_throughput"],
        marker="o",
        label=tree_type,
    )

ax.set_xticks(range(len(x_order)))
ax.set_xticklabels([str(v) for v in x_order])
ax.set_xlabel("Sortedness (k)")
ax.set_ylabel("Ingestion Throughput (M ops/sec)")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
os.makedirs("figures", exist_ok=True)
plt.savefig("figures/ingestion_throughput.png", dpi=150)
plt.show()
