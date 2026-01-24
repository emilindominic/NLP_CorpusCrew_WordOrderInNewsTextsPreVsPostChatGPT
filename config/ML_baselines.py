"""Configuration for ML baseline models:
1. Path to specific directories (data, reports).
2. Experiment settings (models, feature extractors, hyperparameter grids).
3. Scoring metrics for model evaluation.
"""

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import make_scorer, accuracy_score, balanced_accuracy_score, f1_score, precision_score, recall_score

ROOT_DIR = "./data/splits/"
REPORT_DIR = "reports"
REPORT_FILE = f"{REPORT_DIR}/ML_baselines.md"

BASE_MODELS = {
    "NaiveBayes": MultinomialNB(),
    "LogisticRegression": LogisticRegression(max_iter=2500, class_weight="balanced", random_state=12332270),
    "SVM": LinearSVC(max_iter=5000, class_weight= "balanced", random_state=12332270),
}

FEATURE_EXTRACTORS = {
    "NaiveBayes": ["BoW"],
    "LogisticRegression": ["BoW", "TFIDF"],
    "SVM": ["TFIDF"],
}

PARAM_GRIDS = {
    "NaiveBayes": {
        "alpha": [0.01, 0.1, 0.5, 1.0, 1.5, 2.0]
    },

    "LogisticRegression": {
        "C": [0.1, 1.0, 5.0],
        "penalty": ["l2"],
        "solver": ["lbfgs", "saga"]
    },

    "SVM": {
        "C": [0.01, 0.1, 1.0, 5.0, 10.0, 50.0]
    }
}

SCORING_METRICS = {
    "accuracy": make_scorer(accuracy_score),
    "balanced_accuracy": make_scorer(balanced_accuracy_score),
    "f1_weighted": make_scorer(f1_score, average="weighted", zero_division=0),
    "f1_macro": make_scorer(f1_score, average="macro", zero_division=0),
    "precision_macro": make_scorer(precision_score, average="macro", zero_division=0),
    "recall_macro": make_scorer(recall_score, average="macro", zero_division=0),
}
