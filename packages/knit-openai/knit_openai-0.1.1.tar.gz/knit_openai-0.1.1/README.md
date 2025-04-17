# Knit OpenAI SDK

Welcome to the Knit's OpenAI SDK, a powerful toolkit designed to integrate AI-powered agents built using OpenAI with a wide range of SaaS applications. 

As an embedded integration platform, Knit provides a white-labeled solution empowering SaaS companies to effortlessly scale integrations within their own products, enriching customer experiences with dynamic, out-of-the-box functionality.

The Knit OpenAI SDK is designed to facilitate seamless integration between LLM agents and SaaS applications by leveraging Knit's platform and its wide range of connectors. 

## Installation

Kickstart your journey with the Knit OpenAI SDK by installing it via pip:

```bash
pip install knit-openai
```

## Quick Start

First, get your Knit API Key by signing up at [https://dashboard.getknit.dev/signup](https://dashboard.getknit.dev/signup)

Now, we're ready to start using the SDK. Here's a simple guide to help you start integrating with the Knit OpenAI SDK:

```python
from openai import OpenAI
from knit_openai import KnitOpenAI, ToolFilter


client = OpenAI()
knit = KnitOpenAI()

integration_id = "b29fcTlZc2IwSzViSUF1NXI5SmhqOHdydTpjaGFybGllaHI="

tools = knit.find_tools(app_id="charliehr")
tool_defs = knit.get_tools(tools=[ToolFilter(app_id="charliehr", tool_ids=[tool.tool_id for tool in tools])])

assistant = client.beta.assistants.create(
    instructions="You are a bot for employee data in an HRIS system. Use the provided functions to answer questions",
    model="gpt-4o",
    tools=tool_defs,
)
thread = client.beta.threads.create()

print("Adding user message to thread...")
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I want to get the list of offices of the company",
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
)

if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for msg in messages.data:
        print(f"Message {msg.id} from {msg.role}: {msg.content}")
else:
    print(f"Run ended with status: {run.status}")

# Check if required_action exists
if hasattr(run, "required_action") and run.required_action:
    print("Run requires action. Tool calls:")
    # Loop through each tool in the required action section

    tool_outputs = []

    for i, tool in enumerate(run.required_action.submit_tool_outputs.tool_calls):
        print(tool)
        print(f"Tool call {i+1}:")
        print(f"ID: {tool.id}")
        print(f"Function: {tool.function.name}")
        print(f"Arguments: {tool.function.arguments}")

        tool_outputs.append(knit.handle_tool_call(tool, integration_id))

    run = client.beta.threads.runs.submit_tool_outputs_and_poll(
        thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
    )
else:
    print("No tool actions required")

if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for msg in messages.data:
        print(f"Message {msg.id} from {msg.role}: {msg.content}")
else:
```

That's it! It's that easy to get started and add hundreds of SaaS applications to your AI Agent. 

## Detailed Information
That was a quick introduction of how to get started with Knit's OpenAI SDK. 

To know more about how to use its advanced features and for more in depth information, please refer to the detailed guide here: [Knit OpenAI SDK Guide](https://developers.getknit.dev/docs/knit-ai-openai-sdk)

## Support

For support, reach out to kunal@getknit.dev