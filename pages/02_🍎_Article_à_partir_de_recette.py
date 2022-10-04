import pyperclip
import streamlit as st

import GPT3
import scrap_750g_recipe
import trad_deepl

# Creation of a streamlit application to generated an article from a 750g recipe.

st.set_page_config(
    page_title="750g food article generator",
    page_icon=":apple:",
)

if "first_time" not in st.session_state:
    st.session_state["first_time"] = True

st.title("🍎 Générateur d'article à partir d'une recette")

with st.expander("ℹ️ - About this app", expanded=True):

    st.write(
        """     
-   Cette application permet de générer une ébauche d'article à partir d'un lien d'une recette de 750g.
-   L'article se génère automatiquement à l'ouverture de la page.
-   Vous pouvez recharger une partie de l'article si elle vous déplait en appuyant sur le bouton juste au dessus du paragraphe.
-   Pour copier l'article généré appuyez sur le bouton 'Copier l'article' sous l'URL.
-   Si vous changez d'URL pensez bien à appuyer sur Entrée.
-   Le Input text est le texte utilisé pour générer les parties de l'article.
-   Vous pouvez essayer l'application avec cette URL : https://www.750g.com/tajine-de-kefta-aux-oeufs-r76578.htm
	    """
    )

    st.markdown("")


def callback():
    st.session_state["first_time"] = True


st.write("### Entrez l'URL d'une recette de 750g")
url = st.text_input("URL", on_change=callback)
# url = "https://www.750g.com/cookies-aux-pepites-de-chocolat-r89377.htm"

if st.button("Copier l'article"):
    if "Titles" in st.session_state:
        text_to_be_copied = (
            st.session_state["Titles"]
            + st.session_state["Introduction"]
            + "\n\n"
            + st.session_state["ingredients_overview"]
            + st.session_state["Substitutions"]
            + "\n\n"
            + st.session_state["Ingredients"]
            + "\n"
            + st.session_state["Instructions"]
            + st.session_state["Conclusion"]
            + st.session_state["FAQ"]
        )
        pyperclip.copy(text_to_be_copied)
    else:
        st.write("## Erreur : Il n'y a pas d'article à copier")

with st.sidebar:
    st.write("## Caractéristiques de GPT 3")
    temperature = st.slider(
        "temperature", min_value=0.00, max_value=1.00, value=0.70, step=0.01
    )
    top_p = st.slider("top_p", min_value=0.00, max_value=1.00, value=1.00, step=0.01)
    frequency_penalty = st.slider(
        "frequency_penalty", min_value=0.00, max_value=2.00, value=0.20, step=0.01
    )

if url != "":

    def formating(entity, dict_):

        # Function that format the informations scraped from the 750g recipe.

        # Args:
        #     entity (str): the entity to format.

        # Returns:
        #     text (str): the formated text.

        text = ""
        for i, el in enumerate(dict_[entity]):
            line = str(i + 1) + ". " + trad_deepl.traduction(el, "FR", "EN-GB")
            text += line.translate({ord(c): None for c in ["\t", "\n"]}) + "\n"
        text += "\n"
        return text

    def main_elements(url):

        # Function that scrap and format the informations from the 750g recipe.

        # Args:
        #     url (str): the recipe url.

        # Returns:
        #     text (str): the formated text.
        #     title (str): the title of the recipe.
        #     dict_ (dict): a dictionnary with all the scrap informations
        #     nb_tokens (int): the number of tokens used for this text.

        dict_ = scrap_750g_recipe.get_recipe(url)
        title = trad_deepl.traduction(dict_["title"], "FR", "EN-GB")
        nb_tokens = 2000

        text = "Type of Recipe : " + title + "\n\n"
        text += "Ingredients :\n" + formating("ingredients", dict_)
        text += "Instructions :\n" + formating("steps", dict_)
        text += "Features :\n" + formating("features", dict_)
        text += "Nutrition :\n" + formating("nutrition", dict_)
        text += "Equipments :\n" + formating("equipments", dict_)

        return (text, title, dict_, nb_tokens)

    if st.session_state["first_time"]:
        (
            st.session_state["main_text"],
            st.session_state["title"],
            st.session_state["dict_"],
            st.session_state["nb_tokens"],
        ) = main_elements(url)
        st.session_state["Ingredients"] = trad_deepl.traduction(
            formating("ingredients", st.session_state["dict_"]), "EN", "FR"
        )

    with st.sidebar:
        st.write("## Input text")
        st.write(trad_deepl.traduction(st.session_state["main_text"], "EN", "FR"))

    with st.sidebar:
        st.write("Avantages :")
        if st.button("Run Avantages") or st.session_state["first_time"]:
            benefits = GPT3.gen_article(
                ">Write a list of the recipe benefits.",
                st.session_state["main_text"],
                st.session_state["nb_tokens"],
                temperature,
                top_p,
                frequency_penalty,
            )[0]
            st.session_state["Benefits"] = trad_deepl.traduction(benefits, "EN", "FR")
        st.write(st.session_state["Benefits"])
        st.session_state["input_text"] = (
            st.session_state["Benefits"] + st.session_state["main_text"]
        )

    st.write("## Titres :")
    if st.button("🔄 Titres") or st.session_state["first_time"]:
        titles = GPT3.gen_article(
            ">Come up with a list of catchy titles for"
            + st.session_state["title"]
            + "recipe.",
            None,
            st.session_state["nb_tokens"],
            temperature,
            top_p,
            frequency_penalty,
        )[0]
        st.session_state["Titles"] = trad_deepl.traduction(titles, "EN", "FR")

    st.write(st.session_state["Titles"])

    if st.button("🔄 Introduction") or st.session_state["first_time"]:
        introduction = (
            GPT3.gen_article(
                ">write a relatable story about why someone should make these "
                + st.session_state["title"],
                st.session_state["input_text"],
                st.session_state["nb_tokens"],
                temperature,
                top_p,
                frequency_penalty,
            )[0]
            + GPT3.gen_article(
                ">Introduce the recipe and its benefits.",
                st.session_state["input_text"],
                st.session_state["nb_tokens"],
            )[0]
            + GPT3.gen_article(
                ">Write a paragraph about how to store the "
                + st.session_state["title"]
                + " and how long it keeps.",
                st.session_state["input_text"],
                st.session_state["nb_tokens"],
                temperature,
                top_p,
                frequency_penalty,
            )[0]
        )
        st.session_state["Introduction"] = trad_deepl.traduction(
            introduction, "EN", "FR"
        )
    st.write(st.session_state["Introduction"])

    st.write("## Aperçu des ingrédients :")

    ingredients_chosen = st.multiselect(
        "Choose the ingredients (do not forget to run ingredients overview after choosing new ingredients)",
        st.session_state["dict_"]["ingredients"],
        st.session_state["dict_"]["ingredients"][0:2],
    )

    if st.button("🔄 Aperçu des ingrédients") or st.session_state["first_time"]:

        ingredients_overview = ""
        for el in enumerate(ingredients_chosen):
            ingredient = trad_deepl.traduction(el[1], "FR", "EN-GB").translate(
                {ord(c): None for c in ["\t", "\n"]}
            )
            st.session_state[ingredient] = GPT3.gen_article(
                ">Write a paragraph about why this ingredient works for this recipe.\n>Write a paragraph about "
                + ingredient
                + " health benefits.",
                st.session_state["input_text"],
                st.session_state["nb_tokens"],
                temperature,
                top_p,
                frequency_penalty,
            )[0]
            ingredients_overview += (
                "\n\n"
                + "### "
                + el[1].translate({ord(c): None for c in ["\t", "\n"]})
                + ":"
            )
            ingredients_overview += "\n" + trad_deepl.traduction(
                st.session_state[ingredient], "EN", "FR"
            ).translate({ord(c): None for c in ["\t", "\n"]})

        st.session_state["ingredients_overview"] = ingredients_overview

    st.write(st.session_state["ingredients_overview"])

    st.write("## Substitutions :")
    if st.button("🔄 Substitutions") or st.session_state["first_time"]:
        substitutions = GPT3.gen_article(
            ">Write a paragraph about the recipe substitutions.",
            st.session_state["input_text"],
            st.session_state["nb_tokens"],
            temperature,
            top_p,
            frequency_penalty,
        )[0]
        st.session_state["Substitutions"] = trad_deepl.traduction(
            substitutions, "EN", "FR"
        )
    st.write(st.session_state["Substitutions"])

    st.write("## Ingrédients :")
    st.session_state["Ingredients"]

    st.write("## Instructions :")
    if st.button("🔄 Instructions") or st.session_state["first_time"]:
        instructions = GPT3.gen_article(
            ">write the instructions in a fun and creative way.",
            st.session_state["input_text"],
            st.session_state["nb_tokens"],
            temperature,
            top_p,
            frequency_penalty,
        )[0]
        st.session_state["Instructions"] = trad_deepl.traduction(
            instructions, "EN", "FR"
        )
    st.write(st.session_state["Instructions"])

    st.write("## Conclusion :")
    if st.button("🔄 Conclusion") or st.session_state["first_time"]:
        conclusion = GPT3.gen_article(
            ">Write a conclusion.",
            st.session_state["input_text"],
            st.session_state["nb_tokens"],
            temperature,
            top_p,
            frequency_penalty,
        )[0]
        st.session_state["Conclusion"] = trad_deepl.traduction(conclusion, "EN", "FR")
    st.write(st.session_state["Conclusion"])

    st.write("## FAQ :")

    ingredients_chosen_faq = st.multiselect(
        "Choose the ingredients (do not forget to run FAQ after choosing new ingredients)",
        st.session_state["dict_"]["ingredients"],
        st.session_state["dict_"]["ingredients"][0:2],
    )

    if st.button("🔄 FAQ") or st.session_state["first_time"]:

        FAQ = ""
        for el in enumerate(ingredients_chosen_faq):
            ingredient = trad_deepl.traduction(el[1], "FR", "EN-GB").translate(
                {ord(c): None for c in ["\t", "\n"]}
            )
            st.session_state[ingredient + "_FAQ"] = GPT3.gen_article(
                ">Write an FAQ with responses related to the "
                + ingredient
                + " ingredient.",
                st.session_state["input_text"],
                st.session_state["nb_tokens"],
                temperature,
                top_p,
                frequency_penalty,
            )[0]
            FAQ += (
                "\n\n"
                + "### "
                + el[1].translate({ord(c): None for c in ["\t", "\n"]})
                + ":"
            )
            FAQ += "\n" + trad_deepl.traduction(
                st.session_state[ingredient + "_FAQ"], "EN", "FR"
            ).translate({ord(c): None for c in ["\t", "\n"]})

        st.session_state["FAQ"] = FAQ

    st.write(st.session_state["FAQ"])

    st.session_state["first_time"] = False
