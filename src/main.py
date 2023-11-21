from src.tools.WikipediaArticle import WikipediaArticle
from src.tools.networkModelling.mindMapGenerator import create_mind_map
from src.utility.preprocessRunners import pre_process_text_runner
from src.models.latent_dirichlet_allocation import create_model
from src.utility.utility import get_n_grams, set_sections_topics


if __name__ == "__main__":
    summarize = True

    article = WikipediaArticle("https://en.wikipedia.org/wiki/Nico_Ditch")
    article.sections = pre_process_text_runner(article.sections, summarize)

    if not summarize:
        sections_data_words_n_grams, used_keys = get_n_grams(article.sections)
        lda_top_topics = create_model(sections_data_words_n_grams)

        article.sections = set_sections_topics(article.sections, dict(zip(used_keys, lda_top_topics)), list(article.sections.keys())[0])

    article.save()

    g = create_mind_map(f"./data/{article.title}.json")
    g.view()
