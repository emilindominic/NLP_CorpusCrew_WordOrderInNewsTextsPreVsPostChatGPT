"""
Simple heuristic baseline for word order classification.
Uses basic position rules: find verb, check for nouns before/after.
"""

import pandas as pd
import spacy
import time


def classify_simple_heuristic(pos_tags):
    """
    Very simple rule: find first verb, check noun positions around it.
    Assumes SVO if nouns exist both before and after verb.
    """
    noun_tags = {'NOUN', 'PRON', 'PROPN'}
    verb_tags = {'VERB', 'AUX'}

    verb_idx = None
    for i, pos in enumerate(pos_tags):
        if pos in verb_tags:
            verb_idx = i
            break

    if verb_idx is None:
        return "INCOMPLETE"

    has_noun_before = any(pos in noun_tags for pos in pos_tags[:verb_idx])
    has_noun_after = any(pos in noun_tags for pos in pos_tags[verb_idx+1:])

    if has_noun_before and has_noun_after:
        return "SVO"
    elif has_noun_before and not has_noun_after:
        return "SV_only"
    elif not has_noun_before and has_noun_after:
        return "VO_only"
    else:
        return "INCOMPLETE"


def process_sentences(df, nlp):
    predictions = []

    for i, sentence in enumerate(df['sentence']):
        if i % 1000 == 0:
            print(f"  Processed {i}/{len(df)}")

        doc = nlp(str(sentence))
        pos_tags = [token.pos_ for token in doc]
        pred = classify_simple_heuristic(pos_tags)
        predictions.append(pred)

    return predictions


def main():
    print("Simple Heuristic Baseline")
    print("-" * 40)

    test_df = pd.read_csv("data/splits/test.csv")
    print(f"Loaded {len(test_df)} test sentences")

    nlp_models = {
        'eng': spacy.load("en_core_web_sm"),
        'deu': spacy.load("de_core_news_sm"),
        'rus': spacy.load("ru_core_news_sm")
    }

    # store predictions aligned with original indices
    test_df['pred_simple_heuristic'] = None
    start = time.time()

    for lang, nlp in nlp_models.items():
        print(f"\nProcessing {lang}")
        lang_df = test_df[test_df['language'] == lang].copy()
        predictions = process_sentences(lang_df, nlp)
        # assign back using the same indices to preserve row order
        test_df.loc[lang_df.index, 'pred_simple_heuristic'] = predictions

    elapsed = time.time() - start
    print(f"\nCompleted in {elapsed:.2f} seconds")

    # any rows not covered default to INCOMPLETE
    test_df['pred_simple_heuristic'] = test_df['pred_simple_heuristic'].fillna("INCOMPLETE")

    output_path = "data/simple_heuristic_predictions.csv"
    test_df.to_csv(output_path, index=False)
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()
