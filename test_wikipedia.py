import wikipediaapi
import GPT3
from icecream import ic
from tqdm import tqdm
import re

wiki_wiki = wikipediaapi.Wikipedia("en")

page_py = wiki_wiki.page("Dwayne_Johnson")

ic(page_py.summary)
# ic(re.split('\.[a-zA-Z]|\n', page_py.summary))
form = re.findall(".*?(?=\.[A-Z][^.])|.*?\n", page_py.summary)
ic(form)
form = [el for el in form if el != ""]
ic(form)


# for el in re.findall('.*?(?=\.[A-Z][^.])|.*?\n', page_py.summary) :
#     ic(el)


text = ""
for el in tqdm(form):
    paraphrase = GPT3.gen_article(
        "Paraphrase the following paragraph, using as few words from the original paragraph as possible:",
        el,
        prompt_tokens=2000,
        temperature_chosen=0.90,
        top_p_chosen=1.00,
        frequency_penalty_chosen=2.00,
        presence_penalty_chosen=2.00,
    )[0]
    text += paraphrase
ic(text)

with open("text.txt", "w") as f:
    f.write(text)
