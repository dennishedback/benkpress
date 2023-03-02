#! /usr/bin/env python3

# benkpress
# Copyright (C) 2022-2023 Dennis Hedback
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

"""Resources for the benkpress application."""

from pathlib import Path

"""The directory containing the resources."""
_THIS_FILE_DIR = Path(__file__).parent.resolve()

QUICK_START_GUIDE_PATH = _THIS_FILE_DIR / "quickstart.pdf"
