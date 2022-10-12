import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

from article_films import gen_movie_list_article

st.set_page_config(
    page_title="Générateur d'article de classement de films/séries",
    page_icon=":clapper:",
)

if "launch" not in st.session_state:
    st.session_state["launch"] = False

st.title("🎬 Générateur d'article de classement de films/séries")

with st.expander("ℹ️ - About this app", expanded=True):

    st.write(
        """     
-   Cette application permet de générer une ébauche d'article de classement de films sur une plateforme
-   L'article se génère automatiquement dès que vous cliquez sur 'Lancer la génération'.
-   Si un article avec les mêmes paramètres que ceux sélectionnés a été déjà été généré il y a moins de 30 jours, alors il ne sera pas généré à nouveau.
-   Pour copier l'article généré appuyez sur le bouton 'Copier l'article' en dessous de l'article.
-   Pour plus d'informations : https://www.notion.so/webedia-group/NLG-PureBreak-5548ceb2db5941648f06e2a00fa0b4c5
	    """
    )

    st.markdown("")


def callback():
    st.session_state["launch"] = True


col1, col2, col3, col4 = st.columns(4)

with col1:
    nb_entities = st.slider("Nombre de films/séries", 1, 10, 5)
    st.button("Lancer la génération", on_click=callback)

with col2:
    entity_type = st.selectbox("Type", ("Film", "Série"))

with col3:
    genre = st.selectbox(
        "Genre",
        (
            "Action",
            "Adventure",
            "Animation",
            "Biopic",
            "Bollywood",
            "Cartoon",
            "Comedy",
            "ComedyDrama",
            "Concert",
            "Detective",
            "Documentary",
            "Drama",
            "Erotic",
            "Experimental",
            "Family",
            "Fantasy",
            "Historical",
            "HistoricalEpic",
            "Horror",
            "Judicial",
            "KoreanDrama",
            "MartialArts",
            "Medical",
            "Music",
            "Musical",
            "Opera",
            "Romance",
            "ScienceFiction",
            "Show",
            "SportEvent",
            "Spy",
            "Thriller",
            "Unknown",
            "WarMovie",
            "Western",
        ),
    )

with col4:
    provider = st.selectbox(
        "Fournisseur",
        (
            "Netflix France",
            "Amazon Prime Video",
            "Disney+",
            "Apple Tv+ France",
            "OCS",
            "MyCanal",
        ),
    )

if st.session_state["launch"]:
    st.session_state["article"] = gen_movie_list_article.gen_movie_article(
        nb_entities, entity_type, genre, provider
    )
    st.session_state["launch"] = False

if "article" in st.session_state:
    st.write(st.session_state["article"])
    
    copy_button = Button(label="Copier l'article")
    copy_button.js_on_event("button_click", CustomJS(args={"text" : st.session_state["article"]}, code="""
        navigator.clipboard.writeText(text);
        """))

    no_event = streamlit_bokeh_events(
        copy_button,
        events="GET_TEXT",
        key="get_text",
        refresh_on_update=True,
        override_height=75,
        debounce_time=0)
