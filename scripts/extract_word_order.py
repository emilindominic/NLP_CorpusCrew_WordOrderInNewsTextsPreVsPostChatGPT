"""
Extract word order patterns (SVO, SOV, etc.) from CoNLL-U annotated files.
This script reads dependency-parsed sentences and identifies Subject-Verb-Object order.
"""

import argparse
from pathlib import Path
import pandas as pd
from collections import defaultdict


def read_conllu_file(filepath, max_sentences=None):
    """
    Parse a CoNLL-U file and extract sentences with their tokens.
    Returns list of sentences, where each sentence is a list of token dicts.
    """
    sentences = []
    current_sentence = []
    metadata = {}

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            # metadata lines (year, period)
            if line.startswith('# '):
                key_val = line[2:].split(' = ')
                if len(key_val) == 2:
                    metadata[key_val[0]] = key_val[1]

            # empty line = end of sentence
            elif not line:
                if current_sentence:
                    sentences.append({
                        'tokens': current_sentence,
                        'metadata': metadata.copy()
                    })
                    current_sentence = []
                    metadata = {}

                    # stop if we hit the limit
                    if max_sentences and len(sentences) >= max_sentences:
                        break

            # token line
            elif not line.startswith('#'):
                parts = line.split('\t')
                if len(parts) >= 10:
                    # skip multi-word tokens (like 15-16)
                    if '-' in parts[0]:
                        continue

                    token = {
                        'id': int(parts[0]),
                        'text': parts[1],
                        'lemma': parts[2],
                        'upos': parts[3],      # universal POS tag
                        'xpos': parts[4],
                        'feats': parts[5],
                        'head': int(parts[6]) if parts[6] != '_' else 0,
                        'deprel': parts[7],    # dependency relation
                        'deps': parts[8],
                        'misc': parts[9]
                    }
                    current_sentence.append(token)

    return sentences


def extract_svo(sentence_tokens):
    """
    Find Subject, Verb, and Object in MAIN CLAUSE based on dependency relations.
    Only extracts S and O that directly connect to the root verb (main clause).
    This prevents mixing elements from different clauses.
    """
    # S1: Find the root verb
    verb = None
    for token in sentence_tokens:
        if token['deprel'] == 'root' and token['upos'] in ['VERB', 'AUX']:
            verb = token
            break

    # if no root verb found, cant determine anything
    if not verb:
        return {
            'subject': None,
            'verb': None,
            'object': None,
            'has_subject': False,
            'has_verb': False,
            'has_object': False
        }

    # S2: Find subject and object that point to this root verb
    # this ensures we only get elements from the main clause
    subject = None
    obj = None

    for token in sentence_tokens:
        # Subject must point to the root verb
        if token['deprel'] in ['nsubj', 'nsubj:pass'] and token['head'] == verb['id']:
            subject = token

        # Object must point to the root verb
        elif token['deprel'] == 'obj' and token['head'] == verb['id']:
            obj = token

    return {
        'subject': subject,
        'verb': verb,
        'object': obj,
        'has_subject': subject is not None,
        'has_verb': verb is not None,
        'has_object': obj is not None
    }


def determine_word_order(svo_dict):
    """
    Compare positions of S, V, O to determine word order type.
    Returns word order label like "SVO", "SOV", etc.
    """
    s = svo_dict['subject']
    v = svo_dict['verb']
    o = svo_dict['object']

    # if any core element is missing, cant determine full order
    if not (s and v and o):
        # partial orders
        if s and v:
            return 'SV_only'
        elif v and o:
            return 'VO_only'
        elif s and o:
            return 'SO_only'
        else:
            return 'INCOMPLETE'

    # compare positions to determine order
    s_pos = s['id']
    v_pos = v['id']
    o_pos = o['id']

    # 6 possible orders
    if s_pos < v_pos < o_pos:
        return 'SVO'
    elif s_pos < o_pos < v_pos:
        return 'SOV'
    elif v_pos < s_pos < o_pos:
        return 'VSO'
    elif v_pos < o_pos < s_pos:
        return 'VOS'
    elif o_pos < s_pos < v_pos:
        return 'OSV'
    elif o_pos < v_pos < s_pos:
        return 'OVS'
    else:
        return 'UNCLEAR'


def process_conllu_file(filepath, max_sentences=None):
    """
    Process one CoNLL-U file and extract word orders for all sentences.
    Returns list of dicts with sentence info and word order labels.
    """
    sentences = read_conllu_file(filepath, max_sentences)
    results = []

    for sent_data in sentences:
        tokens = sent_data['tokens']
        metadata = sent_data['metadata']

        svo = extract_svo(tokens)
        word_order = determine_word_order(svo)
        sentence_text = ' '.join(t['text'] for t in tokens)

        # compile result
        result = {
            'sent_id': metadata.get('sent_id', 'unknown'),
            'year': metadata.get('year', 'unknown'),
            'period': metadata.get('period', 'unknown'),
            'date': metadata.get('date', 'unknown'),
            'sentence': sentence_text,
            'word_order': word_order,
            'has_subject': svo['has_subject'],
            'has_verb': svo['has_verb'],
            'has_object': svo['has_object'],
        }

        # add actual word positions for debugging
        if svo['subject']:
            result['subj_text'] = svo['subject']['text']
            result['subj_pos'] = svo['subject']['id']
        if svo['verb']:
            result['verb_text'] = svo['verb']['text']
            result['verb_pos'] = svo['verb']['id']
        if svo['object']:
            result['obj_text'] = svo['object']['text']
            result['obj_pos'] = svo['object']['id']

        results.append(result)

    return results


def main():
    parser = argparse.ArgumentParser(description='Extract word orders from CoNLL-U files')
    parser.add_argument('--input', required=True, help='Path to CoNLL-U file or directory')
    parser.add_argument('--output', default='data/word_order_labeled.csv',
                       help='Output CSV file')
    parser.add_argument('--test', type=int, default=None,
                       help='Test mode: process only N sentences per file')

    args = parser.parse_args()

    input_path = Path(args.input)

    if input_path.is_file():
        conllu_files = [input_path]
    else:
        conllu_files = sorted(input_path.glob('*.conllu'))

    print(f"Found {len(conllu_files)} CoNLL-U files")

    # process each file
    all_results = []
    for filepath in conllu_files:
        print(f"\nProcessing: {filepath.name}")

        parts = filepath.stem.split('_')
        language = parts[0]

        results = process_conllu_file(filepath, max_sentences=args.test)

        # add language to each result
        for r in results:
            r['language'] = language

        all_results.extend(results)

        print(f"Extracted {len(results)} sentences")

        # show distribution for this file
        if results:
            order_counts = defaultdict(int)
            for r in results:
                order_counts[r['word_order']] += 1

            print(f"Word order distribution:")
            for order, count in sorted(order_counts.items(), key=lambda x: -x[1]):
                pct = 100 * count / len(results)
                print(f"{order}: {count} ({pct:.1f}%)")

    # save to CSV
    if all_results:
        df = pd.DataFrame(all_results)

        cols = ['sent_id', 'language', 'year', 'period', 'date', 'word_order',
                'sentence', 'has_subject', 'has_verb', 'has_object']

        # add optional columns if they exist
        optional = ['subj_text', 'subj_pos', 'verb_text', 'verb_pos', 'obj_text', 'obj_pos']
        for col in optional:
            if col in df.columns:
                cols.append(col)

        df = df[cols]

        # create output directory if needed
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(output_path, index=False)
        print(f"\n✓ Saved {len(all_results)} sentences to {output_path}")

        # overall statistics
        print(f"\n=== Overall Statistics ===")
        print(f"Total sentences: {len(all_results)}")
        print(f"\nWord order distribution:")
        order_counts = df['word_order'].value_counts()
        for order, count in order_counts.items():
            pct = 100 * count / len(df)
            print(f"  {order}: {count} ({pct:.1f}%)")

        print(f"\nBy language:")
        for lang in df['language'].unique():
            lang_df = df[df['language'] == lang]
            svo_count = len(lang_df[lang_df['word_order'] == 'SVO'])
            pct = 100 * svo_count / len(lang_df)
            print(f"{lang}: {len(lang_df)} sentences, {svo_count} SVO ({pct:.1f}%)")

    else:
        print("No results to save!")


if __name__ == '__main__':
    main()
