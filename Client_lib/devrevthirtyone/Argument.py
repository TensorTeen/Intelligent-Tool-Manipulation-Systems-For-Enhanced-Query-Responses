from typing import Any
import json


class Argument:
    def __init__(self, name: str, description: str, arg_type: str, example: Any, required: bool = True) -> None:
        """
        :param name: The name of the argument.
        :param description: The description of the argument.
        :param arg_type: The type of the argument. Must be one of the following:
                        'str', 'int', 'float', 'bool', 'List[str]', 'List[int]', 'List[float]', 'List[bool]'.
        :param example: The example of the argument. Must be the same type as the type.
        :param required: Whether the argument is required or not. Defaults to True.
        """
        # check the argument only contains small case letters, numbers and underscores,
        # and starts with a letter

        if not isinstance(name, str):
            raise TypeError(f"Argument name '{name}' is not a string.")
        name = name.strip()
        if not name:
            raise ValueError(f"Argument name '{name}' is empty.")

        self.name = name

        # check the description is a string
        if not isinstance(description, str):
            raise TypeError(f"Argument description '{description}' is not a string.")
        self.description = description

        # check the type is str or int or float or bool or list of str or list of int or list of float or list of bool
        if arg_type not in ["str", "int", "float", "bool", "List[str]", "List[int]", "List[float]", "List[bool]"]:
            raise ValueError(f"Argument type '{arg_type}' is not a valid type. It must be one of the following: "
                             f"'str', 'int', 'float', 'bool', 'List[str]', 'List[int]', 'List[float]', 'List[bool]'.")
        self.type = arg_type

        # check if the example is same type as the type
        if arg_type == "str":
            if not isinstance(example, str):
                raise TypeError(f"Argument example '{example}' is not a string.")
        elif arg_type == "int":
            if not isinstance(example, int):
                raise TypeError(f"Argument example '{example}' is not an integer.")
        elif arg_type == "float":
            if not isinstance(example, float):
                raise TypeError(f"Argument example '{example}' is not a float.")
        elif arg_type == "bool":
            if not isinstance(example, bool):
                raise TypeError(f"Argument example '{example}' is not a boolean.")
        elif arg_type == "List[str]":
            if not isinstance(example, list) or not all(isinstance(item, str) for item in example):
                raise TypeError(f"Argument example '{example}' is not a list of strings.")
        elif arg_type == "List[int]":
            if not isinstance(example, list) or not all(isinstance(item, int) for item in example):
                raise TypeError(f"Argument example '{example}' is not a list of integers.")
        elif arg_type == "List[float]":
            if not isinstance(example, list) or not all(isinstance(item, float) for item in example):
                raise TypeError(f"Argument example '{example}' is not a list of floats.")
        elif arg_type == "List[bool]":
            if not isinstance(example, list) or not all(isinstance(item, bool) for item in example):
                raise TypeError(f"Argument example '{example}' is not a list of booleans.")

        self.example = example

        # check if the required is a boolean
        if not isinstance(required, bool):
            raise TypeError(f"Argument required '{required}' is not a boolean.")
        self.required = required

    def __setattr__(self, key, value):
        if key == "name":
            if not isinstance(value, str):
                raise TypeError(f"Argument name '{value}' is not a string.")
            value = value.strip()
            if not value:
                raise ValueError(f"Argument name '{value}' is empty.")
        elif key == "description":
            if not isinstance(value, str):
                raise TypeError(f"Argument description '{value}' is not a string.")
        elif key == "type":
            if value not in ["str", "int", "float", "bool", "List[str]", "List[int]", "List[float]", "List[bool]"]:
                raise ValueError(f"Argument type '{value}' is not a valid type. It must be one of the following: "
                                 f"'str', 'int', 'float', 'bool', 'List[str]', 'List[int]', 'List[float]', "
                                 f"'List[bool]'.")
        elif key == "example":
            if self.type == "str":
                if not isinstance(value, str):
                    raise TypeError(f"Argument example '{value}' is not a string.")
            elif self.type == "int":
                if not isinstance(value, int):
                    raise TypeError(f"Argument example '{value}' is not an integer.")
            elif self.type == "float":
                if not isinstance(value, float):
                    raise TypeError(f"Argument example '{value}' is not a float.")
            elif self.type == "bool":
                if not isinstance(value, bool):
                    raise TypeError(f"Argument example '{value}' is not a boolean.")
            elif self.type == "List[str]":
                if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                    raise TypeError(f"Argument example '{value}' is not a list of strings.")
            elif self.type == "List[int]":
                if not isinstance(value, list) or not all(isinstance(item, int) for item in value):
                    raise TypeError(f"Argument example '{value}' is not a list of integers.")
            elif self.type == "List[float]":
                if not isinstance(value, list) or not all(isinstance(item, float) for item in value):
                    raise TypeError(f"Argument example '{value}' is not a list of floats.")
            elif self.type == "List[bool]":
                if not isinstance(value, list) or not all(isinstance(item, bool) for item in value):
                    raise TypeError(f"Argument example '{value}' is not a list of booleans.")
        elif key == "required":
            if not isinstance(value, bool):
                raise TypeError(f"Argument required '{value}' is not a boolean.")
        super().__setattr__(key, value)

    def __repr__(self):
        is_array = False
        output_type = self.type
        if "List" in self.type:
            is_array = True
            output_type = self.type[5:-1]
        return json.dumps({
            "arg_type": output_type,
            "arg_description": self.description,
            "example": self.example,
            "is_array": is_array,
            "is_required": self.required,
            "arg_name": self.name
        })

    def to_json(self):
        """
        Converts the argument to JSON format.
        :return: The JSON format of the argument.
        """
        arg_type = self.type
        if "List" in self.type:
            arg_type = self.type[5:-1]

        return {
            "argument_name": self.name,
            "arg_description": self.description,
            "argument_type": arg_type,
            "example": self.example,
            "is_array": "List" in self.type,
            "is_required": self.required
        }
