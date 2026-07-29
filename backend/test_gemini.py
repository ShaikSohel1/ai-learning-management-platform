import importlib.metadata
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

# Load environment variables from .env
load_dotenv()

def run_production_health_check():
    print("==================================================")
    print("      GOOGLE GEMINI SDK PRODUCTION HEALTH CHECK    ")
    print("==================================================")

    # 1. Verify .env load & API Key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        print("❌ FAIL: GEMINI_API_KEY is not set or is still default template value.")
        sys.exit(1)
    print("✓ API Key present.")

    # 2. Print SDK Version
    try:
        sdk_version = importlib.metadata.version("google-genai")
        print(f"✓ google-genai SDK Version: {sdk_version}")
    except Exception as e:
        print(f"⚠️ Warning: Could not detect google-genai package version: {e}")

    # 3. Print Configured Model from .env
    configured_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    print(f"✓ Configured Model (GEMINI_MODEL): {configured_model}")

    # 4. Initialize Client & Fetch Available Models
    try:
        client = genai.Client(api_key=api_key)
        print("\n--- Fetching Available Generation Models ---")
        available_models = []
        for m in client.models.list():
            if "generateContent" in (m.supported_actions or []):
                model_short_name = m.name.replace("models/", "")
                available_models.append(model_short_name)
                available_models.append(m.name)
                print(f" • {m.name}")

        # 5. Verify Configured Model Exists
        if configured_model not in available_models and f"models/{configured_model}" not in available_models:
            print(f"\n⚠️ WARNING: Configured model '{configured_model}' was NOT found in the available models list or may be restricted.")
            print("Listed above are the supported models returned by Google's API.")
            print("Note: Proceeding to test configured model directly without mutating settings...")

        # 6. Test Text Generation Prompt ("Hello")
        print(f"\n--- Testing Text Prompt on '{configured_model}' ---")
        prompt = "Hello! Please reply with exactly one word: 'Success'."
        response = client.models.generate_content(
            model=configured_model,
            contents=prompt
        )

        if response and response.text:
            print(f"✓ Text Generation Response: {response.text.strip()}")
        else:
            print(f"❌ FAIL: Received empty response for model '{configured_model}'.")
            sys.exit(1)

        # 7. Test JSON Mode Generation
        print(f"\n--- Testing JSON Mode Response on '{configured_model}' ---")
        json_config = types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json"
        )
        json_prompt = "Return a JSON object with keys 'status' (value 'ok') and 'service' (value 'gemini')."
        json_response = client.models.generate_content(
            model=configured_model,
            contents=json_prompt,
            config=json_config
        )

        if json_response and json_response.text:
            print(f"✓ JSON Mode Response: {json_response.text.strip()}")
        else:
            print(f"❌ FAIL: Received empty response for JSON mode check.")
            sys.exit(1)

        print("\n==================================================")
        print("  ✅ GEMINI INTEGRATION HEALTH CHECK PASSED!      ")
        print("==================================================")
        sys.exit(0)

    except APIError as e:
        print(f"\n❌ FAIL: Gemini APIError [Code {getattr(e, 'code', 'Unknown')}]: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ FAIL: Unexpected error during Gemini health check: {type(e).__name__}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_production_health_check()
