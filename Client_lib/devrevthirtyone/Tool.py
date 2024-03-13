import json
from typing import List
from .Argument import Argument
from .ReturnType import ReturnType


class Tool:
    def __init__(self, name: str, description: str, arguments: List[Argument], return_type: ReturnType) -> None:
        """
        :param name: "The name of the tool.
        :param description: "The description of the tool.
        :param arguments: The arguments of the tool. Must be a list of Argument instances.
        :param return_type: The return type of the tool. Must be a ReturnType instance.
        """
        if not isinstance(name, str):
            raise TypeError(f"Tool name '{name}' is not a string.")
        name = name.strip()
        if not name:
            raise ValueError(f"Tool name '{name}' is empty.")
        self.name = name
        if not isinstance(description, str):
            raise TypeError(f"Tool description '{description}' is not a string.")
        self.description = description
        if not isinstance(arguments, list) or not all(isinstance(argument, Argument) for argument in arguments):
            raise TypeError(f"Tool arguments '{arguments}' is not a list of Argument instances.")

        arg_names = [argument.name for argument in arguments]
        if len(arg_names) != len(set(arg_names)):
            raise ValueError(f"Tool arguments '{arguments}' contains duplicate argument names.")

        self._arguments = arguments  # List of Argument instances

        if not isinstance(return_type, ReturnType):
            raise TypeError(f"Tool return type '{return_type}' is not a ReturnType instance.")
        self._return_type = return_type  # ReturnObject instance

    def add_argument(self, argument: Argument) -> "Tool":
        """
        :param argument: The argument to add. Must be an Argument instance.
        """
        if not isinstance(argument, Argument):
            raise TypeError(f"Argument '{argument}' is not an Argument instance.")
        arg_names = [arg.name for arg in self._arguments]
        if argument.name in arg_names:
            raise ValueError(f"Argument '{argument.name}' already exists in the tool.")
        self._arguments.append(argument)
        return self

    def remove_argument(self, argument_name: str) -> "Tool":
        """
        :param argument_name: The name of the argument to remove.
        """
        arg_names = [arg.name for arg in self._arguments]
        if argument_name not in arg_names:
            raise ValueError(f"Argument '{argument_name}' does not exist in the tool.")
        self._arguments = [arg for arg in self._arguments if arg.name != argument_name]
        return self

    def get_argument(self, argument_name: str) -> Argument:
        """
        :param argument_name: The name of the argument to get.
        """
        for arg in self._arguments:
            if arg.name == argument_name:
                return arg
        raise ValueError(f"Argument '{argument_name}' does not exist in the tool.")

    def get_arguments(self) -> List[Argument]:
        """
        :return: The arguments of the tool.
        """
        return self._arguments

    def get_return_type(self) -> ReturnType:
        """
        :return: The return type of the tool.
        """
        return self._return_type

    def __setattr__(self, key, value):
        if key == "name":
            if not isinstance(value, str):
                raise TypeError(f"Tool name '{value}' is not a string.")
            value = value.strip()
            if not value:
                raise ValueError(f"Tool name '{value}' is empty.")
        elif key == "description":
            if not isinstance(value, str):
                raise TypeError(f"Tool description '{value}' is not a string.")
        super().__setattr__(key, value)

    def __repr__(self):
        return json.dumps({
            "tool_name": self.name,
            "tool_description": self.description,
            "args": [json.loads(repr(argument)) for argument in self._arguments],
            "output": json.loads(repr(self._return_type))
        })

    def to_python(self) -> str:
        """
        Converts the tool to Python code.
        :return: The Python code for the tool.
        """
        code = f"def {self.name}("
        args = []
        for argument in self._arguments:
            arg_code = f"{argument.name}: {argument.type}"
            if not argument.required:
                arg_code += " = None"
            args.append(arg_code)
        code += ", ".join(args)

        code += ") -> " + self._return_type.type + ":\n"
        code += f"\t\"\"\"\n    {self.description}\n"
        code += "Args:\n"
        for argument in self._arguments:
            code += f"\t{argument.name}: {argument.description} e.g. {argument.example}\n"
        code += f"\t:Returns: {self._return_type.description} e.g. {self._return_type.example}\n"
        code += "\t\"\"\"\n"
        return code

    def to_json(self) -> dict:
        """
        Converts the tool to JSON.
        :return: The JSON for the tool.
        """
        return {
            "tool_name": self.name,
            "tool_description": self.description,
            "args": [argument.to_json() for argument in self._arguments],
            "output": self._return_type.to_json()
        }
