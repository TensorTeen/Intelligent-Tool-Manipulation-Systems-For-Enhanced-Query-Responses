import json
from typing import List
from .Tool import Tool
from .Argument import Argument
from .ReturnType import ReturnType
from .EfficientPipeline import solve_efficient


class Manager:
    def __init__(self, tools: List[Tool] = None) -> None:
        """
        :param tools: The tools of the manager. Must be a list of Tool instances.
        """
        if not tools:
            tools = []
        if not isinstance(tools, list) or not all(isinstance(tool, Tool) for tool in tools):
            raise TypeError(f"Manager tools '{tools}' is not a list of Tool instances.")

        # there should be no duplicate tool names
        tool_names = [tool.name for tool in tools]
        if len(tool_names) != len(set(tool_names)):
            raise ValueError(f"Manager tools '{tools}' contains duplicate tool names.")
        self._tools = tools

    def get_tools(self) -> List[Tool]:
        """
        :return: The tools of the manager.
        """
        return self._tools

    def add_tool(self, tool: Tool) -> "Manager":
        """
        Adds a tool to the current context.
        :param tool: The tool to add. Must be a Tool instance.
        :return: The current Manager context.
        """
        if not isinstance(tool, Tool):
            raise TypeError(f"Tool '{tool}' is not a Tool instance.")
        tool_names = [t.name for t in self._tools]
        if tool.name in tool_names:
            raise ValueError(f"Tool '{tool.name}' already exists in the manager.")
        self._tools.append(tool)
        return self

    def remove_tool(self, tool_name: str) -> "Manager":
        """
        Removes a tool from the current context.
        :param tool_name: The name of the tool to remove.
        :return: The current Manager context.
        """
        tool_names = [tool.name for tool in self._tools]
        if tool_name not in tool_names:
            raise ValueError(f"Tool '{tool_name}' does not exist in the manager.")
        self._tools = [tool for tool in self._tools if tool.name != tool_name]
        return self

    def get_tool(self, tool_name: str) -> Tool:
        """
        Gets a tool by it name from the current context.
        :param tool_name: The name of the tool to get.
        :return: The tool.
        """
        for tool in self._tools:
            if tool.name == tool_name:
                return tool
        raise ValueError(f"Tool '{tool_name}' does not exist in the manager.")

    def run_query(self, query: str) -> dict:
        """
        Solves a query, using the tools in the current context.
        :param query: The query to run.
        :return: The solution to the query.
        """
        if not isinstance(query, str):
            raise TypeError(f"Query '{query}' is not a string.")
        query = query.strip()
        if not query:
            raise ValueError(f"Query '{query}' is empty.")
        # TODO: implement this
        json_schema = self.to_json()
        return solve_efficient(json_schema, query)

    def __repr__(self) -> str:
        return json.dumps([json.loads(repr(tool)) for tool in self._tools])

    def to_python(self) -> str:
        """
        Converts the current tools to Python code.
        :return: The Python code to create the manager.
        """
        return "\n".join([tool.to_python() for tool in self._tools])

    @staticmethod
    def from_json(file_location: str) -> "Manager":
        """
        :param file_location: The location of the JSON file to read.
        :returns: A Manager instance.

        This takes a json format as input and creates a Manager with the tools in the json file.
        """
        with open(file_location, "r") as file:
            data = json.load(file)
        tools = []
        for t in data:
            args = []
            for arg in t["args"]:
                if 'is_required' not in arg:
                    arg['is_required'] = True
                arg_type = arg["arg_type"]
                if arg_type.startswith("str"):
                    arg_type = "str"
                elif arg_type.startswith("int"):
                    arg_type = "int"
                elif arg_type.startswith("bool"):
                    arg_type = "bool"
                if arg['is_array']:
                    arg_type = f"List[{arg_type}]"
                args.append(Argument(arg["arg_name"], arg["arg_description"], arg_type, arg["example"],
                                     arg["is_required"]))
            output_type = t["output"]["arg_type"]
            if output_type.startswith("str"):
                output_type = "str"
            elif output_type.startswith("int"):
                output_type = "int"
            elif output_type.startswith("bool"):
                output_type = "bool"
            if t["output"]["is_array"]:
                output_type = f"List[{output_type}]"
            return_type = ReturnType(output_type, t["output"]["description"], t["output"]["example"])
            tools.append(Tool(t["tool_name"], t["tool_description"], args, return_type))
        return Manager(tools)

    def to_json(self) -> List[dict]:
        return [tool.to_json() for tool in self._tools]
