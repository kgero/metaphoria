import json
import re

# ---------------------------------------------------------------------------
# Load the subset once at module level so it's not re-read on every request.
# Adjust the path to wherever you put the JSON file.
# ---------------------------------------------------------------------------
_CNET_PATH = 'conceptnet/conceptnet_en_subset.json'
_cnet_data = None

def _load_cnet():
    global _cnet_data
    if _cnet_data is None:
        print(f'Loading ConceptNet subset from {_CNET_PATH} ...')
        with open(_CNET_PATH, 'r', encoding='utf-8') as f:
            _cnet_data = json.load(f)
        print(f'  Loaded {len(_cnet_data):,} concepts.')
    return _cnet_data


# ---------------------------------------------------------------------------
# These helpers are unchanged from your original code — keep yours if they
# differ, these are placeholders so the module is self-contained.
# ---------------------------------------------------------------------------
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

def isokay(res):
    """Filter out results with no useful surface text."""
    return bool(res.get('surface'))


# ---------------------------------------------------------------------------
# Drop-in replacement for get_cnet_rel
# ---------------------------------------------------------------------------
NATLANG = {
    '/r/HasA':     {'text': 'has a',      'start': 'does '},
    '/r/UsedFor':  {'text': 'used for',   'start': 'is '},
    '/r/CapableOf':{'text': 'capable of', 'start': 'is '},
}

def get_cnet_rel(noun):
    """
    Return list of related concepts with relation.
    Reads from local JSON subset instead of hitting the ConceptNet API.
    """
    data = _load_cnet()
    results = []

    noun_key = noun.replace('_', ' ')          # normalise to match extracted labels
    noun_entry = data.get(noun_key, {})

    for rel, nl in NATLANG.items():
        edges = noun_entry.get(rel, [])
        for e in edges:
            if e.get('surface'):
                results.append({
                    'name':    e['name'],
                    'weight':  e['weight'],
                    'start':   nl['start'],
                    'text':    nl['text'],
                    'surface': e['surface'],
                    'suggest': make_sen(e['surface']),
                })

    results = sorted(results, key=lambda r: r['weight'], reverse=True)
    return [res for res in results if isokay(res)]