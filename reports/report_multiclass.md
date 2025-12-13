# ML_BASELINE REPORT (MULTICLASS)

Generated on: **2025-12-12 22:38:52**

---

## CV RESULTS

### LogisticRegression (BOW)

| feature   | model              | params                                         |   fit_time |   f1_weighted |   f1_macro |   precision_macro |   recall_macro |   accuracy |   balanced_accuracy |
|:----------|:-------------------|:-----------------------------------------------|-----------:|--------------:|-----------:|------------------:|---------------:|-----------:|--------------------:|
| BoW       | LogisticRegression | {'C': 1.0, 'penalty': 'l2', 'solver': 'saga'}  |   202.286  |        0.5777 |     0.3775 |            0.3538 |         0.4222 |     0.5698 |              0.4222 |
| BoW       | LogisticRegression | {'C': 1.0, 'penalty': 'l2', 'solver': 'lbfgs'} |   161.622  |        0.5773 |     0.3778 |            0.3538 |         0.423  |     0.5693 |              0.423  |
| BoW       | LogisticRegression | {'C': 5.0, 'penalty': 'l2', 'solver': 'saga'}  |   254.794  |        0.573  |     0.3678 |            0.3625 |         0.3818 |     0.5715 |              0.3818 |
| BoW       | LogisticRegression | {'C': 5.0, 'penalty': 'l2', 'solver': 'lbfgs'} |   223.647  |        0.5716 |     0.3663 |            0.3591 |         0.3818 |     0.5698 |              0.3818 |
| BoW       | LogisticRegression | {'C': 0.1, 'penalty': 'l2', 'solver': 'saga'}  |  1225.72   |        0.5292 |     0.3579 |            0.324  |         0.4911 |     0.5053 |              0.4911 |
| BoW       | LogisticRegression | {'C': 0.1, 'penalty': 'l2', 'solver': 'lbfgs'} |    86.7015 |        0.5291 |     0.3586 |            0.3245 |         0.4914 |     0.5053 |              0.4914 |


**Best CV configuration:**

- Params: `{'C': 1.0, 'penalty': 'l2', 'solver': 'saga'}`

- F1-weighted: **0.5777**

- F1-macro: 0.3775

- Precision-macro: 0.3538

- Recall-macro: 0.4222

- Accuracy: 0.5698

- Balanced accuracy: 0.4222


---

### NaiveBayes (BOW)

| feature   | model      | params          |   fit_time |   f1_weighted |   f1_macro |   precision_macro |   recall_macro |   accuracy |   balanced_accuracy |
|:----------|:-----------|:----------------|-----------:|--------------:|-----------:|------------------:|---------------:|-----------:|--------------------:|
| BoW       | NaiveBayes | {'alpha': 1.0}  |     0.5782 |        0.4784 |     0.2076 |            0.2948 |         0.2059 |     0.5033 |              0.2059 |
| BoW       | NaiveBayes | {'alpha': 1.5}  |     0.5549 |        0.4675 |     0.1729 |            0.2646 |         0.1704 |     0.5181 |              0.1704 |
| BoW       | NaiveBayes | {'alpha': 2.0}  |     0.5181 |        0.4503 |     0.1527 |            0.2898 |         0.1552 |     0.5204 |              0.1552 |
| BoW       | NaiveBayes | {'alpha': 0.5}  |     0.6041 |        0.44   |     0.2261 |            0.2667 |         0.2772 |     0.4291 |              0.2772 |
| BoW       | NaiveBayes | {'alpha': 0.01} |     0.6283 |        0.3289 |     0.2021 |            0.2092 |         0.3235 |     0.3056 |              0.3235 |
| BoW       | NaiveBayes | {'alpha': 0.1}  |     0.6606 |        0.3203 |     0.197  |            0.2211 |         0.32   |     0.3047 |              0.32   |


**Best CV configuration:**

- Params: `{'alpha': 1.0}`

- F1-weighted: **0.4784**

- F1-macro: 0.2076

- Precision-macro: 0.2948

- Recall-macro: 0.2059

- Accuracy: 0.5033

- Balanced accuracy: 0.2059


---

### LogisticRegression (TFIDF)

| feature   | model              | params                                         |   fit_time |   f1_weighted |   f1_macro |   precision_macro |   recall_macro |   accuracy |   balanced_accuracy |
|:----------|:-------------------|:-----------------------------------------------|-----------:|--------------:|-----------:|------------------:|---------------:|-----------:|--------------------:|
| TFIDF     | LogisticRegression | {'C': 5.0, 'penalty': 'l2', 'solver': 'lbfgs'} |   191.134  |        0.5768 |     0.3766 |            0.3585 |         0.4248 |     0.5687 |              0.4248 |
| TFIDF     | LogisticRegression | {'C': 1.0, 'penalty': 'l2', 'solver': 'lbfgs'} |   121.686  |        0.532  |     0.3614 |            0.3294 |         0.4798 |     0.5116 |              0.4798 |
| TFIDF     | LogisticRegression | {'C': 5.0, 'penalty': 'l2', 'solver': 'saga'}  |   836.978  |        0.5063 |     0.3151 |            0.3189 |         0.4294 |     0.4795 |              0.4294 |
| TFIDF     | LogisticRegression | {'C': 1.0, 'penalty': 'l2', 'solver': 'saga'}  |  1007.6    |        0.3691 |     0.2227 |            0.3082 |         0.3365 |     0.332  |              0.3365 |
| TFIDF     | LogisticRegression | {'C': 0.1, 'penalty': 'l2', 'solver': 'lbfgs'} |    44.0963 |        0.3346 |     0.2659 |            0.2832 |         0.4701 |     0.3143 |              0.4701 |
| TFIDF     | LogisticRegression | {'C': 0.1, 'penalty': 'l2', 'solver': 'saga'}  |  1037.17   |        0.3002 |     0.1902 |            0.2827 |         0.3049 |     0.2735 |              0.3049 |


**Best CV configuration:**

- Params: `{'C': 5.0, 'penalty': 'l2', 'solver': 'lbfgs'}`

- F1-weighted: **0.5768**

- F1-macro: 0.3766

- Precision-macro: 0.3585

- Recall-macro: 0.4248

- Accuracy: 0.5687

- Balanced accuracy: 0.4248


---

### SVM (TFIDF)

| feature   | model   | params      |   fit_time |   f1_weighted |   f1_macro |   precision_macro |   recall_macro |   accuracy |   balanced_accuracy |
|:----------|:--------|:------------|-----------:|--------------:|-----------:|------------------:|---------------:|-----------:|--------------------:|
| TFIDF     | SVM     | {'C': 1.0}  |    16.0064 |        0.5838 |     0.3631 |            0.3593 |         0.3792 |     0.5823 |              0.3792 |
| TFIDF     | SVM     | {'C': 0.1}  |     7.0383 |        0.5696 |     0.3718 |            0.3384 |         0.4793 |     0.5535 |              0.4793 |
| TFIDF     | SVM     | {'C': 5.0}  |    40.8279 |        0.5619 |     0.3324 |            0.3602 |         0.3218 |     0.5668 |              0.3218 |
| TFIDF     | SVM     | {'C': 10.0} |    66.7151 |        0.5514 |     0.32   |            0.3542 |         0.3058 |     0.558  |              0.3058 |
| TFIDF     | SVM     | {'C': 50.0} |   189.858  |        0.5315 |     0.3015 |            0.3413 |         0.2841 |     0.5393 |              0.2841 |
| TFIDF     | SVM     | {'C': 0.01} |     6.0307 |        0.5075 |     0.3201 |            0.3061 |         0.4519 |     0.4909 |              0.4519 |


**Best CV configuration:**

- Params: `{'C': 1.0}`

- F1-weighted: **0.5838**

- F1-macro: 0.3631

- Precision-macro: 0.3593

- Recall-macro: 0.3792

- Accuracy: 0.5823

- Balanced accuracy: 0.3792


---

## VALIDATION RESULTS

| feature   | model              | best_params                                    |   fit_time |   f1_weighted |   f1_macro |   precision_macro |   recall_macro |   accuracy |   balanced_accuracy |
|:----------|:-------------------|:-----------------------------------------------|-----------:|--------------:|-----------:|------------------:|---------------:|-----------:|--------------------:|
| TFIDF     | SVM                | {'C': 1.0}                                     |     9.2189 |        0.5889 |     0.3775 |            0.3656 |         0.4037 |     0.5843 |              0.4037 |
| BoW       | LogisticRegression | {'C': 1.0, 'penalty': 'l2', 'solver': 'saga'}  |    66.8319 |        0.5855 |     0.3976 |            0.3723 |         0.4449 |     0.5769 |              0.4449 |
| TFIDF     | LogisticRegression | {'C': 5.0, 'penalty': 'l2', 'solver': 'lbfgs'} |    85.6159 |        0.5812 |     0.3956 |            0.3697 |         0.4614 |     0.57   |              0.4614 |
| BoW       | NaiveBayes         | {'alpha': 1.0}                                 |     0.4049 |        0.4785 |     0.201  |            0.2863 |         0.2    |     0.5097 |              0.2    |

---

## OVERALL BEST MODEL

**Best model selected based on balanced accuracy score**


- **Model:** LogisticRegression

- **Feature extractor:** TFIDF

- **Best parameters:** `{'C': 5.0, 'penalty': 'l2', 'solver': 'lbfgs'}`

- **F1-weighted:** 0.5812

- **F1-macro:** 0.3956

- **Precision-macro:** 0.3697

- **Recall-macro:** 0.4614

- **Accuracy:** 0.57

- **Balanced accuracy:** 0.4614
