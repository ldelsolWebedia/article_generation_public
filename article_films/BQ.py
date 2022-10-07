import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

# Query functions to fetch data :


def fetch_top_series_by_genre_and_platform(genre, platform, max):
    """Executes the query located in the path given in the filepath to sql query"""
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(project="wbd-seo-data", credentials=credentials)
    sql = """
    SELECT
  t1.id_brand,
  t4.id_series,
  t2.title as original_title,
  t3.title as FR_title,
  ROUND(ROUND(t1.note_base_AC/2,2),1) AS note_sur_5,
  t3.synopsis,
  TO_JSON_STRING(t6.genres) AS genres,
  -- t5.name AS name_company,
  STRING_AGG(DISTINCT t5.name) AS platforms
FROM
  `allocine-bq.dbz_series.series_has_release` AS t4
INNER JOIN
  `allocine-bq.dbz_stats.brand_series_all_time` AS t1
ON
  t1.id_series = t4.id_series
INNER JOIN
  `allocine-bq.dbz_series.series` AS t2
ON
  t2.id = t4.id_series
INNER JOIN
  `allocine-bq.dbz_series.series_localized` AS t3
ON
  t3.id = t4.id_series
INNER JOIN
  `allocine-bq.dbz_executive.company` AS t5
ON
  t5.id = t4.limited_to_id_company
INNER JOIN
  `allocine-bq.ta_allocine.ta_series` AS t6
ON
  t6.id = t4.id_series
WHERE
  t1.id_brand = "AC"
  AND t3.locale = "fr_FR"
  AND t5. id_country = 5001
  AND contains_SUBSTR(t6.genres,@genre_string)
  AND contains_SUBSTR(t5.name,@platform_string)
GROUP BY
  t1.id_brand,
  t4.id_series,
  t2.title,
  t3.title,
  t1.note_base_AC,
  t3.synopsis,
  genres
ORDER BY
  t1.note_base_AC DESC
LIMIT @max
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("genre_string", "STRING", genre),
            bigquery.ScalarQueryParameter("platform_string", "STRING", platform),
            bigquery.ScalarQueryParameter("max", "INT64", max),
        ]
    )
    df = client.query(sql, job_config=job_config).to_dataframe()
    return df


def fetch_reviews_by_series_id(series_id):
    """Executes the query located in the path given in the filepath to sql query"""
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(project="wbd-seo-data", credentials=credentials)
    sql = """
    SELECT
  re.id AS id_review,
  ra.id_user,
  us.id_legacy,
  SPLIT(ra.gid_entity, '._.')[
OFFSET
  (0)] AS type,
  CAST(SPLIT(ra.gid_entity, '._.')[
  OFFSET
    (1)] AS INT64) AS id_series,
  ra.id_brand,
  ROUND(ROUND(ra.rating/2,2),1) AS rating,
  CAST(SUBSTRING(re.stats,STRPOS(re.stats,'"wilson_score": ')+CHAR_LENGTH('"wilson_score": '),STRPOS(re.stats,', "helpful_count":')-STRPOS(re.stats,'"wilson_score": ')-CHAR_LENGTH('"wilson_score": ')) AS FLOAT64) AS wilson_score,
  re.status,
  re.body AS review,
  re.updated_at
FROM
  `allocine-bq.dbz_social.user_has_rating` AS ra
INNER JOIN
  `allocine-bq.dbz_social.user_has_review` AS re
ON
  ra.id = re.id
INNER JOIN
  `allocine-bq.dbz_social.user` AS us
ON
  ra.id_user = us.id
WHERE
  ra.id_brand = "AC"
  AND re.status = "Social.Review.Accepted"
  AND (SPLIT(ra.gid_entity, '._.')[
  OFFSET
    (0)] = 'series.series'
    )
  AND CAST(SPLIT(ra.gid_entity, '._.')[
  OFFSET
    (1)] AS INT64) = @series_id
  AND ra.rating > 8.0
ORDER BY
  ra.rating DESC,
  wilson_score DESC
LIMIT 2
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("series_id", "INT64", series_id),
        ]
    )
    df = client.query(sql, job_config=job_config).to_dataframe()
    return df


def fetch_number_of_ratings_series(series_id):
    """Executes the query located in the path given in the filepath to sql query"""
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(project="wbd-seo-data", credentials=credentials)
    id = "series.series._.{}".format(series_id)
    sql = """
  SELECT
  COUNT(*) AS nb_ratings
FROM
  `allocine-bq.dbz_social.user_has_rating`
WHERE
  gid_entity = @id
AND id_brand = 'AC'
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("id", "STRING", id),]
    )
    df = client.query(sql, job_config=job_config).to_dataframe()
    return int(df["nb_ratings"][0])


def fetch_top_movies_by_genre_and_platform(genre, platform, max):
    """Executes the query located in the path given in the filepath to sql query"""
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(project="wbd-seo-data", credentials=credentials)
    sql = """
    SELECT
  t1.id_brand,
  t4.id_movie,
  t2.title as original_title,
  t3.title as FR_title,
  ROUND(ROUND(t1.note_base_AC/2,2),1) AS note_sur_5,
  t3.synopsis,
  TO_JSON_STRING(t6.genres) AS genres,
  -- t5.name AS name_company,
  STRING_AGG(DISTINCT t5.name) AS platforms
FROM
  `allocine-bq.dbz_movie.movie_has_release` AS t4
INNER JOIN
  `allocine-bq.dbz_stats.brand_movie_all_time` AS t1
ON
  t1.id_movie = t4.id_movie
INNER JOIN
  `allocine-bq.dbz_movie.movie` AS t2
ON
  t2.id = t4.id_movie
INNER JOIN
  `allocine-bq.dbz_movie.movie_localized` AS t3
ON
  t3.id = t4.id_movie
INNER JOIN
  `allocine-bq.dbz_executive.company` AS t5
ON
  t5.id = t4.limited_to_id_company
INNER JOIN
  `allocine-bq.ta_allocine.ta_movie` AS t6
ON
  t6.id = t4.id_movie
WHERE
  t1.id_brand = "AC"
  AND t3.locale = "fr_FR"
  AND t5. id_country = 5001
  AND contains_SUBSTR(t6.genres,@genre_string)
  AND contains_SUBSTR(t5.name,@platform_string)
GROUP BY
  t1.id_brand,
  t4.id_movie,
  t2.title,
  t3.title,
  t1.note_base_AC,
  t3.synopsis,
  genres
ORDER BY
  t1.note_base_AC DESC
LIMIT @max
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("genre_string", "STRING", genre),
            bigquery.ScalarQueryParameter("platform_string", "STRING", platform),
            bigquery.ScalarQueryParameter("max", "INT64", max),
        ]
    )
    df = client.query(sql, job_config=job_config).to_dataframe()
    return df


def fetch_reviews_by_movie_id(movie_id):
    """Executes the query located in the path given in the filepath to sql query"""
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(project="wbd-seo-data", credentials=credentials)
    sql = """
    SELECT
  re.id AS id_review,
  ra.id_user,
  us.id_legacy,
  SPLIT(ra.gid_entity, '._.')[
OFFSET
  (0)] AS type,
  CAST(SPLIT(ra.gid_entity, '._.')[
  OFFSET
    (1)] AS INT64) AS id_movie,
  ra.id_brand,
  ROUND(ROUND(ra.rating/2,2),1) AS rating,
  CAST(SUBSTRING(re.stats,STRPOS(re.stats,'"wilson_score": ')+CHAR_LENGTH('"wilson_score": '),STRPOS(re.stats,', "helpful_count":')-STRPOS(re.stats,'"wilson_score": ')-CHAR_LENGTH('"wilson_score": ')) AS FLOAT64) AS wilson_score,
  re.status,
  re.body AS review,
  re.updated_at
FROM
  `allocine-bq.dbz_social.user_has_rating` AS ra
INNER JOIN
  `allocine-bq.dbz_social.user_has_review` AS re
ON
  ra.id = re.id
INNER JOIN
  `allocine-bq.dbz_social.user` AS us
ON
  ra.id_user = us.id
WHERE
  ra.id_brand = "AC"
  AND re.status = "Social.Review.Accepted"
  AND (SPLIT(ra.gid_entity, '._.')[
  OFFSET
    (0)] = 'movie.movie'
    )
  AND CAST(SPLIT(ra.gid_entity, '._.')[
  OFFSET
    (1)] AS INT64) = @movie_id
  AND ra.rating > 8.0
ORDER BY
  ra.rating DESC,
  wilson_score DESC
LIMIT 2
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("movie_id", "INT64", movie_id),]
    )
    df = client.query(sql, job_config=job_config).to_dataframe()
    return df


def fetch_number_of_ratings_movie(movie_id):
    """Executes the query located in the path given in the filepath to sql query"""
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(project="wbd-seo-data", credentials=credentials)
    id = "movie.movie._.{}".format(movie_id)
    sql = """
  SELECT
  COUNT(*) AS nb_ratings
FROM
  `allocine-bq.dbz_social.user_has_rating`
WHERE
  gid_entity = @id
AND id_brand = 'AC'
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("id", "STRING", id),]
    )
    df = client.query(sql, job_config=job_config).to_dataframe()
    return int(df["nb_ratings"][0])


def fetch_series_synopsis_to_translate(movie_id):
    """Executes the query located in the path given in the filepath to sql query"""
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(project="wbd-seo-data", credentials=credentials)
    sql = """
  SELECT
  *
FROM
  `allocine-bq.dbz_series.series_localized`
WHERE
  locale!="fr_FR"
  AND synopsis IS NOT NULL
  AND id=@series_id
ORDER BY
  CASE
    WHEN locale = 'de_DE' THEN 1
  ELSE
  2
END
  ASC
LIMIT
  1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("series_id", "INT64", movie_id),
        ]
    )
    df = client.query(sql, job_config=job_config).to_dataframe()
    return df


def fetch_movie_synopsis_to_translate(movie_id):
    """Executes the query located in the path given in the filepath to sql query"""
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(project="wbd-seo-data", credentials=credentials)
    sql = """
  SELECT
  *
FROM
  `allocine-bq.dbz_movie.movie_localized`
WHERE
  locale!="fr_FR"
  AND synopsis IS NOT NULL
  AND id=@movie_id
ORDER BY
  CASE
    WHEN locale = 'de_DE' THEN 1
  ELSE
  2
END
  ASC
LIMIT
  1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("movie_id", "INT64", movie_id),]
    )
    df = client.query(sql, job_config=job_config).to_dataframe()
    return df


def fetch_generated_articles():
    """Executes the query located in the path given in the filepath to sql query"""
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(project="wbd-seo-data", credentials=credentials)
    sql = """
  SELECT
  *
FROM
  `wbd-seo-data.content_generation.allocine_ranking_articles`
ORDER BY
  created_at DESC
LIMIT
  100
    """
    job_config = bigquery.QueryJobConfig()
    df = client.query(sql, job_config=job_config).to_dataframe()
    return df


# Functions to manipulate BQ tables :


def stream_bigquery_table(table_id, rows_to_insert):

    dataset_id = "content_generation"

    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(project="wbd-seo-data", credentials=credentials)

    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)

    errors = client.insert_rows(table, rows_to_insert)
    print(errors)


# def create_article_table():

#     project_id = 'wbd-seo-data'
#     dataset_id = 'content_generation'
#     table_id = 'allocine_ranking_articles'

#     schema = [
#         SchemaField('number_of_entities', 'STRING'),
#         SchemaField('type','STRING'),
#         SchemaField('genre', 'STRING'),
#         SchemaField('provider', 'STRING'),
#         SchemaField('article', 'STRING'),
#         SchemaField('created_at', 'DATETIME'),
#     ]
#     client = bigquery.Client(project_id)
#     dataset_ref = client.dataset(dataset_id)
#     table_ref = dataset_ref.table(table_id)
#     table = bigquery.Table(table_ref, schema=schema)
#     table = client.create_table(table)

# create_article_table()

if __name__ == "__main__":
    print(fetch_top_series_by_genre_and_platform("Action", "Netflix France", "2"))
