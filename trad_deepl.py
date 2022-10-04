import deepl
import streamlit as st

translator = deepl.Translator(st.secrets["DEEPL_KEY"])


def traduction(text, source_language, target_language):
    result = translator.translate_text(
        text, source_lang=source_language, target_lang=target_language
    )
    return result.text


if __name__ == "__main__":
    print(traduction("1 egg", "EN", "FR"))
