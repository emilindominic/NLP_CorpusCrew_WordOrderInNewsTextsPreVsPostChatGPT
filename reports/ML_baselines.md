# ML_BASELINE REPORT

Generated on: **2025-11-28 22:06:33**

---

## CV RESULTS

### LogisticRegression (BOW)

| feature   | model              | params                                         |   fit_time |   f1_weighted |   f1_macro |   precision_macro |   recall_macro |   accuracy |   balanced_accuracy |
|:----------|:-------------------|:-----------------------------------------------|-----------:|--------------:|-----------:|------------------:|---------------:|-----------:|--------------------:|
| BoW       | LogisticRegression | {'C': 1.0, 'penalty': 'l2', 'solver': 'saga'}  |    65.8305 |        0.8174 |     0.6945 |            0.685  |         0.7069 |     0.8122 |              0.7069 |
| BoW       | LogisticRegression | {'C': 1.0, 'penalty': 'l2', 'solver': 'lbfgs'} |    16.3505 |        0.8174 |     0.6943 |            0.685  |         0.7066 |     0.8122 |              0.7066 |
| BoW       | LogisticRegression | {'C': 5.0, 'penalty': 'l2', 'solver': 'saga'}  |   109.929  |        0.8139 |     0.6803 |            0.6789 |         0.6818 |     0.8132 |              0.6818 |
| BoW       | LogisticRegression | {'C': 5.0, 'penalty': 'l2', 'solver': 'lbfgs'} |    18.4895 |        0.8137 |     0.6798 |            0.6784 |         0.6811 |     0.813  |              0.6811 |
| BoW       | LogisticRegression | {'C': 0.1, 'penalty': 'l2', 'solver': 'lbfgs'} |     7.5715 |        0.8069 |     0.6971 |            0.679  |         0.7407 |     0.7918 |              0.7407 |
| BoW       | LogisticRegression | {'C': 0.1, 'penalty': 'l2', 'solver': 'saga'}  |    11.3993 |        0.8068 |     0.6971 |            0.679  |         0.7408 |     0.7916 |              0.7408 |


**Best CV configuration:**

- Params: `{'C': 1.0, 'penalty': 'l2', 'solver': 'saga'}`

- F1-weighted: **0.8174**

- F1-macro: 0.6945

- Precision-macro: 0.685

- Recall-macro: 0.7069

- Accuracy: 0.8122

- Balanced accuracy: 0.7069


---

### NaiveBayes (BOW)

| feature   | model      | params          |   fit_time |   f1_weighted |   f1_macro |   precision_macro |   recall_macro |   accuracy |   balanced_accuracy |
|:----------|:-----------|:----------------|-----------:|--------------:|-----------:|------------------:|---------------:|-----------:|--------------------:|
| BoW       | NaiveBayes | {'alpha': 2.0}  |     0.0793 |        0.8002 |     0.6189 |            0.678  |         0.601  |     0.8241 |              0.601  |
| BoW       | NaiveBayes | {'alpha': 1.5}  |     0.0886 |        0.799  |     0.6431 |            0.6534 |         0.6355 |     0.805  |              0.6355 |
| BoW       | NaiveBayes | {'alpha': 1.0}  |     0.0915 |        0.7789 |     0.64   |            0.63   |         0.6583 |     0.7676 |              0.6583 |
| BoW       | NaiveBayes | {'alpha': 0.5}  |     0.0989 |        0.7465 |     0.6178 |            0.6113 |         0.6627 |     0.721  |              0.6627 |
| BoW       | NaiveBayes | {'alpha': 0.01} |     0.0935 |        0.7373 |     0.6033 |            0.5986 |         0.6437 |     0.711  |              0.6437 |
| BoW       | NaiveBayes | {'alpha': 0.1}  |     0.0918 |        0.7312 |     0.6047 |            0.603  |         0.6573 |     0.7011 |              0.6573 |


**Best CV configuration:**

- Params: `{'alpha': 2.0}`

- F1-weighted: **0.8002**

- F1-macro: 0.6189

- Precision-macro: 0.678

- Recall-macro: 0.601

- Accuracy: 0.8241

- Balanced accuracy: 0.601


---

### LogisticRegression (TFIDF)

| feature   | model              | params                                         |   fit_time |   f1_weighted |   f1_macro |   precision_macro |   recall_macro |   accuracy |   balanced_accuracy |
|:----------|:-------------------|:-----------------------------------------------|-----------:|--------------:|-----------:|------------------:|---------------:|-----------:|--------------------:|
| TFIDF     | LogisticRegression | {'C': 5.0, 'penalty': 'l2', 'solver': 'saga'}  |     7.1248 |        0.8175 |     0.697  |            0.6856 |         0.713  |     0.8111 |              0.713  |
| TFIDF     | LogisticRegression | {'C': 5.0, 'penalty': 'l2', 'solver': 'lbfgs'} |     8.7119 |        0.8166 |     0.6964 |            0.6844 |         0.7139 |     0.8095 |              0.7139 |
| TFIDF     | LogisticRegression | {'C': 1.0, 'penalty': 'l2', 'solver': 'saga'}  |     7.1648 |        0.807  |     0.6962 |            0.6783 |         0.7378 |     0.7923 |              0.7378 |
| TFIDF     | LogisticRegression | {'C': 1.0, 'penalty': 'l2', 'solver': 'lbfgs'} |     5.6692 |        0.8066 |     0.696  |            0.6781 |         0.7382 |     0.7918 |              0.7382 |
| TFIDF     | LogisticRegression | {'C': 0.1, 'penalty': 'l2', 'solver': 'saga'}  |     5.9962 |        0.7714 |     0.656  |            0.6444 |         0.712  |     0.7481 |              0.712  |
| TFIDF     | LogisticRegression | {'C': 0.1, 'penalty': 'l2', 'solver': 'lbfgs'} |     2.4659 |        0.7713 |     0.656  |            0.6445 |         0.7122 |     0.7479 |              0.7122 |


**Best CV configuration:**

- Params: `{'C': 5.0, 'penalty': 'l2', 'solver': 'saga'}`

- F1-weighted: **0.8175**

- F1-macro: 0.697

- Precision-macro: 0.6856

- Recall-macro: 0.713

- Accuracy: 0.8111

- Balanced accuracy: 0.713


---

### SVM (TFIDF)

| feature   | model   | params      |   fit_time |   f1_weighted |   f1_macro |   precision_macro |   recall_macro |   accuracy |   balanced_accuracy |
|:----------|:--------|:------------|-----------:|--------------:|-----------:|------------------:|---------------:|-----------:|--------------------:|
| tfidf     | SVM     | {'C': 1.0}  |     6.3281 |        0.8163 |     0.6882 |            0.6827 |         0.6946 |     0.8133 |              0.6946 |
| tfidf     | SVM     | {'C': 5.0}  |    20.8034 |        0.8101 |     0.6676 |            0.673  |         0.663  |     0.8129 |              0.663  |
| tfidf     | SVM     | {'C': 10.0} |    35.5993 |        0.8066 |     0.6596 |            0.6671 |         0.6535 |     0.8107 |              0.6535 |
| tfidf     | SVM     | {'C': 0.1}  |     1.312  |        0.8055 |     0.695  |            0.6771 |         0.7381 |     0.7903 |              0.7381 |
| tfidf     | SVM     | {'C': 50.0} |    88.1831 |        0.7998 |     0.6462 |            0.6547 |         0.6395 |     0.8048 |              0.6395 |
| tfidf     | SVM     | {'C': 0.01} |     0.885  |        0.7697 |     0.6532 |            0.642  |         0.7081 |     0.7463 |              0.7081 |


**Best CV configuration:**

- Params: `{'C': 1.0}`

- F1-weighted: **0.8163**

- F1-macro: 0.6882

- Precision-macro: 0.6827

- Recall-macro: 0.6946

- Accuracy: 0.8133

- Balanced accuracy: 0.6946


---

## VALIDATION RESULTS

| feature   | model              | best_params                                   |   fit_time |   f1_weighted |   f1_macro |   precision_macro |   recall_macro |   accuracy |   balanced_accuracy |
|:----------|:-------------------|:----------------------------------------------|-----------:|--------------:|-----------:|------------------:|---------------:|-----------:|--------------------:|
| BoW       | LogisticRegression | {'C': 1.0, 'penalty': 'l2', 'solver': 'saga'} |    28.5843 |        0.8178 |     0.7019 |            0.692  |         0.7151 |     0.8125 |              0.7151 |
| TFIDF     | LogisticRegression | {'C': 5.0, 'penalty': 'l2', 'solver': 'saga'} |     3.7417 |        0.8163 |     0.7049 |            0.691  |         0.7266 |     0.8082 |              0.7266 |
| tfidf     | SVM                | {'C': 1.0}                                    |     2.7905 |        0.8125 |     0.6938 |            0.6839 |         0.7072 |     0.8067 |              0.7072 |
| BoW       | NaiveBayes         | {'alpha': 2.0}                                |     0.0303 |        0.8036 |     0.6362 |            0.694  |         0.6162 |     0.8252 |              0.6162 |

---

## OVERALL BEST MODEL

**Best model selected based on validation F1-weighted score**


- **Model:** LogisticRegression

- **Feature extractor:** BoW

- **Best parameters:** `{'C': 1.0, 'penalty': 'l2', 'solver': 'saga'}`

- **F1-weighted:** 0.8178

- **F1-macro:** 0.7019

- **Precision-macro:** 0.692

- **Recall-macro:** 0.7151

- **Accuracy:** 0.8125

- **Balanced accuracy:** 0.7151
