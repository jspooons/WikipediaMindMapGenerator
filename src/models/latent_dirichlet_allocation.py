from gensim.models.ldamulticore import LdaMulticore
from src.utility.utility import generate_lda_parameters


def create_model(sections_data_words_n_grams):

    sections_top_topics = []

    for i in range(len(sections_data_words_n_grams)):
        print(i)

        id2word, corpus = generate_lda_parameters(sections_data_words_n_grams[i])

        lda_model = LdaMulticore(corpus=corpus,
                                 id2word=id2word,
                                 num_topics=3,
                                 random_state=100,
                                 chunksize=8,
                                 passes=20,
                                 per_word_topics=True)

        top_topics = {
            'Topic ' + str(i + 1):
                [token for token, score in lda_model.show_topic(i, topn=1)] for i in range(0, lda_model.num_topics)
        }

        sections_top_topics.append(top_topics)

    return sections_top_topics
