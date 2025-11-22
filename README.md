# Course: NLP & Information Extraction (2025WS)

**Topic: Word Order Change in News Before and After ChatGPT**

---

## Team Information
**Corpus Crew (Group 10)**

| Name             | Stud. ID |
|------------------|----------|
| Assylbek Tleules | 12432843 |
| Emily Jacob      | 12143768 |
| Luka             | 12332270 |
| Tehseen Ali Tahir| 12433763 |

---
## Project Overview
Our project investigates **word order patterns in online news articles** before and after the public release of ChatGPT (Nov 2022).
We analyze how syntactic preferences may have shifted between the *Pre-ChatGPT* and *Post-ChatGPT* periods in **English, German, and Russian**, using corpora from the **Leipzig Corpora Collection (News)**.

# Milestone 2: Word Order Extraction & Analysis

## What We Did

In Milestone 2, we extracted word order patterns from the dependency-parsed sentences we created in M1. The goal was to identify how subjects, verbs and objects are arranged in news articles across three languages.

### Main Tasks:
1. **Word Order Extraction**: We wrote script that reads CoNLL-U files from M1 and identifies the Subject-Verb-Object structure in each sentence
2. **Pattern Classification**: Each sentence gets labeled with its word order pattern (like SVO, SOV, VSO, etc)
3. **Data Splitting**: We split the extracted data into training, validation and test sets for future machine learning experiments.
4. continue...
### How It Works

The extraction focuses on the **main clause only** to avoid mixing elements from different parts of complex sentences. We look for:
- **Subject (S)**: nouns that act as the subject of the main verb
- **Verb (V)**: the root verb of the sentence
- **Object (O)**: direct objects of the main verb

Based on their positions in the sentence, we classify them into one of six possible orders: SVO, SOV, VSO, VOS, OSV, or OVS. If sentence is missing some elements, we label it as incomplete or partial (like "SV_only" if there is no object).

## Running the Pipeline

Make sure you already completed Milestone 1 and have the `.conllu` files in `data/conllu/`.

### Step 1: Extract Word Orders

```bash
# Process all languages
bash run_word_order.sh

# Or use Python directly
python scripts/extract_word_order.py --input data/conllu --output data/word_order_all_languages.csv

# Test mode (useful for quick checks)
bash run_word_order.sh --test 100
```

This creates `data/word_order_all_languages.csv` with word order labels for all sentences.

### Step 2: Split Data

```bash
python scripts/split_data.py --config config/m2_config.yaml
```

This creates three files in `data/splits/`:
- `train.csv` (70% of data)
- `val.csv` (15% of data)
- `test.csv` (15% of data)

The split is stratified by language, so each set has balanced mix of English, German and Russian sentences.

## Configuration

All settings are in `config/m2_config.yaml`:
- **cutoff_date**: 2022-11-30 (separates Pre-ChatGPT vs Post-ChatGPT periods)
- **data_split**: ratios for train/val/test (70/15/15)
- **random_seed**: 10 (our group number)
- **stratify_by_language**: keeps language distribution balanced across splits

## What We Got

After running the pipeline, we extracted **154,192 sentences** from all three languages:
- **English**: 47,109 sentences (29.1% are SVO)
- **German**: 55,041 sentences (10.8% are SVO)
- **Russian**: 52,042 sentences (14.5% are SVO)

### Word Order Distribution:
- **SV_only**: 48.1% (sentences with subject and verb, but no direct object)
- **INCOMPLETE**: 23.3% (missing key elements)
- **SVO**: 17.7% (full Subject-Verb-Object pattern)
- **SOV**: 3.6%
- **Others**: less than 3% each

The data shows that English strongly prefers SVO order, while German and Russian use it less often (which makes sense given their more flexible word order).

## Repository Structure (M2 additions)

```
├─ config/
│  └─ m2_config.yaml                # M2 settings (word order extraction, data split)
│
├─ data/
│  ├─ word_order_all_languages.csv  # extracted word orders for all sentences
│  └─ splits/                       # train/val/test splits for ML
│     ├─ train.csv
│     ├─ val.csv
│     └─ test.csv
│
├─ scripts/
│  ├─ extract_word_order.py         # extracts S-V-O patterns from CoNLL-U files
│  └─ split_data.py                 # splits data into train/val/test sets
│
├─ reports/                         # analysis outputs and statistics
│
├─ run_word_order.sh                # convenient script to run word order extraction
└─ requirements.txt                 # Python dependencies
```

## Notes

- The extraction script only looks at the **main clause** to avoid confusing word orders from subordinate clauses
- Sentences without clear root verb or missing critical elements are marked as "INCOMPLETE"
- All scripts handle three languages automatically
