#!/usr/bin/env python3
"""
Extract HasA, UsedFor, and CapableOf relations for English concepts
from the ConceptNet 5.7 assertions CSV dump.

Usage:
    python extract_conceptnet.py conceptnet-assertions-5.7.0.csv.gz

Output:
    conceptnet_en_subset.json
"""

import csv
import gzip
import json
import sys
from collections import defaultdict

RELATIONS = {'/r/HasA', '/r/UsedFor', '/r/CapableOf'}

def is_english(uri):
    return uri.startswith('/c/en/')

def label_from_uri(uri):
    """Extract the human-readable label from a ConceptNet URI like /c/en/knife/n"""
    parts = uri.split('/')
    # parts: ['', 'c', 'en', 'word', optional_pos, ...]
    if len(parts) >= 4:
        return parts[3].replace('_', ' ')
    return None

def main(input_path):
    # data[start_noun][relation] = list of {name, weight, surface}
    data = defaultdict(lambda: defaultdict(list))
    count = 0
    kept = 0

    opener = gzip.open if input_path.endswith('.gz') else open

    print(f"Reading {input_path} ...")
    with opener(input_path, 'rt', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            count += 1
            if count % 500_000 == 0:
                print(f"  {count:,} rows read, {kept:,} kept...")

            if len(row) < 5:
                continue

            _edge_uri, relation, start_uri, end_uri, meta_json = row[:5]

            if relation not in RELATIONS:
                continue
            if not is_english(start_uri) or not is_english(end_uri):
                continue

            try:
                meta = json.loads(meta_json)
            except json.JSONDecodeError:
                continue

            weight = meta.get('weight', 1.0)
            surface = meta.get('surfaceText', '')

            start_label = label_from_uri(start_uri)
            end_label = label_from_uri(end_uri)

            if not start_label or not end_label:
                continue

            data[start_label][relation].append({
                'name': end_label,
                'weight': weight,
                'surface': surface,
            })
            kept += 1

    print(f"Done. {count:,} rows read, {kept:,} kept across {len(data):,} start concepts.")

    # Sort each list by weight descending (mirrors ConceptNet API behaviour)
    output = {}
    for start, rels in data.items():
        output[start] = {}
        for rel, edges in rels.items():
            output[start][rel] = sorted(edges, key=lambda e: e['weight'], reverse=True)

    out_path = 'conceptnet_en_subset.json'
    print(f"Writing {out_path} ...")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False)

    print(f"Done. Output written to {out_path}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extract_conceptnet.py <path-to-assertions.csv.gz>")
        sys.exit(1)
    main(sys.argv[1])