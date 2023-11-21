import re


def add_new_lines(paragraph, maxlen):
    return [add_new_lines_to_sentence(sentence, maxlen) for sentence in paragraph if len(sentence) > 5]


def add_new_lines_to_sentence(text, maxlen):
    i = maxlen
    while i < len(text):
        if text[i] != ' ':
            space_index = text.find(' ', i)

            if space_index != -1:
                text = text[:space_index] + '\n' + text[space_index+1:]
                i = space_index + maxlen + 1  # adding 1 to consider that we have removed a space and added \n
            else:
                i += 1
        else:
            text = text[:i] + '\n' + text[i+1:]
            i += maxlen + 1  # adding 1 to consider that we have removed a space and added \n

    return text


def join_sentences(sentences):
    return ' '.join(sentences)


def split_paragraphs_into_sentences(list_of_paragraphs):
    return [sentence for paragraph in list_of_paragraphs for sentence in paragraph.split(".")]


def split_paragraph_into_sentences(paragraph):
    return paragraph.split(".")


def remove_new_line_tokens(sentences):
    return [sentence.replace('\n', '') for sentence in sentences]


def remove_citations(sentences):
    return [re.sub(r'\[\d+]', '', sentence) for sentence in sentences]


def get_sections_texts(sections, texts, section_title):
    keys = sections.keys()

    if "text" in keys:
        texts[section_title] = sections["text"]

    for key in keys:
        if key != "text":
            get_sections_texts(sections[key], texts, key)

    return texts


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
