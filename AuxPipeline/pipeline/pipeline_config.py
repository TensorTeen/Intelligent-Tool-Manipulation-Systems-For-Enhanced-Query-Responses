from imports import *

class PipeConfig:
    embedding_model: str = 'openai/text-embedding-ada-002'
    openai_model:str = Config.GPT_3_5

    system_template:str = """\
Tool List : 
{tools}


You can output [], if the query is unsolvable with the tools given above
If the query contains ownership indicators such as 'my' followed by an entity like 'work list,' utilize tools like 'who_am_i' to extract the user ID. Then, pass this ID as an argument to a tool designed to retrieve the entity owned by the user.
Given an argument has 'is_array' with a value of 'true,' if the output from the tool $$PREV[i] is not an array, modify it by enclosing it within square brackets [ ]. Output in json.
"""
    prompt_template:str = """\
{query}
"""
    temperature: float = 0.6
    num_retrieved: int = 8
