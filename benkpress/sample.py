#! /usr/bin/env python3

# benkpress
# Copyright (C) 2022 Dennis Hedback
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

""""""

from pathlib import Path
from shutil import copy

import pandas as pd
from docopt import docopt


def filter_sample(source_folder: Path, target_folder: Path, dataset_path: Path):
    """
    Copy files from one folder to another, but only if they aren't part of the given
    dataset. Only copies the first level of files, not recursively.

    Parameters
    ----------
    source_folder : The folder to copy files from.
    target_folder : The folder to copy files to. Must exist.
    dataset_path : The dataset to use as blacklist.
    """
    source_filenames = {f.name for f in source_folder.iterdir() if f.is_file()}
    df = pd.read_csv(dataset_path, index_col=False)
    deny_list = {Path(f).name for f in set(df["file"])}
    valid_sources = [source_folder / f for f in source_filenames.difference(deny_list)]
    for source_filepath in valid_sources:
        copy(source_filepath, target_folder)


def _filter_sample_main():
    """
    Usage: benkpress-filter-sample <src> <dst> <dataset>

    Options:
        -h --help       Show this help screen.
        -v --version    Show version information.
    """
    args = docopt(_filter_sample_main.__doc__)
    source_folder = Path(args["<src>"])
    target_folder = Path(args["<dst>"])
    dataset_path = Path(args["<dataset>"])
    filter_sample(source_folder, target_folder, dataset_path)
    return 0
