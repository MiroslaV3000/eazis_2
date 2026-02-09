from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class NeuralNetworkMethod:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OP_KEY"),
        )

    def detect_language(self, text: str) -> dict:
        completion = self.client.chat.completions.create(
          extra_headers={},
          extra_body={},
          model="meta-llama/llama-4-maverick:free",
          messages=[
            {
              "role": "user",
              "content": [
                  {
                      "type": "text",
                      "text": "determine the language of this text and return exactly one word with the name of the language"
                  },
                  {
                      "type": "text",
                      "text": text
                  },
              ]
            }
          ]
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content