"""Test the final new API key"""
import asyncio
from google import genai

async def test_api():
    api_key = "AIzaSyC_3MSa9fh1Z5L6s7egd2NU_na7Q2zeKTU"

    try:
        print("Testing new API key from fresh account...")
        client = genai.Client(api_key=api_key)

        response = await client.aio.models.generate_content(
            model="models/gemini-2.5-flash",
            contents="Say 'API working' in 2 words."
        )

        print("SUCCESS: API key is working!")
        print(f"Response: {response.text}")
        print("\nQuota: AVAILABLE - Fresh account has full quota")
        return True

    except Exception as e:
        error_msg = str(e)
        print(f"ERROR: {type(e).__name__}")

        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            print("QUOTA EXCEEDED: Even this new key has no quota")
        elif "401" in error_msg or "UNAUTHENTICATED" in error_msg:
            print("INVALID KEY: API key is not valid")
        elif "404" in error_msg:
            print("MODEL NOT FOUND: Check model name")
        else:
            print(f"Error: {error_msg[:300]}")

        return False

if __name__ == "__main__":
    result = asyncio.run(test_api())
    print(f"\nResult: {'PASSED - Ready to use' if result else 'FAILED - Need different key'}")
