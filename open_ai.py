from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

class Client:
    def __init__(self):
        self.client = OpenAI(
        base_url="https://api.aimlapi.com/v1",
        api_key=os.getenv("AI_KEY"))

    def img_analysis(self, text):
        response = self.client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": os.getenv("COMMAND_AI")},
        {"role": "user", "content": text}])
        explanation = response.choices[0].message.content
        return explanation
