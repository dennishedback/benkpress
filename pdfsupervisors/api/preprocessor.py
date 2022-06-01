#! /usr/bin/env python3

from abc import abstractmethod
from typing import Any, List


class PagePreprocessor:
    def _inject_caller(self, supervisor):
        """Used by the caller to inject itself."""
        self._supervisor = supervisor

    @abstractmethod
    def transform(self, pagetext: str) -> List[str]:
        pass

    def accepts_page(self, pagetext: str) -> bool:
        return True

    def begin_pdf(self) -> None:
        pass

    def about_to_end_pdf(self) -> None:
        pass

    def end_pdf(self) -> None:
        pass
