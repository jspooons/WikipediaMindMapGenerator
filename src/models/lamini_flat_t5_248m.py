from transformers import T5Tokenizer, T5ForConditionalGeneration, pipeline, logging
import torch

logging.enable_explicit_format()

# model and tokenizer loading
checkpoint = "MBZUAI/LaMini-Flan-T5-248M"
tokenizer = T5Tokenizer.from_pretrained(checkpoint)
base_model = T5ForConditionalGeneration.from_pretrained(checkpoint, device_map='auto', torch_dtype=torch.float32)


def llm_pipeline(input_text):

    # TODO: if num_words > 512 then split in half, summarize, then combine
    num_words = len(input_text.split(' '))

    pipe_sum = pipeline(
        'summarization',
        model=base_model,
        tokenizer=tokenizer,
        max_length=100)

    result = pipe_sum(input_text)
    result = result[0]['summary_text']

    return result

