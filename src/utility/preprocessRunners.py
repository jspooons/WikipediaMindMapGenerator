from src.utility.utility import *


def pre_process_text_runner(sections):
    keys = sections.keys()

    if "text" in keys:
        sections["text"] = pre_process_text(sections["text"])

    for key in keys:
        if key != "text":
            pre_process_text_runner(sections[key])

    return sections


def pre_process_text(list_of_paragraphs):
    paragraphs_split = split_paragraphs_into_sentences(list_of_paragraphs)
    new_line_tokens_removed = remove_new_line_tokens(paragraphs_split)
    citations_removed = remove_citations(new_line_tokens_removed)
    sentences_lower_case = make_lower_case(citations_removed)
    punctuation_removed = remove_punctuation(sentences_lower_case)
    tokenized_sentences = tokenize(punctuation_removed)
    non_ascii_removed = remove_non_ascii(tokenized_sentences)
    stopwords_removed = remove_stopwords(non_ascii_removed)
    lemmatized_sentences = lemmatization(stopwords_removed)
    filtered_empty_sublists = filter_empty_sublists(lemmatized_sentences)

    return filtered_empty_sublists
