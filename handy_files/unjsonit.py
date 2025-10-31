import json

with open('reflector_w_1f0mm_h_4f0mm/data/poo.json', 'r') as f:
    thing = json.load(f)
    print(len(thing))