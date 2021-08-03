from card_gen import *

if __name__ == '__main__':
    cards = json.load(open('cards.json', 'r'))
    # cards = {k: v for k, v in cards.items() if k in ('Public Education')}
    for name, specs in reversed(cards.items()):
        print(name)
        c = Card(name, **specs)
        defaults = specs['defaults'] if 'defaults' in specs.keys() else {}
        if specs['card_type'] == 'policy':
            if specs['card_sub_type'] == 'economy':
                defaults['fill_color'] = (223, 241, 220)
            elif specs['card_sub_type'] == 'industry':
                defaults['fill_color'] = (236, 239, 255)
        if "components" in specs.keys():
            for cc_specs in specs['components']:
                c.add(CardComponent.from_dict({**defaults, **cc_specs}))
        else:
            c.add(CardComponent.from_dict({**defaults, **specs}))
        c.gen_card(show=False)
