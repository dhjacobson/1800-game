from card_gen import *
import os
import pandas as pd

colors = {'policy': (12, 44, 4), 'technology': (51, 4, 1), 'institution': (3, 30, 74), 'military': (130, 26, 19), 'admin': (206, 181, 105), 'ambition': (89, 59, 89), 'event': (133, 169, 116)}
# colors = {'policy': (12, 44, 4), 'technology': (61, 29, 2), 'institution': (3, 30, 74)}

if __name__ == '__main__':
    output_dir = 'card_pngs'

    cards = json.load(open('cards.json', 'r'))
    # cards = {k: v for k, v in cards.items() if k == 'Telephone'}
    # cards = {k: v for k, v in cards.items() if v['card_type'] in  ('institution')}

    for name, d in reversed(cards.items()):
        if d['card_type'] in ('policy', 'institution', 'technology'):
            for component in d['components']:
                if 'component_type' in component.keys():
                    if component['component_type'] == 'payment-reward':
                        d['paymentreward1'] = {k: v for k, v in component.items() if k != 'component_type'}
                    elif component['component_type'] == 'payment-reward-2':
                        d['paymentreward2'] = {k: v for k, v in component.items() if k != 'component_type'}
                    elif component['component_type'] == 'resources':
                        d['paymentreward1'] = {'payment': component['resources']}
                    elif component['component_type'] == 'text-box':
                        d['text'] = component['text']
                elif 'text' in component.keys():
                    d['text'] = component['text']
                elif 'resources' in component.keys():
                    d['paymentreward1'] = {'payment': component['resources']}
            del d['components']
            d['template'] = 'development-card'

            print(name, d)
            dev_component = DevCardComponent(
                title=name,
                icon=f"icons/{d['card_type']}/{d['card_sub_type']}.png" if d['card_type'] in ('policy', 'technology') else 'icons/institution.png',
                color2=colors[d['card_type']],
                **d)
            c = Card(name, **d)
            c.add(dev_component)

            fpath = os.path.join(output_dir,
                                 'dev',
                                 # d['card_type'],
                                 # d['card_sub_type'] if 'card_sub_type' in d.keys() else '',
                                 f'{name}[face,{d["count"]}].png')
            c.gen_card(fpath)

        else:
            print(name, d)
            c = Card(name, **d, background_color=colors[d['card_type']], component_spacer=60)
            defaults = d['defaults'] if 'defaults' in d.keys() else {}
            # defaults['align'] = 'center'
            defaults['fill_color'] = (255, 255, 255, 150)
            defaults['text_color'] = tuple(rgb//2 for rgb in colors[d['card_type']])
            defaults['outline_color'] = tuple(rgb//2 for rgb in colors[d['card_type']])
            defaults['default_font_size'] = 40
            c.add(TextBoxComponent(name, fill_color=(0, 0, 0, 0), text_color=(255, 255, 255), default_font_size=56, align='center'))
            if "components" in d.keys():
                for cc_specs in d['components']:
                    c.add(CardComponent.from_dict({**defaults, **cc_specs}))
            else:
                c.add(CardComponent.from_dict({**defaults, **d}))

            fpath = os.path.join(output_dir,
                                 d['card_type'],
                                 # d['card_sub_type'] if 'card_sub_type' in d.keys() else '',
                                 f'{name}[face,{d["count"]}].png')
            c.gen_card(fpath)

        # text_components = [comp for comp in d['components'] if 'text' in comp.keys() and not ('component_type' in comp.keys() and comp['component_type'] == 'payment-reward')]
        # resources_components = [comp for comp in d['components'] if 'component_type' in comp.keys() and comp['component_type'] == 'resources']
        # paymentreward_components = [comp for comp in d['components'] if 'component_type' in comp.keys() and comp['component_type'] in ('payment-reward', 'resources')]
        # paymentreward2_components = [comp for comp in d['components'] if 'component_type' in comp.keys() and comp['component_type'] in ('payment-reward-2')]

