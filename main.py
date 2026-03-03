import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function

def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Missing GEMINI_API-KEY in .env")
    
    parser = argparse.ArgumentParser(description="Gemini AI agent project")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model = "gemini-2.5-flash", 
        contents = messages,
        config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt, temperature=0),
    )
    if response.usage_metadata == None:
        raise RuntimeError("No token usage; perhaps a failed API request")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.function_calls:
        function_responses = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)
            if len(function_call_result.parts) == 0 or function_call_result.parts[0].function_response == None or function_call_result.parts[0].function_response.response == None:
                raise Exception("Invalid function call result")
            else: function_responses.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    if not response.function_calls:
        print(response.text)

if __name__ == "__main__":
    main()
