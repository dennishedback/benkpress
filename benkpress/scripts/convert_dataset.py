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

"""
Converts the old benkpress dataset format to new format.

Usage: benkpress-convert-dataset <src> <dst>

Options:
    -h --help       Show this help screen.
    -v --version    Show version information.
"""

import sys
from pathlib import Path

import pandas as pd
from docopt import docopt

from benkpress.api.hash import filename_digest


def main():
    """The main entry point of the script."""
    args = docopt(__doc__)
    source_dataset_path = Path(args["<src>"])
    destination_dataset_path = Path(args["<dst>"])
    dataset = pd.read_csv(source_dataset_path, index_col=0)
    dataset["file"] = dataset["file"].apply(lambda x: filename_digest(Path(x)))
    dataset.to_csv(destination_dataset_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
