# Course: NLP & Information Extraction (2025WS) 

**Topic: Word Order Change in News Before and After ChatGPT**
**Milestone 1: Text Preprocessing**

---

## Team Information
Corpus Crew (group 10)

| Name             | Stud. ID |
|------------------|----------|
| Assylbek Tleules | 12432843 |
| Emily Jacob      | 12143768 |
| Luka             | 12332270 |
| Tehseen Ali Tahir| 12433763 |

---

**Please open README.md and read in "Code" mode, otherwise some indents and tree structures may not display properly.**

## Project Overview
Our project investigates **word order patterns in online news articles** before and after the public release of ChatGPT (Nov 2022).  
We analyze how syntactic preferences may have shifted between the *Pre-ChatGPT* and *Post-ChatGPT* periods in **English, German, and Russian**, using corpora from the **Leipzig Corpora Collection (News)**.

This branch covers **Milestone 1**, which focuses on **data preprocessing, cleaning, and linguistic annotation** to prepare standardized corpora for later syntactic and statistical analysis.

---
## Environment Setup

No need to manually install anything — the `run.sh` script will automatically:
- Create and activate a virtual environment (if missing)
- Install all dependencies from `requirements.txt`
- Execute all steps for Milestone 1

Just make sure **Python 3.12** is available on your system.

```bash
# Run the full pipeline for all languages
bash run.sh

# Example: only English
bash run.sh --lang eng

# Example: test mode (100 sentences per file)
bash run.sh --test

# Example: test mode for 1 language
bash run.sh --lang rus --test
```

## Configuration

All settings live in config/m1_config.yaml. The key fields:
	•	project.cutoff_date — date separating Pre vs Post-ChatGPT (default 2022-11-30)
	•	project.min_tokens — minimum token count per sentence (default 8)
	•	project.deduplicate — whether to remove duplicate sentences (default true)
	•	languages[*].raw_dir — path to raw Leipzig corpora (per language)
	•	languages[*].corpora — list of corpus basenames (eng_news_2019)
	•	languages[*].special_rules.split_2022_by_month — Jan–Nov 2022 -> Pre-ChatGPT, Dec 2022 -> Post-ChatGPT

## Adding Raw Data

Place the Leipzig files under: data/raw/<language>/<corpus_name>/ with the original stems.
data/raw/english/eng_news_2019_10K/eng_news_2019_10K-sentences.txt
data/raw/english/eng_news_2019_10K/eng_news_2019_10K-sources.txt
data/raw/english/eng_news_2019_10K/eng_news_2019_10K-inv_so.txt

## Outputs

Running bash run.sh produces:
	•	Cleaned TSVs per corpus in data/clean/, named like eng_news_2019_10K.tsv, deu_news_2022_10K.tsv and etc.
	•	A combined table data/clean/all_languages_clean.tsv
	•	Linguistic annotations in CoNLL-U format (data/conllu/)
	•	A coverage report reports/m1_stats.md containing per-language/year/period sentence counts, token statistics and missing-date rates.

## Validation

To verify annotations and metadata consistency, run:
```bash
python scripts/validate_m1.py
```

The output should contain - Status: Pass
All steps are deterministic — rerunning the same pipeline reproduces identical cleaned and annotated corpora.

## Repository Structure

├─ config/
│  └─ m1_config.yaml
│
├─ data/
│  ├─ raw/               # place Leipzig corpora here (git-ignored)
│  ├─ clean/             # cleaned TSVs (auto-generated)
│  └─ conllu/            # annotated CoNLL-U files (auto-generated)
│
├─ scripts/
│  ├─ clean_news.py      # cleaning pipeline
│  ├─ annotate_news.py   # stanza-based annotation → CoNLL-U
│  ├─ validate_m1.py     # format & metadata validation
│  └─ m1_summaries.py    # summary stats → reports/m1_stats.md
│
├─ reports/
│  └─ m1_stats.md
│
├─ notebooks/
│  └─ TextPreprocessing.ipynb
│
├─ run.sh
├─ requirements.txt
└─ README.md
