"""List all available Gemini models and test their quota"""
import asyncio
from google import genai

async def list_and_test_models():
    api_key = "AIzaSyD5l-DhQjmI0ErI3i_dupiXC22NM7fU4ZY"

    try:
        print("Fetching available models...\n")
        client = genai.Client(api_key=api_key)

        # List all models
        models = await client.aio.models.list()

        print("Available models:")
        print("=" * 60)

        generation_models = []
        for model in models:
            if hasattr(model, 'name'):
                model_name = model.name
                # Check if it supports generateContent
                if hasattr(model, 'supported_generation_methods'):
                    methods = model.supported_generation_methods
                    if 'generateContent' in methods:
                        generation_models.append(model_name)
                        print(f"✓ {model_name}")
                        if hasattr(model, 'display_name'):
                            print(f"  Display: {model.display_name}")

        print(f"\n{len(generation_models)} models support generateContent")
        print("=" * 60)

        # Test a few promising models
        test_models = [
            "models/gemini-2.0-flash-exp",
            "models/gemini-1.5-pro",
            "models/gemini-pro",
        ]

        print("\nTesting models for available quota...\n")

        for model_name in test_models:
            if model_name in generation_models or True:  # Try anyway
                try:
                    print(f"Testing {model_name}...", end=" ")
                    response = await client.aio.models.generate_content(
                        model=model_name,
                        contents="Hi"
                    )
                    print(f"✓ WORKING - Has quota!")
                    print(f"  Response: {response.text[:50]}")
                    return model_name
                except Exception as e:
                    error_str = str(e)
                    if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                        print("✗ Quota exceeded")
                    elif "404" in error_str:
                        print("✗ Not found")
                    else:
                        print(f"✗ Error: {type(e).__name__}")

        print("\nNo models with available quota found.")
        return None

    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {str(e)[:200]}")
        return None

if __name__ == "__main__":
    working_model = asyncio.run(list_and_test_models())
    if working_model:
        print(f"\n✓ Use this model: {working_model}")
    else:
        print("\n✗ All models exhausted. Need new API key from different Google account.")
