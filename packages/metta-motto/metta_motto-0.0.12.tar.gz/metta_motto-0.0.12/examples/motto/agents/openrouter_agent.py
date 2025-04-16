from motto.agents.api_importer import AIImporter
from .metta_agent import Agent
import json
ai_importer = AIImporter('OpenRouterAgent', key='OPENROUTER_API_KEY', requirements=['requests'], static_client='requests')

class Function:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class ToolCalls:
    def __init__(self, tool_id, call_type, function):
        self.id = tool_id
        self.type = call_type
        self.function = function


class MessageClass:
    def __init__(self, role, content, tool_calls=None):
        self.role = role
        self.content = content
        self.tool_calls = tool_calls


class OpenRouterAgent(Agent):
    '''
    OpenRouter is a unified interface for LLMs, this agent use OpenRouter API to get responses from LLM
    '''

    def __init__(self, model="openai/gpt-3.5-turbo", stream=False):
        super().__init__()

        self._model = model
        self.stream_response = stream

    def __call__(self, messages, functions=[]):
        try:
            ai_importer.check_errors()
            data = {
                "model": self._model,
                "messages": messages,
            }
            if functions:
                tools = []
                for func in functions:
                    dict_values = {}
                    dict_values["type"] = "function"
                    dict_values["function"] = func
                    tools.append(dict_values)

                data["tools"] = tools
            else:
                data["stream"] = self.stream_response

            response = ai_importer.client.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {ai_importer.key}",
                },
                data=json.dumps(data)
            )

            if self.stream_response and not functions:
                return response

            result = json.loads(response.content)
            response_message = result['choices'][0]['message']
            if not functions:
                return MessageClass(response_message['role'], response_message['content'])
            tool_calls = []
            for tool in response_message['tool_calls']:
                tool_calls.append(
                    ToolCalls(tool['id'], tool['type'], Function(tool['function']['name'], tool['function']['arguments'])))

            return MessageClass(response_message['role'], response_message['content'], tool_calls)
        except Exception as e:
            return MessageClass("system", e)

