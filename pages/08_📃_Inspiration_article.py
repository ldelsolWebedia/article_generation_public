import deepl
import streamlit as st
from bokeh.models import CustomJS
from bokeh.models.widgets import Button
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from streamlit_bokeh_events import streamlit_bokeh_events

import GPT3
import scraping.scraping_bs4_article as scraping_bs4_article
import scraping.scraping_sitemap as scraping_sitemap

# from unidecode import unidecode

translator = deepl.Translator(st.secrets["DEEPL_KEY"])

st.set_page_config(
    page_title="Inspiration article jeux vidéo/cinéma", page_icon="📃", layout="wide",
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
-   Pour plus d'informations : https://www.notion.so/webedia-group/Inspiration-article-jeux-vid-o-cin-ma-16004507bcae476fa5e3536c7ee6baf1
	    """
    )

    st.markdown("")


def callback():
    st.session_state["first_time"] = True


col1, col2, col3 = st.columns(3)

with col1:
    nb_entities = st.slider("Nombre d'articles", 1, 50, 10)
    if st.button("Rafraichir la liste d'articles"):
        st.session_state["first_time"] = True

with col2:
    entity = st.text_input("Mot à filtrer", on_change=callback)

with col3:
    theme = st.selectbox("Thème", ("Jeux vidéo", "Cinéma"), on_change=callback)


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


def paraphrase(title, text):
    if st.button(f"🔄 {title}") or st.session_state["paraphrase_process"]:
        st.session_state[title + "traduit"] = translator.translate_text(
            text, target_lang="FR"
        ).text
        st.session_state[title] = GPT3.gen_article(
            """Original: La vidéo de la danse de Topen a été vue plus de 400 000 fois depuis qu'elle a été publiée sur YouTube la semaine dernière, et le plombier dit qu'il a déjà été approché en public pour obtenir son autographe.
Paraphrase: Bien que la vidéo du plombier dansant n'ait été postée sur YouTube que la semaine dernière, elle a déjà été vue plus de 400 000 fois. Topen est devenu une célébrité presque instantanée, des inconnus lui ayant même demandé un autographe.

Original: Selon le magazine Heat, Miley a une liste de règles strictes pour ses futurs hommes lors de ses sorties. Apparemment, son assistant organise ce que le gars doit porter, faire et parler pendant le rendez-vous. Elle n'aime pas non plus les fleurs, il lui est donc interdit de les lui apporter.
Paraphrase: Comme indiqué dans le magazine Heat, Miley Cyrus a un certain nombre de règles bizarres pour les rendez-vous. Elle est si précise sur ce que ses partenaires doivent porter, dire et faire qu'elle demande à son assistant de faire respecter ces règles lors des rendez-vous. Miley Cyrus n'aime même pas les fleurs et ne laisse pas ses partenaires les acheter pour elle.

Original: Les responsables des admissions à l'université déconseillent tous d'écrire un essai d'admission à l'université sur quelque chose que le candidat a appris en étant défoncé ou ivre. "Mais nous recevons toujours quelques-unes de ces dissertations", me dit un responsable des admissions à l'université. "Nous avons même reçu la dissertation classique dans laquelle l'étudiant, alors qu'il était défoncé, a réalisé que le système solaire était un atome et la terre un électron. Vous vous souviendrez que cette conversation a eu lieu dans le film Animal House.
Paraphrase: Les responsables des admissions à l'université recommandent généralement aux étudiants de ne pas écrire leur dissertation d'admission sur une leçon apprise lorsqu'ils étaient défoncés ou ivres ; cependant, certains étudiants ignorent toujours ce conseil. Par exemple, un étudiant a écrit sur la conversation dans Animal House, comme s'il s'agissait de sa propre expérience de défoncé, sur le système solaire comme un atome et la terre comme une élection.

Original: Un homme de Gastonia âgé de 68 ans affirme avoir fait fuir deux hommes masqués qui tentaient de s'introduire chez lui avec son arme qu'il peut garder sur son déambulateur. Il a ensuite collé une note sur sa porte disant que s'ils tentent de pénétrer à nouveau chez lui, il les attendra.
Paraphrase : Deux hommes ont tenté de s'introduire dans la maison d'un homme de 68 ans, mais ils ont été effrayés par l'arme que l'homme gardait sur son déambulateur. Par la suite, l'homme a collé une note sur la porte pour prévenir qu'il attendrait les cambrioleurs s'ils revenaient.

Original: """
            + st.session_state[title + "traduit"]
            + "\nParaphrase:",
            2000,
            temperature,
            top_p,
            frequency_penalty,
            presence_penalty,
        )[0]

    col_paraphrase, col_translate = st.columns(2)

    with col_paraphrase:
        st.write(st.session_state[title])
    with col_translate:
        st.write(st.session_state[title + "traduit"])


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

if st.session_state["first_time"]:
    st.session_state["sitemap"] = scraping_sitemap.sitemap(theme)

    if entity != "":
        st.session_state["sitemap"] = st.session_state["sitemap"][
            st.session_state["sitemap"]["news_title"]
            .str.lower()
            .str.contains(entity.lower())
        ]
        # st.session_state["sitemap"] = st.session_state["sitemap"].loc[unidecode(st.session_state["sitemap"]['news_title'].str).contains(entity.lower())]

    st.session_state["sitemap"] = st.session_state["sitemap"].head(nb_entities)

    if entity == "" or (entity != "" and len(st.session_state["sitemap"]) != 0):
        object_list = translator.translate_text(
            st.session_state["sitemap"]["news_title"], target_lang="FR"
        )
        st.session_state["sitemap"]["news_title"] = [obj.text for obj in object_list]
    else:
        st.write(
            "### Pas d'article trouvé. Veuillez vérifier l'orthographe de votre recherche."
        )

selection = aggrid_interactive_table(df=st.session_state["sitemap"])

if selection["selected_rows"] != []:

    st.write("## Article sélectionné:")
    st.write(selection["selected_rows"][0]["loc"])

    if st.button("paraphraser l'article"):

        st.session_state["paraphrase_process"] = True

        st.session_state["title"] = selection["selected_rows"][0]["news_title"]

        st.write("# " + st.session_state["title"])

        st.session_state["paragraphe_list"] = scraping_bs4_article.get_article(
            selection["selected_rows"][0]["loc"],
            selection["selected_rows"][0]["publication_name"],
        )

        st.session_state["paragraphe_list"] = [
            el for el in st.session_state["paragraphe_list"] if el != ""
        ]

        col_paraphrase, col_translate = st.columns(2)
        with col_paraphrase:
            st.write("### Paragraphe paraphrasé")
        with col_translate:
            st.write("### Paragraphe traduit")
        for i, el in enumerate(st.session_state["paragraphe_list"]):
            paraphrase(f"Paragraphe {i+1}", el)

        st.session_state["text_to_be_copied"] = st.session_state["title"]

        for i in range(len(st.session_state["paragraphe_list"])):
            st.session_state["text_to_be_copied"] += "\n\n" + st.session_state[
                f"Paragraphe {i+1}"
            ].replace("\n", "")

        st.session_state["paraphrase_process"] = False

    elif st.session_state["paragraphe_list"] != []:

        st.write("# " + st.session_state["title"])

        col_paraphrase, col_translate = st.columns(2)
        with col_paraphrase:
            st.write("### Paragraphe paraphrasé")
        with col_translate:
            st.write("### Paragraphe traduit")
        for i, el in enumerate(st.session_state["paragraphe_list"]):
            paraphrase(f"Paragraphe {i+1}", el)

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
