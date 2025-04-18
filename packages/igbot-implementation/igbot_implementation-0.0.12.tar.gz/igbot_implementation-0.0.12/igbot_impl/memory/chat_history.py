import time
from igbot_base.llmmemory import LlmMemory
from openai.types.chat import ChatCompletionMessage


class BasicInMemoryChatHistory(LlmMemory):

    def __init__(self, system_prompt: str):
        self.__last_appended_at = None
        self.__snapshot_at_index = None
        self.__chat_history: list[dict[str, str]] = [{'role': 'system', 'content': system_prompt}]

    def retrieve(self):
        return self.__chat_history.copy()

    def append_user(self, content: str):
        self.__chat_history.append({'role': 'user', 'content': content})
        self.__last_appended_at = time.time()

    def append_assistant(self, content: str):
        self.__chat_history.append({'role': 'assistant', 'content': content})
        self.__last_appended_at = time.time()

    def append_system(self, content: str):
        self.__chat_history.append({'role': 'system', 'content': content})
        self.__last_appended_at = time.time()

    def append_tool_request(self, message):
        self.__chat_history.append(message)
        self.__last_appended_at = time.time()

    def append_tool(self, tool_call_id: str, content: str):
        self.__chat_history.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": content
        })
        self.__last_appended_at = time.time()

    def clean_conversation(self):
        self.__chat_history = [
            item for item in self.__chat_history
            if not (isinstance(item, dict) and item.get("role") == "tool")
               and not isinstance(item, dict)
        ]

    #TODO: delete?
    def delete_last_user_message(self):
        self.remove_last_entry("user")

    def delete_last_tool_message(self):
        self.remove_last_entry("tool")

    def delete_last_assistant_message(self):
        self.remove_last_entry("assistant")

    def remove_last_entry(self, role) -> None:
        if role == 'tool':
            tool_index = None
            for i in range(len(self.__chat_history) - 1, -1, -1):
                if isinstance(self.__chat_history[i], ChatCompletionMessage):
                    tool_index = i
                    break
            if tool_index is None:
                return
            del self.__chat_history[tool_index]
            while tool_index < len(self.__chat_history):
                if self.__chat_history[tool_index].get("role") == 'tool':
                    del self.__chat_history[tool_index]
                else:
                    break
            return

        for i in range(len(self.__chat_history) - 1, -1, -1):
            if self.__chat_history[i].get("role") == role:
                del self.__chat_history[i]
                break
            # ChatCompletionMessage(content=None, refusal=None, role='assistant', audio=None, function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_1OXc4Uix8GuEED0u2WU4nnI4', function=Function(arguments='{"query":"kroki przed ostatecznym osiowaniem"}', name='search_knowledge_base'), type='function')])

    def revert_to_snapshot(self):
        self.__chat_history =  self.__chat_history[:self.__snapshot_at_index + 1]

    def set_snapshot(self):
        self.__snapshot_at_index = len(self.__chat_history) - 1

    def describe(self):
        return (f"BasicInMemoryChatHistory(size={len(self.__chat_history)}, last_updated={self.__last_appended_at},"
                f" last_snapshot_at{self.__snapshot_at_index})")
