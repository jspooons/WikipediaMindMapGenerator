from src.utility.utility import *
from src.models.lamini_flat_t5_248m import llm_pipeline
import logging
import os

logging.basicConfig(format='[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s >> %(message)s',
                    # datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)


def pre_process_text_runner(sections, summarize, key=""):
    keys = sections.keys()

    if "text" in keys:
        sections["text"] = pre_process_text(sections["text"], summarize, key)

    for key in keys:
        if key != "text":
            pre_process_text_runner(sections[key], summarize, key)

    return sections


def pre_process_text(list_of_paragraphs, summarize, key):
    log.info(f"Pre-processing {key} | Summarization enabled: {summarize}")

    log.info(f"Pre-processing | splitting up the paragraphs: {key} | Summarization enabled: {summarize}")
    paragraphs_split = split_paragraphs_into_sentences(list_of_paragraphs)

    log.info(f"Pre-processing | removing new line tokens: {key} | Summarization enabled: {summarize}")
    new_line_tokens_removed = remove_new_line_tokens(paragraphs_split)

    log.info(f"Pre-processing | removing citations: {key} | Summarization enabled: {summarize}")
    citations_removed = remove_citations(new_line_tokens_removed)

    if summarize:
        log.info(f"Pre-processing {key}| join each text | Summarization enabled: {summarize} ")
        sentences_joined = join_sentences(citations_removed)

        log.info(f"Pre-processing {key}| summarize the text | Summarization enabled: {summarize} ")
        text_summarized = llm_pipeline(sentences_joined)

        log.info(f"Pre-processing {key}| add new line tokens every 50 lines | Summarization enabled: {summarize} ")
        new_lines_added = add_new_lines(text_summarized, 50)

        return [new_lines_added]
    else:
        log.info(f"Pre-processing {key}| set characters lower case | Summarization enabled: {summarize} ")
        sentences_lower_case = make_lower_case(citations_removed)

        log.info(f"Pre-processing {key}| remove punctation | Summarization enabled: {summarize} ")
        punctuation_removed = remove_punctuation(sentences_lower_case)

        log.info(f"Pre-processing {key}| tokenize text | Summarization enabled: {summarize} ")
        tokenized_sentences = tokenize(punctuation_removed)

        log.info(f"Pre-processing {key}| remove non-ascii characters | Summarization enabled: {summarize} ")
        non_ascii_removed = remove_non_ascii(tokenized_sentences)

        log.info(f"Pre-processing {key}| remove stopwords | Summarization enabled: {summarize} ")
        stopwords_removed = remove_stopwords(non_ascii_removed)

        log.info(f"Pre-processing {key}| lemmatize | Summarization enabled: {summarize} ")
        lemmatized_sentences = lemmatization(stopwords_removed)

        log.info(f"Pre-processing {key}| remove empty sublists | Summarization enabled: {summarize} ")
        filtered_empty_sublists = filter_empty_sublists(lemmatized_sentences)

        return filtered_empty_sublists
