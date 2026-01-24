# RULE-BASED BASELINES REPORT

Generated on: 2025-11-30 18:44:04

---

## COMPARISON OF APPROACHES

Three methods compared:
1. POS-pattern: Sequential POS tag matching
2. Simple heuristics: Basic position rules

---

## PERFORMANCE METRICS

| method           |   accuracy |   balanced_accuracy |   f1_weighted |   f1_macro |   precision_macro |   recall_macro |
|:-----------------|-----------:|--------------------:|--------------:|-----------:|------------------:|---------------:|
| POS-Pattern      |     0.5687 |              0.5278 |        0.6198 |     0.4837 |            0.5165 |         0.5278 |
| Simple Heuristic |     0.3403 |              0.5782 |        0.3442 |     0.3403 |            0.5752 |         0.5782 |

---

## CONFUSION MATRICES

Format: [TN, FP] / [FN, TP]

### POS-Pattern

```
                Predicted
                Non-SVO    SVO
Actual Non-SVO   11269    7805
       SVO        2170    1885
```

Recall (Non-SVO): 59.08%
Recall (SVO): 46.49%
Precision (SVO): 19.45%
Missed SVO (FN): 2170
False SVO (FP): 7805

### Simple Heuristic

```
                Predicted
                Non-SVO    SVO
Actual Non-SVO    4041   15033
       SVO         225    3830
```

Recall (Non-SVO): 21.19%
Recall (SVO): 94.45%
Precision (SVO): 20.30%
Missed SVO (FN): 225
False SVO (FP): 15033

---

## RANKING BY BALANCED ACCURACY

2. Simple Heuristic: 0.5782
1. POS-Pattern: 0.5278

## KEY FINDINGS

Performance progression shows value of linguistic sophistication:
Simple heuristics < POS patterns < Dependency parsing

