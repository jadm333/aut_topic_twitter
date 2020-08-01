from gensim import matutils
import pandas as pd


def predict_author(new_doc, atmodel, top_n=10, smallest_author=1):
    '''
    Reference: https://nbviewer.jupyter.org/github/RaRe-Technologies/gensim/blob/master/docs/notebooks/atmodel_prediction_tutorial.ipynb
    '''
    def similarity(vec1, vec2):
        '''Similaridad entre dos vectores'''
        dist = matutils.hellinger(matutils.sparse2full(vec1, atmodel.num_topics), \
                                  matutils.sparse2full(vec2, atmodel.num_topics))
        sim = 1.0 / (1.0 + dist)
        return sim

    def get_sims(vec):
        '''Similaridad entre vector y los vectores de los autores'''
        sims = [similarity(vec, vec2) for vec2 in author_vecs]
        return sims

    author_vecs = [atmodel.get_author_topics(author) for author in atmodel.id2author.values()]
    new_doc_topics = atmodel.get_new_author_topics(new_doc)
    # Get similarities.
    sims = get_sims(new_doc_topics)

    # Arrange author names, similarities, and author sizes in a list of tuples.
    table = []
    for elem in enumerate(sims):
        author_name = atmodel.id2author[elem[0]]
        sim = elem[1]
        author_size = len(atmodel.author2doc[author_name])
        if author_size >= smallest_author:
            table.append((author_name, sim, author_size))

    # Make dataframe and retrieve top authors.
    df = pd.DataFrame(table, columns=['Author', 'Score', 'Size'])
    df = df.sort_values('Score', ascending=False)[:top_n]

    return df

def prediction_accuracy(test_author2doc, test_corpus, model, k=5):
    matches=0
    tries = 0
    for author in test_author2doc:
        author_id = model.author2id[author]
        for doc_id in test_author2doc[author]:
            predicted_authors = predict_author(test_corpus[doc_id:doc_id+1], atmodel=model, top_n=k)
            tries = tries+1
            if author_id in predicted_authors["Author"]:
                matches=matches+1

    accuracy = matches/tries
    return accuracy