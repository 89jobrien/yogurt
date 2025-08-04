JSON_RESPONSE = """
The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {{"properties": {{"foo": {{"title": "Foo", "description": "a list of strings", "type": "array", "items": {{"type": "string"}}}}}}, "required": ["foo"]}}
the object {{"foo": ["bar", "baz"]}} is a well-formatted instance of the schema. The object {{"properties": {{"foo": ["bar", "baz"]}}}} is not well-formatted.
"""

# JSON_RESPONSE = """
# The output should be formatted as a JSON instance that conforms to the JSON schema below.

# As an example, for the schema {{"properties": {{"foo": {{"title": "Foo", "description": "a list of strings", "type": "array", "items": {{"type": "string"}}}}}}, "required": ["foo"]}}
# the object {{"foo": ["bar", "baz"]}} is a well-formatted instance of the schema. The object {{"properties": {{"foo": ["bar", "baz"]}}}} is not well-formatted.
# """
# # """
# # Please format your entire response as a single JSON object inside a ```json code block.
# # The JSON object must have a top-level key named "conversation", which contains a list of message objects.
# # Each message object in the list must have two keys: "role" (which must be one of "system", "human", or "ai") and "content" (a string).

# # Example:
# # ```json
# # {
# #   "conversation": [
# #     {
# #       "role": "system",
# #       "content": "You are a helpful assistant."
# #     },
# #     {
# #       "role": "human",
# #       "content": "Hello, how are you?"
# #     },
# #     {
# #       "role": "ai",
# #       "content": "I am doing well, thank you!"
# #     }
# #   ]
# # }
# # ```"""