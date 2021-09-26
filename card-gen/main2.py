from card_gen import *
import os
import pandas as pd

if __name__ == '__main__':
    output_dir = 'card_pngs'

    cards = json.load(open('cards.json', 'r'))
    # cards = {k: v for k, v in cards.items() if k in ('Industrialization')}
    cards = {k: v for k, v in cards.items() if v['card_type'] == 'policy' and len([comp for comp in v['components'] if 'component_type' in comp.keys() and comp['component_type'] == 'payment-reward']) > 0}

    for name, specs in reversed(cards.items()):
        print(name)
        text_components = [comp for comp in specs['components'] if 'text' in comp.keys() and not ('component_type' in comp.keys() and comp['component_type'] == 'payment-reward')]
        paymentreward_components = [comp for comp in specs['components'] if 'component_type' in comp.keys() and comp['component_type'] == 'payment-reward']
        dev_component = FullDevCardComponent(
            title=name,
            icon=f"icons/policy/{specs['card_sub_type']}.png",
            text=text_components[0]['text'] if len(text_components) > 0 else None,
            paymentreward=paymentreward_components[0] if len(paymentreward_components) > 0 else None,
            color2=(12, 44, 4))
        c = Card(name, **specs)
        c.add(dev_component)

        fpath = os.path.join(output_dir, specs['card_type'], specs['card_sub_type'] if 'card_sub_type' in specs.keys() else '', f'{name}[face,{specs["count"]}].png')
        c.gen_card(fpath)
