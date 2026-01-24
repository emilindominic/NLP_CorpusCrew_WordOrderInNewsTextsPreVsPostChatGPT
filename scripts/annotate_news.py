import argparse
import sys
from pathlib import Path
import pandas as pd
import stanza
from stanza.utils.conll import CoNLL
from tqdm import tqdm


def setup_stanza_models(lang_codes):
    for code in lang_codes:
        print(f"Checking Stanza model for {code}...")
        try:
            stanza.download(code, verbose=False)
        except Exception as e:
            print(f"Warning: Could not download {code}: {e}")


def get_stanza_pipeline(lang_code):
    print(f"Loading Stanza pipeline for {lang_code}...")
    return stanza.Pipeline(
        lang_code,
        processors='tokenize,lemma,pos,depparse',
        tokenize_pretokenized=False,
        verbose=False,
        use_gpu=False
    )


def annotate_and_save(df, nlp, output_path, max_sentences=None):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # take sentences and optionally cut to max_sentences
    sentences = df['sentence'].tolist()
    if max_sentences:
        sentences = sentences[:max_sentences]
        df = df.head(max_sentences)

    print(f"Processing {len(sentences)} sentences to {output_path.name}...")

    with open(output_path, 'w', encoding='utf-8') as f:
        batch_size = 50

        # go through data in small batches
        for i in tqdm(range(0, len(sentences), batch_size), desc="Annotating"):
            batch_sents = sentences[i:i + batch_size]
            batch_meta = df.iloc[i:i + batch_size]

            for j, sent_text in enumerate(batch_sents):
                try:
                    row = batch_meta.iloc[j]

                    # metadata we want to preserve from cleaning stage
                    f.write(f"# year = {row['year']}\n")
                    f.write(f"# period = {row['period']}\n")

                    # some rows might have empty or NaN date, we only write if it's real
                    date_val = row.get('date')
                    if pd.notna(date_val) and str(date_val).strip() != "":
                        f.write(f"# date = {date_val}\n")

                    # standard CoNLL-U style comments
                    # sent_id: stable identifier per sentence
                    # text: original surface form
                    sent_id = f"{output_path.stem}__{i + j}"
                    f.write(f"# sent_id = {sent_id}\n")
                    f.write(f"# text = {sent_text}\n")

                    # run stanza and dump as CoNLL-U
                    doc = nlp(sent_text)
                    CoNLL.write_doc2conll(doc, f)

                except Exception as e:
                    print(f"\nError processing: {sent_text[:80]}... -> {e}")
                    continue

    print(f"Saved {output_path.name}")


def process_language_files(in_dir, out_dir, lang_code, stanza_code, max_sentences=None):
    in_dir = Path(in_dir)
    out_dir = Path(out_dir)

    pattern = f"{lang_code}_*.tsv"
    tsv_files = list(in_dir.glob(pattern))

    if not tsv_files:
        print(f"No files found for {lang_code} (pattern: {pattern})")
        return

    print(f"\nFound {len(tsv_files)} files for {lang_code}")

    nlp = get_stanza_pipeline(stanza_code)

    for tsv_path in sorted(tsv_files):
        try:
            df = pd.read_csv(tsv_path, sep='\t')

            output_name = tsv_path.stem.replace('_clean', '') + '.conllu'
            output_path = out_dir / output_name

            annotate_and_save(df, nlp, output_path, max_sentences)

        except Exception as e:
            print(f"Error processing {tsv_path.name}: {e}")
            continue


def main():
    parser = argparse.ArgumentParser(
        description="Annotate cleaned news with Stanza and save as CoNLL-U"
    )
    parser.add_argument(
        '--in_dir',
        type=str,
        default='data/clean',
        help='Directory with cleaned TSV files'
    )
    parser.add_argument(
        '--out_dir',
        type=str,
        default='data/conllu',
        help='Output directory for CoNLL-U files'
    )
    parser.add_argument(
        '--max_sentences',
        type=int,
        default=None,
        help='Max sentences per file (None=all)'
    )
    parser.add_argument(
        '--lang',
        type=str,
        default=None,
        help='Process only specific language (eng|deu|rus)'
    )

    args = parser.parse_args()

    in_dir = Path(args.in_dir)
    if not in_dir.exists():
        print(f"Input directory {in_dir} does not exist")
        sys.exit(1)

    lang_map = {'eng': 'en', 'deu': 'de', 'rus': 'ru'}

    if args.lang:
        if args.lang not in lang_map:
            print(f"Unknown language: {args.lang}")
            sys.exit(1)
        lang_codes = {args.lang: lang_map[args.lang]}
        print(f"Processing only: {args.lang}")
    else:
        lang_codes = lang_map
        print("Processing all languages")

    setup_stanza_models(list(lang_codes.values()))

    for lang_code, stanza_code in lang_codes.items():
        print(f"\n{'=' * 50}")
        print(f"Processing {lang_code.upper()}")
        print(f"{'=' * 50}")
        process_language_files(in_dir, args.out_dir, lang_code, stanza_code, args.max_sentences)

    print(f"\nAll done! CoNLL-U files in {args.out_dir}")


if __name__ == "__main__":
    main()
