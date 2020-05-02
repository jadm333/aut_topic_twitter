# %%
from helpers.reading import read_filter_df
import helpers.preprocesamiento as procs
import spacy

# %%
f_fin = "2017-09-11"
f_ini = "2017-09-04"

# %%
df, f_ini, f_fin = read_filter_df(f_ini=f_ini, f_fin=f_fin, path="data/twitter_accounts/")

# %%
df_char_r = procs.remove_chars(df)
# %%
# def pre_procesamiento(df):
df_ = df_char_r
nlp = spacy.load('es_core_news_md')
# %%
stop_words = ["y", "a", "ante", "a", "bajo", "con", "de", "desde", "durante", "en", "entre", "excepto", "hacia",
              "hasta", "mediante", "para", "por", "salvo", "según", "sin", "sobre", "tras", "y", "e", "ni", "o", "u",
              "que", "si", "como", "donde", "quien", "cual", "cuyo", "cuanto", "el", "lalos", "las"]

for word in stop_words:
    nlp.vocab[word].is_stop = True
# %%
docs = list(df_['text_clean'])
# %%
docs = entidades(docs, nlp)
# %%
docs = bigramas(docs)
# %%
dictionary = filtrar_extremos(docs)
# %%
corpus = [dictionary.doc2bow(doc) for doc in docs]
# %%
# BORRAR TWEETS VACIOS
id_borrar = [i for i in range(0, len(corpus)) if len(corpus[i]) == 0]
df = df.drop(df.index[id_borrar])
df = df.reset_index(drop=True)
docs = list(df['text'])
docs = entidades(docs, nlp)
docs = bigramas(docs)
corpus = [dictionary.doc2bow(doc) for doc in docs]
# %%
# AUTHOR2DOC
author2doc = {}
for aut in df.screen_name.unique():
    author2doc[aut] = []

for index, row in df.iterrows():
    author2doc[row['screen_name']].append(index)

# return corpus, dictionary, author2doc

# %%
# %%
# %%
