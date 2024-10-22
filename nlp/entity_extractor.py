import os
import google.generativeai as genai
from typing import List, Dict
import json

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set up the Generative AI model configuration
generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

class EntityExtractor:
    def extract_entities(self, text: str) -> List[Dict]:
        prompt = f"""
        Extract named entities from the following text. Return the results as a valid JSON array of objects, 
        where each object has 'entity' and 'type' keys. Entity types should be one of: PERSON, ORGANIZATION, LOCATION, DATE.
        Ensure the output is strictly in JSON format, with no additional text.

        Text: {text}

        JSON Output:
        """

        response = model.generate_content(prompt)
        try:
            # Strip any non-JSON content
            json_str = response.text.strip()
            if json_str.startswith('```json'):
                json_str = json_str.split('```json')[1]
            if json_str.endswith('```'):
                json_str = json_str.rsplit('```', 1)[0]
            
            entities = json.loads(json_str)
            return entities
        except json.JSONDecodeError as e:
            print(f"Error: Unable to parse JSON from Gemini response: {e}")
            print(f"Raw response: {response.text}")
            return []
