import os

from dotenv import load_dotenv

from aiframe import BatchCaller
from tests.test_df import test_df

# Load the .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
openai_api_key = os.getenv("OPENAI_KEY")
# Get the Azure OpenAI API key from the environment variable
azure_openai_api_key = os.getenv("AZURE_OPENAI_KEY")
# Get the Azure OpenAI endpoint from the environment variable
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
# get groq api key from the environment variable
groq_api_key = os.getenv("GROQ_API_KEY")
groq_model = "llama3-70b-8192"

print(f"OpenAI API Key: {openai_api_key}")
print(azure_openai_api_key)
print(azure_openai_endpoint)
print(groq_api_key)


# Example usage
if __name__ == "__main__":
    system_prompt = "You are a helpful assistant. Please write the age down to normal text, just output the text version of the age, do not output any extra thoughts"
    column_inputs = ["age"]

    # With OpenAI
    if openai_api_key:
        openai_caller = BatchCaller(
            provider="openai",
            key=openai_api_key,
        )
        # With Openai
        df_with_results = openai_caller.get_response(
            system_prompt=system_prompt,
            df=test_df,
            column_inputs=column_inputs,
            column_output_name="TestOpenai",
            json_mode=False,
            temperature=0.5,
            max_tokens=100,
            batch_size=10,
            sleep_time=10,
            retries=3,
        )
        print(df_with_results)

    # With Azure OpenAI
    if azure_openai_api_key and azure_openai_endpoint:
        # With Azure OpenAI
        azure_openai_caller = BatchCaller(
            provider="azure_openai", key=azure_openai_api_key, url=azure_openai_endpoint
        )

        df_with_results = azure_openai_caller.get_response(
            system_prompt=system_prompt,
            df=test_df,
            column_inputs=column_inputs,
            column_output_name="TestAzureOpenai",
            json_mode=False,
            temperature=0.5,
            max_tokens=100,
            batch_size=10,
            sleep_time=10,
            retries=3,
        )
        print(df_with_results)

    # With Groq
    if groq_api_key:
        groq_caller = BatchCaller(provider="groq", key=groq_api_key, model=groq_model)

        df_with_results = groq_caller.get_response(
            system_prompt=system_prompt,
            df=test_df,
            column_inputs=column_inputs,
            column_output_name="TestGroq",
            json_mode=False,
            temperature=0.5,
            max_tokens=100,
            batch_size=10,
            sleep_time=10,
            retries=3,
        )
        print(df_with_results)
