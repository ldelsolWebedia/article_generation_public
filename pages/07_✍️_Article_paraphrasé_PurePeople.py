import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

import GPT3
import scraping_bs4_purepeople
import trad_deepl

# Creation of a streamlit application to generated an article from a 750g recipe.

st.set_page_config(
    page_title="Générateur d'article paraphrasé PurePeople", page_icon="✍️",
)

if "first_time" not in st.session_state:
    st.session_state["first_time"] = True

st.title("✍️ Générateur d'article paraphrasé PurePeople")

with st.expander("ℹ️ - About this app", expanded=True):

    st.write(
        """     
-   Cette application permet de paraphraser un article de PurePeople à partir de son lien.
-   L'article se génère automatiquement dès que vous entrez une URL.
-   Vous pouvez recharger une partie de l'article si elle vous déplait en appuyant sur le bouton juste au dessus du paragraphe.
-   Pour copier l'article généré appuyez sur le bouton 'Copier l'article' en dessous de l'article.
-   La température correspond à la créativité de GPT3, plus elle sera élevée et plus GPT3 innovera.
-   Le top P est une alternative à la température. Attention, il ne faut pas utiliser les deux en même temps. Si on modifie l’un, il faut mettre l’autre à 1.
-   La frequency penalty fonctionne en diminuant les chances qu'un mot soit sélectionné à nouveau plus il a été utilisé de fois.
-   La presence penalty fonctionne en diminuant les chances qu'un thème soit sélectionné à nouveau plus il a été utilisé de fois.
-   Vous pouvez essayer l'application avec cette URL : https://www.purepeople.com/article/-elle-est-belle-gad-elmaleh-face-a-son-ex-charlotte-casiraghi-ses-details-croustillants-sur-sa-vie-a-monaco_a499708/1
	    """
    )

    st.markdown("")


def callback():
    st.session_state["first_time"] = True

def parafrase(title,text) :
    st.write(f"## {title} :")
    if st.button(f"🔄 {title}") or st.session_state["first_time"]:
        parafrase_text = GPT3.gen_article(
            "Paraphrase the following paragraph, using as few words from the original paragraph as possible:"
            + "\n\n"
            + trad_deepl.traduction(text, "FR", "EN-GB"),
            2000,
            temperature,
            top_p,
            frequency_penalty,
            presence_penalty,
        )[0]
        st.session_state[title] = trad_deepl.traduction(parafrase_text, "EN", "FR")

    st.write(st.session_state[title])


st.write("### Entrez l'URL d'un article PurePeople")
url = st.text_input("URL", on_change=callback)
# url = "https://www.purepeople.com/article/-elle-est-belle-gad-elmaleh-face-a-son-ex-charlotte-casiraghi-ses-details-croustillants-sur-sa-vie-a-monaco_a499708/1"

with st.sidebar:
    st.write("## Caractéristiques de GPT 3")
    temperature = st.slider(
        "temperature", min_value=0.00, max_value=1.00, value=0.70, step=0.01
    )
    top_p = st.slider("top_p", min_value=0.00, max_value=1.00, value=1.00, step=0.01)
    frequency_penalty = st.slider(
        "frequency_penalty", min_value=0.00, max_value=2.00, value=0.20, step=0.01
    )
    presence_penalty = st.slider(
        "presence_penalty", min_value=0.00, max_value=2.00, value=2.00, step=0.01
    )

if url != "":

    if st.session_state["first_time"]:
        st.session_state["scrap_article"] = scraping_bs4_purepeople.get_article(url)

    parafrase("Titre",st.session_state["scrap_article"]["title"])
    parafrase("Résumé",st.session_state["scrap_article"]["summary"])
    paragraphe = st.session_state["scrap_article"]["main_text"].split("\n")
    for i,el in enumerate([el for el in paragraphe if el != '']) :
        parafrase(f"Paragraphe {i+1}",el)

    st.session_state["text_to_be_copied"] = (
        st.session_state["Titre"]
        + st.session_state["Résumé"]
    )

    for i in range(len([el for el in paragraphe if el != ''])) :
        st.session_state["text_to_be_copied"] += st.session_state[f"Paragraphe {i+1}"]

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
