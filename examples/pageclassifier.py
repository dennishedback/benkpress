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

import joblib

from benkpress_api import PassthroughPagePreprocessor, PDFClassifierContext
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

RANDOM_STATE = 999

context = PDFClassifierContext(PassthroughPagePreprocessor(), Pipeline([
    ("Vectorizer", TfidfVectorizer(use_idf=True, max_features=None, stop_words=None)),
    ("Classifier", XGBClassifier(n_estimators=1000, random_state=RANDOM_STATE))
]))

joblib.dump(context, "pagecontext.joblib")
