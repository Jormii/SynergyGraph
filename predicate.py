from __future__ import annotations

from typing import List

from subject import Subject


class IPredicate:

    def head(self) -> Subject:
        raise NotImplementedError(type(self))

    def tails(self) -> List[Subject]:
        raise NotImplementedError(type(self))

    def unwrap(self) -> List[IPredicate]:
        raise NotImplementedError(type(self))
