import gensim
import numpy as np
import random

from nltk.corpus import wordnet as wn

stop = ['is', 'like', 'a', 'an', 'does', 'has', 'capable', 'of', 'in', 'to', 
        'it', 'used', 'for', 'from', 'you', 'can', 'use', 'with', 'or', 'the',
        'on']

def loadGlove(filepath):
    '''
    Return gensim word vectors.
    '''
    print("loading w2v from" + filepath + "...")
    model = gensim.models.KeyedVectors.load_word2vec_format(filepath, limit=40000)
    word_vectors = model.wv
    del model
    print("ready")
    return word_vectors

def loadValence(filepath):
    '''Return dictionary of word:valence score.'''
    d = {}
    with open(filepath, 'r') as f:
        next(f)
        for line in f:
            data = line.split(",")
            word = data[1]
            valence = float(data[2])
            d[word] = valence
    return d

def in_vocab(word):
    '''Return true if word in vocab of glove; else return false.'''
    return word in vectors.vocab


def prepSen(sen):
    '''
    Return sen as list of lower case words, removing punctuation and stop words.
    '''
    prep = [w.strip(',') for w in sen.lower().split() if w not in stop]
    for w in prep:
        if w not in vectors.vocab:
            # print('\"{}\" from \"{}\" not in glove'.format(w, sen))
            return []
    return prep


def order_valence(sentences, poetic, pprint=False):
    if valence.get(poetic) is None:
        print('{} not in valence dict')
        return sentences
    sim = []
    for sen in sentences:
        prep = prepSen(sen)
        v_score = []
        for word in prep:
            if valence.get(word) is not None:
                v_score.append(valence[word])
        sim.append((sen, abs(np.mean(v_score)-valence[poetic])))
    sim = sorted(sim, key=lambda t: t[1])
    if pprint:
        for i, item in enumerate(sim):
            print("{:<45} \t {:<20}".format(item[0], sim[i][1]))
    return [item[0] for item in sim]


def order_sen(sentences, poetic, pprint=False):
    '''
    Return sentences ordered by usefulness.
    '''
    sim = []
    for sen in sentences:
        prep = prepSen(sen)
        prep = [p for p in prep if p != poetic][:-1]  # NAIVE!! TRYING TO GET RID OF CONCRETE WORD
        if len(prep) > 0:
            # sim.append((sen, vectors.n_similarity(prep, [poetic]), prep))  # should this not be vectors.wmdistance?!?!
            sim.append((sen, vectors.wmdistance(prep, [poetic]), prep))
    sim = sorted(sim, key=lambda t: t[1])  # regular order for WMD, REVERSE FOR N_SIM!!!
    if pprint:
        for i, item in enumerate(sim):
            print("{:<45} \t {:<20} \t {}".format(item[0], sim[i][1], sim[i][2]))
    sentences = [item[0] for item in sim]
    # return order_valence(sentences, poetic)
    return sentences

def select_top(sentences, poetic, num=10, reverse=False):
    '''
    Return top sentences based on distance to poetic but not including any 
    sentences with a distance less than 4 to any other sentence selected.
    '''
    ordered = order_sen(sentences, poetic)
    if reverse:
        ordered = ordered[::-1]
    top = [ordered[0]]
    index = 1
    while len(top) < num and index < len(ordered):
        potential = ordered[index]
        index += 1
        add = True
        for sen in top:
            p1 = [p for p in prepSen(sen) if p != poetic][:-1] # NAIVE!! TRYING TO GET RID OF CONCRETE WORD
            p2 = [p for p in prepSen(potential) if p != poetic][:-1] # NAIVE!! TRYING TO GET RID OF CONCRETE WORD
            d = vectors.wmdistance(p1, p2)
            if d < 4:
                add = False
        if add:
            top.append(potential)
    return top

embeddings = 'data/glove.slim.txt'
v = 'data/BRM-emot-submit.csv'
vectors = loadGlove(embeddings)
valence = loadValence(v)
