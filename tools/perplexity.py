import os
import aiohttp
import asyncio
from colorama import Fore

PERPLEXITY_API_KEY = os.environ["PERPLEXITY_API_KEY"]

async def ask_perplexity(parameters: dict):
    print(Fore.MAGENTA + '[TOOL EXECUTION] askPerplexity')
    question = parameters.get("input")
    if not question:
        return "No question provided to Perplexity tool."

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar-pro",
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": question}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }

    # Use aiohttp.ClientSession for making asynchronous requests
    # The 'async with' statement ensures the session is properly closed.
    async with aiohttp.ClientSession() as session:
        try:
            # Use await with session.post() to make the asynchronous request
            async with session.post(url, headers=headers, json=payload) as response:
                # raise_for_status() will raise an exception for 4xx/5xx responses
                response.raise_for_status()
                # Await the .json() call as it's also an async operation
                response_data = await response.json()
                return response_data["choices"][0]["message"]["content"]
        except aiohttp.ClientError as e:
            # Catch aiohttp specific errors (e.g., network issues, bad status codes)
            print(f"Error querying Perplexity AI: {e}")
            return f"An error occurred while contacting Perplexity AI: {e}"
        except KeyError as e:
            # Handle cases where the expected keys are missing from the JSON response
            print(f"Unexpected response format from Perplexity AI: {e}")
            return "An unexpected response format was received from Perplexity AI."
        


# --- Main execution block for testing ---
async def main():
    print("--- Starting Perplexity Debug Test ---")

    # Test Case 1: Valid question
    test_params_1 = {"question": "What is the capital of France?"}
    print(f"\nTesting with: {test_params_1['question']}")
    result_1 = await ask_perplexity(test_params_1)
    print(f"Result 1: {result_1}")

    # Test Case 2: No question provided
    test_params_2 = {"input": None} # Or an empty dict {}
    print(f"\nTesting with: {test_params_2}")
    result_2 = await ask_perplexity(test_params_2)
    print(f"Result 2: {result_2}")

    # Test Case 3: A different question
    test_params_3 = {"message": "Tell me a short fact about space."}
    print(f"\nTesting with: {test_params_3['message']}")
    result_3 = await ask_perplexity(test_params_3)
    print(f"Result 3: {result_3}")

    print("\n--- Perplexity Debug Test Finished ---")


if __name__ == "__main__":
    if not PERPLEXITY_API_KEY:
        print("ERROR: PERPLEXITY_API_KEY environment variable is not set.")
        print("Please set it before running this script.")
    else:
        asyncio.run(main()) # This runs your async main function