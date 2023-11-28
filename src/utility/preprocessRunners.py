from src.utility.utility import *
from src.models.lamini_flat_t5_248m import llm_runner
import logging
import os

logging.basicConfig(format='[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s >> %(message)s',
                    # datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)


def pre_process_text_runner(sections, key=""):
    keys = sections.keys()

    if "text" in keys:
        sections["text"] = pre_process_text(sections["text"], key)

    for key in keys:
        if key != "text":
            pre_process_text_runner(sections[key], key)

    return sections


def pre_process_text(list_of_paragraphs, key):
    log.info(f"Pre-processing {key}")

    log.info(f"Pre-processing | splitting up the paragraphs: {key}")
    paragraphs_split = split_paragraphs_into_sentences(list_of_paragraphs)

    log.info(f"Pre-processing | removing new line tokens: {key}")
    new_line_tokens_removed = remove_new_line_tokens(paragraphs_split)

    log.info(f"Pre-processing | removing citations: {key}")
    citations_removed = remove_citations(new_line_tokens_removed)

    log.info(f"Pre-processing {key} | join each text")
    sentences_joined = join_sentences(citations_removed)

    log.info(f"Pre-processing {key} | summarize the text")
    text_summarized = llm_runner(sentences_joined)

    log.info(f"Pre-processing {key} | split summarized text into sentences")
    paragraph_split = split_paragraph_into_sentences(text_summarized)

    log.info(f"Pre-processing {key} | add new line tokens every 20 characters")
    new_lines_added = add_new_lines(paragraph_split, 20)

    return new_lines_added
