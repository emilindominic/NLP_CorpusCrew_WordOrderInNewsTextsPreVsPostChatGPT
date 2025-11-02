from pathlib import Path


def validate_conllu(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    sentences = 0
    has_pos = False
    has_deps = False
    has_metadata = False

    for line in lines:
        if line.startswith('# year'):
            sentences += 1
            has_metadata = True
        elif line.strip() and not line.startswith('#'):
            parts = line.split('\t')
            if len(parts) >= 10:
                if parts[3] in ['NOUN', 'VERB', 'ADJ', 'DET', 'AUX']:
                    has_pos = True
                if parts[7] in ['nsubj', 'obj', 'root', 'det']:
                    has_deps = True

    print(f"\n{filepath.name}:")
    print(f"  Sentences: {sentences}")
    print(f"  Has metadata: {has_metadata}")
    print(f"  Has POS tags: {has_pos}")
    print(f"  Has dependencies: {has_deps}")
    print(f"  Status: {'PASS' if all([has_metadata, has_pos, has_deps, sentences > 0]) else 'FAIL'}")


conllu_dir = Path('data/conllu')
for file in sorted(conllu_dir.glob('*.conllu')):
    validate_conllu(file)
    