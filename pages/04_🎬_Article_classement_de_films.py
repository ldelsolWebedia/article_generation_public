import pyperclip
import streamlit as st

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
-   Pour copier l'article généré appuyez sur le bouton 'Copier l'article'.
	    """
    )

    st.markdown("")


def callback():
    st.session_state["launch"] = True


col1, col2, col3, col4 = st.columns(4)

with col1:
    nb_entities = st.slider("How old are you?", 1, 10, 5)
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

if st.button("Copier l'article"):
    if "article" in st.session_state:
        pyperclip.copy(st.session_state["article"])
    else:
        st.write("## Erreur : Il n'y a pas d'article à copier")

if st.session_state["launch"]:
    st.session_state["article"] = gen_movie_list_article.gen_movie_article(
        nb_entities, entity_type, genre, provider
    )
    st.session_state["launch"] = False

if "article" in st.session_state:
    st.write(st.session_state["article"])
