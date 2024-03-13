from typing import Any
import json


class ReturnType:
    def __init__(self, return_type: str, description: str, example: Any) -> None:
        """
        :param return_type: The type of the return. Must be one of the following:
                            'str', 'int', 'float', 'bool', 'dict', 'List[str]', 'List[int]', 'List[float]', 'List[bool]'.
        :param description: The description of the return.
        :param example: The example of the return. Must be the same type as the return type.
        """
        if return_type not in ["str", "int", "float", "bool", "dict", "List[str]", "List[int]", "List[float]",
                               "List[bool]"]:
            raise ValueError(f"Return type '{return_type}' is not a valid type. It must be one of the following: "
                             f"'str', 'int', 'float', 'bool', 'dict', 'List[str]', 'List[int]', 'List[float]', "
                             f"'List[bool]'.")

        self.type = return_type

        if not isinstance(description, str):
            raise TypeError(f"Return description '{description}' is not a string.")
        self.description = description

        if return_type == "str":
            if not isinstance(example, str):
                raise TypeError(f"Return example '{example}' is not a string.")
        elif return_type == "int":
            if not isinstance(example, int):
                raise TypeError(f"Return example '{example}' is not an integer.")
        elif return_type == "float":
            if not isinstance(example, float):
                raise TypeError(f"Return example '{example}' is not a float.")
        elif return_type == "bool":
            if not isinstance(example, bool):
                raise TypeError(f"Return example '{example}' is not a boolean.")
        elif return_type == "dict":
            if not isinstance(example, dict):
                raise TypeError(f"Return example '{example}' is not a dictionary.")
        elif return_type == "List[str]":
            if not isinstance(example, list) or not all(isinstance(item, str) for item in example):
                raise TypeError(f"Return example '{example}' is not a list of strings.")
        elif return_type == "List[int]":
            if not isinstance(example, list) or not all(isinstance(item, int) for item in example):
                raise TypeError(f"Return example '{example}' is not a list of integers.")
        elif return_type == "List[float]":
            if not isinstance(example, list) or not all(isinstance(item, float) for item in example):
                raise TypeError(f"Return example '{example}' is not a list of floats.")
        elif return_type == "List[bool]":
            if not isinstance(example, list) or not all(isinstance(item, bool) for item in example):
                raise TypeError(f"Return example '{example}' is not a list of booleans.")

        self.example = example

    def __setattr__(self, key, value):
        if key == "type":
            if value not in ["str", "int", "float", "bool", "dict", "List[str]", "List[int]", "List[float]",
                             "List[bool]"]:
                raise ValueError(f"Return type '{value}' is not a valid type. It must be one of the following: "
                                 f"'str', 'int', 'float', 'bool', 'dict', 'List[str]', 'List[int]', 'List[float]', "
                                 f"'List[bool]'.")
        elif key == "description":
            if not isinstance(value, str):
                raise TypeError(f"Return description '{value}' is not a string.")
        elif key == "example":
            if self.type == "str":
                if not isinstance(value, str):
                    raise TypeError(f"Return example '{value}' is not a string.")
            elif self.type == "int":
                if not isinstance(value, int):
                    raise TypeError(f"Return example '{value}' is not an integer.")
            elif self.type == "float":
                if not isinstance(value, float):
                    raise TypeError(f"Return example '{value}' is not a float.")
            elif self.type == "bool":
                if not isinstance(value, bool):
                    raise TypeError(f"Return example '{value}' is not a boolean.")
            elif self.type == "dict":
                if not isinstance(value, dict):
                    raise TypeError(f"Return example '{value}' is not a dictionary.")
            elif self.type == "List[str]":
                if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                    raise TypeError(f"Return example '{value}' is not a list of strings.")
            elif self.type == "List[int]":
                if not isinstance(value, list) or not all(isinstance(item, int) for item in value):
                    raise TypeError(f"Return example '{value}' is not a list of integers.")
            elif self.type == "List[float]":
                if not isinstance(value, list) or not all(isinstance(item, float) for item in value):
                    raise TypeError(f"Return example '{value}' is not a list of floats.")
            elif self.type == "List[bool]":
                if not isinstance(value, list) or not all(isinstance(item, bool) for item in value):
                    raise TypeError(f"Return example '{value}' is not a list of booleans.")
        super().__setattr__(key, value)

    def __repr__(self):
        is_array = False
        output_type = self.type
        if "List" in self.type:
            is_array = True
            output_type = self.type[5:-1]
        return json.dumps({
            "arg_type": output_type,
            "description": self.description,
            "example": self.example,
            "is_array": is_array
        })

    def to_json(self):
        arg_type = self.type
        if "List" in self.type:
            arg_type = self.type[5:-1]

        return json.dumps({
            "argument_type": self.type,
            "example": self.example,
            "is_array": "List" in self.type,
            "description": self.description,
            "arg_type": arg_type
        })