import streamlit as st
from bokeh.models import CustomJS
from bokeh.models.widgets import Button
from streamlit_bokeh_events import streamlit_bokeh_events

import GPT3
import scraping.scraping_bs4_purepeople as scraping_bs4_purepeople

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
-   Vous pouvez essayer l'application avec cette URL : https://www.purepeople.com/article/-elle-est-belle-gad-elmaleh-face-a-son-ex-charlotte-casiraghi-ses-details-croustillants-sur-sa-vie-a-monaco_a499708/1
-   Pour plus d'informations : https://www.notion.so/webedia-group/G-n-rateur-d-article-paraphras-PurePeople-cceb2c88d8b84aee9cdc973a5fec1493
	    """
    )

    st.markdown("")


def callback():
    st.session_state["first_time"] = True


def paraphrase(title, text):
    if st.button(f"🔄 {title}") or st.session_state["first_time"]:
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
            + text
            + "\nParaphrase:",
            2000,
            temperature,
            top_p,
            frequency_penalty,
            presence_penalty,
        )[0]

    st.write(st.session_state[title])


st.write("### Entrez l'URL d'un article PurePeople")
url = st.text_input("URL", on_change=callback)

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

if url != "":

    if st.session_state["first_time"]:
        st.session_state["scrap_article"] = scraping_bs4_purepeople.get_article(url)

    paraphrase("Titre", st.session_state["scrap_article"]["title"])
    paraphrase("Résumé", st.session_state["scrap_article"]["summary"])
    paragraphe = st.session_state["scrap_article"]["main_text"].split("\n")
    for i, el in enumerate([el for el in paragraphe if el != ""]):
        paraphrase(f"Paragraphe {i+1}", el)

    st.session_state["text_to_be_copied"] = (
        st.session_state["Titre"] + "\n\n" + st.session_state["Résumé"]
    )

    for i in range(len([el for el in paragraphe if el != ""])):
        st.session_state["text_to_be_copied"] += "\n\n" + st.session_state[
            f"Paragraphe {i+1}"
        ].replace("\n", "")

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
