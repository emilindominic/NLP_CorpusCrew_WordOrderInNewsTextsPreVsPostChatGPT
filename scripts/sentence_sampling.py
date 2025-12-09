import pandas as pd

def sample_sentences(df, languages, n_samples=20, seed=10):
    samples = []

    for lang in languages:
        df_lang = df[df['language'] == lang]

        # Sample N sentences for this language
        lang_sample = df_lang.sample(
            n=n_samples,
            random_state=seed
        )

        samples.append(lang_sample)

    # Combine everything
    out_df = pd.concat(samples).reset_index(drop=True)

    # Add empty columns for manual annotation
    out_df['true_word_order'] = ""
    out_df['notes'] = ""

    return out_df


def main():
    df = pd.read_csv('data/splits/test.csv')

    languages = ['eng', 'deu', 'rus']

    sampled_df = sample_sentences(
        df,
        languages,
        n_samples=20,
        seed=10
    )

    sampled_df.to_csv('data/manual_annotation_sample.csv', index=False)
    print("Saved manual annotation sample to data/manual_annotation_sample.csv")


if __name__ == "__main__":
    main()
