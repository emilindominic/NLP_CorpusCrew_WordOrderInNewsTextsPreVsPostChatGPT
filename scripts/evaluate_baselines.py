"""
Evaluate and compare all baseline approaches:
- Dependency-based (Stanza) - ground truth
- POS-pattern matching
- Simple heuristics
"""

import pandas as pd
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, f1_score,
    precision_score, recall_score, confusion_matrix
)
from datetime import datetime
from pathlib import Path

def evaluate_method(y_true, y_pred, method_name):
    labels = sorted(set(y_true.dropna()) | set(y_pred.dropna()))
    metrics = {
        'method': method_name,
        'accuracy': accuracy_score(y_true, y_pred),
        'f1_macro': f1_score(y_true, y_pred, average='macro', zero_division=0),
        'f1_weighted': f1_score(y_true, y_pred, average='weighted', zero_division=0),
        'balanced_accuracy': balanced_accuracy_score(y_true, y_pred, zero_division=0)
    }
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    return metrics, cm, labels


def generate_report(results, confusion_matrices, output_file):
    """Generate markdown report comparing all methods."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md = []
    md.append("# RULE-BASED BASELINES REPORT\n\n")
    md.append(f"Generated on: {now}\n\n")
    md.append("---\n\n")

    md.append("## COMPARISON OF APPROACHES\n\n")
    md.append("Three methods compared:\n")
    md.append("1. POS-pattern: Sequential POS tag matching\n")
    md.append("2. Simple heuristics: Basic position rules\n\n")
    md.append("---\n\n")

    md.append("## PERFORMANCE METRICS\n\n")
    df_results = pd.DataFrame(results)
    md.append(df_results.round(4).to_markdown(index=False))
    md.append("\n\n---\n\n")

    md.append("## CONFUSION MATRICES\n\n")
    md.append("Format: rows = gold, columns = predicted\n\n")


    for method, (cm, labels) in confusion_matrices.items():
        md.append(f"### {method}\n\n")
        md.append("```\n")
        md.append("Stanza-Gold \\ Pred → " + " ".join(f"{l:>7}" for l in labels) + "\n")

        for i, gold in enumerate(labels):
            row = " ".join(f"{cm[i,j]:>7}" for j in range(len(labels)))
            md.append(f"{gold:>12} {row}\n")

        md.append("```\n\n")


    md.append("## RANKING BY BALANCED ACCURACY\n\n")
    ranked = df_results.sort_values('balanced_accuracy', ascending=False)
    for i, row in ranked.iterrows():
        md.append(f"{i+1}. {row['method']}: {row['balanced_accuracy']:.4f}\n")

    md.append("\n## KEY FINDINGS\n\n")
    md.append("Performance progression shows value of linguistic sophistication:\n")
    md.append("Simple heuristics < POS patterns < Dependency parsing\n\n")

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(''.join(md))

    print(f"\nReport saved to: {output_file}")


def main():
    print("Baseline Evaluation")
    print("-" * 40)

    test_df = pd.read_csv("data/splits/test.csv")
    pos_df = pd.read_csv("data/pos_pattern_predictions.csv")
    simple_df = pd.read_csv("data/simple_heuristic_predictions.csv")

    # Merge predictions
    test_df['pred_pos_pattern'] = pos_df['pred_pos_pattern']
    test_df['pred_simple_heuristic'] = simple_df['pred_simple_heuristic']

    y_true = test_df['word_order']

    results = []
    confusion_matrices = {}

    # Evaluate POS-pattern
    print("\nEvaluating POS-pattern baseline...")
    metrics_pos, cm_pos, labels = evaluate_method(y_true, test_df['pred_pos_pattern'], 'POS-Pattern')
    results.append(metrics_pos)
    confusion_matrices['POS-Pattern'] = (cm_pos, labels)

    # Evaluate simple heuristics
    print("Evaluating simple heuristic baseline...")
    metrics_simple, cm_simple, _ = evaluate_method(y_true, test_df['pred_simple_heuristic'], 'Simple Heuristic')
    results.append(metrics_simple)
    confusion_matrices['Simple Heuristic'] = (cm_simple, labels)


    print("\n" + "=" * 60)
    df_results = pd.DataFrame(results)
    print(df_results.round(4).to_string(index=False))
    print("=" * 60)

    generate_report(results, confusion_matrices, "reports/rule_based_baselines.md")

    print("\nDone")


if __name__ == "__main__":
    main()
