import os
import json

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from laptimes.models import Track


class Command(BaseCommand):

    help = 'Seed the database with AC tracks.'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
        parser.add_argument(
            '--save',
            action='store_true',
            help='Save tracks in the database, defaults to False.'
        )

    def handle(self, *args, **options):
        if not os.path.isdir(options['path']):
            raise ValueError('Given path is invalid.')

        errors, saved_tracks = [], 0
        for track_folder in sorted(os.listdir(options['path'])):
            try:
                filepaths = find_ui_filepaths(options['path'], track_folder)
            except ValueError as err:
                errors.append(str(err))  # Show errors last
                continue

            for filepath in filepaths:
                try:
                    data = load_track_ui(filepath)
                except ValueError as err:
                    print(err)
                    continue

                track_name = data['name']
                layout = ''
                if len(filepaths) > 1:
                    layout = os.path.basename(os.path.dirname(filepath))
                # NOTE: using 3 secors as default because does not seem to be
                # included somewhere that information
                track = Track(ac_name=track_folder, name=track_name,
                              layout=layout, sectors=3)
                if options['save'] is True:
                    try:
                        track.save()
                    except IntegrityError:
                        print("{} already exists".format(track))
                        continue
                saved_tracks += 1

        if options['save'] is True:
            msg = "\n{} tracks inserted"
        else:
            msg = "\n{} tracks would have been inserted"
        print(msg.format(saved_tracks))

        for error in errors:
            print('\nERROR: ', error)


def find_ui_filepaths(tracks_path, track):
    """
    Return the filepath of track's ui file which holds its information.

    Handle the case of the file having the prefix "dlc_" which means it is not
    downloaded yet.
    """
    ui_dir = os.path.join(tracks_path, track, 'ui')
    ui_file = os.path.join(ui_dir, 'ui_track.json')
    if os.path.isfile(ui_file):
        return [ui_file]

    ui_file = os.path.join(ui_dir, 'dlc_ui_track.json')
    if os.path.isfile(ui_file):
        return [ui_file]

    files = []
    for layout in os.listdir(ui_dir):
        layout_dir = os.path.join(ui_dir, layout)
        if os.path.isdir(layout_dir):
            ui_file = os.path.join(layout_dir, 'ui_track.json')
            if os.path.isfile(ui_file):
                files.append(ui_file)
                continue
            ui_file = os.path.join(layout_dir, 'dlc_ui_track.json')
            if os.path.isfile(ui_file):
                files.append(ui_file)

    if not files:
        raise ValueError('UI file not found for {}'.format(track))

    return files


def load_track_ui(path, encoding='utf-8-sig'):
    """Try reading with 2 encodings and return loaded data, otherwise raise."""
    try:
        with open(path, encoding=encoding) as fob:
            data = fob.read()
    except UnicodeDecodeError:
        if encoding == 'latin-1':
            raise ValueError("Can't read file")
        return load_track_ui(path, encoding='latin-1')

    data = data.replace('\n', '').replace('\t', '')
    return json.loads(data)
