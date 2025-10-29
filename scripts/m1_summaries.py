import argparse
from pathlib import Path
import pandas as pd


def load_clean_tables(in_dir: Path) -> pd.DataFrame:
    combined = in_dir / "all_languages_clean.tsv"
    if combined.exists():
        return pd.read_csv(combined, sep="\t")
    parts = [p for p in in_dir.glob("*.tsv") if p.name != "all_languages_clean.tsv"]
    if not parts:
        raise FileNotFoundError(f"No TSV files found in {in_dir}")
    dfs = [pd.read_csv(p, sep="\t") for p in parts]
    return pd.concat(dfs, ignore_index=True)


def main():
    ap = argparse.ArgumentParser(description="Produce simple M1 coverage tables")
    ap.add_argument("--in_dir", type=str, default="data/clean", help="Clean TSV directory")
    ap.add_argument("--report_path", type=str, default="reports/m1_stats.md", help="Output Markdown path")
    args = ap.parse_args()

    in_dir = Path(args.in_dir)
    out_md = Path(args.report_path)
    out_md.parent.mkdir(parents=True, exist_ok=True)

    df = load_clean_tables(in_dir)

    # Basic schema checks
    required = {"language", "year", "period", "date", "sentence"}
    missing_cols = required - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing columns in input: {sorted(missing_cols)}")

    # Normalize types
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    # Treat date as text for missingness; empty string means "no date"
    df["date"] = df["date"].astype("string").fillna("")

    # Stable period order
    period_order = pd.CategoricalDtype(categories=["Pre-ChatGPT", "Post-ChatGPT"], ordered=True)
    df["period"] = df["period"].astype(period_order)

    # Main counts
    counts = (
        df.groupby(["language", "year", "period"], observed=True, dropna=False)
        .size()
        .reset_index(name="n_sentences")
        .sort_values(["language", "year", "period"])
    )

    # Per-language totals
    lang_totals = (
        counts.groupby("language", as_index=False)["n_sentences"].sum()
        .rename(columns={"n_sentences": "n_sentences_total"})
        .sort_values("language")
    )

    # Overall total
    overall_total = int(counts["n_sentences"].sum())

    # Missing date percentage by language
    missing = (
        df.assign(missing_date=(df["date"] == ""))
        .groupby("language", as_index=False)["missing_date"]
        .mean()
    )
    missing["pct_missing_date"] = (missing["missing_date"] * 100).round(2)
    missing = missing.drop(columns=["missing_date"]).sort_values("language")

    # Write markdown
    lines = []
    lines.append("# Milestone 1 — Coverage Summary\n")
    lines.append("## Sentences by language, year, period\n")
    lines.append(counts.to_markdown(index=False))
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
