#! /usr/bin/env python3

from sklearn.base import TransformerMixin
from abc import abstractmethod

class Intermediary(TransformerMixin):
    """Used to communicate with the Supervisor GUI from within sklearn compatible
       pipelines."""

    def fit(self, X, y=None):
        """Method for compatibility with skelarn transformers. Its only job is
        to return itself.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data used to compute the per-feature minimum and maximum
            used for later scaling along the features axis.
        y : None
            Ignored.
        Returns
        -------
        self : object
            Pseudo-fitted pseudo transformer.
        """
        return self

    def transform(self, X):
        """Method for compatibility with sklearn transformers. Its only job is
        to pass through X.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data that should be passed through.
        Returns
        -------
        X_tr : {ndarray, sparse matrix} of shape (n_samples, n_features)
            Untransformed array.
        """
        self.callback(X, self._caller)
        return X 

    def _inject_caller(self, supervisor):
        """Used by the caller to inject itself."""
        self._supervisor = supervisor

    @abstractmethod
    def callback(self, X, supervisor):
        """Perform some operation on the caller due to characteristics of X.
        The method is intended to be overridden by concrete subclasses.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data that should be scaled.
        caller: The pdfsupervisor Caller class calling transform on the
                pipeline this Intermediary is part of.
        """
        pass
