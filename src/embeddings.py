import gensim, logging, os, string

from nltk.data import find

# from gensim.scripts.glove2word2vec import glove2word2vec
# glove2word2vec('../data/deps.words', '../data/deps-vectors.txt')


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.ERROR)

def loadVectors(filepath, loadall=False):
    '''
    Return gensim word vectors.
    '''
    print("loading "+filepath+"...")
    if loadall:
        model = gensim.models.KeyedVectors.load_word2vec_format(filepath) 
    else:
        model = gensim.models.KeyedVectors.load_word2vec_format(filepath, limit=40000) 
    word_vectors = model.wv
    del model
    print("ready")
    return word_vectors
