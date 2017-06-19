"""Usage: plots_by_date.py INPUT_PATH OUTPUT_PATH [--dry-run]"""

import os
import glob
import sys
import platform
import itertools
import re

from docopt import docopt
from datetime import datetime


PLOT_FILENAME_PHRASES = ['node', 'grid', 'mesh', 'topology', 'rastrigin']
PLOT_FILENAME_REGEX = re.compile('\A[\w\.]+\.png\Z')


def plots_by_date(input_path, output_path, dry_run=False):
    paths = fetch_paths(input_path)
    paths_by_date = itertools.groupby(paths, creation_date)
    for date, source_paths in paths_by_date:
        if dry_run:
            print date
        target_dir = create_dir(output_path, str(date))
        for source_path in source_paths:
            filename = os.path.basename(source_path)
            target_path = os.path.join(target_dir, filename)
            if dry_run:
                print source_path, ' -> ', target_path
            else:
                os.rename(source_path, target_path)


def fetch_paths(root):
    paths = []
    for root, _dirs, filenames in os.walk(root):
        for filename in filenames:
            if valid_filename(filename):
                paths.append(os.path.join(root, filename))
    return paths


def valid_filename(filename):
    if any(phrase in filename for phrase in PLOT_FILENAME_PHRASES):
        return True
    if PLOT_FILENAME_REGEX.match(filename):
        return True
    return False


def creation_date(path):
    return datetime.fromtimestamp(creation_time(path)).date()


def creation_time(path):
    stat = os.stat(path)
    try:
        return stat.st_birthtime
    except AttributeError:
        return stat.st_mtime


def create_dir(root, name):
    dir_path = os.path.join(root, name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path


if __name__ == '__main__':
    args = docopt(__doc__)

    input_path = args['INPUT_PATH']
    output_path = args['OUTPUT_PATH']
    dry_run = args['--dry-run']

    plots_by_date(input_path, output_path, dry_run=dry_run)
