"""
Tools for expanding a source domain into 'features'. Uses conceptnet API.

List of relations in conceptnet:
https://github.com/commonsense/conceptnet5/wiki/Relations

Decent number of physical nouns have lots of expansion.

Abstract nouns tend to only have expansion if there is also
a physical definition to latch onto...
"""
import requests
from src.badwords import isokay

def make_sen(surfaceText):
    '''
    Return str of suggestion text given surfaceText.

    e.g. surfaceText = '[[a book]] is used for [[explaining]]'
    return = '___, like a book, is used for explaining.'
    '''
    start = surfaceText.find('[')+2
    end = surfaceText.find(']')
    pre = surfaceText[:start]
    concept = surfaceText[start:end]
    post = surfaceText[end:]
    new_text = pre + '___' + post + ' like ' + concept
    return new_text.replace('[', '').replace(']', '').lower()


def get_cnet_rel(noun):
    '''
    Return list of related concepts with relation.
    '''
    results = []
    queries = [
        {'start': '/c/en/' + noun, 'rel': '/r/HasA'},
        {'start': '/c/en/' + noun, 'rel': '/r/UsedFor'},
        {'start': '/c/en/' + noun, 'rel': '/r/CapableOf'}
        ]
    natlang = {
        '/r/HasA': {'text': 'has a', 'start': 'does '},
        '/r/UsedFor': {'text': 'used for', 'start': 'is '},
        '/r/CapableOf': {'text': 'capable of', 'start': 'is '},
    }
    for q in queries:
        obj = requests.get('http://api.conceptnet.io/query', params=q).json()

        for e in obj['edges']:
            if 'start' in q:
                results.append({
                    'name': e['end']['label'],
                    'weight': e['weight'],
                    'start': natlang[q['rel']]['start'],
                    'text': natlang[q['rel']]['text'],
                    'surface': e['surfaceText'],
                    'suggest': make_sen(e['surfaceText'])
                    })
    results = sorted(results, key=lambda tup: tup['weight'], reverse=True)
    return [res for res in results if isokay(res)]
