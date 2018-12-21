import random

from src.expand_source_cnet import get_cnet_rel
from src.analysis import select_top, order_valence, in_vocab


def get_rel_sen(poetic, concrete):
    cnet = get_cnet_rel(concrete)
    text = []
    for item in cnet:
        t = item['suggest'].replace('___', poetic)
        text.append(t)
    return text

def get_suggestions(poetic, concrete):
    if not in_vocab(poetic):
        return []
    r = get_rel_sen(poetic, concrete)
    if len(r) == 0:
        return []
    top = select_top(r, poetic, num=10)
    top = order_valence(top, poetic)
    return top

