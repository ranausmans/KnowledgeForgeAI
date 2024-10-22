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

class RelationshipExtractor:
    def extract_relationships(self, text: str, entities: List[Dict]) -> List[Dict]:
        entity_names = [e['entity'] for e in entities]
        prompt = f"""
        Extract relationships between the following entities found in the text. 
        Return the results as a valid JSON array of objects, where each object has 'subject', 'predicate', and 'object' keys.
        Ensure the output is strictly in JSON format, with no additional text.

        Text: {text}

        Entities: {', '.join(entity_names)}

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
            
            relationships = json.loads(json_str)
            return relationships
        except json.JSONDecodeError as e:
            print(f"Error: Unable to parse JSON from Gemini response: {e}")
            print(f"Raw response: {response.text}")
            return []
