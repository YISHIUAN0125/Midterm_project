from google import genai

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