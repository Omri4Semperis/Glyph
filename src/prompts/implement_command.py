from typing_extensions import Literal
from mcp_object import mcp
from read_an_asset import read_asset

@mcp.prompt()
def implementation_command_prompt(
    plan_or_implement: Literal["plan", "implement"],
    phase_number: int,
    task_number: int
) -> str:
    """
    A useful prompt to instruct the assistant to implement a phase/task.

    Args:
        plan_or_implement (Literal["plan", "implement"]): Whether to plan or implement
        phase_number (int): The phase number to plan/implement
        task_number (int): The task number to plan/implement
    
    Returns:
        str: The implementation command prompt
    """
    template = read_asset("implementation_command.md")
    return template.format(
        plan_or_implement=plan_or_implement.capitalize(),
        phase_number=phase_number,
        task_number=task_number
    )
