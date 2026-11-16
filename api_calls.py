import os
from google import genai
from openai import OpenAI
from anthropic import Anthropic



def run_gemini_call(prompt):
    client = genai.Client(api_key=os.environ["<REPLACE_WITH_AN_API_KEY>"])

    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=prompt
    )
    return interaction.output_text


def run_openai_call(prompt):
    client = OpenAI(api_key=os.environ["<REPLACE_WITH_AN_API_KEY>"])

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    return response.output_text


def run_claude_call(prompt):
    client = Anthropic(api_key=os.environ["<REPLACE_WITH_AN_API_KEY>"])

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.content[0].text


