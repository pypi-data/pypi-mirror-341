# batch6_musigma/grok_chat.py

import os
from groq import Groq, GroqError


try:
    client = Groq(
        api_key="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"
    )
except GroqError as e:
    print(f"Failed to initialize Groq client: {e}")
    client = None

def chat_with_grok(prompt: str, model: str = "llama3-8b-8192") -> str:
    """
    Sends a prompt to the Groq API using the specified model and returns the response.

    Args:
        prompt: The input text/prompt for the Groq model.
        model: The model identifier to use (e.g., "llama3-8b-8192", "mixtral-8x7b-32768").
               Defaults to "llama3-8b-8192".

    Returns:
        The response content string from the Groq model.

    Raises:
        RuntimeError: If the Groq client failed to initialize.
        GroqError: If the API call fails for reasons like invalid API key,
                   rate limits, server errors, etc.
        ValueError: If the API response structure is unexpected.
    """
    if client is None:
        raise RuntimeError("Groq client is not initialized. Check API key or initialization errors.")

    try:
        print(f"Sending prompt to Groq API (model: {model})...")
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
            # You can add other parameters like temperature, max_tokens here
            # temperature=0.7,
            # max_tokens=1024,
        )

        # Extract the response content
        if chat_completion.choices and len(chat_completion.choices) > 0:
            response_content = chat_completion.choices[0].message.content
            if response_content:
                return response_content.strip()
            else:
                raise ValueError("Received an empty response content from Groq API.")
        else:
            raise ValueError("Invalid response structure received from Groq API (no choices).")

    except GroqError as e:
        print(f"Error during Groq API request: {e}")
        # You could check e.status_code, e.type, etc. for more specific handling
        raise # Re-raise the GroqError after logging
    except Exception as e:
        # Catch other potential errors during processing
        print(f"An unexpected error occurred: {e}")
        raise

if __name__ == '__main__':
    # Example usage when running the script directly
    # Make sure GROQ_API_KEY environment variable is set before running this.

    user_prompt = "Explain the concept of Large Language Models in simple terms."
    try:
        # You can specify a different model if needed, e.g., "mixtral-8x7b-32768"
        response = chat_with_grok(user_prompt, model="llama3-8b-8192")
        print("-" * 20)
        print(f"User: {user_prompt}")
        print("-" * 20)
        print(f"Groq: {response}")
        print("-" * 20)
    except (RuntimeError, GroqError, ValueError) as e:
        print(f"Failed to get response from Groq: {e}")
