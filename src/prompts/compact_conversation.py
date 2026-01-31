from mcp_object import mcp

@mcp.tool()
def compact_conversation() -> str:
    """
    A useful prompt to summarize long conversations.
    """
    prompt = """Stop. The conversation has become too long and your context window is getting bloated.

I want to continue this conversation in another session, perhaps with a new model.

Summarize our current conversation to include the following sections:

1. Background: A brief overview of the context and purpose of the conversation.
2. Ambiguities: Any unclear points or questions that need further clarification.
3. Done: A summary of what has been accomplished so far.
4. Failed: A summary of what was attempted but did not succeed.
5. Lessons Learned: Key takeaways or insights gained from the conversation.
6. Stopped While: If I just stopped you, summarize what you were doing/thinking at that moment.
7. Recommendations and next steps: What should I do next to continue making progress?
8. If you think another section is needed, add it anywhere you see fit.

Write it here in this conversation and don't do anything else.
Remember- this is your only chance to summarize the entire conversation, so be thorough on one hand, but on the other hand do not include anything unnecessary or too detailed.

Write it in a ```txt snippet block so I can easily copy it."""

    return prompt
