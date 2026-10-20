import json
import logging
from typing import Dict, Any
from core.config import settings
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalysisService:
    def __init__(self):
        self.model = settings.LLM_MODEL_NAME
        self.base_url = "http://localhost:11434"

    def _construct_prompt(self, raw_text: str) -> str:
        """
        Wraps the raw text into a structured prompt for the LLM.
        """
        return f"""
You are an expert OSINT analyst. Your task is to extract key information from the following text 
and format it as a JSON object.

The raw text is provided below. Please extract:
1. Full Name
2. Known Aliases
3. Reported Phone Numbers
4. Physical Addresses
5. Significant Dates (Birthdays, etc.)
6. Social Media Handles
7. Links to images of subject

Return ONLY a valid JSON object. Do not include any preamble, explanation or comments

RAW TEXT:
{raw_text}
"""

    def analyze_content(self, raw_content: str) -> Dict[str, Any]:
        """
        The 'Hand-off': Takes raw text from the scraper, passes it 
        through the LLM, and returns a structured dictionary.
        """
        prompt = self._construct_prompt(raw_content)
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }

        try:
            logger.info(f"Requesting analysis from {self.model}...")
            response = requests.post(f"{self.base_url}/api", json=payload)
            response.raise_for_status()
            
            # The Ollama response is wrapped in a 'response' field
            response_data = response.json()
            content = response_data.get("response", "{}")
            
            # Parse the JSON string from the LLM
            parsed_data = json.loads(content)
            logger.info("Successfully parsed LLM output.")
            return parsed_data

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            return {}

# Singleton instance for easy access
analyzer = AnalysisService()
