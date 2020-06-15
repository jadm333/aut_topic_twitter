import spacy
from gensim.corpora import Dictionary
from gensim.models import Phrases
import preprocessor as prep


def filtrar_extremos(docs,max_freq=0.5, min_wordcount=2, n_top=3):
    dictionary = Dictionary(docs)
    dictionary.filter_extremes(no_below=min_wordcount, no_above=max_freq)
    dictionary.filter_n_most_frequent(n_top)
    _ = dictionary[0]

    return dictionary


def entidades(docs, nlp):
    processed_docs = []
    for doc in nlp.pipe(docs, n_threads=8, batch_size=100):
        ents = doc.ents

        doc = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]

        doc.extend([str(entity) for entity in ents if len(entity) > 1])

        processed_docs.append(doc)

    return processed_docs


def bigramas(docs):
    bigram = Phrases(docs, min_count=20)
    doc = docs
    for idx in range(len(doc)):
        for token in bigram[doc[idx]]:
            if '_' in token:
                doc[idx].append(token)
    return doc


def remove_chars(df_raw):
    df_ = df_raw.copy()
    prep.set_options(prep.OPT.URL, prep.OPT.EMOJI, prep.OPT.RESERVED, prep.OPT.SMILEY, prep.OPT.NUMBER)
    df_['text_clean'] = df_['text'].apply(prep.clean)
    df_["text_clean"] = df_['text_clean'].str.replace(r"[@#!¿\?\'\"\%\+=\`\~|;áàé\‘\“\”\¡ºª▶️.]", '', regex=True)
    return df_.drop("text", axis=1)
