import datetime

# from article_films import BQ
import BQ
import deepl
from bs4 import BeautifulSoup  # we use bs to clean html synopsis
import streamlit as st

translator = deepl.Translator(st.secrets["DEEPL_KEY"])


def get_top_series_by_genre_and_platform(genre, platform, max):

    df_top = BQ.fetch_top_series_by_genre_and_platform(genre, platform, max)
    list_id = list(df_top["id_series"])
    list_FR_title = list(df_top["FR_title"])
    list_original_title = list(df_top["original_title"])
    list_global_rating = list(df_top["note_sur_5"])

    article = """Voici le top {} des meilleures séries dans la catégorie "{}" disponibles sur {} :
    """.format(
        max, genre, platform
    )
    for i in range(len(list_original_title)):
        df_synopsis = BQ.fetch_series_synopsis_to_translate(int(list_id[i]))
        try:
            synopsis = df_synopsis["synopsis"][0]
        except:
            synopsis = "Pas de synopsis disponible pour cette série."
        df_reviews = BQ.fetch_reviews_by_series_id(int(list_id[i]))
        list_rating = df_reviews["rating"]
        list_review = df_reviews["review"]
        list_id_legacy = df_reviews["id_legacy"]
        nb_ratings = BQ.fetch_number_of_ratings_series(int(list_id[i]))
        try:
            article += """

## {} / {}{} ({} / 5 étoiles, {} notes)

{}
""".format(
                i + 1,
                list_FR_title[i]
                if list_FR_title[i] is not None
                else list_original_title[i],
                (" (" + list_original_title[i] + ")")
                if list_FR_title[i] is not None
                else "",
                list_global_rating[i],
                nb_ratings,
                translator.translate_text(
                    (BeautifulSoup(synopsis, features="lxml").get_text()),
                    target_lang="FR",
                )
                if synopsis != "Pas de synopsis disponible pour cette série."
                else synopsis,  # cleaning up synopsis with Beautifulsoup in case it is still in html and not just in text
            )
        except:
            article += """

## {} / {}{} ({} / 5 étoiles, {} notes)
""".format(
                i + 1,
                list_FR_title[i]
                if list_FR_title[i] is not None
                else list_original_title[i],
                (" (" + list_original_title[i] + ")")
                if list_FR_title[i] is not None
                else "",
                list_global_rating[i],
                nb_ratings,
            )

        for j in range(len(list_review)):
            article += """

[Review from URL : https://www.allocine.fr/membre-{}/critiques/serie-{}/]

{} ({} / 5 étoiles)
""".format(
                list_id_legacy[j],
                list_id[i],
                # gpt3.gpt3('''{}
                # Extrais la phrase la plus informative de ce texte en français :
                # '''.format(list_review[j])).strip(), # EXTRACT PHRASE FROM REVIEW
                list_review[j],
                str(round(float(list_rating[j]))),
            )

    article = article.rstrip("\n").lstrip("\n")
    return article


def get_top_movies_by_genre_and_platform(genre, platform, max):
    df_top = BQ.fetch_top_movies_by_genre_and_platform(genre, platform, max)
    list_id = list(df_top["id_movie"])
    list_FR_title = list(df_top["FR_title"])
    list_original_title = list(df_top["original_title"])
    list_global_rating = list(df_top["note_sur_5"])

    article = """# Voici le top {} des meilleurs films dans la catégorie "{}" disponibles sur {} :
    """.format(
        max, genre, platform
    )
    for i in range(len(list_original_title)):
        df_synopsis = BQ.fetch_movie_synopsis_to_translate(int(list_id[i]))
        try:
            synopsis = df_synopsis["synopsis"][0]
        except:
            synopsis = "Pas de synopsis disponible pour ce film."
        df_reviews = BQ.fetch_reviews_by_movie_id(int(list_id[i]))
        list_rating = df_reviews["rating"]
        list_review = df_reviews["review"]
        list_id_legacy = df_reviews["id_legacy"]
        nb_ratings = BQ.fetch_number_of_ratings_movie(int(list_id[i]))
        try:
            article += """

## {} / {}{} ({} / 5 étoiles, {} notes)

{}
""".format(
                i + 1,
                list_FR_title[i]
                if list_FR_title[i] is not None
                else list_original_title[i],
                (" (" + list_original_title[i] + ")")
                if list_FR_title[i] is not None
                else "",
                list_global_rating[i],
                nb_ratings,
                translator.translate_text(
                    (BeautifulSoup(synopsis, features="lxml").get_text()),
                    target_lang="FR",
                )
                if synopsis != "Pas de synopsis disponible pour ce film."
                else synopsis,  # cleaning up synopsis in case it is still in html and not just in text
            )
        except:
            article += """

## {} / {}{} ({} / 5 étoiles, {} notes)
""".format(
                i + 1,
                list_FR_title[i]
                if list_FR_title[i] is not None
                else list_original_title[i],
                (" (" + list_original_title[i] + ")")
                if list_FR_title[i] is not None
                else "",
                list_global_rating[i],
                nb_ratings,
            )

        for j in range(len(list_review)):
            article += """

[Review from URL : https://www.allocine.fr/membre-{}/critiques/film-{}/]

{} ({} / 5 étoiles)
""".format(
                list_id_legacy[j],
                list_id[i],
                # gpt3.gpt3('''{}
                # Extrais la phrase la plus informative de ce texte en français :
                # '''.format(list_review[j])).strip(), # EXTRACT PHRASE FROM REVIEW
                list_review[j],
                str(round(float(list_rating[j]))),
            )

    article = article.rstrip("\n").lstrip("\n")
    return article


def post_ranking_article_to_BQ(type, genre, platform, max):

    if type.lower() in ["serie", "series", "série", "séries"]:
        article = get_top_series_by_genre_and_platform(genre, platform, max)
        row_to_insert = [
            {
                "number_of_entities": max,
                "type": "series",
                "genre": genre,
                "provider": platform,
                "article": article,
                "created_at": datetime.datetime.now(),
            }
        ]
        BQ.stream_bigquery_table("allocine_ranking_articles", row_to_insert)
        print(
            "New article inserted in : wbd-seo-data.content-generation.allocine_ranking_articles"
        )

    if type.lower() in ["film", "films", "movie", "movies"]:
        article = get_top_movies_by_genre_and_platform(genre, platform, max)
        row_to_insert = [
            {
                "number_of_entities": max,
                "type": "movie",
                "genre": genre,
                "provider": platform,
                "article": article,
                "created_at": datetime.datetime.now(),
            }
        ]
        BQ.stream_bigquery_table("allocine_ranking_articles", row_to_insert)
        print(
            "New article inserted in : wbd-seo-data.content-generation.allocine_ranking_articles"
        )

    return article


def gen_movie_article(nb_entities, entity_type, genre, provider):

    df_to_check = BQ.fetch_generated_articles()
    list_nb_entities_to_check = list(df_to_check["number_of_entities"])
    list_type_to_check = list(df_to_check["type"])
    list_genre_to_check = list(df_to_check["genre"])
    list_provider_to_check = list(df_to_check["provider"])
    list_created_at_to_check = list(df_to_check["created_at"])

    for i in range(len(list_nb_entities_to_check)):
        if [nb_entities, entity_type, genre, provider] == [
            list_nb_entities_to_check[i],
            list_type_to_check[i],
            list_genre_to_check[i],
            list_provider_to_check[i],
        ]:
            if (datetime.datetime.now() - list_created_at_to_check[i]).days >= 30:
                break
            else:
                print(
                    "An article with these parameters has already been generated recently ("
                    + str(list_created_at_to_check[i])
                    + ")"
                )
                return (
                    "An article with these parameters has already been generated recently ("
                    + str(list_created_at_to_check[i])
                    + ")"
                )

    return post_ranking_article_to_BQ(entity_type, genre, provider, nb_entities)

if __name__ == "__main__" :
    print(gen_movie_article(4, "Film", "Action", "Amazon Prime Video"))