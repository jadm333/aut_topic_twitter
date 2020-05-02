import spacy
from gensim.corpora import Dictionary
from gensim.models import Phrases
import preprocessor as prep

def filtrar_extremos(docs,max_freq=0.5,min_wordcount=2,n_top=3):
    dictionary = Dictionary(docs)
    dictionary.filter_extremes(no_below=min_wordcount, no_above=max_freq)
    dictionary.filter_n_most_frequent(n_top)
    _ = dictionary[0]

    return dictionary

def entidades(docs, nlp):
    processed_docs = []
    for doc in nlp.pipe(docs, n_threads=4, batch_size=100):
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


def pre_procesamiento(df):
    nlp = spacy.load('es')



    nlp.vocab["y"].is_stop = True
    nlp.vocab["a"].is_stop = True
    nlp.vocab["ante"].is_stop = True
    nlp.vocab["a"].is_stop = True
    nlp.vocab["bajo"].is_stop = True
    nlp.vocab["con"].is_stop = True
    nlp.vocab["de"].is_stop = True
    nlp.vocab["desde"].is_stop = True
    nlp.vocab["durante"].is_stop = True
    nlp.vocab["en"].is_stop = True
    nlp.vocab["entre"].is_stop = True
    nlp.vocab["excepto"].is_stop = True
    nlp.vocab["hacia"].is_stop = True
    nlp.vocab["hasta"].is_stop = True
    nlp.vocab["mediante"].is_stop = True
    nlp.vocab["para"].is_stop = True
    nlp.vocab["por"].is_stop = True
    nlp.vocab["salvo"].is_stop = True
    nlp.vocab["según"].is_stop = True
    nlp.vocab["sin"].is_stop = True
    nlp.vocab["sobre"].is_stop = True
    nlp.vocab["tras"].is_stop = True
    nlp.vocab["y"].is_stop = True
    nlp.vocab["e"].is_stop = True
    nlp.vocab["ni"].is_stop = True
    nlp.vocab["o"].is_stop = True
    nlp.vocab["u"].is_stop = True
    nlp.vocab["que"].is_stop = True
    nlp.vocab["si"].is_stop = True
    nlp.vocab["como"].is_stop = True
    nlp.vocab["donde"].is_stop = True
    nlp.vocab["quien"].is_stop = True
    nlp.vocab["cual"].is_stop = True
    nlp.vocab["cuyo"].is_stop = True
    nlp.vocab["cuanto"].is_stop = True
    nlp.vocab["el"].is_stop = True
    nlp.vocab["lalos"].is_stop = True
    nlp.vocab["las"].is_stop = True

    docs = list(df['text'])

    docs = entidades(docs ,nlp)

    docs = bigramas(docs)

    dictionary = filtrar_extremos(docs)

    corpus = [dictionary.doc2bow(doc) for doc in docs]

    # BORRAR TWEETS VACIOS
    id_borrar = [i for i in range(0 ,len(corpus)) if len(corpus[i]) == 0]
    df = df.drop(df.index[id_borrar])
    df = df.reset_index(drop=True)
    docs = list(df['text'])
    docs = entidades(docs ,nlp)
    docs = bigramas(docs)
    corpus = [dictionary.doc2bow(doc) for doc in docs]

    # AUTHOR2DOC
    author2doc = {}
    for aut in df.screen_name.unique():
        author2doc[aut] = []

    for index, row in df.iterrows():
        author2doc[row['screen_name']].append(index)


    return corpus, dictionary, author2doc
