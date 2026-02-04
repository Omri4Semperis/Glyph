from typing_extensions import Literal
from mcp_object import mcp

@mcp.prompt()
def create_an_operation_doc_prompt(
    step_to_create_doc_for: float
) -> str:
    """
    Use this prompt when creating an operation document for a specific step in a design log.

    Args:
        step_to_create_doc_for (float): The step number to create the operation document for
    
    Returns:
        str: The generated prompt string.
    """
    prompt = f"""Plan the creation of an operation document for step {step_to_create_doc_for} from NameOfDesignLog.

- First read the glyph rules; then:
- Read the operation document guidelines; and finally:
- write the creation plan for the operation document.

The operation document's Background section must be comprehensive, exhaustive and detailed- Taking all of the relevant information from the design log you can find (anywhere in the design log, not just the step itself).

Before you create the doc, :
1. Prove you read through the design log doc and understood what relevant information is there for the operation doc.
2. Prove tou read through the operation document guidelines and understood them, showing me how you will apply them.
3. You'll keep it SOLID, DRY and Simple.
4. Tell me how many phases and tasks in each phase you plan to have in the operation doc."""

    return prompt
