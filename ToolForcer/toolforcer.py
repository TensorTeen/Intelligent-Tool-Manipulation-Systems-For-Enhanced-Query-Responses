from model import Model
from retriever import STRetriever
from imports import *
from utils import *
from prompts import *

class ToolForcer:
    def __init__(self, model_id, retriever_id, device, load_in_4bit=True, use_vllm=True):
        self.use_vllm=use_vllm
        if use_vllm:
            self.model = Model(model_id=model_id, device=device, load_in_4bit=load_in_4bit, use_vllm=True)
        else:
            self.model = Model(model_id=model_id, device=device, load_in_4bit=load_in_4bit, use_vllm=False)
        self.retriever = STRetriever(retriever_id)
        self.n_retrieved=10
        self.debug=""
        

    def decompose_query(self, query, retrieved_tools):
        """
        Decomposes a user query into tasks that can be solved with one tool each.
        
        Args:
            query (str): The user query to be decomposed.
            retrieved_tools (list): A list of tools to be considered for solving the tasks.
        
        Returns:
            list: A list of tasks, where each task contains the necessary information to call the associated tool.
        """
        decomposition_schema={
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "thought": {"type": "string"},
                    "task": {"type": "string"},
                    "tool_name": {"type": "string", "enum": [tool['tool_name'] for tool in retrieved_tools]+["no_tool"]}
                },
                "required": ["thought"]
            }
        }

        DECOMPOSITION_SYS=f"""
        You are a helpful assistant. Your job is to decompose a user query into tasks that can be solved with one tool each.
        Analyse the list of tools and split the query into tasks. Solve the problem by thinking step by step.
        In each thought, think about what the next step should be in order to solve the problem, based on the available tools. Explain why the tool is required.
        Find the required tool that should be called (make sure it is related to the thought), and construct a task to be completed using it, based on the thought. If no tool is required, use "no_tool".
        Ensure that each task contains the necessary information to call the tool associated with it. Do not create unnecessary steps, if they haven't been mentioned in the query. Keep the minimum number of required tools. Be short and concise.
        The output of the ith task can be referenced using "$$PREV[i]" (starts from 0). DO NOT call tools or write any code in the arguments, and do not make up arguments that don't exist. 
        
        
        If the query cannot be solved with the given tools, just return an empty list []
        
        Note that this is a product management system, and we call our customers revs. Objects are things like customers, parts, and users.
        {formatted_tools(retrieved_tools)}

        Example:
        {DECOMPOSITION_EXAMPLE}
        
        {DECOMPOSITION_EXAMPLE_2}
        
        {DECOMPOSITION_EXAMPLE_3}

        """

        message=f"""
        Query: {query}
        Solution:
        """

        self.debug=message

        task_list = self.model(message=message, system_prompt=DECOMPOSITION_SYS, max_new_tokens=4000, required_json_schema=decomposition_schema)
        self.debug=task_list
        task_list = json.loads(task_list)

        return task_list
    
    def decompose_query_controlllm(self, query, retrieved_tools):
        """
        Decomposes a user query into tasks that can be solved with one tool each, using a prompt similar to controlllm
        
        Args:
            query (str): The user query to be decomposed.
            retrieved_tools (list): A list of tools to be considered for solving the tasks.
        
        Returns:
            list: A list of tasks, where each task contains the necessary information to call the associated tool.
        """
        decomposition_schema={
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "thought": {"type": "string"},
                    "tool_name": {"type": "string", "enum": [tool['tool_name'] for tool in retrieved_tools]},
                    "task": {"type": "string"}
                }
            }
        }

        DECOMPOSITION_SYS=f"""
        The following is a friendly conversation between a human and an AI. The AI is professional and parses user input to several tasks with lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know. The AI assistant can parse user input to several tasks with JSON format as follows:["thought": reasoning after every step to decide on tool and arguments, “task”: task description with argument details, “tool_name”: tool name. The ”task” should describe the task in detail, and AI assistant can add some details to improve the user’s request without changing the user’s original intention. The output of any dependent task can be referenced using "$$PREV[dependency_task_id]. The special tag “dependency_task_id” refers to the one in the dependency task (Please consider whether the dependency task generates arguments required by this tool).Think step by step about all the tasks that can resolve the user’s request. Parse out as few tasks as possible while ensuring that the user request can be resolved. Pay attention to the dependencies and order among tasks. If some inputs of tools are not found, you cannot assume that they already exist. You can think a new task to generate those args that do not exist or ask for the user’s help. If the user request can’t be parsed, you need to reply empty JSON []. Be sure to not miss any intermediate authentication tools to fetch the current state, which may be required in future steps. Start by getting this state information, when required.
<YOUR_SOLUTION> should be strict with JSON format described above.
Your knowledge base consists of tool descriptions and argument descriptions as explained below:
        {retrieved_tools}

        Strictly follow a similar thought process to that shown in the examples
        Examples:
        {DECOMPOSITION_CONTROLLLM_EXAMPLE}

        {DECOMPOSITION_CONTROLLLM_EXAMPLE_2}
        
        """

        

        message=f"""
        Query: {query}
        Solution:
        """

        self.debug=message

        task_list = self.model(message=message, system_prompt=DECOMPOSITION_SYS, max_new_tokens=4000, required_json_schema=decomposition_schema)
        self.debug=task_list
        task_list = json.loads(task_list)

        return task_list

    def generate_tool_schema_1(self, tool):
        """
        Generate the tool schema for a given tool.

        :param tool: The tool object containing information about the tool.
        :type tool: dict

        :return: The tool schema generated for the tool.
        :rtype: dict
        """
        arg_block={
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "argument_name": { "type": "string", "enum": [arg['argument_name'] for arg in tool['args']]},
                    "argument_value": { "type": "string" }
                },
                "required": ["argument_name", "argument_value"]
            }
        }
      
        tool_schema={
        "type": "object",
        "properties": {
            "tool_name": {"type": "string", "enum": [tool['tool_name']]},
            "arguments": arg_block
        },
        "required": ["tool_name", "arguments"]
        }

        return tool_schema

    def generate_tool_json(self, query, task, prev_tasks, tools):
        """
        Generates a JSON file for calling a tool based on the given query, task, previous tasks, and tools.

        Parameters:
            query (str): The query to be solved.
            task (dict): The current task to be performed.
            prev_tasks (list): A list of dictionaries representing the previous tasks.
            tools (list): A list of dictionaries representing the available tools.

        Returns:
            dict: The generated JSON file.
        """
        formatted_tasks=[f"Task {n}:\nThought: {prev_tasks[n]['thought']}\nTask: {prev_tasks[n]['task']}\nTool Required: {prev_tasks[n]['tool_name']}" for n in range(len(prev_tasks))]
        tool=[t for t in tools if t['tool_name']==task['tool_name']][0]

        tool_schema=self.generate_tool_schema_1(tool)
        completed_tasks="Completed Tasks and thought process:" + "\n".join(formatted_tasks) if len(prev_tasks)>0 else ""


        TOOL_SYS=f"""\
        You are a helpful assistant. Your job is to output a json file which can be used to call the tool given below, based on the task given to you.
        These tasks are required in order to solve a given query. In case any arguments are missing in the task, you can still add them to the json.
        The output of the ith task can be referenced using "$$PREV[i]" (starts from 0). This is important, since many queries require a composition of tools.
        You can't reference tools that haven't been called yet.
        
        Tools must be explicitly called and cannot be called inside the arguments.
        

        Example:
        {TOOL_EXAMPLE}

        {TOOL_EXAMPLE_2}

        """
        

        message=f"""
        Query: {query}

        {completed_tasks}

        Your Task:
        {task}

        Answer:
        """

        self.debug=message

        tool_json = self.model(message=message, system_prompt=TOOL_SYS, max_new_tokens=4000, required_json_schema=tool_schema)

        return tool_json


    def __call__(self, query, tools, n_retrieved=10, decomp="base"):
        query=augment_query(query)
        retrieved_tools = self.retriever(tool_set=tools, queries=query, n_retrieved=n_retrieved)[0]
        if decomp=="base":
            tasks=self.decompose_query(query, retrieved_tools)
        else:
            tasks=self.decompose_query_controlllm(query, retrieved_tools)
        solution=[]

        for i, task in enumerate(tasks):
            if all([(field in task) for field in ["task", "thought", "tool_name"]]):
                if task['tool_name']=="no_tool":
                    continue
                try:
                    tool_json = self.generate_tool_json(query, task, tasks[:i], tools=tools)
                    tool_json = json.loads(tool_json)
                    solution.append(tool_json)
                except:
                    self.debug=tool_json
                    solution.append({"tool_name": task['tool_name'], "arguments": []})                
                

        if len(solution)>0:
            try:
                #solution = json.loads(clean_json_regex(json.dumps(solution)))
                solution = remove_invalid_args(tools, solution)
                solution = fix_json(tools, solution)
            except:
                pass
    
            return {
                "solution": solution,
                "tasks": tasks
            }

        else:
            return {
                "solution": [],
                "tasks" : tasks
            }