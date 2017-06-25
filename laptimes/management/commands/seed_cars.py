import os
import json

from django.core.management.base import BaseCommand, CommandError

from laptimes.models import Car


class Command(BaseCommand):

    help = 'Seed the database with AC cars.'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        if not os.path.isdir(options['path']):
            raise ValueError('Given path is invalid.')
        for folder_name in sorted(os.listdir(options['path'])):
            parts = folder_name.split('_')
            if parts and parts[-1] in [upgrade[0] for upgrade in Car.upgrades]:
                upgrade = parts[-1]
            else:
                upgrade = None

            ui_car = os.path.join(options['path'], folder_name, 'ui',
                                  'ui_car.json')
            if not os.path.isfile(ui_car):
                # prefix with dlc_, maybe its not downloaded DLC car
                ui_car = ui_car.replace('ui_car', 'dlc_ui_car')
                if not os.path.isfile(ui_car):
                    print('No info found for: ' + folder_name)
                    continue
            # use utf-8-sig to ignore BOM
            with open(ui_car, encoding='utf-8-sig') as fob:
                data = fob.read().replace('\n', '').replace('\t', '')
            car_data = json.loads(data)
            model = get_model_from_name(car_data)
            car = Car(ac_name=folder_name, brand=car_data['brand'],
                      model=model, upgrade=upgrade)
            car.save()


def get_model_from_name(car_data):
    name = car_data['name'].lstrip(car_data['brand'])  # remove brand
    # remove possible upgrade from the end of name
    upgrades = [upgrade_tuple[1] for upgrade_tuple in Car.upgrades]
    upgrades.extend(['Stage 1', 'Stage 2', 'Stage 3'])
    upgrade_variations = []
    for upgrade in upgrades:
        # because of incosistent data include all typed versions
        upgrade_variations.extend(
            [upgrade, upgrade.lower(), upgrade.replace(' ', ''),
             upgrade.lower().replace(' ', '')]
        )
    for upgrade in upgrade_variations:
        if name.endswith(upgrade):
            name = name.replace(upgrade, '')
            break

    name = name.strip()
    return name
