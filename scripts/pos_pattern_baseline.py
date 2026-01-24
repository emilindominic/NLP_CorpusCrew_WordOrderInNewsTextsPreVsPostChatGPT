"""
POS-pattern baseline for word order classification.
Uses simple POS tag sequence matching without dependency parsing.
"""

import pandas as pd
import spacy
import time


def classify_pos_pattern(pos_tags):
    """
    Classify word order by matching POS tag sequences.
    Identifies first verb and surrounding nouns/pronouns.
    """
    noun_tags = {'NOUN', 'PRON', 'PROPN'}
    verb_tags = {'VERB', 'AUX'}

    positions = []
    for i, pos in enumerate(pos_tags):
        if pos in noun_tags:
            positions.append(('N', i))
        elif pos in verb_tags:
            positions.append(('V', i))

    nouns = [p for p in positions if p[0] == 'N']
    verbs = [p for p in positions if p[0] == 'V']

    if len(nouns) < 2 or len(verbs) < 1:
        return "INCOMPLETE"

    # Use first verb and first two nouns as S, V, O candidates
    subj_pos = nouns[0][1]
    verb_pos = verbs[0][1]
    obj_pos = nouns[1][1]

    if subj_pos < verb_pos < obj_pos:
        return "SVO"
    elif subj_pos < obj_pos < verb_pos:
        return "SOV"
    elif verb_pos < subj_pos < obj_pos:
        return "VSO"
    elif verb_pos < obj_pos < subj_pos:
        return "VOS"
    elif obj_pos < subj_pos < verb_pos:
        return "OSV"
    elif obj_pos < verb_pos < subj_pos:
        return "OVS"
    else:
        return "INCOMPLETE"


def process_sentences(df, nlp):
    predictions = []

    for i, sentence in enumerate(df['sentence']):
        if i % 1000 == 0:
            print(f"  Processed {i}/{len(df)}")

        doc = nlp(str(sentence))
        pos_tags = [token.pos_ for token in doc]
        pred = classify_pos_pattern(pos_tags)
        predictions.append(pred)

    return predictions


def main():
    print("POS-Pattern Baseline")
    print("-" * 40)

    test_df = pd.read_csv("data/splits/test.csv")
    print(f"Loaded {len(test_df)} test sentences")

    # Languagespecific spacy models
    nlp_models = {
        'eng': spacy.load("en_core_web_sm"),
        'deu': spacy.load("de_core_news_sm"),
        'rus': spacy.load("ru_core_news_sm")
    }

    # store predictions aligned with original indices
    test_df['pred_pos_pattern'] = None
    start = time.time()

    for lang, nlp in nlp_models.items():
        print(f"\nProcessing {lang}")
        lang_df = test_df[test_df['language'] == lang].copy()
        predictions = process_sentences(lang_df, nlp)
        # assign back using the same indices to preserve row order
        test_df.loc[lang_df.index, 'pred_pos_pattern'] = predictions

    elapsed = time.time() - start
    print(f"\nCompleted in {elapsed:.2f} seconds")

    # any rows not covered default to INCOMPLETE
    test_df['pred_pos_pattern'] = test_df['pred_pos_pattern'].fillna("INCOMPLETE")

    output_path = "data/pos_pattern_predictions.csv"
    test_df.to_csv(output_path, index=False)
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()
