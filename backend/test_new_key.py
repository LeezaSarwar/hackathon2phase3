"""Test the new Gemini API key"""
import asyncio
from google import genai

async def test_api():
    api_key = "AIzaSyD5l-DhQjmI0ErI3i_dupiXC22NM7fU4ZY"

    try:
        print("Testing new Gemini API key...")
        client = genai.Client(api_key=api_key)

        response = await client.aio.models.generate_content(
            model="models/gemini-2.5-flash",
            contents="Say 'API key working' in 2 words."
        )

        print("SUCCESS: API key is working!")
        print(f"Response: {response.text}")
        print("\nQuota status: OK - Key has available requests")
        return True

    except Exception as e:
        error_msg = str(e)
        print(f"ERROR: {type(e).__name__}")

        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            print("QUOTA EXCEEDED: This API key has no remaining quota")
            print("You need a new API key with available quota")
        elif "401" in error_msg or "UNAUTHENTICATED" in error_msg:
            print("INVALID KEY: This API key is not valid")
        elif "404" in error_msg:
            print("MODEL NOT FOUND: Check the model name")
        else:
            print(f"Message: {error_msg}")

        return False

if __name__ == "__main__":
    result = asyncio.run(test_api())
    print(f"\nTest result: {'PASSED' if result else 'FAILED'}")
