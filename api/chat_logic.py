import json
from datetime import datetime
from fastapi import Request
from fastapi.responses import StreamingResponse
from core.config import openai_client
from api.tool_handler import handle_tool_call
from tools.tools import tools
from api.utils import load_clinic_info


# =========================================================
# Main entry point for handling chat requests
# =========================================================
async def handle_chat_request(request: Request) -> StreamingResponse:
    """
    Handles incoming chat completion requests.
    - Adds current datetime as context for LLM.
    - Forwards messages to the LLM with tool support.
    - Streams back the model's response.
    """
    data = await request.json()
    messages = data["messages"]
    
    try:
        # Add current datetime context to system prompt
        current_time = datetime.now().strftime("%A, %B %d, %Y at %H:%M")
        system_message = {
            "role": "system",
            "content": f"The current date and time is {current_time}. "
                       f"Interpret all user time references accordingly."
        }
        messages = [system_message] + messages

        # First call to OpenAI to check if tool calls are needed
        response = await openai_client.chat.completions.create(
            model=data['model'],
            messages=messages,
            temperature=data['temperature'],
            max_tokens=data['max_tokens'],
            tools=tools,
            tool_choice="auto",
            stream=False
        )

        first_choice = response.choices[0]

        # If LLM wants to use a tool, handle tool calls
        if first_choice.finish_reason == "tool_calls":
            stream_response = await handle_tool_calls(first_choice, messages, data)
        else:
            # Otherwise, proceed with normal chat completion
            stream_response = await handle_regular_chat(messages, data)

        # Stream back the response chunks
        async def event_stream():
            try:
                async for chunk in stream_response:
                    print("Chunk raw:", chunk)  # Debugging output
                    yield f"data: {json.dumps(chunk.model_dump())}\n\n"
                yield "data: [DONE]\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    except Exception as e:
        # In case of any error, send it as a stream response
        return StreamingResponse(
            f"data: {json.dumps({'error': str(e)})}\n\n", 
            media_type="text/event-stream"
        )


# =========================================================
# Tool handling flow
# =========================================================
async def handle_tool_calls(first_choice, messages, data):
    """
    Executes tool calls requested by the model and re-sends updated context.
    """
    tool_calls = first_choice.message.tool_calls
    tool_call_results = []

    # Execute each tool call
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        result = await handle_tool_call(tool_name, args)

        tool_call_results.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })

    # Rebuild conversation with tool results
    updated_messages = messages + [first_choice.message] + tool_call_results

    # Call LLM again with updated context
    return await openai_client.chat.completions.create(
        model=data['model'],
        messages=updated_messages,
        temperature=data['temperature'],
        max_tokens=data['max_tokens'],
        stream=True,
    )


# =========================================================
# Regular chat flow (without tool calls)
# =========================================================
async def handle_regular_chat(messages, data):
    """
    Handles normal chat without tool usage.
    Adds clinic info as system context before querying the LLM.
    """
    clinic_info = load_clinic_info()

    mock_info_message = {
        "role": "system",
        "content": (
            "You are a helpful assistant for a dental clinic. "
            f"Here's some clinic information:\n{clinic_info}"
        )
    }

    enriched_messages = [mock_info_message] + messages

    return await openai_client.chat.completions.create(
        model=data['model'],
        messages=enriched_messages,
        temperature=data['temperature'],
        max_tokens=data['max_tokens'],
        stream=True,
    )
