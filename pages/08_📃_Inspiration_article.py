import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

import scraping.scraping_sitemap as scraping_sitemap
import scraping.scraping_bs4_article as scraping_bs4_article
import GPT3
import deepl

# Creation of a streamlit application to generated an article from a 750g recipe.

translator = deepl.Translator(st.secrets["DEEPL_KEY"])

st.set_page_config(
    page_title="Inspiration article jeux vidéo/cinéma", page_icon="📃",
    layout="wide",
)

if "first_time" not in st.session_state:
    st.session_state["first_time"] = True
    st.session_state["paragraphe_list"] = []
    st.session_state["text_to_be_copied"] = ""

st.title("📃 Inspiration article jeux vidéo/cinéma")

with st.expander("ℹ️ - About this app", expanded=True):

    st.write(
        """     
-   Cette application permet de paraphraser des articles provenant d'autres sites appartenant à Webedia traitant d'un thème commun.
-   En ouvrant l'application la liste des 10 derniers articles écrit par les sites séléctionnés est affiché.
-   En cliquant sur un article de la liste le lien pour aller consulter cet article apparaitra pour que vous le consultiez.
-   Lorsque vous le consultez, vous avez la possibilitée de traduire l'article avec l'outil google translate associé à google chrome.
-   Si vous souhaitez paraphraser l'article séléctionné, vous pouvez appuyer sur le bouton "paraphraser l'article".
-   Vous pouvez recharger une partie de l'article si elle vous déplait en appuyant sur le bouton juste au dessus du paragraphe.
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

col1, col2, col3 = st.columns(3)

with col1:
    nb_entities = st.slider("Nombre d'articles", 1, 50, 10)
    if st.button("Rafraichir la liste d'articles") :
        st.session_state["first_time"] = True

with col2:
    entity = st.text_input("Mot à filtrer",on_change=callback)

with col3:
    theme = st.selectbox("Thème",('Jeux vidéo','Cinéma'),on_change=callback)


def aggrid_interactive_table(df):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="alpine",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
        columns_auto_size_mode="FIT_CONTENTS",
    )

    return selection

def parafrase(title,text) :
    st.write(f"## {title} :")
    if st.button(f"🔄 {title}") or st.session_state["parafrase_process"]:
        parafrase_text = GPT3.gen_article(
            "Paraphrase the following paragraph, using as few words from the original paragraph as possible:"
            + "\n\n"
            + translator.translate_text(text, target_lang="EN-GB").text,
            2000,
            temperature,
            top_p,
            frequency_penalty,
            presence_penalty,
        )[0]
        st.session_state[title] = translator.translate_text(parafrase_text, target_lang="FR").text
        st.session_state[title + "traduit"] = translator.translate_text(text, target_lang="FR").text

    st.write("### Paragraphe traduit")
    st.write(st.session_state[title + "traduit"])
    st.write("### Paragraphe paraphrasé")
    st.write(st.session_state[title])

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

if st.session_state["first_time"]:
    st.session_state["sitemap"] = scraping_sitemap.sitemap(theme)

    if entity != "":
        st.session_state["sitemap"] = st.session_state["sitemap"][st.session_state["sitemap"]['news_title'].str.lower().str.contains(entity.lower())]

    st.session_state["sitemap"] = st.session_state["sitemap"].head(nb_entities)
    
    object_list = translator.translate_text(st.session_state["sitemap"]['news_title'], target_lang="FR")
    st.session_state["sitemap"]['news_title'] = [obj.text for obj in object_list]

selection = aggrid_interactive_table(df=st.session_state["sitemap"])

if selection["selected_rows"] != []:

    st.write("## Article selected:")
    st.write(selection["selected_rows"][0]['loc'])

    if st.button("paraphraser l'article") :

        st.session_state["parafrase_process"] = True

        st.session_state["title"] = selection["selected_rows"][0]['news_title']

        st.write("# " + st.session_state["title"])

        st.session_state["paragraphe_list"] = scraping_bs4_article.get_article(selection["selected_rows"][0]['loc'],selection["selected_rows"][0]['publication_name'])

        st.session_state["paragraphe_list"] = [el for el in st.session_state["paragraphe_list"] if el != '']
        
        for i,el in enumerate(st.session_state["paragraphe_list"]) :
            parafrase(f"Paragraphe {i+1}",el)
        
        st.session_state["text_to_be_copied"] = (
            st.session_state["title"]
        )

        for i in range(len(st.session_state["paragraphe_list"])) :
            st.session_state["text_to_be_copied"] += st.session_state[f"Paragraphe {i+1}"]
        
        st.session_state["parafrase_process"] = False
    
    elif st.session_state["paragraphe_list"] != []:

        st.write("# " + st.session_state["title"])
        
        for i,el in enumerate(st.session_state["paragraphe_list"]) :
            parafrase(f"Paragraphe {i+1}",el)

# st.write(st.session_state["first_time"])

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
