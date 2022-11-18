import deepl
import streamlit as st

translator = deepl.Translator(st.secrets["DEEPL_KEY"])


def traduction(text, source_language, target_language):

    """
    Function that translate a string in input to the specified language
    It uses deepl API

    Args:
        text (str): the text to translate
        source_language (str): origin language
        target_language (str): language to translate to

    Returns:
        str: the result of the translation
    """

    result = translator.translate_text(
        text, source_lang=source_language, target_lang=target_language
    )
    return result.text


if __name__ == "__main__":
    print(traduction("coche", "es", "fr"))
