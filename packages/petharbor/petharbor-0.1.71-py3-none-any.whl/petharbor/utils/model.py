import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from petharbor.utils.logging_setup import get_logger
from petharbor.utils.dataset import DatasetProcessor
from petharbor.utils.annonymisation import replace_token
from tqdm import tqdm
from torch.utils.data import DataLoader

logger = get_logger()


def load_model(model_path, device="cuda" if torch.cuda.is_available() else "cpu"):
    try:
        logger.info(f"Loading model and tokenizer from {model_path}")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForTokenClassification.from_pretrained(model_path).to(device)
        logger.info(f"Model and tokenizer loaded successfully")
    except Exception as e:
        raise RuntimeError(f"Could not load model from {model_path}: {e}")
    return model, tokenizer


def replace_token(text, start, end, replacement):
    """Replace a token in the text with a replacement string."""
    if start < 0 or end > len(text):
        raise ValueError("Start and end indices are out of bounds.")
    return text[:start] + replacement + text[end:]

def get_predictions_and_anonymise(
    model, tokenizer, target_dataset, replaced=True, text_column="text", device="cpu"
):
    logger.info("Getting predictions from the model")
    ner_pipeline = pipeline(
        "token-classification",
        model=model,
        tokenizer=tokenizer,
        aggregation_strategy="simple",
        device=device,
    )

    tag_map = {
        "PER": "<<NAME>>",
        "LOC": "<<LOCATION>>",
        "ORG": "<<ORG>>",
        "MISC": "<<MISC>>"
    }
    logger.info(f'Tag map: {tag_map}')
    
    # Process NER predictions using the dataset's map function
    def process_batch(examples):
        texts = examples[text_column]
        if len(texts) > 1:
            texts = [str(text) for text in texts]
        
        # Get NER predictions for the batch
        ner_results = ner_pipeline(texts)
        
        # If we're replacing entities with tags
        if replaced:
            anonymized_texts = []
            for i, entities in enumerate(ner_results):
                text = texts[i]
                # Sort by start index in reverse order to avoid offset shifts
                for entity in sorted(entities, key=lambda x: x["start"], reverse=True):
                    tag = tag_map.get(entity["entity_group"])
                    if tag:
                        text = replace_token(text, entity["start"], entity["end"], tag)
                anonymized_texts.append(text)
            return {text_column : anonymized_texts}
        else:
            return {"ner_results": ner_results}
    
    processed_dataset = target_dataset.map(process_batch, batched=True)
    
    # Extract the results
    if replaced:
        anonymised_out = processed_dataset[text_column]
    else:
        anonymised_out = processed_dataset["ner_results"]
    
    logger.info("Predictions obtained successfully")
    return anonymised_out