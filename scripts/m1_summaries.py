import argparse
from pathlib import Path
import pandas as pd


def load_clean_tables(in_dir: Path) -> pd.DataFrame:
    """
    Load the cleaned TSV data.

    Priority:
    1. all_languages_clean.tsv if it exists
    2. otherwise, concatenate all *.tsv in the folder
       (except all_languages_clean.tsv to avoid double counting)
    """
    combined = in_dir / "all_languages_clean.tsv"
    if combined.exists():
        return pd.read_csv(combined, sep="\t")

    parts = [p for p in in_dir.glob("*.tsv") if p.name != "all_languages_clean.tsv"]
    if not parts:
        raise FileNotFoundError(f"No TSV files found in {in_dir}")

    dfs = [pd.read_csv(p, sep="\t") for p in parts]
    return pd.concat(dfs, ignore_index=True)


def main():
    ap = argparse.ArgumentParser(description="Produce M1 coverage + cleanup stats report")
    ap.add_argument(
        "--in_dir",
        type=str,
        default="data/clean",
        help="Directory containing cleaned TSV files"
    )
    ap.add_argument(
        "--report_path",
        type=str,
        default="reports/m1_stats.md",
        help="Output Markdown path"
    )
    args = ap.parse_args()

    in_dir = Path(args.in_dir)
    out_md = Path(args.report_path)
    out_md.parent.mkdir(parents=True, exist_ok=True)

    df = load_clean_tables(in_dir)

    required_cols = {"language", "year", "period", "date", "sentence"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing columns in input data: {sorted(missing_cols)}")

    # Normalize types
    # year should be Int64
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

    # date stays as string, "" means "no usable date metadata"
    df["date"] = df["date"].astype("string").fillna("")

    # fix period to a consistent category order
    period_order = pd.CategoricalDtype(
        categories=["Pre-ChatGPT", "Post-ChatGPT"],
        ordered=True
    )
    df["period"] = df["period"].astype(period_order)

    # Sentence length stats after cleaning
    # this gives us an idea of how long the sentences are in each slice
    df["n_tokens"] = df["sentence"].str.split().str.len()

    length_stats = (
        df.groupby(["language", "year", "period"], observed=True)["n_tokens"]
        .agg(
            mean="mean",
            median="median",
            p05=lambda s: s.quantile(0.05),
            p95=lambda s: s.quantile(0.95),
        )
        .round(2)
        .reset_index()
        .sort_values(["language", "year", "period"])
    )

    # Main counts per language/year/period
    counts = (
        df.groupby(["language", "year", "period"], observed=True, dropna=False)
        .size()
        .reset_index(name="n_sentences")
        .sort_values(["language", "year", "period"])
    )

    # Totals by language
    lang_totals = (
        counts.groupby("language", as_index=False)["n_sentences"]
        .sum()
        .rename(columns={"n_sentences": "n_sentences_total"})
        .sort_values("language")
    )

    overall_total = int(counts["n_sentences"].sum())

    # Missing-date share by language
    missing = (
        df.assign(missing_date=(df["date"] == ""))
        .groupby("language", as_index=False)["missing_date"]
        .mean()
    )
    missing["pct_missing_date"] = (missing["missing_date"] * 100).round(2)
    missing = (
        missing.drop(columns=["missing_date"])
        .sort_values("language")
    )

    # Markdown report
    lines = []
    lines.append("# Milestone 1 — Coverage Summary\n")

    lines.append("## Sentences by language, year, period\n")
    lines.append(counts.to_markdown(index=False))

    lines.append("\n\n## Token length (after cleaning)\n")
    lines.append(length_stats.to_markdown(index=False))

    lines.append("\n\n## Totals by language\n")
    lines.append(lang_totals.to_markdown(index=False))

    lines.append(f"\n\n**Overall total sentences:** {overall_total}\n")

    lines.append("\n## Missing date percentage by language\n")
    lines.append(missing.to_markdown(index=False))
    lines.append("\n")

    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
