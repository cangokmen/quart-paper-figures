import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/tpcc_data.csv")

# Insertion throughput in M ops/sec
df["insertion_throughput"] = df["N"] / (df["insertion_time_ns"] / 1e9) / 1e6

fig, ax = plt.subplots(figsize=(8, 5))

n_values = sorted(df["N"].unique())
x_pos = {n: i for i, n in enumerate(n_values)}

for tree_type, group in df.groupby("tree_type"):
    group_sorted = group.sort_values("N")
    xs = [x_pos[n] for n in group_sorted["N"]]
    ax.plot(
        xs,
        group_sorted["insertion_throughput"],
        marker="o",
        label=tree_type,
    )

ax.set_xticks(range(len(n_values)))
ax.set_xticklabels([str(n) for n in n_values])
ax.set_xlabel("N (number of keys)")
ax.set_ylabel("Insertion Throughput (M ops/sec)")
ax.set_title("TPCC Insertion Throughput")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
os.makedirs("figures", exist_ok=True)
plt.savefig("figures/tpcc_insertion_throughput.png", dpi=150)
plt.show()
