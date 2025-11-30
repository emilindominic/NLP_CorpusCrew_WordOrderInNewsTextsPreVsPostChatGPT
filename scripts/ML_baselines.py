"""
Script to run ML baseline experiments with various models and feature extraction methods.
Generates a Markdown report summarizing cross-validation and validation results.
"""

import pandas as pd
import re
import unicodedata
from config.ML_baselines import *
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, balanced_accuracy_score
from sklearn.base import clone
from datetime import datetime
from pathlib import Path


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load train and validation datasets.
    Args:
        None
    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: Train and validation dataframes.
    """
    train_data = pd.read_csv(f"{ROOT_DIR}train.csv")
    val_data = pd.read_csv(f"{ROOT_DIR}val.csv")
    return train_data, val_data

def preprocess_text(text: str) -> str:
    """
    Preprocessing the sentences:
    1. Unicode normalization
    2. Lowercasing
    3. Remove URLs
    4. Remove HTML tags
    5. Remove punctuation
    6. Normalize whitespaces
    Args:
        text (str): Input text.
    Returns:
        str: Preprocessed text.
    """
    
    if not isinstance(text, str):
        return ""

    # Unicode normalization
    text = unicodedata.normalize("NFKC", text)
    # Lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)
    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)
    # Remove punctuation (keep words + numbers)
    text = re.sub(r"[^\w\s]", " ", text)
    # Normalize whitespaces
    text = re.sub(r"\s+", " ", text).strip()

    return text

def encode_target(df: pd.DataFrame, target_col: str = "word_order") -> pd.Series:
    """
    Transform multiclass target column into a binary target.
    Encodes 'SVO' as 1 and anything else as 0.
    Args:
        df (pd.DataFrame): Input DataFrame containing the target column.
        target_col (str): Name of the target column. Defaults to 'word_order'.

    Returns:
        pd.Series: Binary-encoded target labels.
    """
    return (df[target_col] == "SVO").astype(int)

def extract_features(
    X_train: pd.Series,
    X_val: pd.Series,
    method: str = "bow",
):
    """
    Extract features from preprocessed sentences using BoW or TF-IDF.
    Args:
        X_train (pd.Series): Preprocessed training sentences.
        X_val (pd.Series): Preprocessed validation sentences.
        method (str): Feature extraction method ('bow' or 'tfidf').
    Returns:
        X_train_vec, X_val_vec: Vectorized training and validation features.
    """
    method = method.lower()

    if method == "bow":
        vectorizer = CountVectorizer()
    elif method == "tfidf":
        vectorizer = TfidfVectorizer()
    else:
        raise ValueError("method must be 'bow' or 'tfidf'")

    X_train_vec = vectorizer.fit_transform(X_train)
    X_val_vec = vectorizer.transform(X_val)

    return X_train_vec, X_val_vec

def generate_md_report(cv_results_all: list[pd.DataFrame], val_results_all: list[dict]) -> None:
    """
    Generate Markdown report from CV and validation results.
    Args:
        cv_results_all (list[pd.DataFrame]): List of DataFrames with CV results.
        val_results_all (list[dict]): List of dictionaries with validation results.
    Returns:
        None
    """
    
    project_root = Path(__file__).resolve().parents[1]
    output_file = project_root / REPORT_FILE
    output_file.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Merge CV results
    cv_all = pd.concat(cv_results_all, ignore_index=True)

    # Validation DataFrame
    val_df = pd.DataFrame(val_results_all)

    # Get best model overall (based on validation f1_weighted)
    best_overall = val_df.sort_values(by="balanced_accuracy", ascending=False).iloc[0]

    md = []

    # HEADER
    md.append("# ML_BASELINE REPORT\n")
    md.append(f"Generated on: **{now}**\n")
    md.append("---\n")

    # CV RESULTS
    md.append("## CV RESULTS\n")

    for (feature, model), group in cv_all.groupby(["feature", "model"]):

        group = group.sort_values("f1_weighted", ascending=False)
        best_row = group.iloc[0]

        md.append(f"### {model} ({feature.upper()})\n")
        md.append(group.to_markdown(index=False))
        md.append("\n")

        md.append("**Best CV configuration:**\n")
        md.append(f"- Params: `{best_row['params']}`\n")
        md.append(f"- F1-weighted: **{best_row['f1_weighted']}**\n")
        md.append(f"- F1-macro: {best_row['f1_macro']}\n")
        md.append(f"- Precision-macro: {best_row['precision_macro']}\n")
        md.append(f"- Recall-macro: {best_row['recall_macro']}\n")
        md.append(f"- Accuracy: {best_row['accuracy']}\n")
        md.append(f"- Balanced accuracy: {best_row['balanced_accuracy']}\n")
        md.append("\n---\n")

    # VALIDATION RESULTS
    md.append("## VALIDATION RESULTS\n")

    val_df_sorted = val_df.sort_values(by="f1_weighted", ascending=False)

    md.append(val_df_sorted.to_markdown(index=False))
    md.append("\n---\n")

    # OVERALL BEST MODEL
    md.append("## OVERALL BEST MODEL\n")

    md.append("**Best model selected based on balanced accuracy score**\n\n")
    md.append(f"- **Model:** {best_overall['model']}\n")
    md.append(f"- **Feature extractor:** {best_overall['feature']}\n")
    md.append(f"- **Best parameters:** `{best_overall['best_params']}`\n")
    md.append(f"- **F1-weighted:** {best_overall['f1_weighted']}\n")
    md.append(f"- **F1-macro:** {best_overall['f1_macro']}\n")
    md.append(f"- **Precision-macro:** {best_overall['precision_macro']}\n")
    md.append(f"- **Recall-macro:** {best_overall['recall_macro']}\n")
    md.append(f"- **Accuracy:** {best_overall['accuracy']}\n")
    md.append(f"- **Balanced accuracy:** {best_overall['balanced_accuracy']}\n")

    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

def main() -> None:
    """
    Main function that does the following:
    1. Load data
    2. Preprocess sentences
    3. Encode target labels as binary
    4. For each model and feature extraction method:
        a. Extract features
        b. Perform GridSearchCV for hyperparameter tuning
        c. Collect cross-validation results
        d. Evaluate best model on validation set
        e. Collect validation results
    5. Generate Markdown report
    Args:
        None
    Returns:
        None
    """

    # Load data
    train_data, val_data = load_data()

    # Preprocess text
    X_train = train_data["sentence"].apply(preprocess_text)
    X_val = val_data["sentence"].apply(preprocess_text)

    # Encode target labels
    y_train = encode_target(train_data, target_col="word_order")
    y_val = encode_target(val_data, target_col="word_order")

    # Lists for storing results
    cv_results_all = []
    val_results_all = []

    for model_name, model in BASE_MODELS.items():

        methods = FEATURE_EXTRACTORS[model_name]
        param_grid = PARAM_GRIDS[model_name]
        scoring = SCORING_METRICS

        for method in methods:

            # Extract features
            X_train_vec, X_val_vec = extract_features(X_train, X_val, method=method)

            # GridSearchCV for hyperparameter tuning
            grid = GridSearchCV(
                clone(model),
                param_grid,
                scoring=scoring,
                refit="f1_weighted",
                cv=5,
                n_jobs=-1,
            )

            grid.fit(X_train_vec, y_train)

            # Collect cross-validation results
            cv_table = pd.DataFrame(grid.cv_results_)

            cols = {
                "mean_fit_time": "fit_time",
                "mean_test_f1_weighted": "f1_weighted",
                "mean_test_f1_macro": "f1_macro",
                "mean_test_precision_macro": "precision_macro",
                "mean_test_recall_macro": "recall_macro",
                "mean_test_accuracy": "accuracy",
                "mean_test_balanced_accuracy": "balanced_accuracy",
            }

            cv_view = (
                cv_table[["params"] + list(cols)]
                .rename(columns=cols)
                .sort_values(by="f1_weighted", ascending=False)
                .round(4)
            )

            cv_view.insert(0, "model", model_name)
            cv_view.insert(0, "feature", method)

            cv_results_all.append(cv_view)

            # Evaluate best model on validation set
            best_model = grid.best_estimator_
            best_params = grid.best_params_

            y_pred = best_model.predict(X_val_vec)

            f1_weighted = f1_score(y_val, y_pred, average="weighted", zero_division=0)
            f1_macro = f1_score(y_val, y_pred, average="macro", zero_division=0)
            precision = precision_score(y_val, y_pred, average="macro", zero_division=0)
            recall = recall_score(y_val, y_pred, average="macro", zero_division=0)
            accuracy = accuracy_score(y_val, y_pred)
            balanced_accuracy = balanced_accuracy_score(y_val, y_pred)

            # Collect validation results
            val_results_all.append({
                "feature": method,
                "model": model_name,
                "best_params": best_params,
                "fit_time": round(grid.refit_time_, 4),
                "f1_weighted": round(f1_weighted, 4),
                "f1_macro": round(f1_macro, 4),
                "precision_macro": round(precision, 4),
                "recall_macro": round(recall, 4),
                "accuracy": round(accuracy, 4),
                "balanced_accuracy": round(balanced_accuracy, 4)
            })

    # Generate report
    generate_md_report(cv_results_all=cv_results_all, val_results_all=val_results_all,)

if __name__ == "__main__":    
    main()
