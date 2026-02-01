import asyncio
from google import genai

async def list_models():
    client = genai.Client(api_key="AIzaSyBftZdwXxtooXuKbbu7I63JItkZv0DEkYg")

    print("\n" + "="*60)
    print("Available Gemini Models:")
    print("="*60)

    try:
        models = await client.aio.models.list()

        working_models = []
        for model in models:
            print(f"\nModel: {model.name}")
            working_models.append(model.name)

        print("\n" + "="*60)
        print(f"Total models found: {len(working_models)}")
        print("="*60)

        if working_models:
            print(f"\nFirst working model: {working_models[0]}")
            return working_models[0]
        else:
            print("\nNo models found!")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    result = asyncio.run(list_models())
    if result:
        print(f"\n✅ Use this model: {result}")
