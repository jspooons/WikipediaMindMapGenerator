from src.tools.WikipediaArticle import WikipediaArticle
from src.tools.networkModelling.mindMapGenerator import create_mind_map
from src.utility.preprocessRunners import pre_process_text_runner


if __name__ == "__main__":
    summarize = True

    article = WikipediaArticle("https://en.wikipedia.org/wiki/Leopard")
    article.sections = pre_process_text_runner(article.sections, summarize)

    article.save()

    g = create_mind_map(f"./data/{article.title}.json")
    g.view()
