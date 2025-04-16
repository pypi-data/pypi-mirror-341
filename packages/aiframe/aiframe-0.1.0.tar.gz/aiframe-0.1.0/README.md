# 🚀 AIFrame: Clean Your Datasets with AI Magic ✨

![alt text](image.png)

AIFrame is a Python library designed to help you clean and transform datasets effortlessly using the power of Large Language Models (LLMs) on steroids. Improve your entire dataframe data in one shot. Whether you're standardizing formats, rewriting text, or fixing messy columns — AIFrame makes it easy with batch processing and smart prompting. 🧹🤖

## 🔌 Supported Providers
You can plug in your favorite LLM APIs:

- 🧠 OpenAI (Text + JSON)

- ☁️ Azure OpenAI (Text + JSON)

- ⚡️ Groq (Text + JSON)

## 🧑‍💻 Quick Start and Prompt Flexibility

**Installation:**
```bash
pip install aiframe
```

In this example we use OpenAI API to convert numeric ages to plain text:

```python
from aiframe import BatchCaller

system_prompt = (
    "You are a helpful assistant. Please write the age down in normal text. "
    "Only output the text version of the age, no extra commentary."
)
column_inputs = ["age", "city"]

# Using OpenAI
if openai_api_key:
    openai_caller = BatchCaller(
        provider="openai",
        key=openai_api_key,
    )
    
    df_with_results = openai_caller.get_response(
        system_prompt,
        test_df,
        column_inputs,
        column_output_name = "TestOpenAI"
    )
    
    print(df_with_results)
```

# Classes and Methods


## 🧠 Class: BatchCaller
BatchCaller is a Python class for making efficient, reliable batch API calls to language model providers including OpenAI, Azure OpenAI, and Groq. It is designed to process DataFrame rows in bulk while managing retries, batching, timeouts, and JSON formatting.

```python
BatchCaller(
    provider: str = "openai",
    key: str | None = None,
    model: str = "gpt-4o-mini",
    url: str | None = None,
)
```

**Parameters:**

- provider (str): One of "openai", "azure_openai", or "groq". Default is "openai".

- key (str | None): API key used for authentication.

- model (str): Model name to be used (e.g., "gpt-4", "gpt-4o", "mixtral-8x7b").

- url (str | None): Optional custom endpoint for API calls. Defaults to standard provider endpoints.

## 🔁 Method: get_response

Executes batch API calls using the inputs from a pandas DataFrame and stores the AI-generated results in a new column.

```python
get_response(
    system_prompt: str,
    df: pd.DataFrame,
    column_inputs: list,
    column_output_name: str = "ai_result",
    json_mode: bool = False,
    temperature: float = 0,
    max_tokens: int = 8000,
    batch_size: int = 100,
    timeout: float = 20,
    sleep_time: float = 30,
    retries: int = 3,
) -> pd.DataFrame
```


**Parameters:**

- system_prompt (str): The prompt to guide the LLM’s behavior (set as the system message).

- df (pd.DataFrame): Input DataFrame containing rows to be processed.

- column_inputs (list): Column names used to construct the input context for each row.

- column_output_name (str): Name of the new column to store results. Default: "ai_result".

- json_mode (bool): If True, attempts to parse and return structured JSON responses.
🔗 JSON mode reference

- temperature (float): Controls randomness of the output. Lower values are more deterministic.

- max_tokens (int): Maximum number of tokens in the response.

- batch_size (int): Number of inputs to send per API call batch. (Should be tunned to be optimal for TPM capacity of the LLM provider)

- timeout (float): Timeout (in seconds) per request.

- sleep_time (float): Wait time (in seconds) between batches to respect rate limits.

- retries (int): Number of retry attempts per request before returning None.


**Returns:**

A copy of the input DataFrame with an added column containing the AI-generated results.



## ⚙️ Advanced Configuration
Want more control over the prompts, temperature, or batch size?
Check out tests/number_to_text_advanced_config.py
to see how to fine-tune LLM parameters and other advanced options. 🎛️


Extremely suggested: Create LLM pools to increase TPM (Throughput) to load even faster.


