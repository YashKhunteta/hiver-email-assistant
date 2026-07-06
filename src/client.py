import os
import sys
from dotenv import load_dotenv

# Try to load environment variables from a local .env file if it exists
load_dotenv()

class GeminiClient:
    def __init__(self):
        # Check environment variables for Gemini keys
        self.api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        self.is_simulation_mode = not bool(self.api_key)
        
        self.client = None
        if not self.is_simulation_mode:
            try:
                from google import genai
                # Initialize the Google GenAI Client with the key
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[ERROR] Failed to initialize google-genai client: {e}", file=sys.stderr)
                print("[WARNING] Falling back to Simulation Mode.", file=sys.stderr)
                self.is_simulation_mode = True

    def generate(self, prompt: str, system_instruction: str = None) -> str:
        """
        Generate content using Gemini model. 
        If in simulation mode, returns None (caller should handle simulated response).
        """
        if self.is_simulation_mode:
            return None
            
        try:
            # Using the fast and cost-effective gemini-2.5-flash model
            config_args = {}
            if system_instruction:
                # In google-genai, system_instruction can be passed in GenerateContentConfig
                from google.genai import types
                config_args["config"] = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.2
                )
            
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                **config_args
            )
            return response.text
        except Exception as e:
            print(f"[ERROR] API Call failed: {e}", file=sys.stderr)
            print("[WARNING] Defaulting to Simulation Mode for this request.", file=sys.stderr)
            return None
