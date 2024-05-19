# Publication
Please Refer to following ArXiv [link](https://arxiv.org/abs/2401.15724) for the Pre-Print 

## Code Submission by Team-31

Files:


| Component    | Description                                          | Base Model              |
| ------------ | ---------------------------------------------------- | ----------------------- |
| MainPipeline | Our main pipeline based on vanilla GPT-3.5 Turbo.    | GPT-3.5 Turbo           |
| AuxPipeline  | Auxiliary pipeline based on finetuned GPT-3.5 Turbo. | Finetuned GPT-3.5 Turbo |
| Client_lib   | Inference client engine for model interaction.       | N/A                     |


Deployed Links:    
               https://replicate.com/team-31-interiit/toolforcer(ToolForcer)
               https://replicate.com/team-31-interiit/model_test(ToolBenchBert)

Here we have the deployed links of 2 of the 3 pipelines created.

Our first pipeline incorporates an efficient tool retrieval mechanism paired with an innovative prompting strategy to address the inquiry using only one LLM (Large Language Model) API request. The methodology consists of identifying the appropriate tool, breaking down the task, and engaging in sequential reasoning. Considering both deployment expenses and inference duration, this strategy stands out as the optimal solution.

The second approach utilizes Jina embeddings to enhance Tool Retrieval efficiency. It is built upon a custom-designed, three-part framework that includes Tool Retrieval, Decomposition, and Recomposition, all crafted with the aim of optimizing performance in terms of time and cost effectiveness.(https://replicate.com/team-31-interiit/toolforcer(ToolForcer))

## Client Library:
Install the library

```bash
pip install devrevthirtyone
```

Import the tools from pre existing JSON file. Please see the example it should follow the same format

```python
import os

os.environ["OPENAI_API_KEY"] = "OPENAI_KEY"

from devrevthirtyone.Manager import Manager
from devrevthirtyone.Tool import Tool
from devrevthirtyone.Argument import Argument
from devrevthirtyone.ReturnType import ReturnType

if __name__ == "__main__":
    tools_manager = Manager.from_json("examples.json")
    tools_manager.add_tool(Tool(
        "apply",
        "Apply a tool to a list of items",
        [
            Argument("tool_name", "The tool to apply", "str", "get_item_details", True),
            Argument("items", "The items to apply the tool to", "List[str]", ["item1", "item2"], True)
        ],
        ReturnType("dict", "The results of applying the tool to the items", {"item1": "result1", "item2": "result2"})
    ))
    tools_manager.get_tool('apply').add_argument(Argument("new_arg", "A new argument", "str", "new_arg", True))
    tools_manager.remove_tool('apply')
    print(tools_manager.run_query("Merge all my todo work items in the current sprint"))
```

The output is given below, all costs are measured in USD

```python
{
  'embed_calls': 7,
  'return_tools': [],
  'solution': {
    'solution': [
      {
        'tool_name': 'who_am_i',
        'arguments': []
      },
      {
        'tool_name': 'get_sprint_id',
        'arguments': []
      },
      {
        'tool_name': 'merge_work_items',
        'arguments': [
          {
            'argument_name': 'sprint_id',
            'argument_value': '$$PREV[1]'
          }
        ]
      }
    ]
  },
  'time_taken': 8.903069496154785,
  'openai_model': 'gpt-3.5-turbo-1106',
  'embedding_model': 'text-embedding-ada-002',
  'num_embedding_tokens_query': 10,
  'num_embedding_tokens_tool': 166,
  'num_output_tokens': 95,
  'num_input_tokens': 1086,
  'embedding_cost_query': 1.0000000000000002e-06,
  'embedding_cost_tool': 1.66e-05,
  'gpt_input_cost': 0.003258,
  'gpt_output_cost': 0.00057,
  'total_inference_cost': 0.003829,
  'tool_setup_cost': 1.66e-05
}
```

Here is the `examples.json` file

```json
[
    {
        "tool_name": "assign_work_items",
        "tool_description": "Assigns specified work items to a user",
        "args": [
            {
                "arg_name": "work_item_ids",
                "arg_type": "str",
                "is_array": true,
                "is_required": true,
                "arg_description": "List of work item IDs to be assigned",
                "example": [
                    "TASK-456",
                    "ISSUE-789"
                ]
            },
            {
                "arg_name": "user_id",
                "arg_type": "str",
                "is_array": false,
                "is_required": true,
                "arg_description": "The ID of the user to whom the work items are to be assigned",
                "example": "DEVU-456"
            }
        ],
        "output": {
            "description": "Returns true if the work items were successfully assigned to the user; otherwise, false.",
            "arg_type": "bool",
            "is_array": false,
            "is_required": true,
            "example": true
        }
    },
    {
        "tool_name": "validate_work_dependency",
        "tool_description": "Checks if specified work items have dependencies and validates their status",
        "args": [
            {
                "arg_name": "work_item_ids",
                "arg_type": "str",
                "is_array": true,
                "is_required": true,
                "arg_description": "List of work item IDs to check for dependencies",
                "example": [
                    "FEAT-456",
                    "BUG-123"
                ]
            }
        ],
        "output": {
            "description": "Returns a list of booleans indicating whether each work item has dependencies and if they are valid.",
            "arg_type": "bool",
            "is_array": true,
            "is_required": true,
            "example": [
                true,
                false
            ]
        }
    },
    {
        "tool_name": "sync_work_items_with_calendar",
        "tool_description": "Synchronizes work items with a user's calendar to manage deadlines and reminders",
        "args": [
            {
                "arg_name": "user_id",
                "arg_type": "str",
                "is_array": false,
                "is_required": true,
                "arg_description": "The ID of the user whose calendar is to be synchronized",
                "example": "DEVU-567"
            },
            {
                "arg_name": "work_item_ids",
                "arg_type": "str",
                "is_array": true,
                "is_required": true,
                "arg_description": "List of work item IDs to synchronize with the calendar",
                "example": [
                    "FEAT-789",
                    "TASK-890"
                ]
            }
        ],
        "output": {
            "description": "Returns true if the synchronizing process was successful; otherwise, false.",
            "arg_type": "bool",
            "is_array": false,
            "is_required": true,
            "example": true
        }
    },
    {
        "tool_name": "list_sprint_work_items",
        "tool_description": "Lists all work items associated with a particular sprint.",
        "args": [
            {
                "arg_name": "sprint_id",
                "arg_type": "str",
                "is_array": false,
                "is_required": true,
                "arg_description": "The ID of the sprint to retrieve work items for.",
                "example": "SPR-123"
            }
        ],
        "output": {
            "description": "Returns a list of work items associated with the specified sprint.",
            "arg_type": "str",
            "is_array": true,
            "is_required": true,
            "example": [
                "TASK-001",
                "TASK-002",
                "BUG-101"
            ]
        }
    },
    {
        "tool_name": "filter_by_status",
        "tool_description": "Filters and returns work items based on their status.",
        "args": [
            {
                "arg_name": "status",
                "arg_type": "str",
                "is_array": true,
                "is_required": true,
                "arg_description": "The status(es) to filter work items by.",
                "example": [
                    "In Progress",
                    "To Do",
                    "Open",
                    "Blocked"
                ]
            },
            {
                "arg_name": "work_ids",
                "arg_type": "str",
                "is_array": true,
                "is_required": true,
                "arg_description": "List of work item IDs to be filtered",
                "example": [
                    "TASK-456",
                    "ISSUE-789"
                ]
            }
        ],
        "output": {
            "description": "Returns a list of work items that match the specified status(es).",
            "arg_type": "str",
            "is_array": true,
            "is_required": true,
            "example": [
                "TASK-456",
                "ISSUE-789"
            ]
        }
    },
    {
        "tool_name": "merge_work_items",
        "tool_description": "Combines multiple work items into a single item.",
        "args": [
            {
                "arg_name": "source_work_ids",
                "arg_type": "str",
                "is_array": true,
                "is_required": true,
                "arg_description": "The IDs of the source work items to merge.",
                "example": [
                    "TASK-123",
                    "ISSUE-456"
                ]
            },
            {
                "arg_name": "target_work_id",
                "arg_type": "str",
                "is_array": false,
                "is_required": true,
                "arg_description": "The ID of the target work item to merge into.",
                "example": "TASK-789"
            }
        ],
        "output": {
            "arg_type": "str",
            "is_array": true,
            "is_required": true,
            "description": "Returns a list of work items that were merged into the target work item.",
            "example": [
                "TASK-123",
                "ISSUE-456"
            ]
        }
    }
]
```

The arg_type in argument is one of these `str`, `int`, `bool` , `float`. The arg_type in output can also be one of this and can be a `dict` as well. If the arg type is list you can make the `is_array` property true.

If you want to start with blank list of tools

```json
tools_manager = new Manager([])
```
