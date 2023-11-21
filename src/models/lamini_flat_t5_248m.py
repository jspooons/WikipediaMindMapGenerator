from transformers import T5Tokenizer, T5ForConditionalGeneration, pipeline, logging
import torch
import math

logging.enable_explicit_format()

# model and tokenizer loading
checkpoint = "MBZUAI/LaMini-Flan-T5-248M"
tokenizer = T5Tokenizer.from_pretrained(checkpoint)
base_model = T5ForConditionalGeneration.from_pretrained(checkpoint, device_map='auto', torch_dtype=torch.float32)

FAILED_MESSAGE = "I'm sorry, but you haven't provided any context or information for me to summarize. Please provide more details so I can assist you better."
MAX_LEN_INPUT = 512


def llm_runner(input_text):
    num_words = len(input_text.split(' '))

    if num_words > MAX_LEN_INPUT:
        half_len = len(input_text) // 2

        max_len_output = math.floor(half_len * 0.6 if half_len < 150 else 100)

        # Split the input text into two halves
        first_half = input_text[:half_len]
        second_half = input_text[half_len:]

        # Recursively summarize each half
        first_summary = llm_pipeline(first_half, max_len_output)
        second_summary = llm_pipeline(second_half, max_len_output)

        # Combine the summaries
        result = first_summary + " " + second_summary

        return result

    max_len_output = math.floor(num_words * 0.6 if num_words < 150 else 100)
    return llm_pipeline(input_text, max_len_output)


def llm_pipeline(input_text, max_len_output):

    pipe_sum = pipeline(
        'summarization',
        model=base_model,
        tokenizer=tokenizer,
        max_length=max_len_output)

    result = pipe_sum(input_text)
    result = result[0]['summary_text']

    if FAILED_MESSAGE.lower() == result.lower() or FAILED_MESSAGE.lower() in result.lower():
        return ""

    return result
