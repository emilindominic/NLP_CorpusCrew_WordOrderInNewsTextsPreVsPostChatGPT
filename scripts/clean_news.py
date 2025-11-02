import argparse
import csv
from pathlib import Path
import re
import sys
import yaml
import pandas as pd


def clean_sentence(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'<.*?>', '', text)
    text = text.strip().strip('"').strip("'")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def token_count(text: str) -> int:
    return len(text.split())


def load_leipzig_corpus(corpus_dir: Path, corpus_name: str) -> pd.DataFrame:
    search_dirs = [corpus_dir]
    if corpus_dir.is_dir():
        parent = corpus_dir.parent
        if parent.exists() and parent not in search_dirs:
            search_dirs.append(parent)
    else:
        search_dirs = [corpus_dir]

    candidates = []
    for d in search_dirs:
        candidates.extend(list(d.glob(f"{corpus_name}-sentences.txt")))
        candidates.extend(list(d.glob(f"{corpus_name}_*-sentences.txt")))
        m = re.search(r"(\d{4})", corpus_name)
        if m:
            year = m.group(1)
            candidates.extend(list(d.glob(f"*news*{year}*-sentences.txt")))

    candidates = list(dict.fromkeys(candidates))

    if not candidates:
        raise FileNotFoundError(
            f"Could not find a '*-sentences.txt' for '{corpus_name}' in {', '.join(str(s) for s in search_dirs)}"
        )

    sent_fp = candidates[0]
    base_stem = sent_fp.name.replace("-sentences.txt", "")

    src_fp = sent_fp.with_name(f"{base_stem}-sources.txt")
    invso_fp = sent_fp.with_name(f"{base_stem}-inv_so.txt")

    if not src_fp.exists() or not invso_fp.exists():
        sources_exists = src_fp.exists()
        invso_exists = invso_fp.exists()
        print(f"Missing metadata for {base_stem}: "
              f"sources={sources_exists}, inv_so={invso_exists}. Proceeding without dates.")

    sentences = pd.read_csv(
        sent_fp, sep="\t", header=None,
        names=["sentence_id", "sentence"],
        quoting=csv.QUOTE_NONE, encoding="utf-8-sig", on_bad_lines="skip", engine="python"
    )

    if src_fp.exists() and invso_fp.exists():
        sources = pd.read_csv(
            src_fp, sep="\t", header=None,
            names=["source_id", "url", "date"],
            quoting=csv.QUOTE_NONE, encoding="utf-8-sig", on_bad_lines="skip", engine="python"
        )
        inv_so = pd.read_csv(
            invso_fp, sep="\t", header=None,
            names=["source_id", "sentence_id"],
            quoting=csv.QUOTE_NONE, encoding="utf-8-sig", on_bad_lines="skip", engine="python"
        )
        df = inv_so.merge(sources, on="source_id", how="left").merge(sentences, on="sentence_id", how="left")
    else:
        df = sentences.copy()
        df["source_id"] = pd.NA
        df["url"] = pd.NA
        df["date"] = pd.NA

    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=False)
    return df


def get_corpus_year(corpus_name: str):
    m = re.search(r"(\d{4})", corpus_name)
    return int(m.group(1)) if m else None


def sanitize_date(d):
    if pd.isna(d):
        return pd.NaT
    try:
        year = d.year
    except Exception:
        return pd.NaT
    return d if 1990 <= year <= 2025 else pd.NaT


def process_language(lang_cfg: dict, project_cfg: dict, paths_cfg: dict, cutoff: pd.Timestamp) -> list:
    lang_code = lang_cfg["code"]
    lang_name = lang_cfg["name"]
    raw_dir = Path(lang_cfg["raw_dir"])
    corpora = lang_cfg.get("corpora", [])
    split_2022 = lang_cfg.get("special_rules", {}).get("split_2022_by_month", False)

    out_root = Path(paths_cfg["clean_root"])
    out_root.mkdir(parents=True, exist_ok=True)

    def corpus_year_from_name(name: str):
        m = re.search(r"(\d{4})", name)
        return int(m.group(1)) if m else None

    def date_matches_corpus_year(d, corpus_year: int) -> bool:
        if pd.isna(d) or corpus_year is None:
            return False
        return d.year == corpus_year

    processed_dfs = []

    for corpus_name in corpora:
        corpus_dir = raw_dir / corpus_name
        if not corpus_dir.exists():
            corpus_dir = raw_dir

        try:
            df = load_leipzig_corpus(corpus_dir, corpus_name)
        except FileNotFoundError as e:
            print(f"{lang_code}/{corpus_name}: {e}")
            continue

        df["date"] = df["date"].apply(sanitize_date)
        df["language"] = lang_name

        df = df.dropna(subset=["sentence"])
        df["sentence"] = df["sentence"].astype(str).apply(clean_sentence)

        min_toks = int(project_cfg.get("min_tokens", 8))
        df = df[df["sentence"].apply(token_count) >= min_toks]

        if bool(project_cfg.get("deduplicate", True)):
            df = df.drop_duplicates(subset=["sentence"])

        c_year = corpus_year_from_name(corpus_name)
        df["year"] = pd.Series([pd.Int64Dtype().type(c_year)] * len(df), index=df.index)

        def decide_period(d):
            if pd.notnull(d) and date_matches_corpus_year(d, c_year):
                if split_2022 and d.year == 2022:
                    return "Pre-ChatGPT" if d.month <= 11 else "Post-ChatGPT"
                return "Pre-ChatGPT" if d <= cutoff else "Post-ChatGPT"
            if c_year is not None:
                return "Pre-ChatGPT" if c_year <= 2022 else "Post-ChatGPT"
            return "Pre-ChatGPT"

        df["period"] = df["date"].apply(decide_period)

        df_out = df[["language", "year", "period", "date", "sentence"]].copy()

        base_name = corpus_name
        prefix = f"{lang_code}_"
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix):]

        out_fp = out_root / f"{lang_code}_{base_name}.tsv"
        df_out.to_csv(out_fp, sep="\t", index=False)
        print(f"Saved {out_fp}  (rows: {len(df_out)})")
        processed_dfs.append(df_out)

    return processed_dfs


def main():
    ap = argparse.ArgumentParser(description="Preprocess Leipzig News corpora into clean TSVs.")
    ap.add_argument("--config", type=str, default="config/m1_config.yaml", help="Path to YAML config.")
    ap.add_argument("--lang", type=str, default=None, help="Process only specific language (eng|deu|rus)")
    args = ap.parse_args()

    cfg_path = Path(args.config)
    if not cfg_path.exists():
        print(f"Config not found: {cfg_path}")
        sys.exit(1)

    with open(cfg_path, "r", encoding="utf-8-sig") as f:
        cfg = yaml.safe_load(f)

    project_cfg = cfg.get("project", {})
    paths_cfg = cfg.get("paths", {})
    languages = cfg.get("languages", [])

    if args.lang:
        languages = [l for l in languages if l.get("code") == args.lang]
        if not languages:
            print(f"Error: Language '{args.lang}' not found in config")
            sys.exit(1)
        print(f"Processing only language: {args.lang}")

    cutoff_str = project_cfg.get("cutoff_date", "2022-11-30")
    cutoff = pd.to_datetime(cutoff_str, errors="coerce")

    all_dfs = []
    for lang in languages:
        dfs = process_language(lang, project_cfg, paths_cfg, cutoff)
        all_dfs.extend(dfs)

    if project_cfg.get("output_combined", True) and all_dfs:
        combined = pd.concat(all_dfs, ignore_index=True)
        combined["date"] = combined["date"].astype("string").fillna("")
        out_fp = Path(paths_cfg["clean_root"]) / "all_languages_clean.tsv"
        combined.to_csv(out_fp, sep="\t", index=False)
        print(f"Saved combined: {out_fp}  (rows: {len(combined)})")


if __name__ == "__main__":
    main()
