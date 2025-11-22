#!/usr/bin/env python3
"""
Split word order dataset into train/validation/test sets.

This script performs stratified random splitting by language to ensure
balanced language distribution across all three splits.
"""

import argparse
import pandas as pd
import yaml
from pathlib import Path
from sklearn.model_selection import train_test_split


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def split_data(
    input_csv: str,
    train_output: str,
    val_output: str,
    test_output: str,
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    random_seed: int = 42,
    stratify_by_language: bool = True
):
    """
    Split dataset into train/validation/test sets.

    Args:
        input_csv: Path to input CSV with word order labels
        train_output: Path to save training set
        val_output: Path to save validation set
        test_output: Path to save test set
        train_ratio: Proportion of data for training (default: 0.7)
        val_ratio: Proportion of data for validation (default: 0.15)
        test_ratio: Proportion of data for testing (default: 0.15)
        random_seed: Random seed for reproducibility
        stratify_by_language: If True, maintain language distribution across splits
    """

    # Validate ratios
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, \
        f"Ratios must sum to 1.0, got {train_ratio + val_ratio + test_ratio}"

    print(f"Loading data from: {input_csv}")
    df = pd.read_csv(input_csv)

    print(f"Total sentences: {len(df):,}")
    print(f"Random seed: {random_seed}")
    print()

    # Show language distribution
    print("Language distribution:")
    lang_counts = df['language'].value_counts()
    for lang, count in lang_counts.items():
        print(f"  {lang}: {count:,} ({count/len(df)*100:.1f}%)")
    print()

    # Stratify by language if requested
    stratify_col = df['language'] if stratify_by_language else None

    # First split: train vs (val + test)
    train_df, temp_df = train_test_split(
        df,
        test_size=(val_ratio + test_ratio),
        random_state=random_seed,
        stratify=stratify_col
    )

    # Second split: val vs test
    # Adjust the test_size to get correct proportions
    val_size_from_temp = val_ratio / (val_ratio + test_ratio)

    val_df, test_df = train_test_split(
        temp_df,
        test_size=(1 - val_size_from_temp),
        random_state=random_seed,
        stratify=temp_df['language'] if stratify_by_language else None
    )

    # Print split statistics
    print(f"Split ratios: {train_ratio:.0%} train, {val_ratio:.0%} val, {test_ratio:.0%} test")
    print()
    print("Split sizes:")
    print(f"  Train:      {len(train_df):,} sentences ({len(train_df)/len(df)*100:.1f}%)")
    print(f"  Validation: {len(val_df):,} sentences ({len(val_df)/len(df)*100:.1f}%)")
    print(f"  Test:       {len(test_df):,} sentences ({len(test_df)/len(df)*100:.1f}%)")
    print()

    # Show language distribution in each split
    print("Language distribution per split:")
    for split_name, split_df in [("Train", train_df), ("Validation", val_df), ("Test", test_df)]:
        print(f"  {split_name}:")
        split_lang_counts = split_df['language'].value_counts()
        for lang in lang_counts.index:  # Use same order as original
            count = split_lang_counts.get(lang, 0)
            pct = count / len(split_df) * 100
            print(f"    {lang}: {count:,} ({pct:.1f}%)")
    print()

    # Create output directory if needed
    Path(train_output).parent.mkdir(parents=True, exist_ok=True)

    # Save splits
    print("Saving splits...")
    train_df.to_csv(train_output, index=False)
    print(f"  ✓ Train saved to: {train_output}")

    val_df.to_csv(val_output, index=False)
    print(f"  ✓ Validation saved to: {val_output}")

    test_df.to_csv(test_output, index=False)
    print(f"  ✓ Test saved to: {test_output}")
    print()
    print("Done!")


def main():
    parser = argparse.ArgumentParser(description="Split word order dataset into train/val/test")
    parser.add_argument(
        '--config',
        type=str,
        default='config/m2_config.yaml',
        help='Path to config file (default: config/m2_config.yaml)'
    )
    parser.add_argument(
        '--input',
        type=str,
        help='Override input CSV path from config'
    )
    parser.add_argument(
        '--seed',
        type=int,
        help='Override random seed from config'
    )

    args = parser.parse_args()

    # Load config
    config = load_config(args.config)

    # Get paths from config
    input_csv = args.input or config['paths']['word_order_csv']
    train_output = config['paths']['train_split']
    val_output = config['paths']['val_split']
    test_output = config['paths']['test_split']

    # Get split settings from config
    split_config = config['data_split']
    random_seed = args.seed if args.seed is not None else split_config['random_seed']

    # Perform split
    split_data(
        input_csv=input_csv,
        train_output=train_output,
        val_output=val_output,
        test_output=test_output,
        train_ratio=split_config['train_ratio'],
        val_ratio=split_config['val_ratio'],
        test_ratio=split_config['test_ratio'],
        random_seed=random_seed,
        stratify_by_language=split_config['stratify_by_language']
    )


if __name__ == '__main__':
    main()
