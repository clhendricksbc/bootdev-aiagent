import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function
from config import MAX_ITERS

def main():
    parser = argparse.ArgumentParser(description="Gemini AI agent project")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API-KEY in .env")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(MAX_ITERS):
        response = client.models.generate_content(
            model = "gemini-2.5-flash", 
            contents = messages,
            config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt, temperature=0),
        )
        if not response.usage_metadata:
            raise RuntimeError("No token usage; Gemini API response appears to be malformed")
        
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        if not response.function_calls:
            print("Response:")
            print(response.text)
            return
        
        function_responses = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)
            if not function_call_result.parts or not function_call_result.parts[0].function_response or not function_call_result.parts[0].function_response.response:
                raise RuntimeError(f"Empty function response for {function_call.name}")
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])
        if response.function_calls:
            messages.append(types.Content(role="user", parts=function_responses))
    
    print(f"The agent exceeded the maximum number of iterations: {MAX_ITERS}")
    sys.exit(1)

if __name__ == "__main__":
    main()
