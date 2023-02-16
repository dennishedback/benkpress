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

"""NLP operations for the benkpress application and dependent programs."""

import spacy


class Lemmatizer:
    """A lemmatizing tokenizer for a specific language model. Not used by
    benkpress itself, but included for completeness."""

    def __init__(self, spacy_model: str):
        """Initialize a lemmatizer for a specific language model."""
        self._spacy_model = spacy_model
        self._nlp = spacy.load(spacy_model)

    def lemmatize(self, text: str) -> list[str]:
        """Lemmatize a string."""
        return [x.lemma_ for x in self._nlp(text)]


class Sentencizer:
    """A sentence splitting tokenizer for a specific language model. Used
    by benkpress and dependent programs to split page text into sentence targets."""

    def __init__(self, spacy_model: str):
        """Initialize a sentencizer for a specific language model."""
        self._spacy_model = spacy_model
        self._nlp = spacy.load(spacy_model)

    def sentencize(self, text: str) -> list[str]:
        """Split a string into sentences."""
        return [x.text for x in self._nlp(text).sents]
