import aiohttp
import asyncio
import json
from colorama import Fore

async def crt_sh_lookup(parameters: dict) -> str:
    """
    Performs a certificate transparency lookup on crt.sh for a given query.

    Args:
        parameters (dict): A dictionary containing the query for crt.sh.
                           It expects a 'query' key.

    Returns:
        str: A JSON string of the lookup results from crt.sh, or an error message.
    """
    print(Fore.MAGENTA + '[TOOL EXECUTION] crtShLookup')
    query = parameters.get("query")
    if not query:
        return "No query provided for crt.sh lookup. Please provide a 'query' parameter."

    url = f"https://crt.sh/?q={query}&output=json"
    headers = {
        "User-Agent": "ElevenLabs-Agent-Server/1.0 (Certificate Transparency Lookup Tool)"
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, timeout=15) as response:
                response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

                # crt.sh returns a JSON array, even if empty or for errors sometimes.
                # We'll try to parse it and return as a formatted JSON string.
                data = await response.json()
                return json.dumps(data, indent=2)
        except aiohttp.ClientError as e:
            # Catch aiohttp specific errors (e.g., network issues, bad status codes)
            print(f"Network or request error during crt.sh lookup for '{query}': {e}")
            return f"An error occurred while contacting crt.sh: {e}"
        except json.JSONDecodeError:
            # Handle cases where the response is not valid JSON
            response_text = await response.text() if 'response' in locals() else "N/A"
            print(f"Failed to decode JSON response from crt.sh for '{query}'. Response content: {response_text}")
            return "Failed to decode JSON response from crt.sh. The response might not be valid JSON."
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred in crt_sh_lookup for '{query}': {e}")
            return f"An unexpected error occurred: {e}"

# --- Main execution block for testing (optional) ---
async def main():
    print("--- Starting crt.sh Lookup Tool Debug Test ---")

    # Test Case 1: Valid domain
    test_params_1 = {"query": "google.com"}
    print(f"\nTesting with: {test_params_1['query']}")
    result_1 = await crt_sh_lookup(test_params_1)
    print(f"Result 1 (first 500 chars):\n{result_1[:500]}...")

    # Test Case 2: Non-existent domain (should return empty array or specific error from crt.sh)
    test_params_2 = {"query": "nonexistentdomain12345.com"}
    print(f"\nTesting with: {test_params_2['query']}")
    result_2 = await crt_sh_lookup(test_params_2)
    print(f"Result 2:\n{result_2}")

    # Test Case 3: No query provided
    test_params_3 = {}
    print(f"\nTesting with: {test_params_3}")
    result_3 = await crt_sh_lookup(test_params_3)
    print(f"Result 3:\n{result_3}")

    print("\n--- crt.sh Lookup Tool Debug Test Finished ---")

if __name__ == "__main__":
    # This block allows you to run this file directly to test the function.
    asyncio.run(main())