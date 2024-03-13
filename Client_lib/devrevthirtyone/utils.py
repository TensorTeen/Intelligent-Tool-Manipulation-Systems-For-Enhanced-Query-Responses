import json

from .Manager import Manager
from .Tool import Tool
from typing import List


class Output:
    final_ans = []

    def __init__(self, text):
        self.text = text

    def __getitem__(self, key):
        if type(key) == "str":
            return Output(f"'{self.text}['{key}']'")
        return Output(f"'{self.text}[{key}]'")

    def __add__(self, other):
        return Output(f"{self} + {other}")

    def __sub__(self, other):
        return Output(f"{self} - {other}")

    def __mul__(self, other):
        return Output(f"{self} * {other}")

    def __truediv__(self, other):
        return Output(f"{self} / {other}")

    def __floordiv__(self, other):
        return Output(f"{self} // {other}")

    def __mod__(self, other):
        return Output(f"{self} % {other}")

    def __pow__(self, other):
        return Output(f"{self} ** {other}")

    def __lt__(self, other):
        return Output(f"{self} < {other}")

    def __le__(self, other):
        return Output(f"{self} <= {other}")

    def __eq__(self, other):
        return Output(f"{self} == {other}")

    def __ne__(self, other):
        return Output(f"{self} != {other}")

    def __gt__(self, other):
        return Output(f"{self} > {other}")

    def __ge__(self, other):
        return Output(f"{self} >= {other}")

    def __and__(self, other):
        return Output(f"{self} && {other}")

    def __or__(self, other):
        return Output(f"{self} || {other}")

    def __repr__(self):
        return f"'{self.text}'"


def create_py_impl_from_tool(tool: Tool):
    fn = f"def {tool.name}("
    arg_names = [f'{a.name}=None' for a in tool.get_arguments()]
    fn += ",".join(arg_names)
    fn += "):\n"
    fn += "\tcall = { 'tool_name': '" + tool.name + "', 'arguments': [] }\n"
    for arg in tool.get_arguments():
        fn += '\tif (' + arg.name + ' != None):\n'
        fn += '\t\tcall["arguments"].append({ "argument_name": "' + arg.name + '", "argument_value":' + arg.name + '})\n'
    fn += "\tcounter = len(Output.final_ans) - 1\n"
    fn += "\tOutput.final_ans.append(call)\n"
    fn += '\treturn Output(f"$$PREV[{counter}]")\n'
    return fn


def convert_python_to_solution(tools_manager: Manager, code: str) -> List[dict]:
    """
    Converts Python code to a solution.
    :param tools_manager: The tool manager.
    :param code: The Python code.
    :return: The solution.
    """
    arg_replaced = {}  # key: tool, value: (old_arg_name, new_arg_name)[]
    for tool in tools_manager.get_tools():
        arg_replaced[tool.name] = []
        for arg in tool.get_arguments():
            arg_name = arg.name
            if not arg_name.isidentifier():
                # convert to valid identifier
                arg_name = re.sub(r"[^a-zA-Z0-9_]", "_", arg_name)
                if not arg_name[0].isalpha():
                    arg_name = "_" + arg_name
            arg_replaced[tool.name].append((arg.name, arg_name))
    full_code = ""
    for tool in tools_manager.get_tools():
        full_code += create_py_impl_from_tool(tool) + "\n"
    full_code += code
    for tool_name, items in arg_replaced.items():
        for old_arg_name, new_arg_name in items:
            full_code = full_code.replace(old_arg_name, new_arg_name)
    try:
        exec(full_code)
        ret = []
        for call in Output.final_ans:
            tool = tools_manager.get_tool(call["tool_name"])
            replacing_args = {}
            for old_arg_name, new_arg_name in arg_replaced[tool.name]:
                replacing_args[new_arg_name] = old_arg_name
            for arg in call["arguments"]:
                if arg["argument_name"] in replacing_args:
                    arg["argument_name"] = replacing_args[arg["argument_name"]]
                if type(arg["argument_value"]) == Output:
                    arg["argument_value"] = str(arg["argument_value"])
            ret.append(call)
        return ret
    except Exception as e:
        print(e)

    return []


import re
from copy import deepcopy


def augment_query(query):
    for r in ((" my ", " 'MY' "), (" I ", " 'I' "), (" mine ", " 'MINE' "), (" me ", " 'ME' ")):
        query = query.replace(*r)
    return query


def formatted_tools(tools):
    arg_details = {}
    for tool in tools:
        arg_details[tool['tool_name']] = "\n".join([
                                                       f"Argument Name: {arg['arg_name']}, Description: {arg['arg_description']}, Type: {'Array of ' if arg['is_array'] else ''}{arg['arg_type']}, Required: {arg['is_required']}" + (
                                                           f", Example: {arg['example']}" if 'example' in arg else "")
                                                       for arg in tool['args']])
    formatted_tools = "\n".join([
                                    f"\nTool Name: {tool['tool_name']}\nTool Description: {tool['tool_description']}\nReturn Type: {'Array of ' if tool['output']['is_array'] else ''}{tool['output']['arg_type']}, Arguments: [{arg_details[tool['tool_name']]}]\n" + "*" * 50
                                    for tool in tools])
    return formatted_tools


def remove_invalid_args(tools, to_fix):
    to_fix = deepcopy(to_fix)
    for i, tool in enumerate(to_fix):
        actual_tool = [t for t in tools if t['tool_name'] == tool['tool_name']][0]
        actual_args = [arg['arg_name'] for arg in actual_tool['args']]
        args = tool['arguments']

        arg_names = []
        for arg in args.copy():
            if arg['argument_name'] not in actual_args:
                args.remove(arg)
                continue

            # If arg is repeated
            if arg['argument_name'] in arg_names:
                args.remove(arg)
                continue

            arg_names.append(arg['argument_name'])

    return to_fix


def fix_json(tools, to_fix):
    to_fix = deepcopy(to_fix)
    to_fix = remove_invalid_args(tools, to_fix)

    for i, tool in enumerate(to_fix):
        tool_data = [t for t in tools if t['tool_name'] == tool['tool_name']][0]
        for arg in tool['arguments']:
            arg_data = [a for a in tool_data['args'] if a['arg_name'] == arg['argument_name']][0]

            if type(arg['argument_value']) == str:

                pre = re.match(r'^\$\$PREV\[(\d*)\]$', arg['argument_value'])
                if pre:
                    # Get output type of nth tool
                    n = int(pre.group(1))
                    if n < len(to_fix):
                        prev = to_fix[n]['tool_name']
                        prev_array_type = [t for t in tools if t['tool_name'] == prev][0]['output']['is_array']
                        arg_array_type = arg_data['is_array']

                        # if the prev output was a str, but the next tool req.s list input
                        if (not prev_array_type) and arg_array_type:
                            arg['argument_value'] = [arg['argument_value']]
                else:
                    arg_array_type = arg_data['is_array']
                    if arg_array_type:
                        arg['argument_value'] = [arg['argument_value']]


            elif type(arg['argument_value']) == list:

                if len(arg['argument_value']) == 1 and type(arg['argument_value']) == str:

                    pre = re.match(r'^\$\$PREV\[(\d*)\]$', arg['argument_value'][0])
                    if pre:
                        n = int(pre.group(1))
                        if n < len(to_fix):
                            prev = to_fix[n]['tool_name']
                            prev_array_type = [t for t in tools if t['tool_name'] == prev][0]['output']['is_array']
                            arg_array_type = arg_data['is_array']

                            if prev_array_type and arg_array_type:
                                arg['argument_value'] = arg['argument_value'][0]

    return to_fix

