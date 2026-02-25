from __future__ import annotations

from typing import Dict, TypeVar, Generic
from pydantic import RootModel

T = TypeVar("T")


class DictRootModel(RootModel[Dict[str, T]], Generic[T]):
    def as_dict(self):
        return self.root

    def __getitem__(self, key: str) -> T:
        return self.root[key]

    def __getattr__(self, key: str):
        return self.root[key]

    def empty_child(self) -> T:
        raise NotImplementedError

    def get(self, key: str):
        return self.root.get(key, self.empty_child())

    @property
    def keys(self):
        return list(self.root.keys())

    @property
    def values(self):
        return list(self.root.values())
