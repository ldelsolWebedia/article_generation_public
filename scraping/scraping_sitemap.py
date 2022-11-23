import advertools as adv
import pandas as pd
import html

def sitemap(type) :
    
    video_games_url = ['https://www.gamestar.de/sitemapnews.xml','https://www.3djuegos.com/sitemap_news.xml','https://mein-mmo.de/news-sitemap.xml']
    movies_url = ['https://www.moviepilot.de/files/sitemaps/moviepilot_articles.xml.gz','https://www.espinof.com/sitemap_news.xml','https://www.sensacine.com/sitemp/sitemap-news.xml']

    if type == "Jeux vidéo" :
        url_list = video_games_url

    if type == "Cinéma" :
        url_list = movies_url
    
    df = pd.concat([adv.sitemap_to_df(el)[['news_title','publication_name','news_publication_date','loc','publication_language']] for el in url_list])
    df['news_title'] = df['news_title'].apply(html.unescape)
    df = df.sort_values('news_publication_date',ascending=False).reset_index(drop = True)
    return(df)

if __name__ == "__main__" :
    print(sitemap("Cinéma"))