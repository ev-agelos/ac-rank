import os
import json

from django.core.management.base import BaseCommand, CommandError

from laptimes.models import Track


class Command(BaseCommand):

    help = 'Seed the database with AC tracks.'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        if not os.path.isdir(options['path']):
            raise ValueError('Given path is invalid.')
        for track_folder in sorted(os.listdir(options['path'])):
            ui_folder = os.path.join(options['path'], track_folder, 'ui')
            for folder_or_file in sorted(os.listdir(ui_folder)):
                ui_track = os.path.join(ui_folder, folder_or_file)
                if folder_or_file in ('ui_track.json', 'dlc_ui_track.json'):
                    # then no layouts exist sto after reading it continue
                    layout_folder = None
                elif os.path.isdir(ui_track):  # layout folder
                    layout_folder = folder_or_file
                    ui_track = os.path.join(ui_track, 'ui_track.json')
                    if not os.path.isfile(ui_track):
                        # then it should be a non downloaded yet dlc track
                        ui_track = ui_track.replace('ui_track', 'dlc_ui_track')
                        if not os.path.isfile(ui_track):
                            print('No info found for: ' + folder_or_file)
                            continue
                else:
                    # unrelated file
                    continue

                try:  # use utf-8-sig to ignore BOM
                    with open(ui_track, encoding='utf-8-sig') as fob:
                        data = fob.read()
                except UnicodeDecodeError:  # try with latin-1
                    with open(ui_track, encoding='latin-1') as fob:
                        data = fob.read()
                except UnicodeDecodeError:
                    print('Can read file: ', ui_track)
                    continue

                data = data.replace('\n', '').replace('\t', '')
                track_info = json.loads(data)
                # NOTE: using 3 secors as default because does not seem to be
                # included somewhere that information
                track = Track(ac_name=track_folder, name=track_info['name'],
                              layout=layout_folder, sectors=3)
                track.save()
