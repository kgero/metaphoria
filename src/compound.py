import spacy
from src.embeddings import loadVectors
from src.analysis import stop
from src.badwords import isokay


nlp = spacy.load('en_core_web_sm')
dep = loadVectors('data/deps.vectors.slim.txt')

def get_obj(similar, sort, typeblank):
    '''
    Return list of words that are syntactically similar to origin to 'similar',
    but ordered by 'sort'.
    typeblank = 'noun_obj' or 'verb'
    '''
    sim = [(k[0], dep.similarity(sort, k[0])) for k in dep.most_similar_cosmul(positive=[similar], topn=60)]
    sim = sorted(sim, key=lambda t: t[1], reverse=True)
    return [k[0] for k in sim[:10] if isokay(k[0])]


def get_template(suggestion, poetic, concrete):
    '''
    Return template for compounding the suggestion. 

    Template is a dictionary with a str of the template and list different words
    for each 'blank'.

    e.g. 
        suggestion = 'jealousy is for growing flowers like a garden'
        poetic = 'jealousy'
        concrete = 'garden'

    return: 
    { 
      'template': 'jealousy is for growing _p1 and a garden is for growing _c1'
      '_p1': {
        'type': 'noun_obj', 
        'concept': 'jealousy', 
        'origin': 'flowers',
        'fillings': ['resentment', 'loneliness', etc. ]
        },
      '_c1': {
        'type': 'noun_obj', 
        'concept': 'garden', 
        'origin': 'flowers',
        'fillings': ['flowers', 'vegetables', 'creepers', etc.]
        }
    }
    '''
    doc = nlp(suggestion)

    blanks = []
    verbs = []
    new_sen = []
    you = False
    for token in doc:
        if token.text == 'you':
            you = True
            print("~{}~".format(token.text), end=' ')
        elif token.pos_ == 'VERB' and token.text not in stop:
            verbs.append(token.text)
            print("-{}-".format(token.text), end=' ')
        elif token.pos_ == 'NOUN' and token.text not in [concrete, poetic]:
            blanks.append(token.text)
            print("_{}_".format(token.text), end=' ')
        else:
            print("{}".format(token.text), end=' ')
    print('')

    template = {}
    backwards = suggestion.split(' ')[::-1]
    remove_like = backwards[backwards.index('like')+1:][::-1]
    part1 = []
    count = 1
    typeblank = 'noun_obj'
    if len(blanks) == 0:
        blanks = verbs
        typeblank = 'verb'
    for w in remove_like:
        if w in blanks:
            part1.append('_p'+str(count))
            template['_p'+str(count)] = {
                'type': typeblank, 
                'concept': poetic, 
                'origin': w,
                'fillings': get_obj(poetic, w, typeblank)
                }
            count += 1
        else:
            part1.append(w)

    part2 = []
    count = 1
    for w in remove_like:
        if w in blanks:
            part2.append('_c'+str(count))
            template['_c'+str(count)] = {
                'type': typeblank, 
                'concept': concrete, 
                'origin': w,
                'fillings': [w] + get_obj(w, concrete, typeblank)
                }
            count += 1
        elif w == poetic:
            part2.append(concrete)
        else:
            part2.append(w)

    template['template'] = ' '.join(part2) + ' | ' + ' '.join(part1)
    return(template)
