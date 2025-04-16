import json


def get_max_tokens(model_name):
    if model_name == "gpt-3.5-turbo":
        return 10000  # real limit 16385
    if model_name == "gpt-4-turbo-preview":
        return 10000  # Limit max number of tokens to reduce cost (real limit 128000)
    if model_name in ["gpt-4o",  "gpt-4-turbo", "gpt-4o-mini"]:
        return 10000  # Set max number of tokens to reduce cost (real limit 128000)
    raise Exception("Unknown model name")


class MessagesProcessor:
    def __init__(self, model_name, max_response_tokens, cut_history):
        self.model_name = model_name
        self.max_tokens = get_max_tokens(self.model_name) - max_response_tokens
        # we need tokenizer only to calculate number of tokens and cut dialog history if needed
        self.cut_history = cut_history
        if self.cut_history:
            import tiktoken
            self.encoder = tiktoken.encoding_for_model(self.model_name)

    def process_messages(self, messages):
        if self.cut_history:
            messages = self.cut_dialog_history(messages)
        new_messages = []
        for m in messages:
            # append media files to messages
            if m['role'] == 'media':
                try:
                    value = json.loads(m['content'])
                    if isinstance(value, list):
                        new_messages.extend(value)
                    else:
                        new_messages.append(value)
                except:
                    continue
            else:
                new_messages.append(m)

        return new_messages

    def num_tokens_for_single_message(self, m, include_system):
        tokens_per_message = 3  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        num_tokens = tokens_per_message
        if self.is_system_or_media(m, include_system):
            return num_tokens
        if isinstance(m, dict):
            for key, value in m.items():
                num_tokens += len(self.encoder.encode(value))
        if isinstance(m, tuple):
            num_tokens += len(self.encoder.encode(m[1]))
        return num_tokens

    def is_system_or_media(self, m, include_system):
        if isinstance(m, dict):
            if ('role' in m) and (m['role'] == 'media' or (include_system and m['role'] == 'system')):
                return True
        if isinstance(m, tuple):
            if m[0] == 'media' or (include_system and m[0] == 'system'):
                return True
        return False


    def cut_dialog_history(self, messages, include_system=True):
        # remove old history in order to fit into the prompt
        lines_tokens = [self.num_tokens_for_single_message(m, include_system) for m in messages]
        sum_tokens = 0
        i_cut = 0
        for i in reversed(range(len(lines_tokens))):
            sum_tokens += lines_tokens[i]
            if sum_tokens > self.max_tokens:
                i_cut = i + 1
                break
        if i_cut > 0:
            new_messages = messages[i_cut:]
            # do not cut media files
            for m in messages[:i_cut]:
                # do not cut media information
                if self.is_system_or_media(m, include_system):
                    new_messages.append(m)
            return new_messages
        return messages
