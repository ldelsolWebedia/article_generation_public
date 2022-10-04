import pyperclip
import streamlit as st

import GPT3
import scraping_selenium

st.set_page_config(
    page_title="750g PAA food article generator",
    page_icon=":green_apple:",
)

if "first_time" not in st.session_state:
    st.session_state["first_time"] = True

st.title("🍏 Générateur d'article FAQ")

with st.expander("ℹ️ - About this app", expanded=True):

    st.write(
        """     
-   Cette application permet de générer une ébauche d'article FAQ à partir d'un sujet choisi.
-   L'article se génère automatiquement dès que vous rentrez un sujet.
-   Vous pouvez recharger une partie de l'article si elle vous déplait en appuyant sur le bouton juste au dessus du paragraphe.
-   Pour copier l'article généré appuyez sur le bouton 'Copier l'article'.
	    """
    )

    st.markdown("")


def callback():
    st.session_state["first_time"] = True


st.write("### Entrez le sujet de l'article")
subject = st.text_input("Sujet", on_change=callback)

if st.button("Copier l'article"):
    try:
        text_to_be_copied = (
            "## Titres :"
            + st.session_state["Titles"]
            + "## Introduction :"
            + st.session_state["Introduction"]
        )
        for el in st.session_state["PAA"]:
            text_to_be_copied += "## " + el["title"] + " :\n"
            text_to_be_copied += st.session_state[el["title"]] + "\n\n"
        text_to_be_copied += "## Conclusion :" + st.session_state["Conclusion"]
        pyperclip.copy(text_to_be_copied)
    except:
        st.write("## Erreur : Il n'y a pas d'article à copier")

with st.sidebar:
    st.write("## Caractéristiques de GPT 3")
    temperature = st.slider(
        "temperature", min_value=0.00, max_value=1.00, value=0.70, step=0.01
    )
    top_p = st.slider("top_p", min_value=0.00, max_value=1.00, value=1.00, step=0.01)
    frequency_penalty = st.slider(
        "frequency_penalty", min_value=0.00, max_value=2.00, value=0.20, step=0.01
    )
    nb_layer = st.slider("nb_layer", min_value=1, max_value=2, value=1, step=1)

if subject != "":

    st.write("## Titres :")
    if st.button("🔄 Titres") or st.session_state["first_time"]:
        titles = GPT3.gen_article(
            "Ecris une liste de titres accrocheurs pour un article sur" + subject,
            None,
            1000,
            temperature,
            top_p,
            frequency_penalty,
        )[0]
        st.session_state["Titles"] = titles
    st.write(st.session_state["Titles"])

    st.write("## Introduction :")
    if st.button("🔄 Introduction") or st.session_state["first_time"]:
        introduction = GPT3.gen_article(
            "Ecris une histoire racontant pourquoi quelqu'un devrait manger " + subject,
            None,
            1000,
            temperature,
            top_p,
            frequency_penalty,
        )[0]
        st.session_state["Introduction"] = introduction
    st.write(st.session_state["Introduction"])

    if st.session_state["first_time"]:
        st.session_state["PAA"] = scraping_selenium.get_PAA(subject, nb_layer)

    for el in st.session_state["PAA"]:
        st.write("## " + el["title"] + " :\n")
        if st.button("🔄 " + el["title"]) or st.session_state["first_time"]:
            answer = GPT3.gen_article(
                el["title"]
                + ">Ecris un long paragraphe pour répondre à cette question.",
                None,
                1000,
                temperature,
                top_p,
                frequency_penalty,
            )[0]
            section = GPT3.gen_article(
                el["title"]
                + ">Ecris un long paragraphe pour répondre à cette question."
                + answer
                + ">Argumente le paragraphe précédent.",
                None,
                1000,
                temperature,
                top_p,
                frequency_penalty,
            )[0]
            st.session_state[el["title"]] = section
        st.write(st.session_state[el["title"]])

    st.write("## Conclusion :")
    if st.button("🔄 Conclusion") or st.session_state["first_time"]:
        conclusion = GPT3.gen_article(
            "Ecris une conclusion à un article sur " + subject,
            None,
            1000,
            temperature,
            top_p,
            frequency_penalty,
        )[0]
        st.session_state["Conclusion"] = conclusion
    st.write(st.session_state["Conclusion"])

    st.session_state["first_time"] = False
