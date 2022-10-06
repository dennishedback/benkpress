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

from importlib.metadata import EntryPoint, entry_points
from typing import Any, Dict, List

from benkpress_plugins.preprocessors import Preprocessor


class PluginLoader:
    _preprocessor_entry_points: Dict[str, EntryPoint]
    _pipeline_entry_points: Dict[str, EntryPoint]

    def __init__(self):
        """Initalize PluginLoader"""
        PREPROCESSORS_KEY = "benkpress_plugins.preprocessors"
        PIPELINES_KEY = "benkpress_plugins.pipelines"
        self._preprocessor_entry_points = dict()
        self._populate_dict(PREPROCESSORS_KEY, self._preprocessor_entry_points)
        self._pipeline_entry_points = dict()
        self._populate_dict(PIPELINES_KEY, self._pipeline_entry_points)

    def _populate_dict(self, key: str, dict_: Dict[str, EntryPoint]) -> None:
        if key in entry_points():
            for entry_point in entry_points()[key]:
                dict_[entry_point.name] = entry_point

    def get_available_preprocessors(self) -> List[str]:
        """
        Get the names of all installed preprocessors.

        Returns
        -------
        List containing the names of all available preprocessor plugins.
        """
        return [name for name in self._preprocessor_entry_points]

    def get_available_pipelines(self) -> List[str]:
        """
        Get the names of all installed pipelines.

        Returns
        -------
        List containing the names of all available pipeline plugins.
        """
        return [name for name in self._pipeline_entry_points]

    def load_preprocessor(self, name: str) -> Preprocessor:
        """
        Get preprocessor entry point.

        Parameters
        ----------
        name : The name of the installed preprocessor.

        Returns
        -------
        EntryPoint used to load the preprocessor plugin.
        """
        return self._preprocessor_entry_points[name].load()()

    def load_pipeline(self, name: str) -> Any:
        """
        Get pipeline entry point.

        Parameters
        ----------
        name : The name of the installed pipeline.

        Returns
        -------
        EntryPoint used to load the pipeline plugin.
        """
        return self._pipeline_entry_points[name].load()()
