import streamlit as st
from bokeh.models import CustomJS
from bokeh.models.widgets import Button
from streamlit_bokeh_events import streamlit_bokeh_events

import GPT3
import scraping.scraping_selenium_PAA as scraping_selenium_PAA

st.set_page_config(
    page_title="Générateur d'article FAQ", page_icon=":green_apple:",
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
-   Pour copier l'article généré appuyez sur le bouton 'Copier l'article' en dessous de l'article.
-   Pour plus d'informations : https://www.notion.so/webedia-group/G-n-rateur-d-article-FAQ-ba05125db62c448bbc24b874d1a2849e
	    """
    )

    st.markdown("")


def callback():
    st.session_state["first_time"] = True


st.write("### Entrez le sujet de l'article")
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
    nb_layer = st.slider(
        "Nombre de couches : correspond au nombre de couches de “People Also Ask” qui vont être utilisées pour générer l’article. 1 ≃ 4 questions; 2 ≃ 12 questions.",
        min_value=1,
        max_value=2,
        value=1,
        step=1,
    )

if subject != "":

    st.write("## Titres :")
    if st.button("🔄 Titres") or st.session_state["first_time"]:
        titles = GPT3.gen_article(
            "Ecris une liste de titres accrocheurs pour un article sur" + subject,
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
            1000,
            temperature,
            top_p,
            frequency_penalty,
        )[0]
        st.session_state["Introduction"] = introduction
    st.write(st.session_state["Introduction"])

    if st.session_state["first_time"]:
        st.session_state["PAA"] = scraping_selenium_PAA.get_PAA(subject, nb_layer)

    for i, el in enumerate(st.session_state["PAA"]):
        if nb_layer == 2 and i == 4:
            st.write("# Question de niveau 2")
        st.write("## " + el["title"] + " :\n")
        if st.button("🔄 " + el["title"]) or st.session_state["first_time"]:
            answer = GPT3.gen_article(
                el["title"]
                + ">Ecris un long paragraphe pour répondre à cette question.",
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
            1000,
            temperature,
            top_p,
            frequency_penalty,
        )[0]
        st.session_state["Conclusion"] = conclusion
    st.write(st.session_state["Conclusion"])

    st.session_state["text_to_be_copied"] = (
        "## Titres :"
        + st.session_state["Titles"]
        + "## Introduction :"
        + st.session_state["Introduction"]
    )
    for el in st.session_state["PAA"]:
        st.session_state["text_to_be_copied"] += "## " + el["title"] + " :\n"
        st.session_state["text_to_be_copied"] += st.session_state[el["title"]] + "\n\n"
    st.session_state["text_to_be_copied"] += (
        "## Conclusion :" + st.session_state["Conclusion"]
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
