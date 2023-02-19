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

from importlib.metadata import EntryPoint, entry_points
from typing import Any, Dict, List

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline


class PassthroughPageClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self):
        super().__init__()

    def fit(self, X, y):
        return self

    def predict(self, X):
        return [1] * len(X)

    def predict_proba(self, X):
        return [1.0] * len(X)


def DummyPipeline():
    """Returns a dummy classifier pipeline to use as a baseline."""
    return Pipeline(
        [
            ("Vectorizer", CountVectorizer()),
            ("Classifier", DummyClassifier()),
        ]
    )


class PluginLoader:
    # TODO: Refactor into functions
    _page_filter_entry_points: Dict[str, EntryPoint]
    _pipeline_entry_points: Dict[str, EntryPoint]

    def __init__(self):
        """Initalize PluginLoader"""
        PAGE_FILTERS_KEY = "benkpress_plugins.page_filters"
        PIPELINES_KEY = "benkpress_plugins.pipelines"
        self._page_filter_entry_points = dict()
        self._populate_dict(PAGE_FILTERS_KEY, self._page_filter_entry_points)
        self._pipeline_entry_points = dict()
        self._populate_dict(PIPELINES_KEY, self._pipeline_entry_points)

    def _populate_dict(self, key: str, dict_: Dict[str, EntryPoint]) -> None:
        if key in entry_points():
            for entry_point in entry_points()[key]:
                dict_[entry_point.name] = entry_point

    def get_available_page_filters(self) -> List[str]:
        """
        Get the names of all installed page_filters.

        Returns
        -------
        List containing the names of all available page_filter plugins.
        """
        return [name for name in self._page_filter_entry_points]

    def get_available_pipelines(self) -> List[str]:
        """
        Get the names of all installed pipelines.

        Returns
        -------
        List containing the names of all available pipeline plugins.
        """
        return [name for name in self._pipeline_entry_points]

    def load_page_filter(self, name: str) -> Pipeline:
        """
        Get page_filter entry point.

        Parameters
        ----------
        name : The name of the installed page_filter.

        Returns
        -------
        EntryPoint used to load the page_filter plugin.
        """
        return self._page_filter_entry_points[name].load()()

    def load_pipeline(self, name: str) -> Pipeline:
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
