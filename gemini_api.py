from google import genai
from  dotenv import load_dotenv
import os

class  google_genai:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = genai.Client(api_key=self.api_key)
        self.model="gemini-2.0-flash"
    def generate_content(self, contents):
        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
        )
        return response.text
    

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    agent = google_genai(api_key)

    print(agent.generate_content("請問你是誰？"))