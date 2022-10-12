import pyperclip
import streamlit as st
import re
import wikipediaapi

import trad_deepl
import GPT3

st.set_page_config(
    page_title="Générateur de fiche people", page_icon=":star2:",
)

if "first_time" not in st.session_state:
    st.session_state["first_time"] = True

st.title("🌟 Générateur de fiche people")

with st.expander("ℹ️ - About this app", expanded=True):

    st.write(
        """     
-   Cette application permet de générer une ébauche d'article FAQ à partir d'un sujet choisi.
-   L'article se génère automatiquement dès que vous rentrez un sujet.
-   Vous pouvez recharger une partie de l'article si elle vous déplait en appuyant sur le bouton juste au dessus du paragraphe.
-   Pour copier l'article généré appuyez sur le bouton 'Copier l'article'.
-   La température correspond à la créativité de GPT3, plus elle sera élevée et plus GPT3 innovera.
-   Le top P est une alternative à la température. Attention, il ne faut pas utiliser les deux en même temps. Si on modifie l’un, il faut mettre l’autre à 1.
-   La frequency penalty fonctionne en diminuant les chances qu'un mot soit sélectionné à nouveau plus il a été utilisé de fois.
-   nb_layer correspond au nombre de couches de “People Also Ask” qui vont être utilisées pour générer l’article. 1 ≃ 4 questions; 2 ≃ 12 questions.
-   Pour plus d'informations : https://www.notion.so/webedia-group/G-n-rateur-d-article-FAQ-26637257f41f40ceae8b6f310ee89e2c
	    """
    )

    st.markdown("")


def callback():
    st.session_state["first_time"] = True


st.write("### Entrez le sujet de la fiche people")
subject = st.text_input("Sujet", on_change=callback).title()

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
        "temperature", min_value=0.00, max_value=1.00, value=0.90, step=0.01
    )
    top_p = st.slider("top_p", min_value=0.00, max_value=1.00, value=1.00, step=0.01)
    frequency_penalty = st.slider(
        "frequency_penalty", min_value=0.00, max_value=2.00, value=2.00, step=0.01
    )
    presence_penalty = st.slider(
        "presence_penalty", min_value=0.00, max_value=2.00, value=2.00, step=0.01
    )

if subject != "":

    st.write("## " + subject + " :")
    if st.session_state["first_time"]:

        wiki = wikipediaapi.Wikipedia("en")

        page_wiki = wiki.page(subject.replace(" ", "_"))

        if not page_wiki.exists():
            st.write("Erreur : Il n'y a pas de page wikipédia pour " + subject)

        st.session_state["form"] = ""
        paragraph = re.findall(".*?(?=\.[A-Z][^.])|.*?\n", page_wiki.summary)
        paragraph = [el for el in paragraph if el != ""]
        for el in paragraph:
            paraphrase = GPT3.gen_article(
                "Paraphrase the following paragraph, using as few words from the original paragraph as possible:"
                + "\n\n"
                + el,
                2000,
                temperature,
                top_p,
                frequency_penalty,
                presence_penalty,
            )[0]
            paraphrase_fr = trad_deepl.traduction(paraphrase, "EN", "FR")
            st.session_state["form"] += paraphrase_fr + "\n\n"

    st.write(st.session_state["form"])

    st.session_state["first_time"] = False
