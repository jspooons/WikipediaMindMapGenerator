import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import gensim


def add_new_lines(text, maxlen):
    i = maxlen
    while i < len(text):
        if text[i] != ' ':
            space_index = text.find(' ', i)
            if space_index != -1:
                text = text[:space_index] + '\n' + text[space_index+1:]
                i = space_index + maxlen
        else:
            text = text[:i] + '\n' + text[i+1:]
            i += maxlen

    return text


def join_sentences(sentences):
    return ' '.join(sentences)


def split_paragraphs_into_sentences(list_of_paragraphs):
    return [sentence for paragraph in list_of_paragraphs for sentence in paragraph.split(".")]


def remove_new_line_tokens(sentences):
    return [sentence.replace('\n', '') for sentence in sentences]


def remove_citations(sentences):
    return [re.sub(r'\[\d+]', '', sentence) for sentence in sentences]


def make_lower_case(sentences):
    return [sentence.lower() for sentence in sentences]


def remove_punctuation(sentences):
    translator = str.maketrans('', '', string.punctuation)
    return [sentence.translate(translator) for sentence in sentences]


def tokenize(sentences):
    return [word_tokenize(sentence) for sentence in sentences]


def remove_non_ascii(tokenized_sentences):
    for i in range(len(tokenized_sentences)):
        tokenized_sentences[i] = [word for word in tokenized_sentences[i] if all(ord(char) < 128 for char in word)]

    return tokenized_sentences


def remove_stopwords(tokenized_sentences):
    stop_words = stopwords.words('english')
    stop_words.append('us')

    for i in range(len(tokenized_sentences)):
        tokenized_sentences[i] = [word for word in tokenized_sentences[i] if word not in stop_words]

    return tokenized_sentences


def lemmatization(tokenized_sentences):
    wordnet_lemmatizer = WordNetLemmatizer()

    for i in range(len(tokenized_sentences)):
        words_tagged = pos_tag(tokenized_sentences[i])

        # Lemmatize words based on POS tags
        lemmatized_words = []
        for word, tag in words_tagged:
            pos = tag[0].lower() if tag[0].lower() in ['a', 'n', 'v'] else 'n'
            lemmatized_word = wordnet_lemmatizer.lemmatize(word, pos=pos)
            lemmatized_words.append(lemmatized_word)

        tokenized_sentences[i] = lemmatized_words

    return tokenized_sentences


def filter_empty_sublists(tokenized_sentences):
    return [sublist for sublist in tokenized_sentences if sublist]


def get_sections_texts(sections, texts, section_title):
    keys = sections.keys()

    if "text" in keys:
        texts[section_title] = sections["text"]

    for key in keys:
        if key != "text":
            get_sections_texts(sections[key], texts, key)

    return texts


def format_dataset(texts):
    keys = texts.keys()
    dataset = []
    used_keys = []

    for key in keys:
        if len(texts[key]) > 0:
            dataset.append(texts[key])
            used_keys.append(key)

    return dataset, used_keys


def build_ngrams(datasets, choice):
    for i in range(len(datasets)):
        bigram = gensim.models.Phrases(datasets[i], min_count=5, threshold=1)  # higher threshold fewer phrases.
        trigram = gensim.models.Phrases(bigram[datasets[i]], min_count=2, threshold=1)

        bigram_mod = gensim.models.phrases.Phraser(bigram)
        trigram_mod = gensim.models.phrases.Phraser(trigram)

        if choice == 2:
            datasets[i] = [bigram_mod[doc] for doc in datasets[i]]
        elif choice == 3:
            datasets[i] = [trigram_mod[bigram_mod[doc]] for doc in datasets[i]]

    return datasets


def generate_lda_parameters(texts):
    # Create Dictionary
    id2word = gensim.corpora.Dictionary(texts)

    # TODO: try catch if fail, increase no_above or no_below a couple times
    id2word.filter_extremes(no_below=2, no_above=0.6)

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    return id2word, corpus


def get_n_grams(sections):
    texts = get_sections_texts(sections, {}, "")

    datasets, used_keys = format_dataset(texts)

    sections_data_words_n_grams = build_ngrams(datasets, 2)

    return sections_data_words_n_grams, used_keys


def set_sections_topics(sections, sections_top_topics_dict, key):
    keys = sections.keys()

    if "text" in keys:
        if key in sections_top_topics_dict.keys():
            nested_topics = list(sections_top_topics_dict[key].values())
            flattened_list = [item for sublist in nested_topics for item in sublist]
            sections["text"] = flattened_list
        else:
            sections["text"] = []

    for key in keys:
        if key != "text":
            set_sections_topics(sections[key], sections_top_topics_dict, key)

    return sections
