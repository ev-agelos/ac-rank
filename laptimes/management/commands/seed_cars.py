import os
import json

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from laptimes.models import Car


class Command(BaseCommand):

    help = 'Seed the database with AC cars.'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
        parser.add_argument(
            '--save',
            action='store_true',
            help='Save cars in the database, defaults to False.'
        )

    def handle(self, *args, **options):
        if not os.path.isdir(options['path']):
            raise ValueError('Given path is invalid.')

        errors, saved_cars = [], 0
        car_folders = os.listdir(options['path'])
        for car_folder in sorted(car_folders):
            try:
                car_data = load_car_ui(options['path'], car_folder)
            except ValueError as err:
                errors.append(str(err))  # Show errors last
                continue

            model = get_model_from_name(car_data)
            upgrade = get_upgrade_from_folder_name(car_folder)
            car = Car(ac_name=car_folder, brand=car_data['brand'],
                      model=model, upgrade=upgrade)
            if options['save'] is True:
                try:
                    car.save()
                except IntegrityError:
                    print("{} already exists".format(car))
                    continue
            saved_cars += 1

        if options['save'] is True:
            msg = "\n{} cars inserted"
        else:
            msg = "\n{} cars would have been inserted"
        print(msg.format(saved_cars))

        for error in errors:
            print('\nERROR: ', error)


def load_car_ui(cars_path, car):
    """
    Read filepath's contents and return them as json.

    Use utf-8-sig encoding when reading to ignore BOM. Also ignore \n and \t.
    """
    filepath = find_ui_filepath(cars_path, car)
    with open(filepath, encoding='utf-8-sig') as fob:
        data = fob.read().replace('\n', '').replace('\t', '')
    return json.loads(data)


def find_ui_filepath(cars_path, car):
    """
    Return the filepath of car's ui file which holds its information.

    Handle the case of the file having the prefix "dlc_" which means it is not
    downloaded yet.
    """
    ui_dir = os.path.join(cars_path, car, 'ui')
    ui_file = os.path.join(ui_dir, 'ui_car.json')
    if os.path.isfile(ui_file):
        return ui_file

    ui_file = os.path.join(ui_dir, 'dlc_ui_car.json')
    if os.path.isfile(ui_file):
        return ui_file

    raise ValueError('UI file not found for {}'.format(car))


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


def get_upgrade_from_folder_name(car_folder):
    """Return the upgrade found in the given folder name."""
    *_, upgrade = car_folder.rpartition('_')
    if any(upgrade == upgrade_pair[0] for upgrade_pair in Car.upgrades):
        return upgrade

    return None
