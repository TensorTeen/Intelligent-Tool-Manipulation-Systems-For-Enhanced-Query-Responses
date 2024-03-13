
import re
from copy import deepcopy
import json

def augment_query(query):
    for r in ((" my ", " 'my' "), (" I ", " 'I' "), (" mine ", " 'mine' "), (" me ", " 'me' ")):
        query = query.replace(*r)
    return query

def formatted_tools(tools):
    arg_details={}
    for tool in tools:
        arg_details[tool['tool_name']]="\n".join([f"Argument Name: {arg['argument_name']}, Description: {arg['argument_description']}, Type: {'Array of ' if arg['is_array'] else ''}{arg['argument_type']}, Required: {arg['is_required']}" + (f", Example: {arg['example']}" if 'example' in arg else "") for arg in tool['args']])
    formatted_tools="\n".join([f"\nTool Name: {tool['tool_name']}\nTool Description: {tool['tool_description']}\nReturn Type: {'Array of ' if tool['output']['is_array'] else ''}{tool['output']['argument_type']}, Arguments: [{arg_details[tool['tool_name']]}]\n"+"*"*50 for tool in tools])
    return formatted_tools

def remove_invalid_args(tools, to_fix):
    to_fix=deepcopy(to_fix)
    for i, tool in enumerate(to_fix):
        actual_tool=[t for t in tools if t['tool_name']==tool['tool_name']][0]
        actual_args=[arg['argument_name'] for arg in actual_tool['args']]
        args=tool['arguments']

        arg_names=[]
        for arg in reversed(args.copy()):
            if arg['argument_name'] not in actual_args:
                args.remove(arg)
                continue
            
            #If arg is repeated
            if arg['argument_name'] in arg_names:
                args.remove(arg)
                continue

            arg_names.append(arg['argument_name'])
            
    
    return to_fix
                

def fix_json(tools, to_fix):
    to_fix=deepcopy(to_fix)

    for i, tool in enumerate(to_fix):
        tool_data=[t for t in tools if t['tool_name']==tool['tool_name']][0]
        for arg in tool['arguments']:
            arg_data=[a for a in tool_data['args'] if a['argument_name']==arg['argument_name']][0]
        
            if type(arg['argument_value'])==str:

                pre=re.match(r'^\$\$PREV\[(\d*)\]$', arg['argument_value'])
                if pre:
                    #Get output type of nth tool
                    n=int(pre.group(1))
                    if n<len(to_fix):
                        prev=to_fix[n]['tool_name']
                        prev_array_type=[t for t in tools if t['tool_name']==prev][0]['output']['is_array']
                        arg_array_type=arg_data['is_array']
                        
                        #if the prev output was a str, but the next tool req.s list input
                        if (not prev_array_type) and arg_array_type:
                            arg['argument_value']=[arg['argument_value']]
                else:
                    arg_array_type=arg_data['is_array']
                    if arg_array_type:
                        arg['argument_value']=[arg['argument_value']]
                        

            elif type(arg['argument_value'])==list:

                if len(arg['argument_value'])==1 and type(arg['argument_value'])==str:
                
                    pre=re.match(r'^\$\$PREV\[(\d*)\]$', arg['argument_value'][0])
                    if pre:
                        n=int(pre.group(1))
                        if n<len(to_fix):
                            prev=to_fix[n]['tool_name']
                            prev_array_type=[t for t in tools if t['tool_name']==prev][0]['output']['is_array']
                            arg_array_type=arg_data['is_array']
        
                            if prev_array_type and arg_array_type:
                                arg['argument_value']=arg['argument_value'][0]               
                
                        
    return to_fix


def clean_json_regex(ugly_input_json, user_query):

    str1=ugly_input_json
    
    
    pattern = '[^\w\s]'
    user_query_symbols = re.findall(pattern, user_query)
    print(f'user_query_symbols are {user_query_symbols}')
    
    
    # Adding escape character in front of the symbols to use them in regex
    allowed_symbols = ''.join('\\' + s for s in user_query_symbols)
    print(f'allowed_symbols are {allowed_symbols}')
    
    regex_pattern = f'[^a-zA-Z0-9\s\${allowed_symbols}]'
    
    prev_pattern = r'\$\$PREV\[\d\]'
    
    
    # parse the json string
    json_data = json.loads(str1)
    for item in json_data:
        print(f'item is: {item}')
    
        for arg in item.get('arguments', []):
            for i, value in enumerate(arg['argument_value']):
    
                print(f'value is: {value}')
                print(f"arg['argument_value'][i] is: {arg['argument_value'][i]}")
    
                # if "PREV" in value:
                #     print(f"found prevvvv")
                #     continue
    
    
                if isinstance(value, list):
                    for j, list_item in enumerate(value):
                        print(f'list_item = {list_item}')
    
    
                        if "PREV" in list_item:
                            print(f"found prevvvv")
    
                            prev_matches = re.findall(prev_pattern, list_item)
                            stripped_list_item = re.sub(regex_pattern, '', list_item)
                            arg['argument_value'][i][j] = ''.join(prev_matches if prev_matches else stripped_list_item)
    
    
                        elif list_item == "[":
                            value[j] = "[]"
                            # value[j] = re.sub(r'\[', '[]', list_item)
                            print(f'value in loop = {value}')
                        else:
                            value[j] = re.sub(regex_pattern, '', list_item)
                else:
                    print(f'value in else = {value}')
                    print(f"arg['argument_value'][i] value in else = {arg['argument_value'][i]}")
    
                    if "PREV" in value:
                        print(f"found prevvvv")
                        prev_matches = re.findall(prev_pattern, value)
                        stripped_value = re.sub(regex_pattern, '', value)
                        arg['argument_value'][i] = ''.join(prev_matches if prev_matches else stripped_value)
    
                    elif value == "[":
                        print(f'value in loop = {value}')
                        arg['argument_value'][i]= "[]"
                    else:
                        arg['argument_value'][i] = re.sub(regex_pattern, '', value)
    
    
                print(f'New value is: {value}')
                print(f"New arg['argument_value'][i] is: {arg['argument_value'][i]}")
    
                print(f'\n')
    
    
    return json_data        
