import openai
import streamlit as st
from icecream import ic

import trad_deepl

openai.api_key = st.secrets["API_KEY"]
completion = openai.Completion()


def gen_article(
    instructions,
    input,
    prompt_tokens=0,
    temperature_chosen=0.70,
    top_p_chosen=1.00,
    frequency_penalty_chosen=0.20,
):
    if prompt_tokens >= 4000:
        return ("No tokens left", 4000)
    if input is None:
        prompt_chosen = instructions
    else:
        prompt_chosen = input + "\n\n" + instructions
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt_chosen,
        temperature=temperature_chosen,
        max_tokens=4000 - prompt_tokens,
        top_p=top_p_chosen,
        frequency_penalty=frequency_penalty_chosen,
        presence_penalty=0,
    )
    return (response["choices"][0]["text"], response["usage"]["total_tokens"])


if __name__ == "__main__":
    instructions = (
        "write a long article inspired by this text, you can add some informations"
    )
    input = """
    Pour cette recette, votre beurre doit être bien mou.
    Dans un bol, mélangez beurre, œuf, sucre et sucre vanillé. Ajoutez la farine, le sel et la levure petit à petit et mélangez. Ajoutez les pépites de chocolat et mélangez.
    Faites de petites boules, mettez-les sur une plaque de cuisson recouverte de papier sulfurisé et aplatissez-les très légèrement.
    Enfournez à 180°C pendant 10 à 12 min (suivant la texture que vous désirez, moi j'aime quand c'est très moelleux). Laissez refroidir sur une grille.
    """
    text, nb = gen_article(
        instructions, trad_deepl.traduction(input, "FR", "EN-GB"), 3000
    )
    ic(nb)
