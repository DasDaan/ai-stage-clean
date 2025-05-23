import os
import asyncio  # Helps with running things at the same time
import traceback  # Gives more detailed information if something goes wrong
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get your API KEY and notify if it's missing
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("⚠️  WARNING: OPENAI_API_KEY is not found in .env file")

# Create OpenAI client
client = AsyncOpenAI(api_key=api_key)

# Function to validate if API key is working before starting the server
async def validate_api_key():
    try:
        # Send a tiny message to check the API key
        await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=1
        )
        print("✅ API KEY has been found and can be used")
        return True
    except Exception as e:
        print(f"[API Check] ❌ Invalid API key or other error: {e}")
        return False

# Function that sends a user message to OpenAI and returns the response
async def call_openai(message):
    try:
        # If the API key is missing, raise an error
        if not api_key:
            raise ValueError("Your OPENAI API key is missing. Check your .env file")
        

        print(f"[call_openai] Send to OpenAI: '{message[:30]}...'")

        # Call OpenAI and wait for the response
        completion = await asyncio.wait_for(
            client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": message}
                ]
            ),
            timeout=20  # timeout after 20 seconds
        )

        choices = completion.choices

        # Raise an error if the response is empty or invalid
        if not choices or not choices[0].message:
            raise ValueError("No valid response received from OpenAI.")

        # Extract and return the content
        response = choices[0].message.content.strip()
        print(f"[call_openai] Answer received: '{response[:60]}...'")
        return response

    except asyncio.TimeoutError:
        print("[call_openai] ❌ Timeout from OpenAI API.")
        return "⚠️ OpenAI API timed out. Please try again later."

    # General exception catch with traceback
    except Exception as e:
        print(f"[call_openai] ❌ Fout: {e}")
        print(traceback.format_exc())
        return f"⚠️ Error retrieving OpenAI response: {str(e)}"
