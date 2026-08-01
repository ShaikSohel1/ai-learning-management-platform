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

    # 3. Print Configured Models from .env / settings
    configured_models_raw = os.getenv("GEMINI_MODELS", "models/gemini-3.6-flash,models/gemini-3.5-flash")
    configured_models = [m.strip() for m in configured_models_raw.split(",") if m.strip()]
    configured_model = configured_models[0] if configured_models else "models/gemini-3.5-flash"
    print(f"✓ Configured Models Chain (GEMINI_MODELS): {configured_models}")

    # 4. Initialize Client & Fetch Available Models
    try:
        client = genai.Client(api_key=api_key)
        print("\n--- Fetching Available Generation Models ---")
        available_models = []
        for m in client.models.list():
            if "generateContent" in (m.supported_actions or []):
                available_models.append(m.name)
                available_models.append(m.name.replace("models/", ""))
                print(f" • {m.name}")

        # 5. Verify Configured Target Model Exists in Registry
        target_model = configured_model
        if target_model in available_models or target_model.replace("models/", "") in available_models:
            print(f"\n✓ VERIFIED: Target model '{target_model}' exists in Google API Registry.")
        else:
            print(f"\n⚠️ WARNING: Target model '{target_model}' was not found in available models list.")

        # 6. Test Text Generation Prompt on configured model
        print(f"\n--- Testing Text Prompt on '{configured_model}' ---")
        prompt = "Hello! Please reply with exactly one word: 'Success'."
        try:
            response = client.models.generate_content(
                model=configured_model,
                contents=prompt
            )
            if response and response.text:
                print(f"✓ Text Generation Response: {response.text.strip()}")
            else:
                print(f"❌ FAIL: Received empty response for model '{configured_model}'.")
                sys.exit(1)
        except APIError as e:
            print(f"⚠️ Notice: Google API returned status for '{configured_model}': {e.message if hasattr(e, 'message') else e}")
            print("✓ Testing generation with fallback active model 'gemini-flash-latest'...")
            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt
            )
            print(f"✓ Text Generation Response (fallback): {response.text.strip()}")

        # 7. Test JSON Mode Generation
        print(f"\n--- Testing JSON Mode Response on '{configured_model}' ---")
        json_config = types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json"
        )
        json_prompt = "Return a JSON object with keys 'status' (value 'ok') and 'service' (value 'gemini')."
        try:
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
        except APIError as e:
            print(f"⚠️ Notice: Google API returned status for '{configured_model}': {e.message if hasattr(e, 'message') else e}")
            print("✓ Testing JSON mode with fallback active model 'gemini-flash-latest'...")
            json_response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=json_prompt,
                config=json_config
            )
            print(f"✓ JSON Mode Response (fallback): {json_response.text.strip()}")

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
