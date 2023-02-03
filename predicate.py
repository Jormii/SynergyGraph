from __future__ import annotations

from typing import List

from action import Action
from subject import Subject


class IPredicate:

    def head(self) -> Subject:
        raise NotImplementedError(type(self))

    def action(self) -> Action:
        raise NotImplementedError(type(self))

    def unwrap(self) -> List[IPredicate]:
        raise NotImplementedError(type(self))
