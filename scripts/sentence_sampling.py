import pandas as pd

def sample_sentences(df, languages, n_per_period=50, seed=42):
    samples = []

    for lang in languages:
        df_lang = df[df['language'] == lang]

        # Pre-ChatGPT sampling
        pre = df_lang[df_lang['period'] == 'Pre-ChatGPT'].sample(
            n=n_per_period, random_state=seed
        )
        pre['sample_period'] = 'Pre'

        # Post-ChatGPT sampling
        post = df_lang[df_lang['period'] == 'Post-ChatGPT'].sample(
            n=n_per_period, random_state=seed
        )
        post['sample_period'] = 'Post'

        samples.append(pre)
        samples.append(post)

    return pd.concat(samples).reset_index(drop=True)


def main():
    df = pd.read_csv('data/word_order_all_languages.csv')

    languages = ['eng', 'deu', 'rus']

    sampled_df = sample_sentences(df, languages, n_per_period=50)
    sampled_df.to_csv('data/manual_annotation_sample.csv', index=False)

    print("Saved manual annotation sample to data/manual_annotation_sample.csv")


if __name__ == "__main__":
    main()
