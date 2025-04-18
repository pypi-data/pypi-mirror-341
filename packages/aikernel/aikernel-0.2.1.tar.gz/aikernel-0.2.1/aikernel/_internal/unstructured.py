from typing import Any

from aikernel._internal.router import LLMRouter
from aikernel._internal.types.provider import LiteLLMMessage
from aikernel._internal.types.request import (
    LLMAssistantMessage,
    LLMSystemMessage,
    LLMToolMessage,
    LLMUserMessage,
)
from aikernel._internal.types.response import LLMResponseUsage, LLMUnstructuredResponse
from aikernel.errors import NoResponseError


def llm_unstructured_sync(
    *,
    messages: list[LLMUserMessage | LLMAssistantMessage | LLMSystemMessage | LLMToolMessage],
    router: LLMRouter[Any],
) -> LLMUnstructuredResponse:
    rendered_messages: list[LiteLLMMessage] = []
    for message in messages:
        if isinstance(message, LLMToolMessage):
            invocation_message, response_message = message.render_call_and_response()
            rendered_messages.append(invocation_message)
            rendered_messages.append(response_message)
        else:
            rendered_messages.append(message.render())

    response = router.complete(messages=rendered_messages)
    used_model = router.translate_model_name(model_name=response.model)

    if len(response.choices) == 0:
        raise NoResponseError(model_name=used_model)

    text = response.choices[0].message.content or ""
    usage = LLMResponseUsage(input_tokens=response.usage.prompt_tokens, output_tokens=response.usage.completion_tokens)

    response = LLMUnstructuredResponse(text=text, model=used_model, usage=usage)
    return response


async def llm_unstructured(
    *,
    messages: list[LLMUserMessage | LLMAssistantMessage | LLMSystemMessage | LLMToolMessage],
    router: LLMRouter[Any],
) -> LLMUnstructuredResponse:
    rendered_messages: list[LiteLLMMessage] = []
    for message in messages:
        if isinstance(message, LLMToolMessage):
            invocation_message, response_message = message.render_call_and_response()
            rendered_messages.append(invocation_message)
            rendered_messages.append(response_message)
        else:
            rendered_messages.append(message.render())

    response = await router.acomplete(messages=rendered_messages)
    used_model = router.translate_model_name(model_name=response.model)

    if len(response.choices) == 0:
        raise NoResponseError(model_name=used_model)

    text = response.choices[0].message.content or ""
    usage = LLMResponseUsage(input_tokens=response.usage.prompt_tokens, output_tokens=response.usage.completion_tokens)

    response = LLMUnstructuredResponse(text=text, model=used_model, usage=usage)
    return response
