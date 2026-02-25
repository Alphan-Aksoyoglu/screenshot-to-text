from __future__ import annotations


from screenshot_to_text.models.dict_root_model import DictRootModel
from typing import List
from pydantic import BaseModel


class Tool(BaseModel):
    name: str
    cmd: List[str]


class Tools(DictRootModel[Tool]):
    @property
    def tools(self):
        return self.keys

    @property
    def tool_infos(self):
        return self.values

    def empty_child(self) -> Tool:
        return Tool(name="", cmd=[])

    def available_tools(self, filter_func) -> List[Tool]:
        return [tool for tool in self.tool_infos if filter_func(tool.name)]

    def alternative_tools(self, filter_func) -> List[Tool]:
        available_tools = self.available_tools(filter_func)
        return [tool for tool in self.tool_infos if tool not in available_tools]


class ToolTypes(DictRootModel[Tools]):
    def empty_child(self) -> Tools:
        return Tools({})

    @property
    def tool_types(self):
        return self.keys


class SupportedPlatforms(DictRootModel[ToolTypes]):
    def empty_child(self) -> ToolTypes:
        return ToolTypes({})

    @property
    def supported_platforms(self):
        return self.keys
