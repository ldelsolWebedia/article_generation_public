import streamlit as st
from bokeh.models import CustomJS
from bokeh.models.widgets import Button
from streamlit_bokeh_events import streamlit_bokeh_events

import GPT3
import scraping.scraping_metacritic as scraping_metacritic
import scraping.scraping_senscritique as scraping_senscritique
import trad_deepl

st.set_page_config(
    page_title="Générateur de fiche jeux vidéo", page_icon=":video_game:",
)

if "first_time" not in st.session_state:
    st.session_state["first_time"] = True

st.title("🎮 Générateur de fiche jeux vidéo")

with st.expander("ℹ️ - About this app", expanded=True):

    st.write(
        """     
-   Cette application permet de générer une ébauche de fiche jeux vidéo à partir d'un jeu choisi.
-   La fiche se génère automatiquement dès que vous rentrez un nom de jeu.
-   Vous pouvez recharger une partie de la fiche si elle vous déplait en appuyant sur le bouton juste au dessus du paragraphe.
-   Pour copier l'article généré appuyez sur le bouton 'Copier l'article' en dessous de l'article.
-   Pour plus d'informations : https://www.notion.so/webedia-group/G-n-rateur-de-fiche-jeux-vid-o-8cd2d605f5664f2f9271b21267fc7ef8
	    """
    )

    st.markdown("")


def callback():
    st.session_state["first_time"] = True


st.write("### Entrez le sujet de la fiche jeux vidéo")
subject = st.text_input("Sujet", on_change=callback)

with st.sidebar:
    st.write("## Caractéristiques de GPT 3")
    temperature = st.slider(
        "Temperature : La température correspond à la créativité de GPT3, plus elle sera élevée et plus GPT3 innovera.",
        min_value=0.00,
        max_value=1.00,
        value=0.70,
        step=0.01,
    )
    top_p = st.slider(
        "Top p : Le top P est une alternative à la température. Attention, il ne faut pas utiliser les deux en même temps. Si on modifie l’un, il faut mettre l’autre à 1.",
        min_value=0.00,
        max_value=1.00,
        value=1.00,
        step=0.01,
    )
    frequency_penalty = st.slider(
        "Frequency penalty : La frequency penalty fonctionne en diminuant les chances qu'un mot soit sélectionné à nouveau plus il a été utilisé de fois.",
        min_value=0.00,
        max_value=2.00,
        value=0.20,
        step=0.01,
    )
    presence_penalty = st.slider(
        "Presence_penalty : La presence penalty fonctionne en diminuant les chances qu'un thème soit sélectionné à nouveau plus il a été utilisé de fois.",
        min_value=0.00,
        max_value=2.00,
        value=2.00,
        step=0.01,
    )

if subject != "":

    st.write("## " + subject + " :")

    if st.session_state["first_time"]:
        st.session_state["features"] = scraping_senscritique.get_JV_features(subject)
    st.write(st.session_state["features"])

    if st.button("🔄 Résumé") or st.session_state["first_time"]:
        summary = scraping_metacritic.get_JV_summary(subject)
        summary_paraph = GPT3.gen_article(
            "Paraphrase the following paragraph, using as few words from the original paragraph as possible:"
            + "\n\n"
            + summary,
            2000,
            temperature,
            top_p,
            frequency_penalty,
            presence_penalty,
        )[0]
        st.session_state["summary"] = trad_deepl.traduction(summary_paraph, "EN", "FR")
    st.write(st.session_state["summary"])

    st.session_state["text_to_be_copied"] = (
        "## "
        + subject
        + " :"
        + "\n\n"
        + st.session_state["features"]
        + st.session_state["summary"]
    )

    copy_button = Button(label="Copier l'article")
    copy_button.js_on_event(
        "button_click",
        CustomJS(
            args={"text": st.session_state["text_to_be_copied"]},
            code="""
        navigator.clipboard.writeText(text);
        """,
        ),
    )

    no_event = streamlit_bokeh_events(
        copy_button,
        events="GET_TEXT",
        key="get_text",
        refresh_on_update=True,
        override_height=75,
        debounce_time=0,
    )

    st.session_state["first_time"] = False
