import openai
import streamlit as st

openai.api_key = st.secrets["API_KEY"]
completion = openai.Completion()


def gen_article(
    prompt_text,
    prompt_tokens=0,
    temperature_chosen=0.70,
    top_p_chosen=1.00,
    frequency_penalty_chosen=0.20,
    presence_penalty_chosen=0.00,
):

    """
    Function that generate a text with GPT3 from an input and an instruction

    Args:
        prompt_text (str): the input text for GPT3.
        prompt_tokens (int): number of tokens used for the prompt_text.
        temperature_chosen (float): The temperature corresponds to the creativity of GPT3, the higher it is, the more GPT3 will innovate.
        top_p_chosen (float): The top P is an alternative to the temperature. Be careful, you must not use both at the same time. If you change one, you must set the other to 1.
        frequency_penalty_chosen (float): The frequency penalty works by decreasing the chances that a word will be selected again the more times it has been used
        presence_penalty_chosen (float): The presence penalty works by decreasing the chances that a theme will be selected again the more times it has been used

    Returns:
        str: the text generated by GPT3
        int: the total number of tokens used
    """

    if prompt_tokens >= 4000:
        return ("No tokens left", 4000)
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt_text,
        temperature=temperature_chosen,
        max_tokens=4000 - prompt_tokens,
        top_p=top_p_chosen,
        frequency_penalty=frequency_penalty_chosen,
        presence_penalty=presence_penalty_chosen,
    )
    return (response["choices"][0]["text"], response["usage"]["total_tokens"])
