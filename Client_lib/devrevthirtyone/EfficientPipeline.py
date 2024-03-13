from typing import List
from .pipeline import Pipeline
from .pipeline_config import PipeConfig

examples = [
    {
        "query": "Allocate the work items I own that are at the 'QA' stage and with 'medium' severity to the current sprint, after prioritizing and summarizing them.",
        "solution": [
            {
                "tool_name": "who_am_i",
                "arguments": []
            },
            {
                "tool_name": "works_list",
                "arguments": [
                    {
                        "argument_name": "owned_by",
                        "argument_value": ["$$PREV[0]"]
                    },
                    {
                        "argument_name": "stage.name",
                        "argument_value": ["QA"]
                    },
                    {
                        "argument_name": "type",
                        "argument_value": ["ticket"]
                    },
                    {
                        "argument_name": "ticket.severity",
                        "argument_value": ["medium"]
                    }
                ]
            },
            {
                "tool_name": "prioritize_objects",
                "arguments": [
                    {
                        "argument_name": "objects",
                        "argument_value": "$$PREV[2]"
                    }
                ]
            },
            {
                "tool_name": "summarize_objects",
                "arguments": [
                    {
                        "argument_name": "objects",
                        "argument_value": "$$PREV[3]"
                    }
                ]
            },
            {
                "tool_name": "get_sprint_id",
                "arguments": []
            },
            {
                "tool_name": "add_work_items_to_sprint",
                "arguments": [
                    {
                        "argument_name": "work_ids",
                        "argument_value": "$$PREV[1]"
                    },
                    {
                        "argument_name": "sprint_id",
                        "argument_value": "$$PREV[2]"
                    }
                ]
            }
        ]
    },
    {
        "query": "Create actionable tasks from the summary of all 'high' severity tickets associated with 'REV-456', get similar work items to those tasks, prioritize by severity, and filter out those that don't need immediate action.",
        "solution": [
            {
                "tool_name": "works_list",
                "arguments": [
                    {
                        "argument_name": "ticket.severity",
                        "argument_value": ["high"]
                    },
                    {
                        "argument_name": "ticket.rev_org",
                        "argument_value": ["REV-456"]
                    },
                    {
                        "argument_name": "type",
                        "argument_value": ["ticket"]
                    },
                    {
                        "argument_name": "ticket.needs_response",
                        "argument_value": True
                    }
                ]
            },
            {
                "tool_name": "summarize_objects",
                "arguments": [
                    {
                        "argument_name": "objects",
                        "argument_value": "$$PREV[0]"
                    }
                ]
            },
            {
                "tool_name": "create_actionable_tasks_from_text",
                "arguments": [
                    {
                        "argument_name": "text",
                        "argument_value": "$$PREV[1]"
                    }
                ]
            },
            {
                "tool_name": "get_similar_work_items",
                "arguments": [
                    {
                        "argument_name": "work_id",
                        "argument_value": "$$PREV[2]"
                    }
                ]
            },
            {
                "tool_name": "prioritize_objects",
                "arguments": [
                    {
                        "argument_name": "objects",
                        "argument_value": "$$PREV[3]"
                    }
                ]
            }
        ]
    }
]


def solve_efficient(tools: List[dict], query: str) -> List[dict]:
    pipe = Pipeline(PipeConfig)
    output = pipe(query, tools, examples)
    return output
