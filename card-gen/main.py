from card_gen import *
import os
import pandas as pd

if __name__ == '__main__':
    output_dir = 'card_pngs'

    cards = json.load(open('cards.json', 'r'))
    print(f"Unique Count:\t{sum(1 for specs in cards.values())}")
    print(f"Card Count:\t\t{sum(specs['count'] for specs in cards.values())}")
    print('')
    for card_type, (unique, total) in pd.DataFrame.from_dict(cards, orient='index').groupby('card_type')['count'].agg(['count', 'sum']).iterrows():
        print(f'{card_type}:'.ljust(15) + f'\t{unique} unique; {total} total')

    cards = {k: v for k, v in cards.items() if k in ('Infrastructure')}
    for name, specs in reversed(cards.items()):
        print(name)
        c = Card(name, **specs)
        defaults = specs['defaults'] if 'defaults' in specs.keys() else {}
        # defaults['font'] = 'GillSans Condensed Bold.otf'
        if specs['card_type'] == 'policy':
            if specs['card_sub_type'] == 'economy':
                defaults['fill_color'] = (223, 241, 220)
            elif specs['card_sub_type'] == 'industry':
                defaults['fill_color'] = (236, 239, 255)
        if specs['card_type'] == 'technology':
            c.add(CornerIconComponent(f"icons/tech/{specs['card_sub_type']}.png"))
        if "components" in specs.keys():
            for cc_specs in specs['components']:
                c.add(CardComponent.from_dict({**defaults, **cc_specs}))
        else:
            c.add(CardComponent.from_dict({**defaults, **specs}))

        fpath = os.path.join(output_dir, specs['card_type'], specs['card_sub_type'] if 'card_sub_type' in specs.keys() else '', f'{name}[face,{specs["count"]}].png')
        c.gen_card(fpath)
