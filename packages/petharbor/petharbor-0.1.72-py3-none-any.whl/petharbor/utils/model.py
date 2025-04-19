from transformers import pipeline
from transformers import logging as hf_logging

# Set the level to capture what you want (e.g., info, warning)
hf_logging.set_verbosity_info()  # or set_verbosity_warning(), etc.

hf_logging.enable_propagation()  # Let it go to root logger
hf_logging.disable_default_handler()

from petharbor.utils.logging_setup import get_logger
from tqdm.contrib.logging import logging_redirect_tqdm
import pandas as pd

logger = get_logger()


def replace_token(text, start, end, replacement):
    """Replace a token in the text with a replacement string."""
    if start < 0 or end > len(text):
        logger.warning(
            f"Start index {start} or end index {end} is out of bounds for text of length {len(text)}"
        )
        raise ValueError("Start and end indices are out of bounds.")
    return text[:start] + replacement + text[end:]

def get_predictions_and_anonymise(
    model, tokenizer, target_dataset, tag_map, replaced=True, text_column="text", device="cpu"):
    if tokenizer is None:
        tokenizer = model
    logger.info("Getting predictions from the model")
    ner_pipeline = pipeline(
        "token-classification",
        model=model,
        tokenizer=tokenizer,
        aggregation_strategy="simple",
        device= device,
    )
 
    logger.info(f'Tag map: {tag_map}')
    
    # Process NER predictions using the dataset's map function
    # Your function
    def process_batch(examples):
        texts = examples[text_column]
        if len(texts) > 1:
            texts = [str(text) for text in texts]
                
        # Get NER predictions for the batch
        ner_results = ner_pipeline(texts)
        
        if replaced:
            anonymized_texts = []
            for i, entities in enumerate(ner_results):
                text = texts[i]
                for entity in sorted(entities, key=lambda x: x["start"], reverse=True):
                    tag = tag_map.get(entity["entity_group"])
                    if tag:
                        text = replace_token(text, entity["start"], entity["end"], tag)
                anonymized_texts.append(text)
            return {text_column: anonymized_texts}
        else:
            return {"ner_results": ner_results}

    if len(target_dataset) >1:
        num_proc = 1
    else:
        num_proc = 1

    # get date
    date_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    with logging_redirect_tqdm():
        processed_dataset = target_dataset.map(
            process_batch,
            batched=True,
            desc=f"[{date_time} |   INFO  | PetHarbor-Advance]",
            num_proc=num_proc,
        )
    
    # Extract the results
    if replaced:
        anonymised_out = processed_dataset[text_column]
    else:
        anonymised_out = processed_dataset["ner_results"]
    
    logger.info("Predictions obtained successfully")
    return anonymised_out