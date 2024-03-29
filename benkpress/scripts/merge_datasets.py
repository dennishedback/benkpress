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

"""
Usage: benkpress-merge-datasets <src1> <src2> <dst>

Options:
    -h --help       Show this help screen.
    -v --version    Show version information.
"""


import sys

import pandas as pd
from docopt import docopt


def main():
    args = docopt(__doc__)
    df1 = pd.read_csv(args["<src1>"], index_col=0)
    df2 = pd.read_csv(args["<src2>"], index_col=0)
    df1_unique_file_ids = set(df1["file"].unique())
    df2_unique_file_ids = set(df2["file"].unique())
    deny_list = df1_unique_file_ids.intersection(df2_unique_file_ids)
    df2 = df2[~df2["file"].isin(deny_list)]
    df = pd.concat([df1, df2])
    df.to_csv(args["<dst>"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
