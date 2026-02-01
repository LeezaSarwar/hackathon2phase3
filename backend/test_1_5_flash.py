"""Test gemini-1.5-flash model with current API key"""
import asyncio
from google import genai

async def test_model():
    api_key = "AIzaSyD5l-DhQjmI0ErI3i_dupiXC22NM7fU4ZY"

    try:
        print("Testing gemini-1.5-flash model...")
        client = genai.Client(api_key=api_key)

        response = await client.aio.models.generate_content(
            model="models/gemini-1.5-flash",
            contents="Say 'Working' in one word."
        )

        print("SUCCESS: gemini-1.5-flash is working!")
        print(f"Response: {response.text}")
        print("\nThis model has available quota!")
        return True

    except Exception as e:
        error_msg = str(e)
        print(f"ERROR: {type(e).__name__}")

        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            print("QUOTA EXCEEDED: gemini-1.5-flash also has no quota")
            if "1.5" in error_msg:
                print("Quota info found in error:")
                # Try to extract quota info
                if "limit:" in error_msg:
                    import re
                    limit_match = re.search(r'limit: (\d+)', error_msg)
                    if limit_match:
                        print(f"  Daily limit: {limit_match.group(1)} requests")
        elif "404" in error_msg:
            print("MODEL NOT FOUND: gemini-1.5-flash may not be available")
            print("Error details:", error_msg[:200])
        else:
            print(f"Unexpected error: {error_msg[:200]}")

        return False

if __name__ == "__main__":
    result = asyncio.run(test_model())
    print(f"\nTest result: {'PASSED' if result else 'FAILED'}")
