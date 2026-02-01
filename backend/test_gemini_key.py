"""Test script to verify Gemini API key is working"""
import asyncio
from google import genai
from google.genai import types

async def test_gemini_api():
    """Test if the Gemini API key works"""
    api_key = "AIzaSyBEas_qKqyAM3QrItJTSyMmX4WFTtFZdCI"

    try:
        print("Testing Gemini API key...")
        client = genai.Client(api_key=api_key)

        # Simple test prompt
        response = await client.aio.models.generate_content(
            model="models/gemini-2.5-flash",
            contents="Say 'Hello, API key is working!' in one sentence."
        )

        print(f"✅ SUCCESS: {response.text}")
        return True

    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(test_gemini_api())
