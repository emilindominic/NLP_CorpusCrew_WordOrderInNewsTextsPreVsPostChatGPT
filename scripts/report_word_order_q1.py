"""
Md report for Topic 4, Q1:

Input: data/word_order_all_languages.csv
Output: reports/word_order_q1.md + simple plots
"""

from pathlib import Path
from typing import List, Sequence, Tuple

import pandas as pd

import matplotlib
# headless backend for CLI runs
matplotlib.use("Agg")
import matplotlib.pyplot as plt


DATA_PATH = Path("data/word_order_all_languages.csv")
REPORT_PATH = Path("reports/word_order_q1.md")
PLOTS_DIR = Path("reports/plots")
PLOT_SVO_PERIOD = PLOTS_DIR / "q1_svo_period.png"
PLOT_SVO_YEAR = PLOTS_DIR / "q1_svo_year.png"
PLOT_STACKED_PERIOD = PLOTS_DIR / "q1_stacked_period.png"
PLOT_HEATMAP_YEAR = PLOTS_DIR / "q1_heatmap_year.png"

# keep order labels stable, even if some are missing
ORDER_LABELS: List[str] = [
    "SVO",
    "SOV",
    "VSO",
    "VOS",
    "OVS",
    "OSV",
    "VO_only",
    "SV_only",
    "SO_only",
    "INCOMPLETE",
    "UNCLEAR",
]
FULL_ORDERS: List[str] = ["SVO", "SOV", "VSO", "VOS", "OVS", "OSV"]
PARTIAL_ORDERS: List[str] = ["VO_only", "SV_only", "SO_only", "INCOMPLETE", "UNCLEAR"]


def sort_year_value(val):
    """Sort years numerically where possible, keep unknown at the end."""
    if str(val) == "unknown":
        return float("inf")
    try:
        return int(val)
    except ValueError:
        return val


def df_to_md(df: pd.DataFrame) -> str:
    """Convert df to a simple markdown table."""
    headers = ["| " + " | ".join(df.columns.astype(str)) + " |"]
    separator = ["|" + "|".join([" --- " for _ in df.columns]) + "|"]
    rows = [
        "| "
        + " | ".join(str(val) for val in row)
        + " |"
        for row in df.itertuples(index=False, name=None)
    ]
    return "\n".join(headers + separator + rows)


def format_counts_and_share(
    grouped: pd.DataFrame, shares: pd.DataFrame, orders: Sequence[str]
) -> pd.DataFrame:
    """Return table with count (pct%) strings and total."""
    table = pd.DataFrame(index=grouped.index)
    for order in orders:
        def fmt(idx) -> str:
            count = grouped.at[idx, order] if order in grouped.columns else 0
            denom = grouped.at[idx, "total"]
            pct = 0.0 if denom == 0 else shares.at[idx, order]
            return f"{count} ({pct:.1f}%)"

        table[order] = [fmt(idx) for idx in grouped.index]

    table["total"] = grouped["total"]
    return table.reset_index()


def order_distribution(
    df: pd.DataFrame, group_cols: Sequence[str], orders: Sequence[str]
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Compute count + share tables by group.
    Returns (formatted_table, raw_counts, shares).
    """
    counts = (
        df.groupby(list(group_cols) + ["word_order"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=orders, fill_value=0)
    )

    counts["total"] = counts.sum(axis=1)
    shares = counts.div(counts["total"].replace(0, pd.NA), axis=0) * 100
    shares = shares.fillna(0.0)

    formatted = format_counts_and_share(counts, shares, orders)
    return formatted, counts, shares


def compact_summary(counts: pd.DataFrame) -> pd.DataFrame:
    """Compact view: full orders plus partial bucket share."""
    # counts index is multiindex of group cols
    df = counts.copy()
    df["partial_total"] = df[PARTIAL_ORDERS].sum(axis=1)
    compact_cols = FULL_ORDERS + ["partial_total", "total"]
    return df[compact_cols].reset_index()


def compact_with_pct(counts: pd.DataFrame, shares: pd.DataFrame) -> pd.DataFrame:
    """Compact view with count (pct%)."""
    comp_counts = counts.copy()
    comp_counts["partial_total"] = comp_counts[PARTIAL_ORDERS].sum(axis=1)
    comp_shares = shares.copy()
    comp_shares["partial_total"] = comp_shares[PARTIAL_ORDERS].sum(axis=1)
    orders_compact = FULL_ORDERS + ["partial_total"]
    return format_counts_and_share(comp_counts, comp_shares, orders_compact)


def plot_svo_by_period(share_period: pd.DataFrame) -> None:
    """Bar chart: SVO share per language, split by period."""
    # share_period index = (language, period)
    plot_df = (
        share_period.reset_index()[["language", "period", "SVO"]]
        .query("period != 'unknown'")
        .rename(columns={"SVO": "svo_pct"})
    )

    if plot_df.empty:
        return

    plt.figure(figsize=(8, 4))
    for lang in sorted(plot_df["language"].unique()):
        subset = plot_df[plot_df["language"] == lang]
        plt.bar(
            subset["period"],
            subset["svo_pct"],
            alpha=0.6,
            label=lang,
        )

    plt.ylabel("SVO share (%)")
    plt.title("SVO share by period (Pre vs Post ChatGPT)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOT_SVO_PERIOD, dpi=150)
    plt.close()


def plot_svo_by_year(share_year: pd.DataFrame) -> None:
    """Line chart: SVO share per language over years."""
    plot_df = share_year.reset_index()
    plot_df = plot_df[plot_df["year"] != "unknown"]

    if plot_df.empty:
        return

    plot_df["year_num"] = plot_df["year"].apply(sort_year_value)
    plot_df = plot_df[plot_df["year_num"] != float("inf")]
    years_sorted = sorted(plot_df["year_num"].unique())

    plt.figure(figsize=(8, 4))
    for lang in sorted(plot_df["language"].unique()):
        subset = plot_df[plot_df["language"] == lang].copy()
        subset = subset.sort_values("year_num")
        plt.plot(subset["year_num"], subset["SVO"], marker="o", label=lang)

    plt.ylabel("SVO share (%)")
    plt.title("SVO share by year")
    plt.xticks(years_sorted, [str(int(y)) for y in years_sorted], rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOT_SVO_YEAR, dpi=150)
    plt.close()


def plot_stacked_period(period_shares: pd.DataFrame) -> None:
    """Stacked bars per language for full orders, pre vs post."""
    if period_shares.empty:
        return

    plot_df = (
        period_shares.reset_index()[["language", "period"] + FULL_ORDERS]
        .query("period != 'unknown'")
    )
    if plot_df.empty:
        return

    langs = sorted(plot_df["language"].unique())
    periods = ["Pre-ChatGPT", "Post-ChatGPT"]
    x_positions = range(len(langs))

    width = 0.38
    colors = plt.get_cmap("tab20").colors
    order_colors = {order: colors[i % len(colors)] for i, order in enumerate(FULL_ORDERS)}

    plt.figure(figsize=(9, 5))
    for i, period in enumerate(periods):
        bottoms = [0] * len(langs)
        for order in FULL_ORDERS:
            heights = []
            for lang in langs:
                row = plot_df[(plot_df["language"] == lang) & (plot_df["period"] == period)]
                val = row[order].values[0] if not row.empty else 0
                heights.append(val)

            plt.bar(
                [x + (i - 0.5) * width for x in x_positions],
                heights,
                width=width,
                bottom=bottoms,
                color=order_colors[order],
                edgecolor="white",
            )
            bottoms = [b + h for b, h in zip(bottoms, heights)]

    plt.xticks([x for x in x_positions], langs)
    plt.ylabel("Share (%)")
    plt.title("Full word orders by language and period")
    handles = [plt.Rectangle((0, 0), 1, 1, color=order_colors[o]) for o in FULL_ORDERS]
    plt.legend(handles, FULL_ORDERS, title="Order", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(PLOT_STACKED_PERIOD, dpi=150)
    plt.close()


def plot_heatmap_year(year_shares: pd.DataFrame) -> None:
    """Heatmap per language showing full order shares over years."""
    if year_shares.empty:
        return

    plot_df = year_shares.reset_index()
    plot_df = plot_df[plot_df["year"] != "unknown"]
    if plot_df.empty:
        return

    plot_df["year_num"] = plot_df["year"].apply(sort_year_value)
    plot_df = plot_df[plot_df["year_num"] != float("inf")]

    langs = sorted(plot_df["language"].unique())
    plt.figure(figsize=(10, 3 * len(langs)))

    for idx, lang in enumerate(langs, start=1):
        subset = plot_df[plot_df["language"] == lang].copy()
        subset = subset.sort_values("year_num")
        data = subset[FULL_ORDERS]
        years = [str(int(y)) for y in subset["year_num"].tolist()]

        ax = plt.subplot(len(langs), 1, idx)
        im = ax.imshow(data, aspect="auto", cmap="Blues", vmin=0, vmax= max(1.0, data.values.max()))
        ax.set_xticks(range(len(FULL_ORDERS)))
        ax.set_xticklabels(FULL_ORDERS)
        ax.set_yticks(range(len(years)))
        ax.set_yticklabels(years)
        ax.set_title(f"{lang}: full order share (%)")
        for i in range(len(years)):
            for j in range(len(FULL_ORDERS)):
                ax.text(j, i, f"{data.values[i][j]:.0f}", ha="center", va="center", color="black", fontsize=8)

    plt.tight_layout()
    plt.savefig(PLOT_HEATMAP_YEAR, dpi=150)
    plt.close()


def main() -> None:
    if not DATA_PATH.exists():
        raise SystemExit(f"Input not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    df["word_order"] = df["word_order"].fillna("INCOMPLETE")
    orders = ORDER_LABELS

    # Summary numbers
    total_sentences = len(df)
    languages = ", ".join(sorted(df["language"].unique()))
    period_counts = df["period"].value_counts().to_dict()

    # Pre/Post by language
    period_table, period_counts_raw, period_shares = order_distribution(
        df, ["language", "period"], orders
    )

    # yearly by language
    year_table, year_counts_raw, year_shares = order_distribution(df, ["language", "year"], orders)
    # ensure year ordering
    years_sorted = sorted(df["year"].unique(), key=sort_year_value)
    langs_sorted = sorted(df["language"].unique())
    idx = pd.MultiIndex.from_product([langs_sorted, years_sorted], names=["language", "year"])
    year_counts_raw = year_counts_raw.reindex(idx).fillna(0)
    year_counts_raw["total"] = year_counts_raw.sum(axis=1)
    year_counts_raw = year_counts_raw[year_counts_raw["total"] > 0]
    year_shares = year_counts_raw.div(year_counts_raw["total"].replace(0, pd.NA), axis=0) * 100
    year_shares = year_shares.fillna(0.0)
    year_table = format_counts_and_share(year_counts_raw, year_shares, orders)

    # compact views with pct
    compact_period = compact_with_pct(period_counts_raw, period_shares)
    compact_year = compact_with_pct(year_counts_raw, year_shares)

    # quick deltas for SVO pre vs post
    deltas = []
    for lang in sorted(df["language"].unique()):
        pre = period_shares.loc[(lang, "Pre-ChatGPT"), "SVO"] if (
            lang,
            "Pre-ChatGPT",
        ) in period_shares.index else 0.0
        post = period_shares.loc[(lang, "Post-ChatGPT"), "SVO"] if (
            lang,
            "Post-ChatGPT",
        ) in period_shares.index else 0.0
        deltas.append((lang, pre, post, post - pre))

    # plots
    plot_svo_by_period(period_shares)
    plot_svo_by_year(year_shares)
    plot_stacked_period(period_shares)
    plot_heatmap_year(year_shares)

    lines = []
    lines.append("# Word order trends (Q1)")
    lines.append("")
    lines.append(
        "Data from data/word_order_all_languages.csv. "
        f"Total sentences: {total_sentences}. "
        f"Languages: {languages}. "
        f"Period labels counts: {period_counts}."
    )
    lines.append(
        "Goal: show how word order labels move over time (Pre vs Post and by year), per language."
    )
    lines.append("")
    lines.append("## Quick read")
    for lang, pre, post, delta in deltas:
        trend = "up" if delta > 0 else "down" if delta < 0 else "flat"
        lines.append(
            f"- {lang}: SVO share pre {pre:.1f}%, post {post:.1f}% ({trend} {delta:+.1f} pp)."
        )
    lines.append(
        "- Partial/INCOMPLETE is large, so full S-V-O extraction is not always possible."
    )
    if period_counts.get("unknown", 0) > 0:
        lines.append(
            f"- There are {period_counts['unknown']} sentences with period=unknown, kept but separate."
        )

    lines.append("")
    lines.append("## Compact view")
    lines.append("")
    lines.append(df_to_md(compact_period))

    lines.append("")
    lines.append("### Yearly compact")
    lines.append("")
    lines.append(df_to_md(compact_year))

    lines.append("")
    lines.append("## Pre vs Post ChatGPT")
    lines.append("")
    lines.append(df_to_md(period_table))

    lines.append("")
    lines.append("## Yearly view")
    lines.append("")
    lines.append(df_to_md(year_table))

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written to {REPORT_PATH}")
    print(f"Plots: {PLOT_SVO_PERIOD} , {PLOT_SVO_YEAR}")


if __name__ == "__main__":
    main()
