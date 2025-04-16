import asyncio
import json

import aiohttp
import nest_asyncio
import pandas as pd
from tqdm import tqdm

nest_asyncio.apply()


"""BatchCaller class defining the class for making batch API calls to OpenAI, Azure OpenAI, or Groq."""


class BatchCaller:
    def __init__(
        self,
        provider: str = "openai",
        key: str | None = None,
        model: str = "gpt-4o-mini",
        url: str | None = None,
    ):
        self.provider = provider
        self.key = key
        self.model = model
        self.url = self._get_url(url)

    def _get_url(self, url):
        if self.provider == "openai":
            return "https://api.openai.com/v1/chat/completions"
        elif self.provider == "groq":
            return "https://api.groq.com/openai/v1/chat/completions"
        return url

    def _format_input(self, row, column_inputs):
        return "\n".join(f"{col}: {row[col]}" for col in column_inputs if col in row)

    async def _call_api_with_retries(self, session, payload, headers):
        for attempt in range(self.retries):
            try:
                async with session.post(
                    self.url, headers=headers, json=payload, timeout=self.timeout
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        content = data["choices"][0]["message"]["content"]
                        if "response_format" in payload and isinstance(
                            payload["response_format"], dict
                        ):
                            return json.loads(content)
                        return content
                    raise Exception(
                        f"API error {response.status}: {await response.text()}"
                    )
            except Exception as e:
                if attempt == self.retries - 1:
                    print(f"Final failure after {self.retries} retries: {e}")
                    return None
                await asyncio.sleep(1)

    async def _make_batch_calls(self, list_inputs):
        results = [None] * len(list_inputs)

        async with aiohttp.ClientSession() as session:
            with tqdm(total=len(list_inputs), desc="Processing", unit="req") as pbar:
                for i in range(0, len(list_inputs), self.batch_size):
                    batch = list_inputs[i : i + self.batch_size]
                    tasks = []

                    for idx, input_text in enumerate(batch, start=i):
                        messages = [
                            {"role": "system", "content": self.system_prompt},
                            {"role": "user", "content": input_text},
                        ]

                        headers = {
                            "Authorization": f"Bearer {self.key}"
                            if self.provider in ["openai", "groq"]
                            else None,
                            "api-key": self.key
                            if self.provider == "azure_openai"
                            else None,
                            "Content-Type": "application/json",
                        }
                        headers = {k: v for k, v in headers.items() if v is not None}

                        payload = {
                            "messages": messages,
                            "temperature": self.temperature,
                            "max_tokens": self.max_tokens,
                        }

                        if self.provider in ["openai", "groq"]:
                            payload["model"] = self.model

                        if self.json_mode:
                            payload["response_format"] = (
                                {"type": "json_object"}
                                if self.provider != "azure_openai"
                                else "json_object"
                            )

                        task = self._call_api_with_retries(session, payload, headers)
                        tasks.append(task)

                    responses = await asyncio.gather(*tasks)
                    results[i : i + len(batch)] = responses
                    pbar.update(len(batch))

                    if i + self.batch_size < len(list_inputs):
                        await asyncio.sleep(self.sleep_time)

        return results

    def _run_async(self, coro):
        try:
            return asyncio.run(coro)
        except RuntimeError as e:
            if "asyncio.run() cannot be called from a running event loop" in str(e):
                nest_asyncio.apply()
                return asyncio.get_event_loop().run_until_complete(coro)
            else:
                raise

    def get_response(
        self,
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
    ):
        self.system_prompt = system_prompt
        self.json_mode = json_mode
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.batch_size = batch_size
        self.timeout = timeout
        self.sleep_time = sleep_time
        self.retries = retries

        """
        system_prompt: str: The system prompt to be used for the API call.
        df: pd.DataFrame: The input or original DataFrame.
        column_inputs: list: The list of columns to be used as inputs for the API call (Context for the LLM).
        column_output_name: str: The name of the column to store the results.
        json_mode: bool: If True, the output will be in JSON format. extra info of JSON mode at https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/json-mode?tabs=python
        temperature: float: The temperature parameter for the API call.
        max_tokens: int: The maximum number of tokens for the API call.
        batch_size: int: The size of the batch for the API call (important to use in accordance to the provider TPM limits). Try creating pools for higher TPM
        timeout: float: The timeout for the API call
        sleep_time: float: The sleep time between batches.
        retries: int: The number of retries for the API call before surrender and returning None.
        """

        list_inputs = [
            self._format_input(row, column_inputs) for _, row in df.iterrows()
        ]
        results = self._run_async(self._make_batch_calls(list_inputs))
        df[column_output_name] = results
        return df
