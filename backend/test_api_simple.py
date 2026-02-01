"""Simple test for Gemini API key"""
import asyncio
from google import genai

async def test_api():
    api_key = "AIzaSyBEas_qKqyAM3QrItJTSyMmX4WFTtFZdCI"

    try:
        print("Testing Gemini API...")
        client = genai.Client(api_key=api_key)

        response = await client.aio.models.generate_content(
            model="models/gemini-2.5-flash",
            contents="Say hello in one word."
        )

        print("SUCCESS: API key is working")
        print(f"Response: {response.text}")
        return True

    except Exception as e:
        print(f"ERROR: {type(e).__name__}")
        print(f"Message: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_api())
    print(f"\nTest result: {'PASSED' if result else 'FAILED'}")
