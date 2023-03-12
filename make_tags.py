import json
import re
from pathlib import Path

with open('conf/corpus.json', encoding='utf-8') as f:
    data = json.load(f)

cols = data['lang_props']['ket']['gloss_selection']['columns']

tags = []

for col in cols:
    for tag in col:
        tags.extend(re.split(r'[.=-]', tag['value']))

with open('conf/categories.json', 'w', encoding='utf-8') as f:
    json.dump(
        {'ket': {
            x: 'tag' for x in sorted(set(tags))
        }}, f, ensure_ascii=False, indent=2
    )

for file in Path('corpus/ket/').iterdir():
    with file.open(encoding='utf-8') as f:
        text = json.load(f)
    
    for sentence in text['sentences']:
        for word in sentence['words']:
            if "ana" not in word:
                continue
            for ana in word['ana']:
                glosses = re.sub(r'\{.*?\}', '', ana['gloss_index']).strip('-=')
                glosses = re.split(r'[.=-]+', glosses)
                ana['gr.tag'] = glosses
                del word['gr.tag']
    
    with file.open('w', encoding='utf8') as f:
        json.dump(text, f, ensure_ascii=False, indent=2)