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
# from unidecode import unidecode

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

def paraphrase(title,text) :
    st.write(f"## {title} :")
    if st.button(f"🔄 {title}") or st.session_state["paraphrase_process"]:
        paraphrase_text = GPT3.gen_article(
            """Original: The video of Topen’s dancing has racked up more than 400,000 views since it was posted on YouTube last week, and the plumber says he’s already been approached in public for his autograph.
Paraphrase: Even though the YouTube video of the dancing plumber was only posted last week, it has already had more than 400,000 views. Topen has become an almost instant celebrity as strangers have even asked him for autographs.

Original: According to Heat magazine, Miley has a list of intense rules for her men-to-be while out on dates. Apparently her assistant arranges what the guy must wear, do, and talk about on the date. She’s also not into flowers, so he’s banned from bringing her those.
Paraphrase: As stated in Heat magazine, Miley Cyrus has a number of bizarre rules for dating. She’s so specific about what her dates wear, say, and do, that she has her assistant enforce these rules on dates. Cyrus doesn’t even like flowers and won’t let her dates buy them for her.

Original: College admissions officers all advise against writing a college admission essay about something that an applicant learned while stoned or drunk. “But we still get a few of those essays,” a college admissions officer tells me. “We even got the classic one about how the student, while stoned, realized that the solar system is an atom and the earth is an electron. You’ll remember, that conversation occurred in the movie Animal House.
Paraphrase: College admissions officers generally tell students not to write their admissions essays about a lesson they learned when being stoned or drunk; however, some students still ignore the advice. For instance, one student wrote about the conversation in Animal House, as if it were his own stoned experience, about the solar system as an atom and the earth as an election.

Original: A 68-year-old Gastonia man says he scared off two men in ski masks trying to break in his home with his gun he can keep on his walker. And then he taped a note to his door saying if they try to break in his house again, he will be waiting on them.
Paraphrase: Two men attempted to break into a 68-year-old man’s home; however, they were scared off by the gun the man kept on his walker. Afterwards, the man taped a note to the door warning that he’d be waiting for the burglars if they came back.

Original: """
            + translator.translate_text(el, target_lang="EN-GB").text
            + "\nParaphrase:",
            2000,
            temperature,
            top_p,
            frequency_penalty,
            presence_penalty,
        )[0]
        st.session_state[title] = translator.translate_text(paraphrase_text, target_lang="FR").text
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
    
    if entity == "" or (entity != "" and len(st.session_state["sitemap"]) != 0) :
        object_list = translator.translate_text(st.session_state["sitemap"]['news_title'], target_lang="FR")
        st.session_state["sitemap"]['news_title'] = [obj.text for obj in object_list]
    else :
        st.write("### Pas d'article trouvé. Veuillez vérifier l'orthographe de votre recherche.")

selection = aggrid_interactive_table(df=st.session_state["sitemap"])

if selection["selected_rows"] != []:

    st.write("## Article selected:")
    st.write(selection["selected_rows"][0]['loc'])

    if st.button("paraphraser l'article") :

        st.session_state["paraphrase_process"] = True

        st.session_state["title"] = selection["selected_rows"][0]['news_title']

        st.write("# " + st.session_state["title"])

        st.session_state["paragraphe_list"] = scraping_bs4_article.get_article(selection["selected_rows"][0]['loc'],selection["selected_rows"][0]['publication_name'])

        st.session_state["paragraphe_list"] = [el for el in st.session_state["paragraphe_list"] if el != '']
        
        for i,el in enumerate(st.session_state["paragraphe_list"]) :
            paraphrase(f"Paragraphe {i+1}",el)
        
        st.session_state["text_to_be_copied"] = (
            st.session_state["title"]
        )

        for i in range(len(st.session_state["paragraphe_list"])) :
            st.session_state["text_to_be_copied"] += st.session_state[f"Paragraphe {i+1}"]
        
        st.session_state["paraphrase_process"] = False
    
    elif st.session_state["paragraphe_list"] != []:

        st.write("# " + st.session_state["title"])
        
        for i,el in enumerate(st.session_state["paragraphe_list"]) :
            paraphrase(f"Paragraphe {i+1}",el)

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
