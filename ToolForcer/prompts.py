DECOMPOSITION_EXAMPLE="""
        Query: Summarize high severity tickets from the customer (rev) UltimateCustomer and add them to the current sprint.
        Solution:
        [
            {
                "thought": "First, we need to get the id of the customer UltimateCustomer",
                "tool_name": "search_object_by_name",
                "task": "Use the search_object_by_name tool with the argument 'query' = UltimateCustomer"
            },
            {
                "thought": "Next, we need to get the high severity tickets for the customer",
                "tool_name": "works_list",
                "task": "Use the works_list tool with the arguments: 'issue.rev_orgs' = "$$PREV[0]", 'ticket_severity' = 'high', and 'type' = 'ticket'."
            },
            {
                "thought": "Now, we need to summarize the high severity tickets obtained from the previous task",
                "tool_name": "summarize_objects",
                "task": "Use the summarize_objects tool with the output of the second task, argument 'objects' = "$$PREV[1]""
            },
            {
                "thought": "In order to add the tool to the current sprint, we need to get the current sprint ID",
                "tool_name": "get_sprint_id",
                "task": "Use the get_sprint_id tool to get the current sprint ID"
            },
            {
                "thought": "Finally, we need to add the work items obtained using works_list in the second task to the current sprint, whose ID was obtained in the previous task.",
                "tool_name": "add_work_items_to_sprint",
                "task": "Use the add_work_items_to_sprint tool with arguments 'work_ids'='$$PREV[1]' and 'sprint_id'='$$PREV[3]'
            }
        ]
        """

DECOMPOSITION_EXAMPLE_2="""Query: Find my P0 issues and add generate a summary of them.
Solution:
[
    {
        "thought": "First, I need to identify the current user to find issues related to them.",
        "tool_name": "who_am_i",
        "task": "Use the 'who_am_i' tool with no arguments to get the current user ID."           
    },
    {
        "thought": "Now, I need to list all P0 issues specifically since I'm looking for issues with the highest priority.",
        "tool_name": "works_list",
        "task": "Use the 'works_list' tool with the arguments 'type'=['issue'], 'created_by'=['$$PREV[0]'], and 'issue_priority'=['P0']."
    },
    {
        "thought": "With the prioritized P0 issues, I need to summarize them for efficient addition to the sprint.",
        "tool_name": "summarize_objects",
        "task": "Use the 'summarize_objects' tool with the output from the prioritize_objects task as argument 'objects'=['$$PREV[1]']."
    }
"""

DECOMPOSITION_EXAMPLE_3="""Query : Obtain work items from the customer support channel, summarize the ones related to part 'FEAT-345' part and prioritize them.
Solution:
[
    {
        "thought": "First, retrieve all work items from the customer support channel related to 'FEAT-345'.",
        "tool_name": "works_list",
        "task": "Use the 'works_list' tool with the arguments 'ticket.source_channel'= ['customer support'] and 'applies_to_part'= ["FEAT-345"]."
    },
    {
        "thought": "Next, summarize the work items related to 'FEAT-345' for clarity.",
        "tool_name": "summarize_objects",
        "task": "Use the 'summarize_objects' tool with the 'objects' argument being the output from the 'works_list' tool, 'objects'='$$PREV[0]'."
    },
    {
        "thought": "Finally, prioritize the issues from the customer support channel that are urgent.",
        "tool_name": "prioritize_objects",
        "task": "Use the 'prioritize_objects' tool with the 'objects' argument being the output from the 'works_list' tool, argument 'objects' = '$$PREV[0]'."
    }
]
"""


DECOMPOSITION_CONTROLLLM_EXAMPLE="""
        Query: Summarize high severity tickets from the customer (rev) UltimateCustomer and add them to the current sprint.
        Solution:
        [
            {{
                "thought": "First, we need to get the id of the customer UltimateCustomer",
                "tool_name": "search_object_by_name",
                "task": "Use the search_object_by_name tool with the argument 'query' = UltimateCustomer",
                "id": 0                
            }},
            {{
                "thought": "Next, we need to get the high severity tickets for the customer",
                "tool_name": "works_list",
                "task": "Use the works_list tool with the arguments: 'issue.rev_orgs' = "[$$PREV[0]]", 'ticket_severity' = '[high]', and 'type' = '[ticket]'."
                "id":1                
            }},
            {{
                "thought": "Now, we need to summarize the high severity tickets obtained from the previous task",
                "tool_name": "summarize_objects",
                "task": "Use the summarize_objects tool with the output of the second task, argument 'objects' = "$$PREV[1]"",
                "id":2                
            }},
            {{
                "thought": "In order to add the tool to the current sprint, we need to get the current sprint ID",
                "tool_name": "get_sprint_id",
                "task": "Use the get_sprint_id tool to get the current sprint ID",
                "id":3                
            }},
            {{
                "thought": "Finally, we need to add the work items obtained using works_list in the second task to the current sprint, whose ID was obtained in the previous task.",
                "tool_name": "add_work_items_to_sprint",
                "task": "Use the add_work_items_to_sprint tool with arguments 'work_ids'='$$PREV[1]' and 'sprint_id'='$$PREV[3]',
                "id":4                
            }}
        ]
        """

DECOMPOSITION_CONTROLLLM_EXAMPLE_2="""Query: Find my P0 issues and add a summary to the sprint.
Solution:
[
    {
        "thought": "First, I need to identify the current user to find issues related to them.",
        "tool_name": "who_am_i",
        "task": "Use the 'who_am_i' tool with no arguments to get the current user ID.",
        "id": 0                
    },
    {
        "thought": "Now, I need to list all P0 issues specifically since I'm looking for issues with the highest priority.",
        "tool_name": "works_list",
        "task": "Use the 'works_list' tool with the arguments 'type'=['issue'], 'created_by'=['$$PREV[0]'], and 'issue_priority'=['P0'].",
        "id": 1
    },
    {
        "thought": "With the prioritized P0 issues, I need to summarize them for efficient addition to the sprint.",
        "tool_name": "summarize_objects",
        "task": "Use the 'summarize_objects' tool with the output from the prioritize_objects task as argument 'objects'=['$$PREV[2]'].", 
        "id": 3
    },
    {
        "thought": "In order to add the summary to the sprint, I need to know the current sprint ID.",
        "tool_name": "get_sprint_id",
        "task": "Use the 'get_sprint_id' tool with no arguments to retrieve the sprint ID.",
        "id": 4
    },
    {
        "thought": "Finally, I need to add the summary of the P0 issues to the sprint by using its ID.",
        "tool_name": "add_work_items_to_sprint",
        "task": "Use the 'add_work_items_to_sprint' tool with the arguments 'work_ids'='$$PREV[3]' and 'sprint_id'='$$PREV[4]'.",
        "id": 5
    }
]
"""


TOOL_EXAMPLE="""
        Query: Summarize high severity tickets from the customer UltimateCustomer.

        Completed Tasks and thought process:
        Task 0:
        Thought: First, we need to get the id of the customer UltimateCustomer
        Task: Use the search_object_by_name tool with the argument 'query' = UltimateCustomer
        Tool_name: search_object_by_name

        Your Task:
        Task 1:
        Thought: Next, we need to get the high severity tickets for the customer
        Task: Use the works_list tool with the arguments: 'issue.rev_orgs' = "$$PREV[0]", 'ticket_severity' = 'high', and 'type' = 'ticket'.
        Tool_name: works_list


        Answer:
        {
            "tool_name": "works_list",
            "arguments": [
            {
                "argument_name": "ticket.rev_org",
                "argument_value": [
                    ['$$PREV[0]']
                ]
            },
            {
                "argument_name": "ticket.severity",
                "argument_value": [
                    ['high']
                ]
            },
            {
                "argument_name": "type",
                "argument_value": [
                ['ticket']
            ]
            }
        ]
        }
        """

TOOL_EXAMPLE_2="""
        Query : Obtain work items from the customer support channel, summarize the ones related to part 'FEAT-345' part and prioritize them.
        
        Completed tasks and thought process:
        Task 0:
        Thought: First, retrieve all work items from the customer support channel related to 'FEAT-345'
        Tool_name: works_list
        Task: "Use the 'works_list' tool with the arguments 'ticket.source_channel'= ['customer support'] and 'applies_to_part'= ["FEAT-345"]
        
        Task 1:
        Thought: Next, summarize the work items related to 'FEAT-345' for clarity.
        Tool_name: summarize_objects
        Task: Use the 'summarize_objects' tool with the 'objects' argument being the output from the 'works_list' tool, 'objects'='$$PREV[0]'
        
        Your Task: 
        Task 2:
        Thought: Finally, prioritize the issues from the customer support channel that are urgent.
        Tool_name: "prioritize_objects
        Task: "Use the 'prioritize_objects' tool with the 'objects' argument being the output from the 'works_list' tool, argument 'objects' = '$$PREV[1]'
        
        Answer:
        {
            "tool_name": "prioritize_objects",
            "arguments": [
                {
                    "argument_name": "objects",
                    "argument_value": "$$PREV[1]"
                }
            ]
        }
"""
