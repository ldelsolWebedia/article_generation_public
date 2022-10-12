import streamlit as st
import re
import wikipediaapi
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

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
-   Cette application permet de générer une ébauche de fiche people à partir d'un sujet choisi.
-   La fiche se génère automatiquement dès que vous rentrez un sujet.
-   Vous pouvez recharger une partie de la fiche si elle vous déplait en appuyant sur le bouton juste au dessus du paragraphe.
-   Pour copier l'article généré appuyez sur le bouton 'Copier l'article' en dessous de l'article.
-   La température correspond à la créativité de GPT3, plus elle sera élevée et plus GPT3 innovera.
-   Le top P est une alternative à la température. Attention, il ne faut pas utiliser les deux en même temps. Si on modifie l’un, il faut mettre l’autre à 1.
-   La frequency penalty fonctionne en diminuant les chances qu'un mot soit sélectionné à nouveau plus il a été utilisé de fois.
-   La presence penalty fonctionne en diminuant les chances qu'un thème soit sélectionné à nouveau plus il a été utilisé de fois.
	    """
    )

    st.markdown("")


def callback():
    st.session_state["first_time"] = True


st.write("### Entrez le sujet de la fiche people")
subject = st.text_input("Sujet", on_change=callback).title()

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

        st.session_state["info"] = GPT3.gen_article(
                "Ecris une liste en donnant dans l'ordre : la date de naissance, le métier, le signe astrologique, le pays de naissance, la ville de naissance de " 
                + subject
                + "\n\n"
                + "- Naissance :",
                2000,
                0.00,
                1.00,
                0.00,
                0.00,
            )[0]

    st.write("- Naissance :" + st.session_state["info"])

    if st.session_state["first_time"] or st.button("🔄 Biographie"):

        wiki = wikipediaapi.Wikipedia("en")

        page_wiki = wiki.page(subject.replace(" ", "_"))

        if not page_wiki.exists():
            st.write("Erreur : Il n'y a pas de page wikipédia pour " + subject)

        st.session_state["bio"] = ""
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
            st.session_state["bio"] += paraphrase_fr + "\n"

    st.write(st.session_state["bio"])

    st.session_state["text_to_be_copied"] = (
        "## " + subject + " :"
        + "\n\n"
        + "- Naissance :"
        + st.session_state["info"]
        + "\n"
        + st.session_state["bio"]
    )
    
    copy_button = Button(label="Copier l'article")
    copy_button.js_on_event("button_click", CustomJS(args={"text" : st.session_state["text_to_be_copied"]}, code="""
        navigator.clipboard.writeText(text);
        """))

    no_event = streamlit_bokeh_events(
        copy_button,
        events="GET_TEXT",
        key="get_text",
        refresh_on_update=True,
        override_height=75,
        debounce_time=0)

    st.session_state["first_time"] = False
