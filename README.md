# Course: NLP & Information Extraction (2025WS)

**Topic 4: Word Order Change in News Before and After ChatGPT**

---

## Team Information
**Corpus Crew (Group 10)**

| Name             | Stud. ID |
|------------------|----------|
| Assylbek Tleules | 12432843 |
| Emily Jacob      | 12143768 |
| Luka Santek      | 12332270 |
| Tehseen Ali Tahir| 12433763 |

---

# Milestone 2: Word Order Extraction & Analysis

## What We Did
  - **Word Order Extraction**: From M1 CoNLL-U files, extract main-clause S, V, O and assign a word order label (SVO/SOV/VSO/VOS/OSV/OVS or partials like SV_only, VO_only, INCOMPLETE).
  - **Data Splitting**: Stratified by language into train/val/test.
  - **Baselines**:
    - Rule-based:
      - **Simple heuristic**: find first verb; check if nouns appear before/after --> SVO, SV_only, VO_only, INCOMPLETE.
      - **POS-pattern**: first verb + first two nouns as S/V/O candidates; map to canonical orders or INCOMPLETE.
    - ML (binary): predict **SVO vs non-SVO** using BoW/TF-IDF features with Logistic Regression, Multinomial Naive Bayes and Linear SVM.
    - ML (multiclass): predict SVO word order as one of the 9 classes (SVO, SV_only, VSO, INCOMPLETE, etc.) with Logistic Regression, Multinomial Naive Bayes and Linear SVM.
  - **Evaluation**: Rule-based baselines evaluated against Stanza-derived labels (`reports/rule_based_baselines.md`); ML CV/val in `reports/report_binary.md` and `reports/report_multiclass.md`.


## Ground truth using Stanza
We treat Stanza dependency parses as the current “ground truth”: main-clause root verb, nsubj/nsubj:pass and obj linked to that root define S/V/O and the order label. This is our working label source for baselines and ML. For the final stage we’ll add a small human-annotated gold set (~300 sentences) to measure Stanza’s error rate and re-interpret model scores accordingly.

## Running the Pipeline

Make sure you already completed Milestone 1 and have the `.conllu` files in `data/conllu/`.

### Extract Word Orders

```bash
# Process all languages (default output: data/word_order_all_languages.csv)
bash run_word_order.sh

# Test mode (limit sentences per file)
bash run_word_order.sh --test 100

# Direct Python
python scripts/extract_word_order.py --input data/conllu --output data/word_order_all_languages.csv
```

### Split Data

```bash
# Auto-download spaCy models if missing
bash run_rule_based.sh

# Skip model download if already installed
bash run_rule_based.sh --skip-download
```

This creates three files in `data/splits/`:
- `train.csv` (70% of data)
- `val.csv` (15% of data)
- `test.csv` (15% of data)

The split is stratified by language, so each set has balanced mix of English, German and Russian sentences.

### Rule-Based Baselines + Evaluation

```bash
python scripts/split_data.py --config config/m2_config.yaml
```

### ML Baselines + Evaluation

```bash
python scripts/ML_baselines.py
```
Output: reports/report_binary.md and reports/report_multiclass.md (CV + validation results).

## Configuration

All settings are in `config/m2_config.yaml`:
- **cutoff_date**: 2022-11-30 (separates Pre-ChatGPT vs Post-ChatGPT periods)
- **data_split**: ratios for train/val/test (70/15/15)
- **random_seed**: 10 (our group number)
- **stratify_by_language**: keeps language distribution balanced across splits

## Future Work (Final Submission)
- Human gold standard (~300 sentences): use to measure Stanza parsing error and contextualize baseline/ML scores.
- Temporal stats: clean year/period, run chi-square or similar tests to quantify pre/post shifts; answer topic questions with plots/tables.
- Qualitative analysis: inspect common parser/model errors (SVO vs non-SVO flips).

## Repository Structure (M2 additions)

```
├─ config/
│  └─ m2_config.yaml                # M2 settings (word order extraction, data split)
│  └─ ML_baselines.py
├─ data/
│  ├─ word_order_all_languages.csv  # extracted word orders for all sentences
│  ├─ pos_pattern_predictions.csv
│  ├─ simple_heuristic_predictions.csv
│  └─ splits/                       # train/val/test splits for ML
│     ├─ train.csv
│     ├─ val.csv
│     └─ test.csv
├─ scripts/
│  ├─ extract_word_order.py         # extracts S-V-O patterns from CoNLL-U files
│  ├─ split_data.py                 # splits data into train/val/test sets
│  ├─ simple_heuristic_baseline.py
│  ├─ pos_pattern_baseline.py
│  ├─ evaluate_baselines.py
│  └─ ML_baselines.py
├─ reports/                         # analysis outputs and statistics
│  ├─ report_binary.md.md
│  ├─ report_multiclass.md
│  └─ rule_based_baselines.md
├─ run_word_order.sh                # convenient script to run word order extraction
├─ run_rule_based.sh
└─ requirements.txt                 # Python dependencies
```

## Notes

- The extraction script only looks at the **main clause** to avoid confusing word orders from subordinate clauses
- Sentences without clear root verb or missing critical elements are marked as "INCOMPLETE"
- All scripts handle three languages automatically
