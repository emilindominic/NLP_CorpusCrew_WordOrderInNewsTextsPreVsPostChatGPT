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

**Please open README.md and read in "Code" mode, because some parts are not viewed as they should.**

## Project Overview
Our project investigates **word order patterns in online news articles** before and after the public release of ChatGPT (Nov 2022).  
We analyze how syntactic preferences may have shifted between the *Pre-ChatGPT* and *Post-ChatGPT* periods in **English, German, and Russian**, using corpora from the **Leipzig Corpora Collection (News)**.

This branch covers **Milestone 1**, which focuses on **data preprocessing** and **corpus preparation** for further linguistic analysis.

---
## Environment Setup

No need to manually install anything — the `run.sh` script will automatically:
- Create and activate a virtual environment (if missing)
- Install all dependencies from `requirements.txt`
- Execute all steps for Milestone 1

Just make sure **Python 3.12** is available on your system.

## Configuration

All settings live in config/m1_config.yaml. The key fields:
	•	project.cutoff_date: date that separates Pre vs Post (default 2022-11-30).
	•	project.min_tokens: minimum tokens per sentence kept (default 8).
	•	project.deduplicate: remove exact duplicate sentences (default true).
	•	languages[*].raw_dir: where raw Leipzig corpora reside (per language).
	•	languages[*].corpora: list of corpus base names (e.g., eng_news_2019).
	•	languages[*].special_rules.split_2022_by_month (German only): Jan–Nov 2022 = Pre, Dec 2022 = Post.

## Adding Raw Data

Place the Leipzig files under data/raw/<language>/<corpus_name>/ with the original stems.
data/raw/english/eng_news_2019/eng_news_2019_100K-sentences.txt
data/raw/english/eng_news_2019/eng_news_2019_100K-sources.txt
data/raw/english/eng_news_2019/eng_news_2019_100K-inv_so.txt

## Outputs

Running bash run.sh produces:
	•	Cleaned TSVs per corpus in data/clean/, named like eng_news_2019.tsv, deu_news_2022.tsv, rus_news_2024.tsv.
	•	A combined table data/clean/all_languages_clean.tsv.
	•	A coverage report reports/m1_stats.md with sentence counts per language × year × period, plus missing date rates.

## Repository Structure

├─ config/
│  └─ m1_config.yaml
├─ data/
│  ├─ raw/              # place Leipzig corpora here (git-ignored)
│  └─ clean/            # generated outputs (git-ignored)
├─ scripts/
│  ├─ clean_news.py     # preprocessing pipeline
│  └─ m1_summaries.py   # coverage tables --> reports/m1_stats.md
├─ reports/
│  └─ m1_stats.md
├─ notebooks/
│  └─ TextPreprocessing.ipynb
├─ run.sh
├─ requirements.txt
└─ README.md
